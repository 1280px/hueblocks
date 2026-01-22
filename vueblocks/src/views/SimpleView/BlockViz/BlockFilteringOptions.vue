<script setup lang="ts">
import type { Blockset } from '@/types/blocksets'
import type { Palette } from '@/types/palettes'

import { computed, watch } from 'vue'

import SlottedDropdown from '@/components/SlottedDropdown.vue'
import { overlayShow } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import BlockPickPalette from '../BlockPick/BlockPickPalette.vue'

const GlobalStore = useGlobalStore()

const blocksetsDataNames = computed((): Blockset['name'][] => {
    if (!GlobalStore.blocksetsData) { return ['Loading…'] }

    return GlobalStore.blocksetsData.map(bsd => bsd !== '<hr>' ? bsd.name : '<hr>')
})

const blockdataPaletteNames = computed((): Palette['name'][] => {
    if (!GlobalStore.currBlocksetPalettes) { return ['Loading…'] }

    return GlobalStore.currBlocksetPalettes.map(pal => pal !== '<hr>' ? pal.name : '<hr>')
})

// We assume the 'Edit palette' option is always the latest -- brittle!
async function processPaletteChange(newIdx: number, oldIdx: number) {
    if (newIdx === (GlobalStore.currBlocksetPalettes.length - 1)) {
        // console.log(GlobalStore.currPaletteIdx, newIdx, oldIdx)

        const res = await overlayShow(
            [BlockPickPalette, { originalPaletteIdx: oldIdx }],
        )

        if (res !== null) {
            GlobalStore.customPaletteTextures = [...res]
            GlobalStore.toggleCustomPalette(true)
            GlobalStore.currPaletteIdx = GlobalStore.currBlocksetPalettes.length - 2
        }
        else {
            GlobalStore.currPaletteIdx = oldIdx
        }
    }
    else {
        GlobalStore.currPaletteIdx = newIdx
    }
}

watch(
    () => GlobalStore.currPaletteIdx,
    (newIdx, oldIdx) => processPaletteChange(newIdx, oldIdx),
)
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
                >
                    Palette:
                </SlottedDropdown>

                <!-- <div style="display: flex; justify-content: center; flex-wrap: wrap;">
                    <SlottedDropdown
                        v-model="SimpleViewStore.blockFilteringCfg.noiseMinThreshold"
                        :names="['No threshold', 'Low noise', 'Low & Medium noise', 'Medium & High noise']"
                        :default="0"
                    >
                        <abbr title="Filters out blocks with colour texture variability percentage higher than given. The lower the threshold, the less 'noisy' (texture-prominent) blocks will be used for generation.">Noise:</abbr>
                    </SlottedDropdown>
                </div> -->
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
