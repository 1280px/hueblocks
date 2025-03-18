<script setup>
    import {ref, defineProps} from 'vue'

    const props = defineProps({
        isReady: {
            type: Boolean,
            required: true
        }
    })
</script>

<template>
    <button type="submit" :isReady="props.isReady">
        <slot v-if="!props.isReady" name="normal"></slot>
        <slot v-else name="disabled"></slot>
    </button>
</template>

<style lang="scss" scoped>
    button {
        height: 64px;
    }
</style>
