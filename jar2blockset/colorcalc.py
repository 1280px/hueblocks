import sys

import numpy as np
from PIL import Image


def add_srgb_gamma(c_lrgb):
    # return np.power(c_lrgb, 1/2)
    if (c_lrgb >= 0.0031308):
        return (1.055 * np.power(c_lrgb, (1 / 2.4))) - 0.055
    else:
        return c_lrgb * 12.92
    
def remove_srgb_gamma(c_srgb):
    # return np.power(c_srgb, 2)
    if (c_srgb >= 0.04045):
        return np.power((c_srgb + 0.055) / 1.055, 2.4)
    else:
        return c_srgb / 12.92


def img2rgb(texture_path, colorcalc_rule):
    img = Image.open(texture_path)

    # Modern method -- instead of calculating avg color as literal averages
    # of each RGB channel (+- resampling artefacts), find sqrts of mean of
    # each channel squared. This results in result color being more vibrant,
    # closer to original image brightness! Check this amazing article and
    # video in it: https://sighack.com/post/averaging-rgb-colors-the-right-way
    if colorcalc_rule == 'modern':
        srgb2lrgb = np.vectorize(lambda color: remove_srgb_gamma(color / 255.0))
        lrgb2srgb = np.vectorize(lambda color: add_srgb_gamma(color) * 255.0)

        img_np = np.asarray(
            img.convert("RGB"),
            dtype=np.float64 # Otherwise will almost certainly overflow 
        )

        mean_of_squares = np.mean(srgb2lrgb(img_np), axis=(0, 1))

        sqrts_of_mean_of_squares = np.clip(
            lrgb2srgb(mean_of_squares),
        0, 255) # Prevent color being out of 0..255 range

        img.close()
        return [int(c) for c in sqrts_of_mean_of_squares]

    # Legacy method -- just like it worked in older versions of HueBlocks:
    # using PIL antialias, shrink image to a single pixel and take its color
    elif colorcalc_rule == 'legacy':
        # Even though it is said that Image.LANCZOS gives the same color
        # as now-deprecated Image.ANTIALIAS, in reality the results are
        # a bit different! Not much can be done about this, sadly, though.
        img_proc = img.resize((1, 1), Image.Resampling.LANCZOS)
        img_proc_np = np.asarray(img_proc.convert("RGB"))

        img_color = img_proc_np[0][0]

        img.close()
        return [int(c) for c in img_color]

    else:
        print(f'Incorrect colorcalc rule "{colorcalc_rule}"!')
        img.close()
        sys.exit(1)


def img2lab(texture_path, srgb=None):
    # Since image colors stored as RGB, we get average RGB color
    # (if it wasn't pre-calculated and provided) from image first
    if srgb is None:
        srgb = img2rgb(texture_path, 'modern')

    # Convert to linear RGB and normalize to 0..1
    lrgb = np.array(
        [remove_srgb_gamma(color / 255.0) for color in srgb]
    )

    # The following process is exactly the same as implemented
    # client-side, so, see rgb2lab(1) in colors.ts for more details.

    # LRGB -> CIEXYZ -> LMS
    l = 0.4122214708 * lrgb[0] + 0.5363325363 * lrgb[1] + 0.0514459929 * lrgb[2]
    m = 0.2119034982 * lrgb[0] + 0.6806995451 * lrgb[1] + 0.1073969566 * lrgb[2]
    s = 0.0883024619 * lrgb[0] + 0.2817188376 * lrgb[1] + 0.6299787005 * lrgb[2]

    # LMS -> LMS'
    l_ = np.power(l, 1 / 3)
    m_ = np.power(m, 1 / 3)
    s_ = np.power(s, 1 / 3)

    # LMS' -> Lab
    lab = np.array([
        +0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        +1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        +0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    ])

    # Force non-scientific notation because it breaks client-side logic
    return [f'{lab[0]:.20f}', f'{lab[1]:.20f}', f'{lab[2]:.20f}']

