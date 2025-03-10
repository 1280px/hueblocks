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


    // https://vite.dev/guide/env-and-mode
    const _baseUrl = import.meta.env.BASE_URL !== '/' ? import.meta.env.BASE_URL : '.'

    const blocksetsPath = _baseUrl + '/' + '_blocksets.json'
    const blocksetsData = ref(null)

    const loadBlocksetsData = async () => {
        const res = await fetch(blocksetsPath)
        const json = await res.json()

        // If blocksets data not found, we are really really screwed
        blocksetsData.value = json.length ? json : [{
            name: 'Error!!! No data found'
        }]
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
        return _baseUrl + '/' + blocksetsData?.value[_currBlocksetIdx]?.dir
    })


    const currBlocksetBlockdata = ref(null)
    const loadBlocksetBlockdata = async () => {
        const res = await fetch(currBlocksetDir.value + '/' + '_blockdata.json')
        currBlocksetBlockdata.value = await res.json()
    }
    const currBlocksetPalettes = ref(null)
    const loadBlocksetPalettes = async () => {
        const res = await fetch(currBlocksetDir.value + '/' + '_palettes.json')
        const json = await res.json()

        // If no palettes found, we're okay, just don't add anything
        currBlocksetPalettes.value = json.keys().length ? json : []

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
