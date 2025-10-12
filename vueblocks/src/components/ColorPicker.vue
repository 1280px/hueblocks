<script setup lang="ts">
import type { ColorHEX, ColorRGB } from '@/types/colors'
import type { ColorbarSeg } from '@/types/simpleview'
import { computed, defineModel } from 'vue'
import { hex2rgb, rgb2hex } from '@/colors'
import Icon from '@/components/Icon.vue'

const { blockpick } = defineProps<{
    blockpick: () => ColorbarSeg,
}>()

const cbItem = defineModel<ColorbarSeg>()

const currColorRgb = computed<ColorRGB>({
    get: () => cbItem.value!.color,
    set: (rgb: ColorRGB) => cbItem.value!.color = rgb,
})
const currColorHex = computed<ColorHEX>({
    get: () => rgb2hex(currColorRgb.value),
    set: hex => currColorRgb.value = hex2rgb(hex),
})

async function applyBlockPickColor(
    getBlockPickColor: typeof blockpick,
) {
    const res: ColorbarSeg = await getBlockPickColor()

    if (res) {
        currColorRgb.value.forEach((c, i) => {
            currColorRgb.value[i] = res.color[i]
        })
        if (res.blockRef) {
            cbItem.value!.blockRef = res.blockRef
        }
    }
}
</script>

<template>
    <div class="color-controls">
        <input
            v-model="currColorHex"
            type="color" placeholder="cbItemColor"
        >
        <button
            v-if="blockpick"
            title="Pick colour from a block…"
            @click="async () => await applyBlockPickColor(blockpick)"
        >
            <Icon name="block" />
        </button>
    </div>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .color-controls {
        display: flex; flex-direction: row;
        width: 80px;
    }
    .color-controls > button {
        min-width: 32px;
    }
</style>
