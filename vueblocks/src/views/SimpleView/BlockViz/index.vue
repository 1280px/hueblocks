<script setup>
    import {ref, computed} from 'vue'
    import { useGlobalStore } from '@/stores/GlobalStore'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'

    import BigBlackButton from './BigBlackButton.vue'
    import SidePicker from '@/components/SidePicker.vue'
    import SlottedButton from '@/components/SlottedButton.vue'
    import SlottedDropdown from '@/components/SlottedDropdown.vue'
    import SlottedCheckbox from '@/components/SlottedCheckbox.vue'
    import Block from '@/components/Block.vue'
    import Icon from '@/components/Icon.vue'

    const GlobalStore = useGlobalStore()
    const SimpleViewStore = useSimpleViewStore()

    const blocksetsDataNames = computed(() => {
        if (!GlobalStore.blocksetsData) {
            return ['Loading...']
        }
        return GlobalStore.blocksetsData.map((bsd) => bsd.name)
    })

    const blockdataPaletteNames = computed(() => {
        if (!GlobalStore.currBlocksetPalettes) {
            return ['Loading...']
        }
        return GlobalStore.currBlocksetPalettes.map((pal) => pal.name)
    })
</script>

<template>
    <section class="blockviz-controls__wrap">
        <div class="blockviz-controls">
            <div class="blockviz-controls__blob round">
                <SidePicker v-model="GlobalStore.blockFacing" />
            </div>

            <div class="blockviz-controls__blob">
                <BigBlackButton @click="SimpleViewStore.blockVizGenerate(
                    GlobalStore.currBlocksetIdx,
                    GlobalStore.currBlocksetBlockdata,
                    GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx],
                    GlobalStore.blockFacing
                )" :isLoaded="!GlobalStore.currBlocksetBlockdata">
                    <template #normal>GENERATE BLOCK GRAIDENT</template>
                    <template #disabled>Loading blockdata, please wait…</template>
                </BigBlackButton>
            </div>

            <div class="blockviz-controls__blob round">
                <SlottedButton class="round"
                    @click="GlobalStore.changeBlockSize(0.5)"
                title="Zoom out (0.5x)">
                    <Icon name="zoom-out" />
                </SlottedButton>
                <SlottedButton class="round"
                    @click="GlobalStore.changeBlockSize(2.0)"
                title="Zoom in (2.0x)">
                    <Icon name="zoom-in" />
                </SlottedButton>
            </div>
        </div>
    </section>

    <section class="blockviz-options--blockset__wrap">
        <div class="blockviz-options--blockset">
            <div class="blockviz-options--blockset__inner">
                <SlottedDropdown :names="blocksetsDataNames"
                    v-model="GlobalStore.currBlocksetIdx"
                >
                    Version:
                </SlottedDropdown>

                <SlottedDropdown :names="blockdataPaletteNames"
                    v-model="GlobalStore.currPaletteIdx"
                >
                    Palette:
                </SlottedDropdown>
            </div>

            <div class="blockviz-options--blockset__inner">
                <!-- <div style="display: flex">
                    <SlottedDropdown :names="['0%', '30%', '50%']" :default="0"
                        v-model="SimpleViewStore.blockDataCfg.noiseMinThreshold"
                    >
                        <abbr title="Filters out blocks with colour noise percentage higher than given. The lower the threshold, the less 'noisy' blocks will be used for generation."
                        >Noise:</abbr>
                    </SlottedDropdown>
                    <SlottedDropdown :names="['30%', '50%', '70%', '80%', '100%']" :default="4"
                        v-model="SimpleViewStore.blockDataCfg.noiseMaxThreshold"
                    >
                        &nbsp;to
                    </SlottedDropdown>
                </div> -->

                <SlottedCheckbox v-model="SimpleViewStore.blockDataCfg.useCIELAB">
                    <abbr title="Use colourspace closer to how human eyes percive colour. Results in more vibrant looking and accurate, but less dark and contrast gradients."
                    >Use&nbsp;CIELAB</abbr>
                </SlottedCheckbox>
            </div>
        </div>
    </section>

    <section class="blockviz-data__wrap">
        <div class="blockviz-data"
            :class="{ 'one-row': SimpleViewStore.blockVizCfg.resultsInOneRow }"
        >
            <div v-for="(row, i) in SimpleViewStore.blockVizData">
                <Block v-for="(block, i) in row.textures" :key="i"
                    :name="block.name" :blocksetIdx="row.blocksetIdx" :texture="block.texture"
                />
            </div>
        </div>
    </section>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .blockviz-controls__wrap {
        height: 48px;
        transform: translateY(32px);
        margin: 4px 0 32px;
        background: linear-gradient(#181818bb, $dark_bg);
    }
    .blockviz-controls {
        @include flex-center;
        gap: 2vw; // 4vw;
        height: 64px;
        transform: translateY(-32px);
    }
    .blockviz-controls__blob {
        @include flex-center;
        // height: 40px;
        gap: 4px;
        border-radius: calc($BR_big + $BR_regular);
        padding: 4px;
        background: linear-gradient(#181818bb 50%, $trans 51%);

        &.round {
            border-radius: $BR_round;
        }
    }

    .blockviz-options--blockset__wrap {
        background: $dark_bg;
    }
    .blockviz-options--blockset {
        @include responsive-width;
        margin: auto;

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
        display: flex;
        flex-direction: column;
        margin: 16px;

        & > div {
            display: flex;
            flex-direction: row;
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
</style>
