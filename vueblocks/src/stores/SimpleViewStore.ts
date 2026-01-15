import type { Block, BlockFacing, DisplayBlock } from '@/types/blocks'
import type { BlocksetIndex } from '@/types/blocksets'
import type { ColorLAB, ColorRGB } from '@/types/colors'
import type { Palette } from '@/types/palettes'
import type { BlockDisplayConfig, BlockFilteringConfig, BlockVizRow, ColorbarSeg } from '@/types/simpleview'

import { defineStore } from 'pinia'
import { ref } from 'vue'

import { rgb2lab } from '@/colors'

export const useSimpleViewStore = defineStore('SimpleViewStore', () => {
    const blockDisplayCfg = ref<BlockDisplayConfig>({
        hideDuplicates: true,
        resultsInOneRow: false,
        keepPrevResults: false,
        showColorsDebug: false,
    })

    const blockFilteringCfg = ref<BlockFilteringConfig>({
        useOkLAB: true,
    })

    const colorbarData = ref<ColorbarSeg[]>([
        {
            color: [12, 34, 56],
            blockRef: null,
            steps: 8,
        },
        {
            color: [200, 100, 20],
            blockRef: null,
            steps: 16,
        },
        {
            color: [122, 43, 172],
            blockRef: {
                name: 'Purple Wool',
                blocksetIdx: 1,
                texture: 'purple_wool.png',
            },
            steps: 4,
        },
        {
            color: [48, 0, 64],
            blockRef: null,
            steps: 4,
        },
    ])

    const blockVizData = ref<BlockVizRow[]>([])

    function blockVizCalcRGB(
        blocksetIdx: BlocksetIndex,
        blockdata: Block[],
        startRGB: ColorRGB,
        endRGB: ColorRGB,
        steps: number,
    ): BlockVizRow {
        const newSegData = []

        for (let step = 0; step < steps; step++) {
            // Calculate step color as linear mixture of start and end colors
            const stepRGB = [
                // ((endRGB[0] ** 0.1) * (step / (steps - 1))
                //     + (startRGB[0] ** 0.5) * (((steps - 1) - step) / (steps - 1))) ** 2,
                // ((endRGB[1] ** 0.1) * (step / (steps - 1))
                //     + (startRGB[1] ** 0.5) * (((steps - 1) - step) / (steps - 1))) ** 2,
                // ((endRGB[2] ** 0.1) * (step / (steps - 1))
                //     + (startRGB[2] ** 0.5) * (((steps - 1) - step) / (steps - 1))) ** 2,
                endRGB[0] * (step / (steps - 1)) + startRGB[0] * (((steps - 1) - step) / (steps - 1)),
                endRGB[1] * (step / (steps - 1)) + startRGB[1] * (((steps - 1) - step) / (steps - 1)),
                endRGB[2] * (step / (steps - 1)) + startRGB[2] * (((steps - 1) - step) / (steps - 1)),
            ] as ColorRGB
            // console.log(startRGB, endRGB, stepRGB)

            // Now go through all blockdata and find block with closest RGB
            let closestBlock: DisplayBlock = { name: 'missingNo' } as DisplayBlock
            let closestBlockScore: number = 0

            for (const block of blockdata) {
                const blockScore = (
                    255 - Math.abs(stepRGB[0] - block.rgb[0])
                    + 255 - Math.abs(stepRGB[1] - block.rgb[1])
                    + 255 - Math.abs(stepRGB[2] - block.rgb[2])
                ) / (255 * 3)
                // 0.0 means 'completely opposite color', 1.0 means 'same color';
                // values < 0.8 in 99% of cases are pretty much junk.

                // I also tried using Weighted Euclidian, but somehow it seems to
                // give worse results on tests than the abomination of a code above!
                // https://www.baeldung.com/cs/compute-similarity-of-colours

                if (blockScore > closestBlockScore) {
                    closestBlock = {
                        name: block.name,
                        texture: block.texture,
                        blocksetIdx,
                    }
                    closestBlockScore = blockScore

                    if (blockDisplayCfg.value.showColorsDebug) {
                        closestBlock.debugData = {
                            rgbTarget: stepRGB,
                            rgbReal: block.rgb,
                        }
                    }
                }
                // console.log(closestBlock, closestBlockScore)
            }
            newSegData.push(closestBlock)
        }
        return newSegData
    }

    function blockVizCalcOkLAB(
        blocksetIdx: BlocksetIndex,
        blockdata: Block[],
        startRGB: ColorRGB,
        endRGB: ColorRGB,
        steps: number,
    ): BlockVizRow {
        const newSegData = []

        const startLAB = rgb2lab(startRGB)
        const endLAB = rgb2lab(endRGB)

        for (let step = 0; step < steps; step++) {
            // Just like in RGB, in OkLAB "step" color can be found linearly
            const stepLAB = [
                endLAB[0] * (step / (steps - 1)) + startLAB[0] * (((steps - 1) - step) / (steps - 1)),
                endLAB[1] * (step / (steps - 1)) + startLAB[1] * (((steps - 1) - step) / (steps - 1)),
                endLAB[2] * (step / (steps - 1)) + startLAB[2] * (((steps - 1) - step) / (steps - 1)),
            ] as ColorLAB
            // console.log(startLAB, endLAB, stepLAB)

            // OkLAB, unlike CIELAB, is uniform, meaning color deltas
            // can be computed as simple as using Euclidian distance:
            let closestBlock: DisplayBlock = { name: 'missingNo' } as DisplayBlock
            let closestBlockDelta: number = Infinity

            for (const block of blockdata) {
                // const blockDelta = deltaE(stepLAB, block.lab)

                const blockDelta = (
                    (stepLAB[0] - block.lab[0]) ** 2
                    + (stepLAB[1] - block.lab[1]) ** 2
                    + (stepLAB[2] - block.lab[2]) ** 2
                ) ** (1 / 2)

                if (blockDelta < closestBlockDelta) {
                    closestBlock = {
                        name: block.name,
                        texture: block.texture,
                        blocksetIdx,
                    }
                    closestBlockDelta = blockDelta

                    if (blockDisplayCfg.value.showColorsDebug) {
                        closestBlock.debugData = {
                            labReal: block.lab,
                            labTarget: stepLAB,
                        }
                    }
                }
                // console.log(closestBlock, closestBlockDelta)
            }
            newSegData.push(closestBlock)
        }
        return newSegData
    }

    const getFilteredBlockdata = (
        blockdata: Block[],
        palette: Palette,
        facing: BlockFacing,
    ): Block[] => {
        const res = blockdata.filter(
            (block) => {
                if (
                    palette.count > 0 // 'All blocks' (0) is fake palette and contains 0 textures
                    || palette.count === -2 // -2 is used by 'Custom palette' option
                ) {
                    if (!palette.textures.includes(block.texture)) {
                        return false
                    }
                }

                // if ((block.noise < blockFilteringCfg.value.noiseThresholdMin) &&
                //     (block.noise > blockFilteringCfg.value.noiseThresholdMax)) {
                // return false
                // }

                if (facing !== 'all') {
                    if (facing === 'sides') {
                        if (block.sides.every(s => s === 'top' || s === 'bottom')) {
                            return false
                        }
                        return true
                    }
                    else {
                        return block.sides.includes(facing)
                    }
                }
                return true
            },
        )
        return res
    }

    const blockVizGenerate = (
        blocksetIdx: BlocksetIndex,
        blockdata: Block[],
        palette: Palette,
        facing: BlockFacing,
    ) => {
        // First, fulter out blockdata to exclude blocks with
        // undesired side facing, palette, or noise coefficients:
        const filteredBlockdata = getFilteredBlockdata(blockdata, palette, facing)

        // Create a blockviz row objecy for new render results...
        let newBlockVizRow: BlockVizRow = []

        // And then, render the whole colorbar data, segment by segment!
        for (let cbIdx = 0; cbIdx < colorbarData.value.length - 1; cbIdx++) {
            const segStart = colorbarData.value[cbIdx].color
            const segEnd = colorbarData.value[cbIdx + 1].color
            const segSteps = colorbarData.value[cbIdx].steps

            let seg: BlockVizRow = []
            if (blockFilteringCfg.value.useOkLAB) {
                seg = blockVizCalcOkLAB(blocksetIdx, filteredBlockdata, segStart, segEnd, segSteps)
            }
            else {
                seg = blockVizCalcRGB(blocksetIdx, filteredBlockdata, segStart, segEnd, segSteps)
            }

            newBlockVizRow.push(...seg)
        }

        // Finally, check the row's texture data for duplicates
        if (blockDisplayCfg.value.hideDuplicates) {
            newBlockVizRow = newBlockVizRow.filter((db, i) => {
                return i <= 0 || db.texture !== newBlockVizRow[i - 1].texture
            })
        }

        if (blockDisplayCfg.value.keepPrevResults) {
            blockVizData.value.push(newBlockVizRow)
        }
        else {
            blockVizData.value = [newBlockVizRow]
        }
    }

    return {
        blockDisplayCfg, blockFilteringCfg,
        colorbarData,
        getFilteredBlockdata,
        blockVizData, blockVizGenerate,
    }
})
