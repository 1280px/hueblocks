import type { Block, DisplayBlock } from './blocks'
import type { BlocksetIndex } from './blocksets'
import type { ColorRGB } from './colors'

export interface BlockDisplayConfig {
    hideDuplicates: boolean,
    resultsInOneRow: boolean,
    keepPrevResults: boolean,
}
export interface BlockFilteringConfig {
    useCIELAB: boolean,
    // noiseThresholdMin: 0,
    // noiseThresholdMax: 4,
}

export interface ColorbarSeg {
    color: ColorRGB,
    blockRef: DisplayBlock | null,
    steps: number, // Length between CURRENT and NEXT color segments,
} // will be ignored if this is the last color segment in colorbar

export type ColorbarPopoverData = null
    | { mode: 'color', cbIdx: number }
    | { mode: 'steps', cbIdx: number }
    | { mode: 'addItem', side: 'left' | 'right' }

export interface BlockVizRow {
    blocksetIdx: BlocksetIndex,
    textures: Block[],
}
