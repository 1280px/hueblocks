let overlay = null // <-- Same data accessible from everywhere!

function overlayBind(ref) {
    overlay = ref
}

function overlayShow(newInnerComponent, newInnerProps) {
    return overlay.show(newInnerComponent, newInnerProps)
}


export {
    overlayBind, overlayShow
}
