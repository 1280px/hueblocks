import type { Component, Ref } from 'vue'
import type { Block } from './blocks'
import type Overlay from '@/widgets/Overlay.vue'

export type OverlayContent = [
    Component | null,
    any, // TODO: derive the actual type for props
]

export type HTMLOverlayElement = Ref<typeof Overlay>

export interface BlockTooltip {
    name: Block['name'],
    target: HTMLElement | null,
}
