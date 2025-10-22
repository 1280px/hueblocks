<script setup lang="ts">
import type { Palette } from '@/types/palettes'

import { ref } from 'vue'

import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'
import BlockDisplayOptions from './BlockViz/BlockDisplayOptions.vue'
import BlockFilteringOptions from './BlockViz/BlockFilteringOptions.vue'
import BlockVizControls from './BlockViz/BlockVizControls.vue'
import BlockVizData from './BlockViz/BlockVizData.vue'
import Colorbar from './Colorbar/index.vue'

const GlobalStore = useGlobalStore()
const SimpleViewStore = useSimpleViewStore()

// This is a rather fragile solution, however, as it's impossible to
// remove rows other than delete all of them, it is toletable I guess?
const hiddenBlockIds = ref<Set<string>>(
    new Set(), // Format: 'row_block'
)

function bbbAction() {
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
        hiddenBlockIds.value.clear()
    }
}
</script>

<template>
    <main>
        <section class="colorbar__wrap">
            <Colorbar />
        </section>

        <BlockDisplayOptions />
    </main>

    <footer>
        <section class="blockviz__wrap">
            <BlockVizControls @bbb-click="bbbAction()" />

            <BlockFilteringOptions />

            <BlockVizData
                :hidden-block-ids="hiddenBlockIds"
                @hide-block="(pos) => hiddenBlockIds.add(pos)"
            />
        </section>
    </footer>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    main {
        @include responsive-width;
        display: flex; flex-direction: column;
        margin: 0 auto;
    }
    footer {
        flex: 1;
        display: flex; flex-direction: column;
    }

    .colorbar__wrap {
        @include flex-center;
        align-items: baseline;
        gap: 4px;
    }

    .blockviz__wrap {
        flex: 1;
        display: flex; flex-direction: column;
    }
</style>
