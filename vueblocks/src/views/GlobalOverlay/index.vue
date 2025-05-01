<script setup>
    import {watch, ref} from 'vue'

    const visible = ref(false)
    const innerComponent = ref(null), innerProps = ref({})
    let res = null

    const show = (newInnerComponent, newInnerProps = {}) => {
        innerComponent.value = newInnerComponent
        innerProps.value = newInnerProps
        visible.value = true

        return new Promise((resolve) => {
            res = resolve
        })
    }

    const done = (data) => {
        visible.value = false

        res?.(data || null)
    }

    const d = ref()

    watch(visible, async (v) => {
        if (v === true) {
            // Apparently setImmediate() is not supported in Vue?
            setTimeout(() => d.value?.showModal(), 1)
        }
    })

    defineExpose({
        show, // --> overlayShow()
        visible // --> overlayIsShown()
    })
</script>

<template>
    <Transition name="overlay">
        <dialog class="overlay" v-if="visible" ref="d" @cancel.prevent>
            <component :is="innerComponent" v-bind="innerProps" @done="done" />
        </dialog>
    </Transition>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    // Unfortunately Vue doesn't know how to process ::backdrop
    // in <Transition>, so we'll have to tape some crutches...
    .overlay {
        display: flex; flex-direction: column;
        width: 100%; max-width: 100vw;
        height: 100%; max-height: 100vh;
        margin: 0; padding: 32px;
        inset: 0; box-sizing: border-box;
        overflow-y: scroll;
        background-color: $accent-dark_25; border-color: transparent;
        backdrop-filter: blur(4px);
    }

    .overlay-enter-active, .overlay-leave-active {
        opacity: 1;
        transition: opacity $TR_slow cubic-bezier(.48, .3, .15, .86);
    }
    .overlay-enter-from, .overlay-leave-to {
        opacity: 0;
    }
</style>
