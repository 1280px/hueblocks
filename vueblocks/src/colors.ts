import type { ColorHEX, ColorLAB, ColorRGB } from './types/colors'

// RGB <--> LAB color converters and LHC distance calculator
// Source: https://github.com/antimatter15/rgb-lab/

function lab2rgb(lab: ColorLAB): ColorRGB {
    let y = (lab[0] + 16) / 116
    let x = lab[1] / 500 + y
    let z = y - lab[2] / 200
    let r; let g; let b

    x = 0.96422 * ((x * x * x > 0.008856) ? x * x * x : (x - 16 / 116) / 7.787)
    y = 1.00000 * ((y * y * y > 0.008856) ? y * y * y : (y - 16 / 116) / 7.787)
    z = 0.82521 * ((z * z * z > 0.008856) ? z * z * z : (z - 16 / 116) / 7.787)

    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    r = (r > 0.0031308) ? (1.055 * r ** (1 / 2.4) - 0.055) : 12.92 * r
    g = (g > 0.0031308) ? (1.055 * g ** (1 / 2.4) - 0.055) : 12.92 * g
    b = (b > 0.0031308) ? (1.055 * b ** (1 / 2.4) - 0.055) : 12.92 * b

    return [Math.max(0, Math.min(1, r)) * 255, Math.max(0, Math.min(1, g)) * 255, Math.max(0, Math.min(1, b)) * 255]
}

function rgb2lab(rgb: ColorRGB): ColorLAB {
    let r = rgb[0] / 255
    let g = rgb[1] / 255
    let b = rgb[2] / 255
    let x; let y; let z

    r = (r > 0.04045) ? ((r + 0.055) / 1.055) ** 2.4 : r / 12.92
    g = (g > 0.04045) ? ((g + 0.055) / 1.055) ** 2.4 : g / 12.92
    b = (b > 0.04045) ? ((b + 0.055) / 1.055) ** 2.4 : b / 12.92

    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.96422
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 0.82521

    x = (x > 0.008856) ? x ** (1 / 3) : (7.787 * x) + 16 / 116
    y = (y > 0.008856) ? y ** (1 / 3) : (7.787 * y) + 16 / 116
    z = (z > 0.008856) ? z ** (1 / 3) : (7.787 * z) + 16 / 116

    return [(116 * y) - 16, 500 * (x - y), 200 * (y - z)]
}

function deltaE(labA: ColorLAB, labB: ColorLAB): number {
    const deltaL = labA[0] - labB[0]
    const deltaA = labA[1] - labB[1]
    const deltaB = labA[2] - labB[2]

    const c1 = Math.sqrt(labA[1] * labA[1] + labA[2] * labA[2])
    const c2 = Math.sqrt(labB[1] * labB[1] + labB[2] * labB[2])

    const deltaC = c1 - c2
    let deltaH = deltaA * deltaA + deltaB * deltaB - deltaC * deltaC
    deltaH = deltaH < 0 ? 0 : Math.sqrt(deltaH)

    const deltaLKlsl = deltaL / (1.0)
    const deltaCkcsc = deltaC / (1.0 + 0.045 * c1)
    const deltaHkhsh = deltaH / (1.0 + 0.015 * c1)

    const i = deltaLKlsl * deltaLKlsl + deltaCkcsc * deltaCkcsc + deltaHkhsh * deltaHkhsh

    return i < 0 ? 0 : Math.sqrt(i)
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
    return `rgb(${rgb[0] || 0}, ${rgb[1] || 0}, ${rgb[2] || 0})`
}

export {
    deltaE,
    getCssRgb,
    getRandomRbg,
    hex2rgb,
    lab2rgb,
    rgb2hex,
    rgb2lab,
}
