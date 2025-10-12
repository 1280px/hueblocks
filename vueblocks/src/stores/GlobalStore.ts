/* eslint-disable ts/no-use-before-define */
import type { Block, BlockFacing } from '@/types/blocks'
import type { Blockset, BlocksetIndex } from '@/types/blocksets'
import type { Palette, PaletteIndex } from '@/types/palettes'

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useGlobalStore = defineStore('GlobalStore', () => {
    // These two are currently unused, reserved for future
    const locale = ref<string>('en')
    const viewMode = ref<string>('simple')

    // https://vite.dev/guide/env-and-mode
    const _baseUrl = import.meta.env.BASE_URL !== '/' ? import.meta.env.BASE_URL : '.'

    const getIconPath = (icon: string) => `${_baseUrl}/icons/${icon}.svg`

    const blockSize = ref<string>('64px')
    const changeBlockSize = (scale: number) => {
        const newBlockSize = Number.parseInt(blockSize.value) * scale

        if (newBlockSize >= 16 && newBlockSize <= 256) {
            blockSize.value = `${newBlockSize}px`
        }
    }

    const blockFacing = ref<BlockFacing>('all')

    const blocksetsPath = `${_baseUrl}/blocksets/` + `_blocksets.json`

    const blocksetsData = ref<((Blockset | '<hr>')[])>([])
    const loadBlocksetsData = async () => {
        const res = await fetch(blocksetsPath)
        const data = await res.json()

        // If no blocksets data found, we are really really screwed
        blocksetsData.value = data.length
            ? data // .reverse() // <-- Not needed when running from j2bs generated config
            : [{ name: 'Error!!! No data found' }]
    }

    const _currBlocksetIdx = ref<BlocksetIndex>(0) // <-- We use this to store the actial value
    const currBlocksetIdx = computed<BlocksetIndex>({ // outside the computed property below:
        get: () => _currBlocksetIdx.value,
        set: (value) => {
            _currBlocksetIdx.value = value
            currPaletteIdx.value = 0
            loadBlocksetBlockdata()
            loadBlocksetPalettes()
        },
    })

    const getBlocksetPath = (blocksetIdx: number) => {
        if (
            !blocksetsData.value
            || !blocksetsData?.value[blocksetIdx]
            || blocksetsData.value[blocksetIdx] === '<hr>'
        ) {
            return 'missingNo'
        }
        return `${_baseUrl}/blocksets/${blocksetsData?.value[blocksetIdx]?.dir}`
    }

    const getTexturePath = (blocksetIdx: number, texture: string) => {
        const blocksetPath = getBlocksetPath(blocksetIdx)
        return `${blocksetPath}/${texture}`
    }

    const currBlocksetBlockdata = ref<Block[]>([])
    const loadBlocksetBlockdata = async () => {
        const blocksetPath = getBlocksetPath(currBlocksetIdx.value)
        const res = await fetch(`${blocksetPath}/` + `_blockdata.json`)
        const data = await res.json() as Block[]

        // Blockdata timestamp isn't used -- let's log it here at least
        console.info(`Loaded blockset #${currBlocksetIdx.value} -- ${data[0]}`)

        currBlocksetBlockdata.value = data.slice(1)
    }

    const currBlocksetPalettes = ref<(Palette | '<hr>')[]>([])
    const loadBlocksetPalettes = async () => {
        const blocksetPath = getBlocksetPath(currBlocksetIdx.value)
        const res = await fetch(`${blocksetPath}/` + `_palettes.json`)
        let data = await res.json() as Palette[]

        data = data.filter((p: any) => (p?.count > 0) && p?.textures)

        // If no valid palettes found, we're okay, just don't add anything
        currBlocksetPalettes.value = data.length ? data : []

        currBlocksetPalettes.value = [
            ...currBlocksetPalettes.value,
            '<hr>',
            // {
            //     name: 'Custom palette',
            //     textures: [],
            //     count: -1,
            // },
            {
                name: 'Edit palette…',
                textures: [],
                count: -1,
            },
        ]

        currBlocksetPalettes.value.unshift({
            name: 'Default (all blocks)',
            textures: [],
            count: -1,
        })
    }

    const currPaletteIdx = ref<PaletteIndex>(0)

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
        currPaletteIdx,
    }
})
