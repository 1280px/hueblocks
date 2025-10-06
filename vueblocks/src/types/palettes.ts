import type { Block } from './blocks'

export interface Palette {
    name: string,
    textures: Block['texture'][],
    count: number,
}

export type PaletteIndex = number
