<script setup lang="ts">
import type { BlockTooltip as BlockTooltipT } from '@/types/overlays'

import { ref } from 'vue'

import Block from '@/components/Block.vue'
import BlockTooltip from '@/components/BlockTooltip.vue'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const { hiddenBlockIds } = defineProps<{
    hiddenBlockIds: Set<string>,
}>()

const emit = defineEmits<{
    hideBlock: [pos: string],
}>()

const SimpleViewStore = useSimpleViewStore()

const tooltipData = ref<BlockTooltipT>({ target: null, name: 'missingNo' })

function copyBlockTextureName(name: string) {
    navigator.clipboard.writeText(name.split('.png')[0])
}
</script>

<template>
    <section class="blockviz-data__wrap">
        <div
            class="blockviz-data"
            :class="{ 'one-row': SimpleViewStore.blockDisplayCfg.resultsInOneRow }"
        >
            <div v-for="(row, i) in SimpleViewStore.blockVizData" :key="i">
                <Block
                    v-for="(db, j) in row" :key="j"
                    :name="db.name" :blockset-idx="db.blocksetIdx" :texture="db.texture"
                    :class="{ 'block-hidden': hiddenBlockIds.has(`${i}_${j}`) }"
                    :debug-data="SimpleViewStore.blockDisplayCfg.showColorsDebug ? db.debugData : undefined"
                    @click="(e: Event) => {
                        emit('hideBlock', `${i}_${j}`);
                        // Force update class bc Vue won't detect it until any next event
                        (e.currentTarget as HTMLElement).classList.add('block-hidden')
                    }"
                    @contextmenu.prevent="() => copyBlockTextureName(db.texture)"
                    @mouseenter.prevent="(e: MouseEvent) => tooltipData = {
                        target: e.target as HTMLElement, name: db.name,
                    }"
                    @mouseleave.prevent="() => tooltipData.target = null"
                />
            </div>
        </div>
    </section>

    <BlockTooltip :tooltip-data="tooltipData" />
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .blockviz-controls__wrap {
        background: linear-gradient(transparent 32px, $dark_em 32px, $dark_bg);
    }
    .blockviz-controls {
        @include flex-center;
        height: 64px;
        gap: 2vw; // 4vw;
    }
    .blockviz-controls__blob {
        @include flex-center;
        padding: 4px; gap: 4px;
        background: linear-gradient($dark_em 50.5%, $trans 50.5%);
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

            // That's probably a dumb solution, but it does, indeed, work
            & *:last-child {
                padding-right: 16px;
            }
        }
    }

    .side-picker__wrap {
        width: 84px; height: 40px;
    }
</style>
