<script setup lang="ts">
const { variant = 'normal', isShown = true } = defineProps<{
    variant?: 'normal' | 'error' | 'success',
    isShown?: boolean,
}>()
</script>

<template>
    <Transition name="msgbox">
        <blockquote v-if="isShown" :class="variant">
            <slot />
        </blockquote>
    </Transition>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    blockquote {
        display: flex; flex-direction: column;
        margin: auto; padding: 12px; gap: 8px;
        animation: $TR_slow overlay-fade;
        line-height: 1.3;

        &.normal {
            background-color: $accent-light_25;
            border: 2px solid $white_50;
        }
        &.error {
            background-color: $error_30;
            border: 2px solid $error;
        }
        &.success {
            background-color: $success_30;
            border: 2px solid $success;
        }
    }

    .msgbox-enter-active, .msgbox-leave-active {
        opacity: 1;
        transition: opacity $TR_fancy cubic-bezier(.02, .04, .92, .98);
    }
    .msgbox-enter-from, .msgbox-leave-to {
        opacity: 0;
    }
</style>
