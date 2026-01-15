<script setup lang="ts">
import type { ColorHEX, ColorRGB } from '@/types/colors'
import { computed } from 'vue'
import { hex2rgb, rgb2hex } from '@/colors'
import Icon from '@/components/Icon.vue'
import SlottedButton from './SlottedButton.vue'

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
        <SlottedButton
            v-if="colorpickIcon && colorpickText"
            variant="black"
            :title="colorpickText"
            @click="() => emit('colorpick')"
        >
            <Icon :name="colorpickIcon" />
        </SlottedButton>
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
        border-left-width: 0; border-radius: 0 $BR_big $BR_big 0;
    }

    .color-picker > input {
        appearance: none;
        height: 100%; // fix for Safari (otherwise doesn't show picker at all)
        margin: 0; padding: 0;
        background-color: $accent-dark_80;
        border: 2px solid $accent-dark_25;
        border-radius: $BR_big 0 0 $BR_big;
        cursor: pointer;
        transition: $TR_regular;

        &:not(:disabled) {
            &:hover {
                border-color: $accent-dark_80;
            }
            &:focus-visible, &:hover:active {
                background-color: $accent_bg;
                border: 4px solid $accent-dark_60;
                outline: none;
                transition: $TR_fast;
            }
        }

        &:last-child {
            border-radius: $BR_big; // In case colorpick was not provided
        }
    }
</style>
