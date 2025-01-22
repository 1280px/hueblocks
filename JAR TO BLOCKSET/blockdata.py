import os
import sys

import numpy as np
from PIL import Image
from yaml import safe_load

import filters


def get_blacklisted_blocks(blacklist_path, blocks_path):
    blocks_names = sorted(os.listdir(blocks_path))

    with open(blacklist_path, 'r') as blacklist_f:
        blacklist_raw = safe_load(blacklist_f)

    print('blacklist')
    blacklist = filters.compute_filter(blacklist_raw['filters'], blocks_names)

    # We don't care about metadata in this case, so we just strip it out
    return list(blacklist.keys())


def get_autoparser_rules(autoparser_path, blocks_path):
    with open(autoparser_path, 'r') as autoparser_f:
        autoparser_raw = safe_load(autoparser_f)

    # First, get naming and colorcalc rules from file, no changes needed
    naming_rules = autoparser_raw['naming'] 
    colorcalc_rule = autoparser_raw['colorcalc']


    # Second, compute facing filters! This will take MUCH longer...
    sides = ['top', 'bottom', 'north', 'south', 'east', 'west', 'sides', 'all']
    blocks_names = sorted(os.listdir(blocks_path))

    # At first we compute filters for every facing option (bruh!!1)
    facing_filters = {
        side: {} for side in sides
    }
    for side in facing_filters.keys():
        print(side)
        facing_filters[side] = filters.compute_filter(autoparser_raw['facing'][side], blocks_names)

    # Now we need to convert this object of objects into a list of pairs
    # consisting out of a texture name and a tuple of its applicable sides.
    # We will also get rid of duplicates by prioritizing regular filters
    # over wildcard filters and one-sided options over multi-sided options.
    textures_to_sides = dict()

    for name in blocks_names:
        name_present = {
            side: facing_filters[side].get(name, 'X') for side in sides
        }
        # print(name, name_present)

        present_sides = []
        # Since "all" option currently includes overrides only, it has the
        # highest priority at this moment; the second priority have all the
        # one-sided options; so, 'sides' option actually the least important!
        # We also translate "all" and "sides" multi-side options into list
        # of one-side options, just to make blockset facing data more simple.
        if name_present['all'] != 'X':
            present_sides = sides.copy()[:-2]

        else:
            for side in sides[:-2]: 
                if name_present[side] != 'X':
                    present_sides.append(side)
            
            if present_sides:
                pass

            elif name_present['sides'] != 'X':
                present_sides = sides.copy()[2:-2]

            # No filters matched, meaning this texture is used on all sides
            else:
                present_sides = sides.copy()[:-2]
        # print(present_sides, '\n')

        textures_to_sides[name] = present_sides


    # Finally, return all the rules as dict
    return {
        'naming': naming_rules,
        'colorcalc': colorcalc_rule,
        'facing': textures_to_sides
    }


def generate_naming(string, naming_rule):
    if naming_rule == 'none':
        return string

    string_new = os.path.splitext(string)[0]
    # Underscores used by block assets, and dashes commonly used in JAR filenames
    string_new = ' '.join(string_new.split('_'))
    string_new = ' '.join(string_new.split('-'))

    if naming_rule == 'title':
        return string_new.title()
    elif naming_rule == 'capital':
        return string_new.capitalize()
    elif naming_rule == 'sep':
        return string_new

    else:
        print(f'Incorrect naming rule "{naming_rule}"!')
        sys.exit(1)
    

def calc_avg_color(texture_path, colorcalc_rule):
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

        # Compare results!
        # img_proc = img.resize((1, 1), Image.Resampling.LANCZOS)
        # img_proc_np = np.asarray(img_proc.convert("RGB"))
        # img_color = img_proc_np[0][0]
        # print(texture_path, '\nlegacy:', list(img_color), 'modern:', list(sqrts_of_mean_of_squares), '\n')

        img.close()
        return [int(c) for c in sqrts_of_mean_of_squares]

    # Legacy method -- just like it worked in older versions of HueBlocks:
    # using PIL antialias, shrink image to a single pixel and take its color
    elif colorcalc_rule == 'legacy':
        # Image.LANCZOS does exactly the same as now-deprecated Image.ANTIALIAS
        img_proc = img.resize((1, 1), Image.Resampling.LANCZOS)
        img_proc_np = np.asarray(img_proc.convert("RGB"))
        img_color = img_proc_np[0][0]

        img.close()
        return [int(c) for c in img_color]

    else:
        print(f'Incorrect colorcalc rule "{colorcalc_rule}"!')
        img.close()
        sys.exit(1)


def generate_textures_data(textures_path, facing_filters, naming_rule, colorcalc_rule):
    textures_data = []

    for texture_name in sorted(os.listdir(textures_path)):
        texture_sides = facing_filters.get(
            texture_name,
            # Fallback just in case (should never be used actually)
            ['top', 'bottom', 'north', 'south', 'east', 'west']
        )
        texture_path = os.path.join(textures_path, texture_name)

        texture_data = {
            'name': generate_naming(texture_name, naming_rule),
            # Full path can later be computed using blockset's dir property
            'texture': texture_name,
            'color': calc_avg_color(texture_path, colorcalc_rule),
            'sides': texture_sides
        }
        textures_data.append(texture_data)

    return textures_data
