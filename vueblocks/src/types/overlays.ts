import type { Ref, VueElement } from 'vue'
import type { Block } from './blocks'
import type Overlay from '@/widgets/Overlay/index.vue'

export interface OverlayContent {
    content: VueElement | null,
    props: any,
}

export type HTMLOverlayElement = Ref<typeof Overlay>

export interface BlockTooltip {
    name: Block['name'],
    target: HTMLElement | null,
}
