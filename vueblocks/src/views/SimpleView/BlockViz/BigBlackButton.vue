<script setup lang="ts">
import { defineProps } from 'vue'

const { isLoaded = true } = defineProps<{
    isLoaded?: boolean,
}>()
</script>

<template>
    <button type="submit" :disabled="isLoaded">
        <slot v-if="!isLoaded" name="normal" />
        <slot v-else name="disabled" />
    </button>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    button {
        height: 60px;
        padding: 0 20px;
        border-radius: $BR_big;
    }
</style>
