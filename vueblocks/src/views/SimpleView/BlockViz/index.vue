<script setup lang="ts">
import type { Blockset } from '@/types/blocksets'
import type { BlockTooltip } from '@/types/overlays'
import type { Palette } from '@/types/palettes'

import { computed, ref } from 'vue'
import { Wowerlay } from 'wowerlay'
import Block from '@/components/Block.vue'
import Icon from '@/components/Icon.vue'
import SidePicker from '@/components/SidePicker.vue'

import SlottedButton from '@/components/SlottedButton.vue'
import SlottedCheckbox from '@/components/SlottedCheckbox.vue'
import SlottedDropdown from '@/components/SlottedDropdown.vue'
import { overlayShow } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'
import BlockPickPalette from '../BlockPick/BlockPickPalette.vue'
import BigBlackButton from './BigBlackButton.vue'

const GlobalStore = useGlobalStore()
const SimpleViewStore = useSimpleViewStore()

const tooltipData = ref<BlockTooltip>({ target: null, name: 'missingNo' })

const blocksetsDataNames = computed((): Blockset['name'][] => {
    if (!GlobalStore.blocksetsData) { return ['Loading…'] }

    return GlobalStore.blocksetsData.map(bsd => bsd !== '<hr>' ? bsd.name : '<hr>')
})

const blockdataPaletteNames = computed((): Palette['name'][] => {
    if (!GlobalStore.currBlocksetPalettes) { return ['Loading…'] }

    return GlobalStore.currBlocksetPalettes.map(pal => pal !== '<hr>' ? pal.name : '<hr>')
})

// This is a rather fragile solution, however, as it's impossible to
// remove rows other than delete all of them, it is toletable I guess?
const hiddenBlockIds = ref<Set<string>>(new Set()) // Format: 'row_block'

function copyBlockTextureName(name: string) {
    navigator.clipboard.writeText(name.split('.png')[0])
}

// We assume the Edit palette option is always the latest one,
// which is kinda brittle, but the opposite can't happen normally
const processPaletteIdx = computed({
    get: () => GlobalStore.currPaletteIdx,
    set: (idx) => {
        if (idx === (GlobalStore.currBlocksetPalettes.length - 1)) {
            test()
        }
        else {
            GlobalStore.currPaletteIdx = idx
        }
    },
})
// TODO: fix this faulty piece of logic below and above (bruh)

async function test() {
    const res = await overlayShow([BlockPickPalette, []])
    console.log(res)

    if (res !== null) {
        GlobalStore.currPaletteIdx = 1
    }
    else {
        GlobalStore.currPaletteIdx = 0
    }
}
</script>

