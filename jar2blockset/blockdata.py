import os
import sys

from yaml import safe_load

import filters
import colorcalc


def get_blacklisted_blocks(blacklist_path, textures_path):
    textures_names = sorted(os.listdir(textures_path))

    with open(blacklist_path, 'r') as blacklist_f:
        blacklist_raw = safe_load(blacklist_f)

    blacklist = filters.compute_filter(blacklist_raw['filters'], textures_names, 'blacklist')

    # We don't care about metadata in this case, so we just strip it out
    return list(blacklist.keys())


def get_autoparser_rules(autoparser_path, textures_path):
    with open(autoparser_path, 'r') as autoparser_f:
        autoparser_raw = safe_load(autoparser_f)

    textures_names = sorted(os.listdir(textures_path))
    textures_names = list(filter(lambda file: file.endswith('.png'), textures_names))


    # First, get naming and colorcalc rules from file, no changes needed
    naming_rules = autoparser_raw['naming']
    colorcalc_rule = autoparser_raw['colorcalc']


    # Second, compute facing filters! This will take MUCH longer...
    sides = ['top', 'bottom', 'north', 'south', 'east', 'west', 'sides', 'all']

    # At first we compute filters for every facing option (bruh!!1)
    facing_filters = {
        side: {} for side in sides
    }
    for side in facing_filters.keys():
        facing_filters[side] = filters.compute_filter(autoparser_raw['facing'][side], textures_names, side)

    # Now we need to convert this object of objects into a list of pairs
    # consisting out of a texture name and a tuple of its applicable sides.
    # We will also get rid of duplicates by prioritizing regular filters
    # over wildcard filters and one-sided options over multi-sided options.
    textures_to_sides = dict()

    for name in textures_names:
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


def generate_textures_data(textures_path, facing_filters, naming_rule, colorcalc_rule):
    textures_data = []

    textures_names = sorted(os.listdir(textures_path))
    textures_names = list(filter(lambda file: file.endswith('.png'), textures_names))

    for texture_name in textures_names:
        texture_sides = facing_filters.get(
            texture_name,
            # Fallback just in case (should never be used actually)
            ['top', 'bottom', 'north', 'south', 'east', 'west']
        )

        texture_path = os.path.join(textures_path, texture_name)

        texture_rgb = colorcalc.img2rgb(texture_path, colorcalc_rule)
        texture_lab = colorcalc.img2lab(texture_path, texture_rgb)

        texture_data = {
            'name': generate_naming(texture_name, naming_rule),
            # Full path can later be computed using blockset's dir property
            'texture': texture_name,
            'rgb': texture_rgb,
            'lab': texture_lab,
            'sides': texture_sides
        }
        textures_data.append(texture_data)

    return textures_data
