import { computed, ref } from 'vue'

// Same ref data accessible from everywhere!
let overlay = ref<HTMLDialogElement | null>(null)

function overlayBind(ref) {
    overlay.value = ref
}

function overlayShow(newInnerComponent, newInnerProps) {
    return overlay.value?.show(newInnerComponent, newInnerProps)
}

const overlayIsShown = computed(() => {
    return overlay.value?.visible || false
})

export {
    overlayBind,
    overlayIsShown,
    overlayShow,
}
