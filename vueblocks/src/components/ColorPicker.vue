<script setup lang="ts">
import type { ColorHEX, ColorRGB } from '@/types/colors'
import { computed, defineModel } from 'vue'
import { hex2rgb, rgb2hex } from '@/colors'
import Icon from '@/components/Icon.vue'

const { colorpickIcon = null, colorpickText = null } = defineProps<{
    colorpickIcon?: string | null,
    colorpickText?: string | null,
}>()

const emit = defineEmits<{
    colorpick: [],
}>()

const color = defineModel<ColorRGB>()

const currColorRgb = computed<ColorRGB>({
    get: () => color.value!,
    set: (rgb: ColorRGB) => color.value! = rgb,
})
const currColorHex = computed<ColorHEX>({
    get: () => rgb2hex(currColorRgb.value),
    set: hex => currColorRgb.value = hex2rgb(hex),
})
</script>

<template>
    <div class="color-picker">
        <input
            v-model="currColorHex"
            type="color" placeholder="cbItemColor"
        >
        <button
            v-if="colorpickIcon && colorpickText"
            :title="colorpickText"
            @click="() => emit('colorpick')"
        >
            <Icon :name="colorpickIcon" />
        </button>
    </div>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .color-picker {
        flex: 1 1 0;
        display: flex; flex-direction: row;
        max-width: 80px;
    }

    .color-picker > button {
        min-width: 32px;
    }
</style>
