<script setup lang="ts">
import type { Block as BlockT } from '@/types/blocks'
import type { BlockTooltip as BlockTooltipT } from '@/types/overlays'
import type { Palette } from '@/types/palettes'

import { defineEmits, ref, watch } from 'vue'

import Block from '@/components/Block.vue'
import BlockTooltip from '@/components/BlockTooltip.vue'
import Icon from '@/components/Icon.vue'
import SlottedButton from '@/components/SlottedButton.vue'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const emit = defineEmits<{
    done: [blocks?: BlockT[]],
}>()

const GlobalStore = useGlobalStore()
const SimpleViewStore = useSimpleViewStore()

const blockdataByAlphabet = ref<Record<string, BlockT[]>>({})
const selectedBlockdata = ref<Set<BlockT>>(new Set())

const tooltipData = ref<BlockTooltipT>({ target: null, name: 'missingNo' })

function updateBlocksetData() {
    const filteredBlockdata = SimpleViewStore.getFilteredBlockdata(
        GlobalStore.currBlocksetBlockdata,
        (
            GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx] === '<hr>'
                ? GlobalStore.currBlocksetPalettes[0] as Palette // 'All Blocks' palette always comes first
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

watch(
    () => GlobalStore.currBlocksetBlockdata,
    () => updateBlocksetData(),
    { immediate: true },
)
</script>

<template>
    <header>
        <h2>— &nbsp; Pick blocks you want to use as a palette &nbsp; —</h2>
    </header>

    <main>
        <h1>Work in progress!!!</h1>

        <hr>

        <section v-for="bdLetter of Object.keys(blockdataByAlphabet)" :key="bdLetter">
            <span>{{ bdLetter }}</span>
            <Block
                v-for="block of blockdataByAlphabet[bdLetter]" :key="block.name"
                :name="block.name" :blockset-idx="GlobalStore.currBlocksetIdx" :texture="block.texture"
                @mouseenter.prevent="(e: MouseEvent) => tooltipData = {
                    target: e.target as HTMLElement, name: block.name,
                }"
                @mouseleave.prevent="(e: MouseEvent) => tooltipData.target = null"
            />
        </section>
    </main>

    <aside>
        <SlottedButton
            class="round"
            title="Cancel (ESC)"
            @click="emit('done')"
        >
            <Icon name="close" />
        </SlottedButton>

        <SlottedButton
            class="round"
            title="Zoom out (test minus)"
            @click="GlobalStore.changeBlockSize(1 / 1.5)"
        >
            <Icon name="zoom-out" />
        </SlottedButton>

        <SlottedButton
            class="round"
            title="Zoom in (test plus)"
            @click="GlobalStore.changeBlockSize(1.5)"
        >
            <Icon name="zoom-in" />
        </SlottedButton>

        <SlottedButton
            class="round"
            :disabled="selectedBlockdata.entries.length < 3"
            :title="selectedBlockdata.entries.length < 3 ? 'Please select at least 3 blocks!' : 'Select'"
            @click="emit('done', Array.from(selectedBlockdata))"
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
</style>
