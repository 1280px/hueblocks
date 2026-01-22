<script setup lang="ts">
import type { BlockFacing, Block as BlockT } from '@/types/blocks'
import type { BlockTooltip as BlockTooltipT } from '@/types/overlays'
import type { Palette } from '@/types/palettes'
import type { ColorbarSeg } from '@/types/simpleview'

import { ref, watch } from 'vue'

import Block from '@/components/Block.vue'
import BlockTooltip from '@/components/BlockTooltip.vue'
import Icon from '@/components/Icon.vue'
import SidePicker from '@/components/SidePicker.vue'
import SlottedButton from '@/components/SlottedButton.vue'
import { overlayIsShown } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const { originalFacing = 'all' } = defineProps<{
    originalFacing?: BlockFacing,
}>()

const emit = defineEmits<{
    done: [block?: Omit<ColorbarSeg, 'steps'>],
}>()

const GlobalStore = useGlobalStore()
const SimpleViewStore = useSimpleViewStore()

const blockdataByAlphabet = ref<Record<string, BlockT[]>>({})
const localFilterByFacing = ref<BlockFacing>(originalFacing)

const tooltipData = ref<BlockTooltipT>({ target: null, name: 'missingNo' })

function updateBlocksetData() {
    const filteredBlockdata = SimpleViewStore.getFilteredBlockdata(
        GlobalStore.currBlocksetBlockdata,
        (
            GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx] === '<hr>'
                ? GlobalStore.currBlocksetPalettes[0] as Palette // 'All Blocks' always comes first
                : GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx] as Palette
        ),
        localFilterByFacing.value,
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
    overlayIsShown,
    () => {
        updateBlocksetData()
        localFilterByFacing.value = originalFacing
    },
    { immediate: true },
)
</script>

<template>
    <header>
        <h2>— &nbsp; Pick a block to use as colour reference &nbsp; —</h2>
    </header>

    <main>
        <section v-for="bdLetter of Object.keys(blockdataByAlphabet)" :key="bdLetter">
            <span>{{ bdLetter }}</span>

            <button
                v-for="block of blockdataByAlphabet[bdLetter]" :key="block.name"
                class="block__click-wrap"
                @click="emit('done', {
                    color: block.rgb,
                    blockRef: {
                        name: block.name,
                        blocksetIdx: GlobalStore.currBlocksetIdx,
                        texture: block.texture,
                    },
                })"
                @mouseenter.prevent="(e: MouseEvent) => tooltipData = {
                    target: e.target as HTMLElement, name: block.name,
                }"
                @mouseleave.prevent="(e: MouseEvent) => tooltipData.target = null"
            >
                <Block
                    :name="block.name"
                    :blockset-idx="GlobalStore.currBlocksetIdx"
                    :texture="block.texture"
                />
            </button>
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

        <SidePicker
            v-model="localFilterByFacing" :is-compact="true" @change="updateBlocksetData()"
        />

        <SlottedButton
            round
            title="Zoom out (0.5x)"
            :disabled="Number.parseInt(GlobalStore.blockSize) <= 16"
            @click="GlobalStore.changeBlockSize(0.5)"
        >
            <Icon name="zoom-out" />
        </SlottedButton>

        <SlottedButton
            round
            title="Zoom in (2.0x)"
            :disabled="Number.parseInt(GlobalStore.blockSize) >= 256"
            @click="GlobalStore.changeBlockSize(2.0)"
        >
            <Icon name="zoom-in" />
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

    .block__click-wrap {
        appearance: none;
        width: fit-content; height: fit-content;
        padding: 0;
        background: none; border: none;

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
    }
</style>
