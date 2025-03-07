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
        // return ['Not Currently Impleneted!']
    })
</script>

<template>
    <section class="blockviz-controls__wrap">
        <div class="blockviz-controls">
            <div class="blockviz-controls__blob">
                Side: 
                <SidePicker v-model="GlobalStore.blockFacing" />
            </div>

            <BigBlackButton @click="SimpleViewStore.blockVizGenerate(
                GlobalStore.currBlocksetBlockdata,
                GlobalStore.currBlocksetPalettes[GlobalStore.currPaletteIdx],
                GlobalStore.blockFacing
            )" :isReady="!GlobalStore.blocksetsData">
                <template #normal>GENERATE BLOCK GRAIDENT</template>
                <template #disabled>Loading data, please wait…</template>
            </BigBlackButton>

            <div class="blockviz-controls__blob">
                <SlottedButton class="round" @click="GlobalStore.changeBlockSize(0.5)">➖</SlottedButton>
                <SlottedButton class="round" @click="GlobalStore.changeBlockSize(2.0)">➕</SlottedButton>
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
            :class="{'one-row': SimpleViewStore.blockVizCfg.resultsInOneRow}"
        >
            <Block v-for="(block, i) in SimpleViewStore.blockVizData"
                :key="i" :name="block.name" :texture="block.texture"
            />
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
        gap: 4vw;
        height: 64px;
        transform: translateY(-32px);
    }
    .blockviz-controls__blob {
        @include flex-center;
        height: 40px;
        gap: 4px;
        border-radius: $BR_round;
        padding: 4px;
        background: linear-gradient(#181818bb 50%, $trans 51%);
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
        flex-wrap: wrap;
        margin: 16px;

        &.one-row {
            flex-wrap: nowrap !important;
        }
    }
</style>
