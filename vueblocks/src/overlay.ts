import type { HTMLOverlayElement, OverlayContent } from './types/overlays'

import { computed, ref } from 'vue'

const overlay = ref<HTMLOverlayElement | null>(null)

function overlayBind(ref: HTMLOverlayElement) {
    overlay.value = ref
}

function overlayShow(newContent: OverlayContent) {
    return overlay.value?.show(newContent)
}

const overlayIsShown = computed<any>(() => {
    return overlay.value?.visible || false
})

export {
    overlayBind,
    overlayIsShown,
    overlayShow,
}
