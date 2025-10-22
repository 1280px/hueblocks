<script setup lang="ts">
import type { ColorRGB } from '@/types/colors'

import { defineProps } from 'vue'

import { getCssRgb } from '@/colors'
import SlottedButton from '@/components/SlottedButton.vue'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const { value, bg } = defineProps<{
    value: number,
    bg: [ColorRGB, ColorRGB],
}>()

const SimpleViewStore = useSimpleViewStore()
</script>

<template>
    <section
        class="colorbar__len-segment"
        :style="{
            flex: value,
            background: (
                `linear-gradient(
                ${SimpleViewStore.blockFilteringCfg.useCIELAB ? 'in lab' : ''} 90deg,
                ${getCssRgb(bg[0])}, ${getCssRgb(bg[1])})`
            ),
        }"
    >
        <SlottedButton class="trans">
            <span class="colorbar__len-segment__count">
                {{ value || 'missingNo' }}
            </span>
            <span class="colorbar__len-segment__appendix">
                blocks
            </span>
        </SlottedButton>
    </section>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .colorbar__len-segment {
        @include flex-center;
        flex: 1;
        container-type: inline-size;

        @container (max-width: 75px) {
            .colorbar__len-segment__appendix {
                display: none;
            }
        }

        & button.trans {
            flex: 1;
            margin: 0 4px;
            text-shadow: $SH_subtle;
        }
    }
</style>
