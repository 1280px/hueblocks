<script setup>
    import {ref, defineModel, computed} from 'vue'
    import { overlayShow } from '@/overlay'
    import { hex2rgb, rgb2hex } from '@/colors'

    import Icon from '@/components/Icon.vue'
    import BlockPick from '@/views/GlobalOverlay/BlockPick.vue'

    const cbItem = defineModel()

    const currColorRgb = computed({
        get: () => cbItem.value.color,
        set: (rgb) => cbItem.value.color = rgb
    })
    const currColorHex = computed({
        get: () => rgb2hex(currColorRgb.value),
        set: (hex) => currColorRgb.value = hex2rgb(hex)
    })

    const getBlockPickColor = async () => {
        const res = await overlayShow(
            BlockPick, {'mode': 'single'}
        )

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
        <input type="color"
            v-model="currColorHex" placeholder="cbItemColor"
        >
        <button title="Pick colour from a block…"
            @click="getBlockPickColor"
        >
            <Icon name="block" />
        </button>
    </div>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .color-controls {
        display: flex;
        flex-direction: row;
        width: 80px;
    }
    .color-controls > button {
        min-width: 32px;
    }
</style>
