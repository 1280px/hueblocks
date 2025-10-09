import type { BlocksetIndex } from './blocksets'
import type { ColorLAB, ColorRGB } from './colors'

export const blockFacing = ['all', 'sides', 'top', 'bottom', 'north', 'west', 'south', 'east'] as const
// Note that 'all' and 'sides' are meta-faces, meaning OptiFine CTM
// provides them as aliases for all sides and all sides except top and bottom
// respectively, and for that reason j2bs blocksets don't use them at all.

export type BlockFacing = typeof blockFacing[number]

export interface Block {
    name: string,
    texture: string,
    sides: BlockFacing[],
    rgb: ColorRGB,
    lab: ColorLAB,
}

// Small clarification -- "blockdata" is simply an array of Block objects.
// It's not a separate type or anything like this! Not to be confused
// with "blockset", which is blockdata plus metadata like name and amount.

// Used by Block component, blockset index is stored so it won't
// change every time current blockset is changed as well:
export interface DisplayBlock extends Pick<Block, 'name' | 'texture'> {
    blocksetIdx: BlocksetIndex,
}

export interface BlockTooltip {
    name: Block['name'],
    target: HTMLElement | null,
}
