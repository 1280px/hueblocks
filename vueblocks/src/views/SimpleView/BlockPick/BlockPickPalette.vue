<script setup lang="ts">
import type { Block as BlockT } from '@/types/blocks'
import type { BlockTooltip as BlockTooltipT } from '@/types/overlays'
import type { Palette } from '@/types/palettes'

import { ref, watch } from 'vue'

import Block from '@/components/Block.vue'
import BlockTooltip from '@/components/BlockTooltip.vue'
import Icon from '@/components/Icon.vue'
import SlottedButton from '@/components/SlottedButton.vue'
import { overlayIsShown } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const { originalPaletteIdx = -1 } = defineProps<{
    originalPaletteIdx?: number,
}>()

const emit = defineEmits<{
    done: [blocks?: BlockT['texture'][]],
}>()

const GlobalStore = useGlobalStore()
const SimpleViewStore = useSimpleViewStore()

const blockdataByAlphabet = ref<Record<string, BlockT[]>>({})

const errText = ref<string>('')

const tooltipData = ref<BlockTooltipT>({ target: null, name: 'missingNo' })

function updateBlocksetData() {
    const filteredBlockdata = SimpleViewStore.getFilteredBlockdata(
        GlobalStore.currBlocksetBlockdata,
        (
            GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx] === '<hr>'
                ? GlobalStore.currBlocksetPalettes[0] as Palette // 'All Blocks' always comes first
                : GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx] as Palette
        ),
        'all',
    )

    blockdataByAlphabet.value = {}

    for (const block of filteredBlockdata.sort(
        (b1, b2) => b1.name.localeCompare(b2.name),
    )) {
        const letter = block.name[0]
        if (!blockdataByAlphabet.value[letter]) {
            blockdataByAlphabet.value[letter] = []
        }
        blockdataByAlphabet.value[letter].push(block)
    }
}

// https://stackoverflow.com/questions/39007637/javascript-set-vs-array-performance
const selectedTextures = ref<Set<BlockT['texture']>>(new Set())

function selectTexture(texture: BlockT['texture'], isAdded: boolean) {
    if (isAdded && !selectedTextures.value.has(texture)) {
        selectedTextures.value.add(texture)
    }
    else if (!isAdded && selectedTextures.value.has(texture)) {
        selectedTextures.value.delete(texture)
    }
}

function selectPaletteTextures(paletteIdx: number) {
    selectedTextures.value.clear()

    // console.log(paletteIdx)
    if (
        GlobalStore.currBlocksetPalettes[paletteIdx] === '<hr>'
        || !GlobalStore.currBlocksetPalettes[paletteIdx].textures.length
    ) {
        return
    }

    const filteredBlockdata = SimpleViewStore.getFilteredBlockdata(
        GlobalStore.currBlocksetBlockdata,
        GlobalStore.currBlocksetPalettes[paletteIdx],
        'all',
    )
    selectedTextures.value = new Set(
        filteredBlockdata.map(block => block.texture),
    )
    // console.log(selectedTextures.value)
}

async function handlePaletteImport() {
    try {
        const newSelectedTextures: BlockT['texture'][] = await GlobalStore.importCustomPalette()
        selectedTextures.value = new Set(newSelectedTextures)
        errText.value = ''
    }
    catch (err) {
        errText.value = (err as Error).message ?? 'An unknown import error has occured :('
    }
}

watch(
    overlayIsShown,
    () => {
        updateBlocksetData()
        selectPaletteTextures(originalPaletteIdx)
    },
    { immediate: true },
)
</script>

<template>
    <header>
        <h2 v-if="selectedTextures.size < 3">
            — &nbsp; Pick 3+ blocks you want to use as a palette &nbsp; —
        </h2>
        <h2 v-else>
            — &nbsp; Editing custom palette ({{ selectedTextures.size }}
            / {{ GlobalStore.currBlocksetBlockdata.length }} blocks) &nbsp; —
        </h2>

        <h3 v-show="errText">
            {{ errText }}
        </h3>
    </header>

    <main>
        <section v-for="bdLetter of Object.keys(blockdataByAlphabet)" :key="bdLetter">
            <span>{{ bdLetter }}</span>

            <template v-for="block of blockdataByAlphabet[bdLetter]" :key="block.name">
                <input
                    :id="block.texture" type="checkbox" class="block__select-cb"
                    :checked="selectedTextures.has(block.texture)"
                    @change="(e: InputEvent) => selectTexture(
                        block.texture, (e.target as HTMLInputElement).checked,
                    )"
                >

                <label
                    :for="block.texture" class="block__select-wrap"
                    @mouseenter.prevent="(e: MouseEvent) => tooltipData = {
                        target: e.target as HTMLElement, name: block.name,
                    }"
                    @mouseleave.prevent="() => tooltipData.target = null"
                >
                    <Block
                        :name="block.name"
                        :blockset-idx="GlobalStore.currBlocksetIdx"
                        :texture="block.texture"
                    />
                </label>
            </template>
        </section>
    </main>

    <aside>
        <SlottedButton
            round
            title="Cancel (ESC)"
            @click="emit('done')"
        >
            <Icon name="close" />
        </SlottedButton>

        <SlottedButton
            round
            title="Import palette textures…"
            @click="handlePaletteImport()"
        >
            <Icon name="import" />
        </SlottedButton>

        <SlottedButton
            round
            :disabled="selectedTextures.size < 3"
            :title="selectedTextures.size < 3
                ? 'Please select at least 3 blocks!'
                : 'Export selected textures… (right click to export unselected)'"
            @click="GlobalStore.exportCustomPalette(Array.from(selectedTextures))"
            @contextmenu.prevent="GlobalStore.exportCustomPalette(
                GlobalStore.currBlocksetBlockdata.map(b => b.texture)
                    .filter(t => !selectedTextures.has(t)),
            )"
        >
            <Icon name="export" />
        </SlottedButton>

        <SlottedButton
            round
            :disabled="selectedTextures.size < 3"
            :title="selectedTextures.size < 3
                ? 'Please select at least 3 blocks!'
                : 'Update custom palette'"
            @click="emit('done', Array.from(selectedTextures))"
        >
            <Icon name="check" />
        </SlottedButton>
    </aside>

    <BlockTooltip :tooltip-data="tooltipData" />
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    section {
        display: flex;
        flex-wrap: wrap;
        width: 100%;
        margin: 4px 4px 20px;

        & span {
            position: absolute;
            margin-left: -32px;
        }
    }

    .block__select-cb {
        display: none;
    }

    .block__select-wrap {
        & .block {
            transition: $TR_regular;
        }

        &:hover, &:focus {
            z-index: 999;

            & .block {
                box-shadow: 0 0 0 4px $white_50, 0 0 8px 4px #0004;
                transition: all 0ms, scale $TR_slow;
            }

            &:active .block {
                box-shadow: 0 0 0 2px $white_80, 0 0 4px 4px #0004;
                transition: $TR_regular;
                scale: 0.875;
            }
        }

        .block__select-cb:checked + & .block {
            transition: all $TR_regular, scale $TR_slow;
            scale: 0.75;
        }
    }
</style>
