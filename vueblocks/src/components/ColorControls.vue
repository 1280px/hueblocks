<script setup>
    import {ref} from 'vue'
    import { overlayShow } from '@/overlay'

    import Icon from '@/components/Icon.vue'
    import BlockPick from '@/views/GlobalOverlay/BlockPick.vue'
</script>

<template>
    <div class="color-controls">
        <input type="color"
            v-model="cbItemColor" placeholder="cbItemColor"
        >
        <button title="Pick colour from a block…"
            @click="overlayShow(BlockPick, {'mode': 'single'})"
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
