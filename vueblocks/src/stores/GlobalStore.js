import {ref, computed} from 'vue'
import {defineStore} from 'pinia'


export const useGlobalStore = defineStore('GlobalStore', () => {
    const locale = ref('en')
    const viewMode = ref('simple')

    // https://vite.dev/guide/env-and-mode
    const _baseUrl = import.meta.env.BASE_URL !== '/' ? import.meta.env.BASE_URL : '.'

    const getIconPath = (icon) => _baseUrl + '/icons/' + icon + '.svg'


    const blockSize = ref('64px')
    const changeBlockSize = (scale) => {
        const newBlockSize = parseInt(blockSize.value) * scale

        if (newBlockSize >= 16 && newBlockSize <= 256) {
            blockSize.value = newBlockSize + 'px'
        }
    }

    const blockFacing = ref('all')


    const blocksetsPath = _baseUrl + '/blocksets/' + '_blocksets.json'
    const blocksetsData = ref(null)

    const loadBlocksetsData = async () => {
        const res = await fetch(blocksetsPath)
        const data = await res.json()

        // If no blocksets data found, we are really really screwed
        blocksetsData.value = data.length ? data : [{
            name: 'Error!!! No data found'
        }]
    }

    let _currBlocksetIdx = ref(0) // We use this to store the actial value outside the computed property
    const currBlocksetIdx = computed({
        get: () => _currBlocksetIdx.value,
        set: (value) => {
            _currBlocksetIdx.value = value
            loadBlocksetBlockdata()
            loadBlocksetPalettes()
        }
    })
    
    const getBlocksetPath = (blocksetIdx) => {
        if (!blocksetsData.value || !blocksetsData?.value[blocksetIdx]) {
            return 'missingNo'
        }
        return _baseUrl + '/blocksets/' + blocksetsData?.value[blocksetIdx]?.dir
    }
    const getTexturePath = (blocksetIdx, texture) => {
        const blocksetPath = getBlocksetPath(blocksetIdx)
        return blocksetPath + '/' + texture
    }


    const currBlocksetBlockdata = ref(null)
    const loadBlocksetBlockdata = async () => {
        const blocksetPath = getBlocksetPath(currBlocksetIdx.value)
        const res = await fetch(blocksetPath + '/' + '_blockdata.json')
        currBlocksetBlockdata.value = await res.json()
    }
    const currBlocksetPalettes = ref(null)
    const loadBlocksetPalettes = async () => {
        const blocksetPath = getBlocksetPath(currBlocksetIdx.value)
        const res = await fetch(blocksetPath + '/' + '_palettes.json')
        let data = await res.json()
        data = data.filter((p) => p.count && (p.count > 0) && p.textures)

        // If no valid palettes found, we're okay, just don't add anything
        currBlocksetPalettes.value = data.length ? data : []
        
        // Add default pseudo-palette
        currBlocksetPalettes.value.unshift({
            name: 'Default (all blocks)',
            count: -1
        })
    }

    const currPaletteIdx = ref(null)


    return {
        locale, viewMode, getIconPath,
        blockSize, changeBlockSize,
        blockFacing,
        blocksetsPath,
        blocksetsData, loadBlocksetsData,
        currBlocksetIdx,
        getBlocksetPath, getTexturePath,
        currBlocksetBlockdata, loadBlocksetBlockdata,
        currBlocksetPalettes, loadBlocksetPalettes,
        currPaletteIdx
    }
})
