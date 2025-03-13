<script setup>
    import {ref, computed, defineProps} from 'vue'
    import { useGlobalStore } from '@/stores/GlobalStore'
    
    const GlobalStore = useGlobalStore()
    const {texture, name} = defineProps({
        texture: {
            type: String,
            required: true,
            default: 'missingNo'
        },
        name: {
            type: String,
            required: false
        }
    })
</script>

<template>
    <img class="block" :src="GlobalStore.getTexturePath(texture)" :alt="name"
        :style="{'width': GlobalStore.blockSize, 'height': GlobalStore.blockSize}"
    >
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .block {
        width: 64px; height: 64px;
        background-color: $accent-light_25;
        image-rendering: pixelated;
    }
</style>
