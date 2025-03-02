import os
import sys

import numpy as np
from PIL import Image


def img2rgb(texture_path, colorcalc_rule):
    img = Image.open(texture_path)

    # Modern method -- instead of calculating avg color as literal averages
    # of each RGB channel (+- resampling artefacts), find sqrts of mean of
    # each channel squared. This results in result color being more vibrant,
    # closer to original image brightness! Check this amazing article and
    # video in it: https://sighack.com/post/averaging-rgb-colors-the-right-way
    if colorcalc_rule == 'modern':
        img_np = np.asarray(
            img.convert("RGB"),
            dtype=np.float64 # Otherwise will almost certainly overflow 
        )
        img_np = img_np ** 2

        mean_of_squares = np.mean(img_np, axis=(0, 1))

        sqrts_of_mean_of_squares = np.floor(
            np.sqrt(mean_of_squares)
        ).astype(np.uint8) # Prevent color being out of 0-255 range

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


def img2lab(texture_path, rgb=None):
    # Since image color are stored as RGB, we get average RGB color
    # (if it wasn't pre-calculated and provided) from image first
    if rgb is None:
        rgb = img2rgb(texture_path, 'modern')

    # See this amazing intractive article for colorspace conversion
    # details: https://observablehq.com/@mbostock/lab-and-rgb

    # Convert to linear light RGB and normalize to 0..1
    def color2llrgb(color):
        value = color / 255
        return (value / 12.92) if (value <= 0.04045) else ((value + 0.055) / 1.055)**2.4

    llrgb = np.array(
        [color2llrgb(color) for color in rgb]
    )

    # Now, convert from RGB to XYZ in two steps: first convert colorspace
    # from LLRGB to XYZ, and then convert chromatic adaptation from D65
    # (ref in RGB) to D50 (ref in CIELAB). Matrices taken from:
    # 1. http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    # 2. http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
    bradford_lrgbD65_xyzD65 = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])
    bradford_xyzD65_xyzD50 = np.array([
        [1.0478112, 0.0228866, -0.0501270],
        [0.0295424, 0.9904844, -0.0170491],
        [-0.0092345, 0.0150436, 0.7521316]
    ])

    xyz = np.dot(
        bradford_xyzD65_xyzD50,
        np.dot(
            bradford_lrgbD65_xyzD65,
            llrgb
        )
    )

    # Finally, convert from XYZ to CIELAB
    def lab_f(x):
        return np.cbrt(x) if (x > ((6/29)**3)) else ((1/3) * (29/6)**2 * x + (4/29))

    # (pre-calculated from Bradford RGB D65 -> XYZ D50 conversion
    # matrix by summing its values along the horizontal axis)
    xyz_tristimulus = np.array([0.96422, 1.0, 0.82521])

    f_xyz_norm = np.array(
        [lab_f(xyz[i] / xyz_tristimulus[i]) for i in range(xyz.shape[0])]
    )

    lab = np.array([
        116 * f_xyz_norm[1] - 16,
        500 * (f_xyz_norm[0] - f_xyz_norm[1]),
        200 * (f_xyz_norm[1] - f_xyz_norm[2])
    ])

    # print('CONTROL:', texture_path, lab, rgb, '\n')
    return list(lab)
