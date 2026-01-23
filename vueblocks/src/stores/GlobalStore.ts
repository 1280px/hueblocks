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

            toggleCustomPalette(false)
            customPaletteTextures.value = []

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
            {
                name: 'Default (all blocks)',
                textures: [],
                count: -1,
            },
            ...currBlocksetPalettes.value,
            '<hr>',
            // {
            //     name: 'Custom palette',
            //     textures: [],
            //     count: -2,
            // },
            {
                name: 'Edit current palette…',
                textures: [],
                count: -3,
            },
        ]
    }

    const currPaletteIdx = ref<PaletteIndex>(2)

    const customPaletteTextures = ref<Palette['textures']>([])
    const toggleCustomPalette = (isShown: boolean) => {
        const customIdx = currBlocksetPalettes.value.findIndex(
            (pal: Palette | '<hr>') => (pal !== '<hr>' && pal.count === -2),
        )

        if (isShown && customIdx === -1) {
            // We want to show the option right before 'Edit palette'
            const editIdx = currBlocksetPalettes.value.findIndex(
                (pal: Palette | '<hr>') => (pal !== '<hr>' && pal.count === -3),
            )

            currBlocksetPalettes.value.splice(editIdx, 0, {
                name: 'Custom palette',
                textures: customPaletteTextures.value,
                count: -2,
            })
        }
        else if (!isShown && customIdx !== -1) {
            currBlocksetPalettes.value.splice(customIdx, 1)
        }
    }

    const importCustomPalette = async () => {
        const opener = document.createElement('input')
        opener.setAttribute('type', 'file')
        opener.setAttribute('accept', 'application/json')
        opener.style.display = 'none'
        document.body.appendChild(opener)
        opener.click()

        const file: File | undefined = await new Promise((resolve) => {
            opener.onchange = () => resolve(opener.files?.[0])
        })
        if (!file) { throw new Error('') }
        opener.remove()

        let textures: Palette['textures']
        try {
            textures = await new Promise((resolve) => {
                const reader = new FileReader()
                reader.onload = () => {
                    resolve(JSON.parse(reader!.result as string)) // Yuck.
                }
                reader.readAsText(file)
            })
        }
        catch (err) {
            throw new Error((err as Error).message ?? 'Unable to read JSON!')
        }

        // eslint-disable-next-line prefer-const
        let missings = [...textures]
        for (const block of currBlocksetBlockdata.value) {
            const idx = missings.indexOf(block.texture)
            if (idx !== -1) {
                missings.splice(idx, 1)
            }
        }

        if (missings.length) {
            // eslint-disable-next-line no-alert
            if (confirm(
                `${missings.length} textures from this palette do not exist!\n\n`
                + 'This might\'ve happened because of incorrectly chosen verion, i.e. if a palette '
                + 'was created a while ago and some textures used by it are now named differently. '
                + '\n\nPress "Cancel" to abort, or "OK" to drop missing textures and continue.',
            )) {
                return textures.filter(texture => !missings.includes(texture))
            }
            else { throw new Error('') }
        }
        else {
            return textures
        }
    }

    const exportCustomPalette = (customPaletteTextures: Palette['textures']) => {
        const json = (
            JSON.stringify(customPaletteTextures, null, 4)
        )
        const blob = new Blob(
            [json],
            { type: 'application/json' },
        )

        const addr = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.setAttribute('href', addr)
        link.setAttribute('download', 'palette.json') // Otherwise FF just opens JSON
        document.body.appendChild(link)
        link.click()
        link.remove()
    }

    return {
        locale, viewMode, getIconPath,
        blockSize, changeBlockSize,
        blockFacing,
        blocksetsPath,
        blocksetsData, loadBlocksetsData, currBlocksetIdx,
        getBlocksetPath, getTexturePath,
        currBlocksetBlockdata, loadBlocksetBlockdata,
        currBlocksetPalettes, loadBlocksetPalettes, currPaletteIdx,
        customPaletteTextures, toggleCustomPalette, importCustomPalette, exportCustomPalette,
    }
})
