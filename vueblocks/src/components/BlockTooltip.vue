<script setup lang="ts">
import type { BlockTooltip } from '@/types/overlays'

import { computed } from 'vue'

import { Wowerlay } from 'wowerlay'
import { useGlobalStore } from '@/stores/GlobalStore'

const { tooltipData } = defineProps<{
    tooltipData: BlockTooltip,
}>()

const GlobalStore = useGlobalStore()

const blockPixelGap = computed<number>(() => Number.parseInt(GlobalStore.blockSize) / 16)
</script>

<template>
    <Wowerlay
        :target="tooltipData.target" :visible="tooltipData.target !== null"
        position="bottom-start" :gap="blockPixelGap * -15"
        class="tooltip" :style="{ 'margin-left': `${blockPixelGap}px` }"
    >
        {{ tooltipData.name }}
    </Wowerlay>
</template>

<style lang="scss" scoped>
    @use '@/assets/popovers' as *;
</style>
