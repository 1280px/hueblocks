<script setup>
import { ref, watch } from 'vue'

const visible = ref(false)
const cancellable = ref(true)
const innerComponent = ref(null); const innerProps = ref({})
let res = null

function show(newInnerComponent, newInnerProps = {}, newCancellable = true) {
    innerComponent.value = newInnerComponent
    innerProps.value = newInnerProps
    cancellable.value = newCancellable
    visible.value = true

    return new Promise((resolve) => {
        res = resolve
    })
}

const dialogRef = ref()

function done(data) {
    visible.value = false

    // Even though dialog is just a nested element, we still
    // have to close it to unfreeze background interactions:
    setTimeout(() => dialogRef.value?.close(), 750)

    res?.(data || null)
}

watch(visible, async (v) => {
    if (v === true) {
        setTimeout(() => dialogRef.value?.show(), 1)
    }
})

defineExpose({
    show, // --> overlayShow()
    visible, // --> overlayIsShown()
})
</script>

<template>
    <Transition name="overlay">
        <dialog
            v-show="visible" ref="dialogRef" class="overlay"
            @cancel="cancellable ? done() : $event.preventDefault()"
        >
            <component :is="innerComponent" v-bind="innerProps" @done="done" />
        </dialog>
    </Transition>
</template>

<style lang="scss" scoped>
    @use 'sass:color';
    @use '@/assets/variables' as *;

    // Unfortunately Vue doesn't know how to process ::backdrop
    // in <Transition>, so we'll have to tape some crutches...
    .overlay {
        display: flex; flex-direction: column;
        width: 100%; max-width: 100vw; height: 100%; max-height: 100vh;
        margin: 0; padding: 32px;
        inset: 0; box-sizing: border-box;
        overflow-y: scroll;
        background-color: color.mix($dark_80, $accent-dark); border-color: $trans;
        z-index: 99;

        @media (any-pointer: fine) {
            background-color: $accent-dark_25;
            backdrop-filter: blur(4px);
        }
    }
    .overlay::backdrop {
        background: none !important;
    }

    .overlay-enter-active, .overlay-leave-active {
        opacity: 1;
        transition: opacity $TR_slow cubic-bezier(.48, .3, .15, .86);
    }
    .overlay-enter-from, .overlay-leave-to {
        opacity: 0;
    }
</style>
