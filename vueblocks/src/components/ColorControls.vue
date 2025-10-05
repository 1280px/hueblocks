<script setup lang="ts">
import { computed, defineModel } from 'vue'

import { hex2rgb, rgb2hex } from '@/colors'
import Icon from '@/components/Icon.vue'

const { blockpickFun } = defineProps<{
    blockpickFun: () => any,
}>()

const cbItem = defineModel()

const currColorRgb = computed({
    get: () => cbItem.value.color,
    set: rgb => cbItem.value.color = rgb,
})
const currColorHex = computed({
    get: () => rgb2hex(currColorRgb.value),
    set: hex => currColorRgb.value = hex2rgb(hex),
})

async function applyBlockPickColor(getBlockPickColor) {
    const res = await getBlockPickColor()

    if (res) {
        currColorRgb.value.forEach((c, i) => {
            currColorRgb.value[i] = res.color[i]
        })
        if (res.blockRef) {
            cbItem.value.blockRef = res.blockRef
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
            v-if="blockpickFun"
            title="Pick colour from a block…"
            @click="async () => await applyBlockPickColor(blockpickFun)"
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
