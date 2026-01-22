<script setup lang="ts">
import type { DisplayBlock } from '@/types/blocks'

import { computed, ref } from 'vue'

import { getCssRgb, lab2rgb } from '@/colors'
import { useGlobalStore } from '@/stores/GlobalStore'

const {
    blocksetIdx = -1,
    texture = 'missingNo',
    name = '',
    debugData,
} = defineProps<DisplayBlock>()

const GlobalStore = useGlobalStore()

// We only want to show background when image is not loaded,
// so textrues with alpha channel will show up normally:
const isLoaded = ref<boolean>(false)

const debugTargetCssColor = computed(() => {
    return debugData?.rgbTarget
        ? getCssRgb(debugData.rgbTarget)
        : debugData?.labTarget
            ? getCssRgb(lab2rgb(debugData.labTarget))
            : undefined
})

const debugRealCssColor = computed(() => {
    return debugData?.rgbReal
        ? getCssRgb(debugData.rgbReal)
        : debugData?.labReal
            ? getCssRgb(lab2rgb(debugData.labReal))
            : undefined
})

// Formulas are exactly the same as in SimpleViewStore
function debugGetColorAccuracy() {
    if (debugData?.rgbTarget && debugData?.rgbReal) {
        return ((
            255 - Math.abs(debugData.rgbTarget[0] - debugData.rgbReal[0])
            + 255 - Math.abs(debugData.rgbTarget[1] - debugData.rgbReal[1])
            + 255 - Math.abs(debugData.rgbTarget[2] - debugData.rgbReal[2])
        ) / (255 * 3) * 100).toFixed(2)
    }
    // if (debugData?.labTarget && debugData?.labReal) {
    //     const de = deltaE(debugData?.labTarget, debugData?.labReal)
    //     const deMax = 80 // Average from 30 observed WORST EVER deltas (super bruh)
    //     // const deMax = 17 // Based on WORST EVER OBSERVED delta (super super bruh)
    //     return (100 * (1 - de / deMax)).toFixed(2)
    // }
    if (debugData?.labTarget && debugData?.labReal) {
        return ((1 - (
            (debugData.labTarget[0] - debugData.labReal[0]) ** 2
            + (debugData.labTarget[1] - debugData.labReal[1]) ** 2
            + (debugData.labTarget[2] - debugData.labReal[2]) ** 2
        ) ** (1 / 2)) * 100).toFixed(2)
    }
    return 0
}
</script>

<template>
    <div
        :class="{ loading: !isLoaded }" class="block"
        :style="{
            width: GlobalStore.blockSize,
            height: debugData
                ? `${Number.parseInt(GlobalStore.blockSize) * 2}px`
                : GlobalStore.blockSize,
        }"
    >
        <img
            v-show="isLoaded" :src="GlobalStore.getTexturePath(blocksetIdx, texture)" :alt="name"
            @load="isLoaded = true" @error="isLoaded = false"
        >
        <span v-show="!isLoaded">{{ name || texture || 'Error!' }}</span>

        <div
            v-if="debugData" :class="{ loading: !isLoaded }" class="debug-color"
            :style="{
                background:
                    `linear-gradient(90deg, ${debugTargetCssColor} 50%, ${debugRealCssColor} 50%)`,
                fontSize: `${Number.parseInt(GlobalStore.blockSize) / 3}px`,
            }"
        >
            {{ debugGetColorAccuracy() }}
        </div>
    </div>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .block {
        image-rendering: pixelated;
        overflow: clip;
        text-align: left; line-break: anywhere;
        transition: $TR_regular, background 0ms;

        &.loading {
            background: $accent-light_25;
        }

        & img {
            width: 100%;
        }
    }

    .block-hidden {
        width: 0 !important; height: 0 !important;
        transition: $TR_slow;
    }

    .debug-color {
        display: flex;
        justify-content: center; align-items: center;
        height: 50%;
        margin-top: -3px;
        text-shadow: $SH_subtle;
    }
</style>
