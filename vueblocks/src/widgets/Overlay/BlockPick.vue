<script setup>
// This overlay inner component is in widgets dir because it
// expected to be shared across many different views & modes!
import { defineEmits, onMounted, ref, watch } from 'vue'

import Block from '@/components/Block.vue'
import Icon from '@/components/Icon.vue'
import SidePicker from '@/components/SidePicker.vue'
import SlottedButton from '@/components/SlottedButton.vue'

import { overlayIsShown } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const { mode } = defineProps({
    mode: {
        type: String,
        required: true,
    },
})

const emit = defineEmits([
    'done',
])

const GlobalStore = useGlobalStore()
const SimpleViewStore = useSimpleViewStore()

const selectedBlockdata = ref([{}])

const blockdataByAlphabet = ref({})
const blocksetIdx = ref(-1)
const localFilterByFacing = ref('all')

function updateBlocksetData() {
    blocksetIdx.value = GlobalStore.currBlocksetIdx
    const filteredBlockdata = SimpleViewStore.getFilteredBlockdata(
        GlobalStore.currBlocksetBlockdata,
        GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx],
        localFilterByFacing.value || 'all',
    )

    const newBlockdataByAlphabet = {}

    for (const block of filteredBlockdata.sort(
        (b1, b2) => b1.name.localeCompare(b2.name),
    )) {
        const letter = block.name[0]
        if (!newBlockdataByAlphabet[letter]) {
            newBlockdataByAlphabet[letter] = []
        }
        newBlockdataByAlphabet[letter].push(block)
    }

    blockdataByAlphabet.value = newBlockdataByAlphabet
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
    <div class="blockpick">
        <header v-if="mode === 'palette'">
            <h2>— &nbsp; Pick blocks you want to use as a palette &nbsp; —</h2>
        </header>
        <header v-else-if="mode === 'color'">
            <h2>— &nbsp; Pick a block to use as colour reference &nbsp; —</h2>
        </header>

        <main v-if="mode === 'palette'">
            TODO: Consider whether this section should be left untouched until the
            palettes refresh (and, well, whether palettes refresh is needed at all...)
        </main>

        <main v-else-if="mode === 'color'">
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
                    />
                </button>
            </section>
        </main>
    </div>

    <aside class="blockpick-controls">
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

        <SlottedButton
            v-if="mode === 'palette'" class="round"
            :disabled="selectedBlockdata.length < 3"
            :title="selectedBlockdata.length < 3 ? 'Please select at least 3 blocks!' : 'Select'"
            @click="emit('done', selectedBlockdata)"
        >
            <Icon name="check" />
        </SlottedButton>
    </aside>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;
    .blockpick {
        @include responsive-width;

        flex: 1;
        position: relative;
        display: flex; flex-direction: column;
        margin: auto;
    }

    header {
        @include flex-center;
        margin-bottom: 32px;

        @media (max-width: 880px) {
            margin-top: 64px;
        }
    }

    main {
        display: flex; flex-direction: column;
        width: 100%;
    }
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

    .blockpick-controls {
        position: absolute;
        top: 32px; right: 32px;
        display: flex; flex-direction: row-reverse;
        justify-content: center; align-items: flex-end;
        margin: 0; gap: 4px;

        @media (min-width: 880px) {
            flex-direction: column;
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
            transition: all $TR_fast, scale $TR_slow;

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

    .side-picker__wrap {
        width: 84px; height: 40px;
    }
</style>