<template>
    <section class="blockviz-controls__wrap">
        <div class="blockviz-controls">
            <div class="blockviz-controls__blob round">
                <SidePicker v-model="GlobalStore.blockFacing" />
            </div>

            <div class="blockviz-controls__blob">
                <BigBlackButton
                    :is-loaded="!GlobalStore.currBlocksetBlockdata"
                    @click="() => {
                        SimpleViewStore.blockVizGenerate(
                            GlobalStore.currBlocksetIdx,
                            GlobalStore.currBlocksetBlockdata,
                            (
                                GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx] === '<hr>'
                                    ? GlobalStore.currBlocksetPalettes[0] as Palette // 'All Blocks' palette always comes first
                                    : GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx] as Palette
                            ),
                            GlobalStore.blockFacing,
                        )
                        if (SimpleViewStore.blockVizData.length < 2) {
                            hiddenBlockIds.clear()
                        }
                    }"
                >
                    <template #normal>
                        GENERATE BLOCK GRAIDENT
                    </template>
                    <template #disabled>
                        Loading blockdata, please wait…
                    </template>
                </BigBlackButton>
            </div>

            <div class="blockviz-controls__blob round">
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
            </div>
        </div>
        <small>
            tip: left click a block to hide it, right click to copy id
        </small>
    </section>

    <section class="blockviz-options--blockset__wrap">
        <div class="blockviz-options--blockset">
            <div class="blockviz-options--blockset__inner">
                <SlottedDropdown
                    v-model="GlobalStore.currBlocksetIdx"
                    :names="blocksetsDataNames"
                >
                    Version:
                </SlottedDropdown>

                <SlottedDropdown
                    v-model="processPaletteIdx"
                    :names="blockdataPaletteNames"
                >
                    Palette:
                </SlottedDropdown>
            </div>

            <div class="blockviz-options--blockset__inner">
                <!-- <div style="display: flex; justify-content: center; flex-wrap: wrap;">
                    <SlottedDropdown
                        v-model="SimpleViewStore.blockFilterCfg.noiseMinThreshold" :names="['0%', '30%', '50%']"
                        :default="0"
                    >
                        <abbr title="Filters out blocks with colour noise percentage higher than given. The lower the threshold, the less 'noisy' blocks will be used for generation.">Noise:</abbr>
                    </SlottedDropdown>
                    <SlottedDropdown
                        v-model="SimpleViewStore.blockFilterCfg.noiseMaxThreshold" :names="['30%', '50%', '70%', '80%', '100%']"
                        :default="4"
                    >
                        &nbsp; to
                    </SlottedDropdown>
                </div> -->

                <SlottedCheckbox v-model="SimpleViewStore.blockFilterCfg.useCIELAB">
                    <abbr title="Use colourspace closer to how human eyes percive colour. Results in more vibrant looking and accurate, but less dark and contrast gradients.">Use&nbsp;CIELAB</abbr>
                </SlottedCheckbox>
            </div>
        </div>
    </section>

    <section class="blockviz-data__wrap">
        <div
            class="blockviz-data"
            :class="{ 'one-row': SimpleViewStore.blockVizCfg.resultsInOneRow }"
        >
            <div v-for="(row, i) in SimpleViewStore.blockVizData" :key="i">
                <Block
                    v-for="(block, j) in row.textures" :key="j"
                    :name="block.name" :blockset-idx="row.blocksetIdx" :texture="block.texture"
                    :class="{ 'block-hidden': hiddenBlockIds.has(`${i}_${j}`) }"
                    @click="() => hiddenBlockIds.add(`${i}_${j}`)"
                    @contextmenu.prevent="() => copyBlockTextureName(block.texture)"
                    @mouseenter.prevent="(e: MouseEvent) => tooltipData = {
                        target: e.target as HTMLElement,
                        name: block.name,
                    }"
                    @mouseleave.prevent="(e: MouseEvent) => tooltipData.target = null"
                />
            </div>
        </div>
    </section>

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

    .blockviz-controls__wrap {
        background: linear-gradient(transparent 32px, #181818bb 32px, $dark_bg);
    }
    .blockviz-controls {
        @include flex-center;
        height: 64px;
        gap: 2vw; // 4vw;
    }
    .blockviz-controls__blob {
        @include flex-center;
        padding: 4px; gap: 4px;
        background: linear-gradient(#181818bb 50.5%, $trans 50.5%);
        border-radius: calc($BR_big + $BR_regular);

        &.round {
            border-radius: $BR_round;
        }
    }

    .blockviz-options--blockset__wrap {
        background: $dark_bg;
    }
    .blockviz-options--blockset {
        @include responsive-width;
        margin: 6px auto 0;

        &, .blockviz-options--blockset__inner {
            @include flex-center;
            flex-wrap: wrap;
            gap: 8px 16px;
        }
    }

    .blockviz-data__wrap {
        flex: 1;
        background: $dark_bg;
        overflow: auto;
    }
    .blockviz-data {
        display: flex; flex-direction: column;
        margin: 16px;

        & > div {
            display: flex; flex-direction: row;
            flex-wrap: wrap;
        }

        &.one-row, &.one-row > div {
            flex-wrap: nowrap !important;

            // That's probably a dumb solution but it'll work for now...
            & *:last-child {
                padding-right: 16px;
            }
        }
    }

    .side-picker__wrap {
        width: 84px; height: 40px;
    }
</style>
