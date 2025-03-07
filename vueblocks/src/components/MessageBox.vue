<script setup>
    import {ref, defineProps, onMounted} from 'vue'

    const props = defineProps({
        duration: {
            type: Number,
            required: true
        }
    })

    const showMsgBox = ref(true)

    onMounted(() => {
        if (+props.duration > 0) {
            setTimeout(
                () => { showMsgBox.value = false },
                (+props.duration) * 1000
            )
        }
    })
</script>

<template>
    <Transition name="msgbox">
        <blockquote v-if="showMsgBox">
            <slot></slot>
        </blockquote>
    </Transition>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    blockquote {
        display: block;
        margin: auto; padding: 8px;
        border: 2px solid moccasin; border-radius: $TR_regular;
    }

    .msgbox-enter-active, .msgbox-leave-active {
        opacity: 1;
        transition: opacity $TR_message cubic-bezier(.22, .61, .36, 1);
    }

    .msgbox-enter-from, .msgbox-leave-to {
        opacity: 0;
    }
</style>
