<script setup lang="ts">
import type { OverlayContent } from '@/types/overlays'

import { ref, watch } from 'vue'

const visible = ref<boolean>(false)
const cancellable = ref<boolean>(true)
let res = null

const content = ref<OverlayContent>([null, { }])

function show(newContent: OverlayContent, newCancellable = true) {
    content.value = newContent
    cancellable.value = newCancellable
    visible.value = true

    // Force microtask
    return new Promise(
        (resolve) => { res = resolve },
    )
}

const dialogRef = ref()

function done(data?) {
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
    show, // --> overlayShow() in overlay.ts
    visible, // --> overlayIsShown() in overlay.ts
})
</script>

<template>
    <Transition name="overlay">
        <dialog
            v-show="visible" ref="dialogRef" class="overlay"
            @cancel="cancellable ? done() : $event.preventDefault()"
        >
            <component :is="content[0]" v-bind="content[1]" @done="done" />

            <!-- <button @click="done">
                An example how to close Overlay component
            </button> -->
        </dialog>
    </Transition>
</template>

<style lang="scss">
    @use 'sass:color';
    @use '@/assets/variables' as *;

    // Unfortunately Vue doesn't know how to process ::backdrop
    // in <Transition>, so we'll have to tape some crutches...
    dialog.overlay {
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
    dialog.overlay::backdrop {
        background: none !important;
    }

    .overlay-enter-active, .overlay-leave-active {
        opacity: 1;
        transition: opacity $TR_slow cubic-bezier(.48, .3, .15, .86);
    }
    .overlay-enter-from, .overlay-leave-to {
        opacity: 0;
    }

    // Expected inner sections are <header> for title,
    // <main> for body, and <aside> for controls:
    dialog.overlay > header {
        @include flex-center;
        margin-bottom: 32px;

        @media (max-width: 800px) {
            margin-top: 64px;
        }
    }
    dialog.overlay > main {
        @include responsive-width;
        flex: 1;
        display: flex; flex-direction: column;
        margin: auto;
    }
    dialog.overlay > aside {
        // TODO: simplify this rule
        position: absolute;
        top: 32px; right: 32px;
        display: flex; flex-direction: row-reverse;
        justify-content: center; align-items: flex-end;
        margin: 0; gap: 4px;

        @media (min-width: 800px) {
            flex-direction: column;
        }
    }
</style>
