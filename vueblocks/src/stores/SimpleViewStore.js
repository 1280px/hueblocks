import {ref, computed} from 'vue'
import {defineStore} from 'pinia'
import {rgb2lab, deltaE} from '@/colors'


export const useSimpleViewStore = defineStore('SimpleViewStore', () => {
    const blockVizCfg = ref({
        hideDuplicates: true,
        resultsInOneRow: false,
        keepPrevResults: false,
    })

    const blockDataCfg = ref({
        // Note that blockdata and palettes are in global store!
        useCIELAB: true,
        // See names in corersponding DD in BlockViz.vue for context
        noiseThresholdMin: 0,
        noiseThresholdMax: 4,
    })


    const colorbarData = ref([
        {
            // type: 'color',
            color: [12, 34, 56], 
            blockRef: null,
            steps: 6 // Length between CURRENT and NEXT color segments,
                     // will be ignored if this is the last color segment
        },
        // {
        //     type: 'length', <-- No longer used; now length is stored next to color
        //     value: 6,
        //     // bg: [[18, 52, 86], [131, 86, 35]] <-- Calculated at runtime instead
        // },
        {
            color: [200, 100, 20],
            blockRef: null,
            steps: 14
        },
        {
            color: [122, 43, 172],
            blockRef: { // Currently unused because BlockPick is not a thing yet
                name: "Purple Wool",
                texture: "purple_wool.png"
            },
            steps: 3
        },
        {
            color: [64, 0, 64],
            blockRef: null,
            steps: 3
        }
    ])


    const blockVizData = ref([])
    
    // Uses exactly the same algorithm as original HueBlocks;
    // results in faster but more "inaccurate" graident generation
    function blockVizCalcRGB(blockdata, startRGB, endRGB, steps) {
        for (let step = 0; step < steps; step++) {
            // Calculate step color as linear mixture of start and end colors
            const stepRGB = [
                endRGB[0] * (step / (steps-1)) + startRGB[0] * (((steps-1) - step) / (steps-1)),
                endRGB[1] * (step / (steps-1)) + startRGB[1] * (((steps-1) - step) / (steps-1)),
                endRGB[2] * (step / (steps-1)) + startRGB[2] * (((steps-1) - step) / (steps-1))
            ]
            // console.log(startRGB, endRGB, stepRGB)

            // Now go through all blockdata and find block with closest RGB
            let [closestBlock, closestBlockScore] = [{name: 'missingNo'}, 0]

            for (const block of blockdata) {
                const blockScore = (
                    255 - Math.abs(stepRGB[0] - block.rgb[0]) +
                    255 - Math.abs(stepRGB[1] - block.rgb[1]) +
                    255 - Math.abs(stepRGB[2] - block.rgb[2])
                ) / (255*3)
                // 0.0 means 'completely opposite colour', 1.0 means 'same colour';
			    // values < 0.8 in 99% of cases are junk

                if (blockScore > closestBlockScore) {
                    closestBlock = block
                    closestBlockScore = blockScore
                }
                // console.log(closestBlock, closestBlockScore)
            }

            if ((blockVizCfg.value.hideDuplicates) &&
                (blockVizData.value.length > 0) &&
                (closestBlock.texture === blockVizData.value.at(-1).texture)) {
                continue
            }
            blockVizData.value.push(closestBlock)
        }
    }

    // Uses CIELAB transformations and sqrt of mean of squares;
    // results in better but noticeably slower gradient generation
    function blockVizCalcCIELAB(blockdata, startRGB, endRGB, steps) {
        // Here I'm using antimatter15's RGB<->LAB convertors implementation:
        // https://github.com/antimatter15/rgb-lab/blob/master/color.js
        const startLAB = rgb2lab(startRGB)
        const endLAB = rgb2lab(endRGB)
    
        for (let step = 0; step < steps; step++) {
            // Just like in RGB, in CIELAB "step" color can be found linearly
            const stepLAB = [
                endLAB[0] * (step / (steps-1)) + startLAB[0] * (((steps-1) - step) / (steps-1)),
                endLAB[1] * (step / (steps-1)) + startLAB[1] * (((steps-1) - step) / (steps-1)),
                endLAB[2] * (step / (steps-1)) + startLAB[2] * (((steps-1) - step) / (steps-1))
            ]
            // console.log(startLAB, endLAB, stepLAB)

            // L*a*b deltas computed the same way as Euclidian distance
            // (the smaller <=> the closer), which I find very neat
            let [closestBlock, closestBlockDelta] = [{name: 'missingNo'}, Infinity]

            for (const block of blockdata) {
                const blockDelta = deltaE(stepLAB, block.lab)

                if (blockDelta < closestBlockDelta) {
                    closestBlock = block
                    closestBlockDelta = blockDelta
                }
                // console.log(closestBlock, closestBlockDelta)
            }

            if ((blockVizCfg.value.hideDuplicates) &&
                (blockVizData.value.length > 0) &&
                (closestBlock.texture === blockVizData.value.at(-1).texture)) {
                continue
            }
            blockVizData.value.push(closestBlock)
        }
    }

    const blockVizGenerate = (blockdata, palette, facing) => {
        // First, fulter out blockdata to exclude blocks with
        // undesired side facing, palette, or noise coefficients:
        const blockdataFiltered = blockdata.slice(1).filter(
            (block) => {
                if (palette.count > 0) {
                    if (!palette.textures.includes(block.texture)) {
                        return false
                    }
                }

                // if ((block.noise < blockDataCfg.value.noiseThresholdMin) &&
                //     (block.noise > blockDataCfg.value.noiseThresholdMax)) {
                // return false
                // }

                if (facing !== 'all') {
                    if (facing === 'sides') {
                        if (block.sides.every((s) => s === 'top' || s === 'bottom')) {
                            return false
                        }
                        return true
                    }
                    else if (block.sides.includes(facing)) {
                        return true
                    }
                }
                else {
                    return true
                }
            }
        )
        // console.log(blockdata, blockdataFiltered)
    
        if (!blockVizCfg.value.keepPrevResults) {
            blockVizData.value = []
        }
        
        // And then, render the whole colorbar data, segment by segment!
        for (let cbIdx = 0; cbIdx < colorbarData.value.length-1; cbIdx++) {            
            const segStart = colorbarData.value[cbIdx].color
            const segEnd = colorbarData.value[cbIdx+1].color
            const segSteps = colorbarData.value[cbIdx].steps

            if (blockDataCfg.value.useCIELAB) {
                blockVizCalcCIELAB(blockdataFiltered, segStart, segEnd, segSteps)
            }
            else {
                blockVizCalcRGB(blockdataFiltered, segStart, segEnd, segSteps)
            }
        }
    }


    return {
        blockVizCfg, blockDataCfg,
        colorbarData,
        blockVizData, blockVizGenerate
    }
})
