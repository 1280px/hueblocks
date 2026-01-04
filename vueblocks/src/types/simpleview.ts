import type { DisplayBlock } from './blocks'
import type { ColorRGB } from './colors'

export interface BlockDisplayConfig {
    hideDuplicates: boolean,
    resultsInOneRow: boolean,
    keepPrevResults: boolean,
    showColorsDebug: boolean,
}
export interface BlockFilteringConfig {
    useOkLAB: boolean,
    // noiseThresholdMin: 0.0,
    // noiseThresholdMax: 1.0,
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

export type BlockVizRow = DisplayBlock[]
