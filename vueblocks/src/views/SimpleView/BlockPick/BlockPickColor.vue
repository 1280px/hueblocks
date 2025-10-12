<script setup lang="ts">
import type { BlockFacing, Block as BlockT } from '@/types/blocks'
import type { BlockTooltip } from '@/types/overlays'
import type { ColorbarSeg } from '@/types/simpleview'

import { defineEmits, onMounted, ref, watch } from 'vue'
import { Wowerlay } from 'wowerlay'

import Block from '@/components/Block.vue'
import Icon from '@/components/Icon.vue'
import SidePicker from '@/components/SidePicker.vue'
import SlottedButton from '@/components/SlottedButton.vue'

import { overlayIsShown } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const emit = defineEmits<{
    done: [block?: Omit<ColorbarSeg, 'steps'>],
}>()

const GlobalStore = useGlobalStore()
const SimpleViewStore = useSimpleViewStore()

const blockdataByAlphabet = ref<Record<string, BlockT[]>>({})

const blocksetIdx = ref<number>(-1)
const localFilterByFacing = ref<BlockFacing>('all')
const tooltipData = ref<BlockTooltip>({ target: null, name: 'missingNo' })

function updateBlocksetData() {
    blocksetIdx.value = GlobalStore.currBlocksetIdx

    const filteredBlockdata = SimpleViewStore.getFilteredBlockdata(
        GlobalStore.currBlocksetBlockdata,
        GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx],
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

watch([overlayIsShown, localFilterByFacing], (v) => {
    if (v) {
        // Prevent unneeded update when overlay is being hidden
        updateBlocksetData()
    }
    if (!v) {
        // Reconnect to reactive properties
    }
})

onMounted(() => {
    updateBlocksetData()
})
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
                class="block__click-wrap" @click="emit('done', {
                    color: block.rgb,
                    blockRef: {
                        name: block.name,
                        blocksetIdx,
                        texture: block.texture,
                    },
                })"
            >
                <Block
                    :name="block.name" :blockset-idx="blocksetIdx" :texture="block.texture"
                    @mouseenter.prevent="(e: MouseEvent) => tooltipData = {
                        target: e.target as HTMLElement, name: block.name,
                    }"
                    @mouseleave.prevent="(e: MouseEvent) => tooltipData.target = null"
                />
            </button>
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

        <SidePicker v-model="localFilterByFacing" :is-compact="true" />

        <SlottedButton
            class="round"
            title="Zoom out (0.5x)"
            @click="GlobalStore.changeBlockSize(0.5)"
        >
            <Icon name="zoom-out" />
        </SlottedButton>

        <SlottedButton
            class="round"
            title="Zoom in (2.0x)"
            @click="GlobalStore.changeBlockSize(2.0)"
        >
            <Icon name="zoom-in" />
        </SlottedButton>
    </aside>

    <Wowerlay
        :target="tooltipData.target" :visible="tooltipData.target !== null"
        position="top-start" :gap="parseInt(GlobalStore.blockSize) / 16 * -15"
        class="tooltip" :style="{ 'margin-left': `${parseInt(GlobalStore.blockSize) / 16}px` }"
    >
        {{ tooltipData.name }}
    </Wowerlay>
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
        width: fit-content; height: fit-content;
        padding: 0;
        appearance: none;
        background: none;
        border: none;
        transition: $TR_regular;

        &:hover, &:focus {
            box-shadow: 0 0 0 4px $white_50, 0 0 8px 4px #0004;
            z-index: 999;
            transition: all 0ms, scale $TR_slow;

            &:active {
                box-shadow: 0 0 0 2px $white_80, 0 0 4px 4px #0004;
                transition: $TR_regular;
                scale: 0.875;
            }
        }

        &:checked .block {
            transition: all $TR_regular, scale $TR_slow;
            scale: 0.875;
        }
    }
</style>
