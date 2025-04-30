let overlay = null // <-- Accessible from every component!

function overlayBind(ref) {
    console.log(ref)
    overlay = ref
}

function overlayShow(newInnerComponent, newInnerProps) {
    console.log(overlay)
    return overlay.show(newInnerComponent, newInnerProps)
}


export {
    overlayBind, overlayShow
}
