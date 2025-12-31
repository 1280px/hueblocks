<script setup lang="ts">
import { onMounted, ref } from 'vue'

const { duration } = defineProps<{
    duration: number,
}>()

const showMsgbox = ref<boolean>(true)

onMounted(() => {
    setTimeout(
        () => { showMsgbox.value = false },
        (Math.max(+(duration || 0), 1)) * 1000,
    )
})
</script>

<template>
    <Transition name="msgbox">
        <blockquote v-if="showMsgbox">
            <slot />
        </blockquote>
    </Transition>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    blockquote {
        display: block;
        margin: auto; padding: 8px;
        border: 2px solid moccasin; border-radius: $TR_regular;
        animation: $TR_slow overlay-fade;
    }

    .msgbox-enter-active, .msgbox-leave-active {
        opacity: 1;
        transition: opacity $TR_fancy cubic-bezier(.02, .04, .92, .98);
    }
    .msgbox-enter-from, .msgbox-leave-to {
        opacity: 0;
    }
</style>
