import {ref, computed} from 'vue'
import {defineStore} from 'pinia'


export const useGlobalStore = defineStore('GlobalStore', () => {
    // const locale = ref('en')
    
    const blockSize = ref('64px')
    const changeBlockSize = (scale) => {
        const newBlockSize = parseInt(blockSize.value) * scale
        console.log(newBlockSize)
        if (newBlockSize >= 16 && newBlockSize <= 256) {
            blockSize.value = newBlockSize + 'px'
        }
    }

    const blockFacing = ref('all')
    // const blockSides = computed(() => {
    //     let sideNames = ['top', 'bottom', 'north', 'south', 'east', 'west']

    //     // 0 = 'all', which is simply all sides
    //     if (blockFacing.value === 'all') { 
    //         return sideNames
    //     }

    //     // 1 = 'sides', which is all sides except top and bottom
    //     else if (blockFacing.value === 'sides') { 
    //         return sideNames.slice(2)
    //     }

    //     // 2 to 7 = optifine CTM facing values in the same order
    //     else {
    //         return blockFacing.value
    //     }
    // })


    const blocksetsPath = '../data/_blocksets.json'
    const blocksetsData = ref(null)

    const loadBlocksetsData = async () => {
        const res = await fetch(blocksetsPath)
        blocksetsData.value = await res.json()
    }

    let _currBlocksetIdx = 0
    const currBlocksetIdx = computed({
        get: () => _currBlocksetIdx,
        set: (value) => {
            _currBlocksetIdx = value
            loadBlocksetBlockdata()
            loadBlocksetPalettes()
        }
    })

    const currBlocksetDir = computed(() => {
        if (!blocksetsData.value) {
            return undefined
        }
        return blocksetsData?.value[_currBlocksetIdx]?.dir
    })


    const currBlocksetBlockdata = ref(null)
    const loadBlocksetBlockdata = async () => {
        const res = await fetch(currBlocksetDir.value + '/_blockdata.json')
        currBlocksetBlockdata.value = await res.json()
    }
    const currBlocksetPalettes = ref(null)
    const loadBlocksetPalettes = async () => {
        const res = await fetch(currBlocksetDir.value + '/_palettes.json')
        currBlocksetPalettes.value = await res.json()

        // Also add default pseudo-palette
        currBlocksetPalettes.value.unshift({
            name: 'Default (all blocks)',
            count: -1
        })
    }

    const currPaletteIdx = ref(null)


    const getBlockTexturePath = (texture) => currBlocksetDir.value + '/' + texture


    return {
        // locale,
        blockSize, changeBlockSize,
        blockFacing,
        blocksetsPath,
        blocksetsData, loadBlocksetsData,
        currBlocksetIdx, currBlocksetDir,
        currBlocksetBlockdata, loadBlocksetBlockdata,
        currBlocksetPalettes, loadBlocksetPalettes,
        currPaletteIdx,
        getBlockTexturePath
    }
})
