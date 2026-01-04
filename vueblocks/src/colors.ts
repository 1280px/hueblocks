import type { ColorHEX, ColorLAB, ColorRGB } from './types/colors'

// Linear RGB (it used below) <--> Serial RGB (used by JS)

function addSrgbGamma(c_lrgb: number): number {
    // return c_lrgb ** (1 / 2)
    return (c_lrgb >= 0.0031308) ? (1.055 * (c_lrgb ** (1 / 2.4))) - 0.055 : (c_lrgb * 12.92)
}

function removeSrgbGamma(c_srgb: number): number {
    // return c_srgb ** 2
    return (c_srgb >= 0.04045) ? ((c_srgb + 0.055) / 1.055) ** 2.4 : (c_srgb / 12.92)
}

// Linear RGB <--> OkLAB (not CIELAB!) converters, based on this blogpost:
// https://bottosson.github.io/posts/oklab/#converting-from-linear-srgb-to-oklab

function rgb2lab(srgb: ColorRGB): ColorLAB {
    // SRGB -> LRGB
    const lrgb = srgb.map(color => removeSrgbGamma(color / 255.0))

    // LRGB -> CIEXYZ -> LMS
    // https://en.wikipedia.org/wiki/Oklab_color_space#Conversion_from_sRGB
    const l = 0.4122214708 * lrgb[0] + 0.5363325363 * lrgb[1] + 0.0514459929 * lrgb[2]
    const m = 0.2119034982 * lrgb[0] + 0.6806995451 * lrgb[1] + 0.1073969566 * lrgb[2]
    const s = 0.0883024619 * lrgb[0] + 0.2817188376 * lrgb[1] + 0.6299787005 * lrgb[2]

    // LMS -> LMS'
    const l_ = l ** (1 / 3)
    const m_ = m ** (1 / 3)
    const s_ = s ** (1 / 3)

    // LMS' -> Lab
    // https://en.wikipedia.org/wiki/Oklab_color_space#Conversion_from_CIE_XYZ
    return [
        +0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        +1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        +0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    ]
}

function lab2rgb(lab: ColorLAB): ColorRGB {
    // Lab -> LMS'
    const l_ = +lab[0] + 0.3963377774 * +lab[1] + 0.2158037573 * +lab[2]
    const m_ = +lab[0] - 0.1055613458 * +lab[1] - 0.0638541728 * +lab[2]
    const s_ = +lab[0] - 0.0894841775 * +lab[1] - 1.2914855480 * +lab[2]

    // LMS' -> LMS
    const l = l_ ** 3
    const m = m_ ** 3
    const s = s_ ** 3

    // LMS -> CIEXYZ -> LRGB (inverse matrix)
    const lrgb: ColorRGB = [
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    ]

    // LRGB -> SRGB
    return lrgb.map(color => addSrgbGamma(color) * 255.0) as ColorRGB
}

// Compact HEX <--> RGB converters I found on S.O. years ago
// Source: has drown in the flow of its rapid century

function hex2rgb(hex: ColorHEX): ColorRGB {
    return [+`0x${hex[1]}${hex[2]}`, +`0x${hex[3]}${hex[4]}`, +`0x${hex[5]}${hex[6]}`]
}
function rgb2hex(rgb: ColorRGB): ColorHEX {
    return `#${((1 << 24) + (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]).toString(16).slice(1)}`
}

// Other useful stuff

function getRandomRbg(lightK: number): ColorRGB {
    return [
        Math.floor((
            (lightK + Math.random()) * 120
            + (Math.random() * 2) * 40
            + (Math.random() * 56)
        ) ** lightK % 255),
        Math.floor((
            (lightK + Math.random()) * 100
            + (Math.random() * 4) * 30
            + (Math.random() * 16)
        ) ** lightK % 255),
        Math.floor((
            (lightK + Math.random()) * 80
            + (Math.random() * 2) * 40
            + (Math.random() * 96)
        ) ** lightK % 255),
    ]
}

function getCssRgb(rgb: ColorRGB): string {
    return `rgb(${Math.floor(rgb[0] || 0)}, ${Math.floor(rgb[1] || 0)}, ${Math.floor(rgb[2] || 0)})`
}

export {
    getCssRgb,
    getRandomRbg,
    hex2rgb,
    lab2rgb,
    rgb2hex,
    rgb2lab,
}
