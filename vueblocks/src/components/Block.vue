<script setup lang="ts">
import type { DisplayBlock } from '@/types/blocks'

import { ref } from 'vue'

import { useGlobalStore } from '@/stores/GlobalStore'

const {
    blocksetIdx = -1,
    texture = 'missingNo',
    name = '',
} = defineProps<DisplayBlock>()

const GlobalStore = useGlobalStore()

// We only want to show background when image is not loaded,
// so textrues with alpha channel will show up normally:
const isLoaded = ref<boolean>(false)
</script>

<template>
    <div
        :class="{ loading: !isLoaded }" class="block"
        :style="{ width: GlobalStore.blockSize, height: GlobalStore.blockSize }"
    >
        <img
            v-show="isLoaded" :src="GlobalStore.getTexturePath(blocksetIdx, texture)" :alt="name"
            @load="isLoaded = true" @error="isLoaded = false"
        >
        <span v-show="!isLoaded">{{ name || texture || 'Error!' }}</span>
    </div>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .block {
        image-rendering: pixelated;
        overflow: clip;
        line-break: anywhere;
        text-align: left;
        transition: $TR_regular, background 0ms;

        &.loading {
            background: $accent-light_25;
        }

        & img {
            height: 100%;
        }
    }

    .block-hidden {
        width: 0 !important; height: 0 !important;
        transition: $TR_slow;
    }
</style>
