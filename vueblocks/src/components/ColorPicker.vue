<script setup lang="ts">
import type { ColorHEX, ColorRGB } from '@/types/colors'
import type { ColorbarSeg } from '@/types/simpleview'
import { computed, defineModel } from 'vue'
import { hex2rgb, rgb2hex } from '@/colors'
import Icon from '@/components/Icon.vue'

const { colorpick } = defineProps<{
    colorpick: () => ColorbarSeg,
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

async function applyPickedColor(
    getPickedColor: typeof colorpick,
) {
    const res: ColorbarSeg = await getPickedColor()

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
    <div class="color-picker">
        <input
            v-model="currColorHex"
            type="color" placeholder="cbItemColor"
        >
        <button
            v-if="colorpick"
            title="Pick colour from a block…"
            @click="async () => await applyPickedColor(colorpick)"
        >
            <Icon name="block" />
        </button>
    </div>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .color-picker {
        display: flex; flex-direction: row;
        width: 80px;
    }

    .color-picker > button {
        min-width: 32px;
    }
</style>
