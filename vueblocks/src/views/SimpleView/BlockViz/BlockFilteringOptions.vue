<script setup lang="ts">
import type { Blockset } from '@/types/blocksets'
import type { Palette } from '@/types/palettes'

import { computed } from 'vue'

import SlottedCheckbox from '@/components/SlottedCheckbox.vue'
import SlottedDropdown from '@/components/SlottedDropdown.vue'
import { overlayShow } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'
import BlockPickPalette from '../BlockPick/BlockPickPalette.vue'

const GlobalStore = useGlobalStore()
const SimpleViewStore = useSimpleViewStore()

const blocksetsDataNames = computed((): Blockset['name'][] => {
    if (!GlobalStore.blocksetsData) { return ['Loading…'] }

    return GlobalStore.blocksetsData.map(bsd => bsd !== '<hr>' ? bsd.name : '<hr>')
})

const blockdataPaletteNames = computed((): Palette['name'][] => {
    if (!GlobalStore.currBlocksetPalettes) { return ['Loading…'] }

    return GlobalStore.currBlocksetPalettes.map(pal => pal !== '<hr>' ? pal.name : '<hr>')
})

// We assume the 'Edit palette' option is always the latest -- brittle!
async function processPaletteChange(idx: number) {
    if (idx === (GlobalStore.currBlocksetPalettes.length - 1)) {
        const res = await overlayShow(
            [BlockPickPalette, { originalPaletteIdx: GlobalStore.currPaletteIdx }],
        )

        // console.log(res, GlobalStore.currPaletteIdx, GlobalStore.customPaletteTextures)

        if (res !== null) {
            GlobalStore.customPaletteTextures = [...res]
            GlobalStore.toggleCustomPalette(true)
            GlobalStore.currPaletteIdx = GlobalStore.currBlocksetPalettes.length - 2
        }
        else {
            GlobalStore.currPaletteIdx = 0
        }
    }
    else {
        GlobalStore.currPaletteIdx = idx
    }
}
</script>

<template>
    <section class="blockviz-options__wrap">
        <div class="blockviz-options">
            <div class="blockviz-options__inner">
                <SlottedDropdown
                    v-model="GlobalStore.currBlocksetIdx"
                    :names="blocksetsDataNames"
                >
                    Version:
                </SlottedDropdown>

                <SlottedDropdown
                    v-model="GlobalStore.currPaletteIdx"
                    :names="blockdataPaletteNames"
                    @update:model-value="processPaletteChange"
                >
                    Palette:
                </SlottedDropdown>
            </div>

            <div class="blockviz-options__inner">
                <!-- <div style="display: flex; justify-content: center; flex-wrap: wrap;">
                    <SlottedDropdown
                        v-model="SimpleViewStore.blockFilteringCfg.noiseMinThreshold" :names="['0%', '30%', '50%']"
                        :default="0"
                    >
                        <abbr title="Filters out blocks with colour noise percentage higher than given. The lower the threshold, the less 'noisy' blocks will be used for generation.">Noise:</abbr>
                    </SlottedDropdown>
                    <SlottedDropdown
                        v-model="SimpleViewStore.blockFilteringCfg.noiseMaxThreshold" :names="['30%', '50%', '70%', '80%', '100%']"
                        :default="4"
                    >
                        &nbsp; to
                    </SlottedDropdown>
                </div> -->

                <SlottedCheckbox v-model="SimpleViewStore.blockFilteringCfg.useCIELAB">
                    <abbr
                        title="Use colourspace closer to how human eyes percive colour. Results in more vibrant and accurate, but less saturacted and contrast gradients."
                    >
                        Use&nbsp;CIELAB
                    </abbr>
                </SlottedCheckbox>
            </div>
        </div>
    </section>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .blockviz-options__wrap {
        background: $dark_bg;
    }
    .blockviz-options {
        @include responsive-width;
        margin: 6px auto 0;

        &, .blockviz-options__inner {
            @include flex-center;
            flex-wrap: wrap;
            gap: 8px 16px;
        }
    }
</style>
