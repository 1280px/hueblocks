import type { Block, DisplayBlock } from './blocks'
import type { BlocksetIndex } from './blocksets'
import type { ColorRGB } from './colors'

export interface BlockVizConfig {
    hideDuplicates: boolean,
    resultsInOneRow: boolean,
    keepPrevResults: boolean,
}
export interface BlockFilterConfig {
    useCIELAB: boolean,
    // noiseThresholdMin: 0,
    // noiseThresholdMax: 4,
}

export interface ColorbarSeg {
    color: ColorRGB,
    blockRef: DisplayBlock | null,
    steps: number, // Length between CURRENT and NEXT color segments,
} // will be ignored if this is the last color segment in colorbar

export interface BlockVizRow {
    blocksetIdx: BlocksetIndex,
    textures: Block[],
}
