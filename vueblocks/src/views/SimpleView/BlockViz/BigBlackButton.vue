<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    isLoaded: {
        type: Boolean,
        required: true,
    },
})
</script>

<template>
    <button type="submit" :disabled="props.isLoaded">
        <slot v-if="!props.isLoaded" name="normal" />
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
