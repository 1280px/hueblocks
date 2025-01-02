import os
import sys
from shutil import rmtree

import numpy as np
from PIL import Image

import zipfile
from yaml import safe_load
from json import encoder


def extract_blocks_from_jar(jar_path, output_path):
    with zipfile.ZipFile(jar_path, 'r') as jar_f:
        for file in jar_f.namelist():
            if (
                file.startswith('assets/minecraft/textures/block') # 1.13+
                or file.startswith('assets/minecraft/textures/blocks') # 1.6.1--1.12.2
                or file.startswith('textures/blocks') # 1.5--1.6
            ):
                fname = os.path.basename(file)

                if fname: # Exclude directories themselves
                    with jar_f.open(file) as source, open(os.path.join(output_path, fname), 'wb') as target:
                        # Note that we intentionally do not exclude .txt/.mcmeta files,
                        # as they'll be useful later to determine whether the texture
                        # is actually animated or just has an irregular non-square shape!
                        target.write(source.read())
    return


def compute_filter(lines, names):
    # Sequentially computes a filter; returns LIST OF PAIRS of filtered
    # block names and filter type metadata, which will be used later for
    # prioritization of regular filter rules over wildcard filter rules.
    rules = {}
    print(f'Computing filter from {len(lines)} lines...')

    for line in lines:
        # Exclude wildcard-only filter, just in case
        if line == '$':
            print('Wildcard filter "$" is not allowed -- like, why would you want to remove EVERYTHING from blockset?')
            continue
        
        line_star = line.find('$')

        if line_star == -1: # No wildcard
            rules[line] = 'R'

        elif line_star == len(line)-1: # Prefix wildcard
            for name in names:
                if name.startswith(line.split('$')[0]):
                    # Prioritize regular filters over wildcard!
                    if name not in rules or rules[name] != 'R':
                        rules[name] = 'W'

        elif line_star == 0: # Suffix wildcard
            for name in names:
                if name.endswith(line.split('$')[1]):
                    # Prioritize regular filters over wildcard!
                    if name not in rules or rules[name] != 'R':
                        rules[name] = 'W'

    print(f'Finished computation into {len(rules)} rules.\n')
    return rules


def get_blacklisted_blocks(blacklist_path, blocks_path):
    blocks_names = sorted(os.listdir(blocks_path))

    with open(blacklist_path, 'r') as blacklist_f:
        blacklist_raw = safe_load(blacklist_f)

    blacklist = compute_filter(blacklist_raw['filters'], blocks_names)

    # We don't care about metadata in this case, so we just strip it out
    return list(blacklist.keys())


def get_autoparse_facing(autoparse_path, blocks_path):
    sides = ['top', 'bottom', 'north', 'south', 'east', 'west', 'sides', 'all']
    blocks_names = sorted(os.listdir(blocks_path))

    with open(autoparse_path, 'r') as autoparse_f:
        autoparse_raw = safe_load(autoparse_f)

    # First we compute filters for every single facing option (bruh!!1)
    facing_filters = {
        side: {} for side in sides
    }
    for side in facing_filters.keys():
        # print(side)
        facing_filters[side] = compute_filter(autoparse_raw['facing'][side], blocks_names)

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
    return textures_to_sides


def get_autoparse_naming(autoparse_path):
    with open(autoparse_path, 'r') as autoparse_f:
        autoparse_raw = safe_load(autoparse_f)
    
    naming_rules = autoparse_raw['naming']
    return naming_rules


def get_autoparse_colorcalc(autoparse_path):
    with open(autoparse_path, 'r') as autoparse_f:
        autoparse_raw = safe_load(autoparse_f)
    
    colorcalc_rule = autoparse_raw['colorcalc']
    return colorcalc_rule


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
            np.sqrt(mean_of_squares),
            # dtype=np.uint8
        ).astype(np.uint8) # Prevent color being out of 0-255 range

        # Compare results!
        img_proc = img.resize((1, 1), Image.Resampling.LANCZOS)
        img_proc_np = np.asarray(img_proc.convert("RGB"))
        img_color = img_proc_np[0][0]
        print(texture_path, '\nlegacy:', list(img_color), 'modern:', list(sqrts_of_mean_of_squares), '\n')

        return list(sqrts_of_mean_of_squares)

    # Legacy method -- just like it worked in older versions of HueBlocks:
    # using PIL antialias, shrink image to a single pixel and take its color
    elif colorcalc_rule == 'legacy':
        # Image.LANCZOS does exactly the same as now-deprecated Image.ANTIALIAS
        img_proc = img.resize((1, 1), Image.Resampling.LANCZOS)
        img_proc_np = np.asarray(img_proc.convert("RGB"))
        img_color = img_proc_np[0][0]

        return list(img_color)

    else:
        print(f'Incorrect colorcalc rule "{colorcalc_rule}"!')
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('\nNot enough arguments! See README for help.')
        sys.exit(0)
    JAR_PATH = sys.argv[1]
    EXCLUDE_ALPHA = (sys.argv[2] == '1') if len(sys.argv) >= 3 else True
    EXCLUDE_ANIMATED = (sys.argv[3] == '1') if len(sys.argv) >= 4 else True
    BLACKLIST_PATH = (
        (sys.argv[4] if (sys.argv[4] != 'None') else None)
        if len(sys.argv) >= 5 else 'blacklist-default.yml'
    )
    AUTOPARSE_PATH = (
        (sys.argv[5] if (sys.argv[5] != 'None') else None)
        if len(sys.argv) >= 6 else 'autoparse-default.yml'
    )
    # print(JAR_PATH, EXCLUDE_ALPHA, EXCLUDE_ANIMATED, BLACKLIST_PATH, AUTOPARSE_PATH)
    OUTPUT_PATH = os.path.splitext(JAR_PATH)[0]


    # Ask what to do if generated blockset files already exist
    if os.path.isdir(OUTPUT_PATH):
        if input(f'\nOutput dir "{OUTPUT_PATH}" already exists! Type Y to replace: ').upper() == 'Y':
            rmtree(OUTPUT_PATH)
    os.mkdir(OUTPUT_PATH)

    if os.path.isfile(OUTPUT_PATH + '.json'):
        if input(f'\nBlockset data "{OUTPUT_PATH + ".json"}" already exists! Type Y to delete: ').upper() == 'Y':
            os.remove(OUTPUT_PATH + '.json')


    # Extract block texture assets from jar
    extract_blocks_from_jar(JAR_PATH, OUTPUT_PATH)
    print(f'\nExtracted {len(os.listdir(OUTPUT_PATH))} assets from JAR\n')

    # Populate list of blacklisted block textures
    blacklist = get_blacklisted_blocks(BLACKLIST_PATH, OUTPUT_PATH)


    # Now let's go through every extracted file and remove the unwanted ones
    for fname in sorted(os.listdir(OUTPUT_PATH)):
        if fname.endswith('.png'):
            img = Image.open(os.path.join(OUTPUT_PATH, fname))
            img_np = np.asarray(img)

            # (A) Exclude textures containing alpha channel
            if EXCLUDE_ALPHA:
                # Older textures used P onlu for textures without alpha and RBGA only
                # for ones with alpha. However, some newer textures also use P even
                # though they use alpha, so, we have to check it as well, to be sure.
                if img.mode == 'RGBA':
                    if (img_np[:, :, 3].min()) < 255:
                        os.remove(os.path.join(OUTPUT_PATH, fname))
                        # print('Excluded', fname, '(A RGBA)')
                        continue

                elif img.mode == 'P':
                    img_temp = img.convert("RGBA")
                    img_temp_np = np.asarray(img_temp)

                    if (img_temp_np[:, :, 3].min()) < 255:
                        os.remove(os.path.join(OUTPUT_PATH, fname))
                        # print('Excluded', fname, '(A P)')
                        continue

            fname_noext = os.path.splitext(fname)[0]

            # If a texture has corrresponding txt (1.5) or mcmeta (1.6+) file,
            # than it is animated, meaning it is N times taller its width.
            if (
                os.path.isfile(os.path.join(OUTPUT_PATH, fname_noext + '.txt'))
                or os.path.isfile(os.path.join(OUTPUT_PATH, fname + '.mcmeta'))
            ):
                # (B) Exclude textures with .txt/.mcmeta if option is true;
                # otherwise, use blend of first & last frames as a new texture.
                if EXCLUDE_ANIMATED:
                    os.remove(os.path.join(OUTPUT_PATH, fname))
                    # print('Excluded', fname, '(B)')

                else:
                    img_first_frame = img.convert("RGBA").crop((0, 0, img_np.shape[1], img_np.shape[1]))
                    img_last_frame = img.convert("RGBA").crop((0, img_np.shape[0]-img_np.shape[1], img_np.shape[1], img_np.shape[0]))

                    img_new = Image.blend(img_first_frame, img_last_frame, alpha=0.5)
                    img_new.convert("RGB").save(os.path.join(OUTPUT_PATH, fname))
                    # img_new.show()
                    # print('Modified', fname, '(B)')

            # (C) Exclude textures from the blacklist
            if fname in blacklist:
                try:
                    os.remove(os.path.join(OUTPUT_PATH, fname))
                    # print('Excluded', fname, '(C)')
                except:  # Prevent FileNotFoundError in case teh file was already deleted
                    pass # by the filters below, or didn't even exist in the first place.

            img.close()

    # Remove animation metadata crap because we don't need it anymore
    for fname in sorted(os.listdir(OUTPUT_PATH)):
        if fname.endswith('.mcmeta') or fname.endswith('.txt'):
            os.remove(os.path.join(OUTPUT_PATH, fname))
    print(f'Filtered out down to {len(os.listdir(OUTPUT_PATH))} assets\n')


    # (D) Generate blockset data about each texture
    autoparse_facing_filters = get_autoparse_facing(AUTOPARSE_PATH, OUTPUT_PATH)
    autoparse_naming_rules = get_autoparse_naming(AUTOPARSE_PATH)
    autoparse_colorcalc_rule = get_autoparse_colorcalc(AUTOPARSE_PATH)
    print('Computed autoparse rules, processing textures...\n')

    blockset_data = {
        'name': generate_naming(os.path.split(JAR_PATH)[-1], autoparse_naming_rules['blockset']),
        'dir': OUTPUT_PATH,
        'count': len(os.listdir(OUTPUT_PATH)),
        'data': generate_textures_data(
            OUTPUT_PATH,
            autoparse_facing_filters, autoparse_naming_rules['textures'], autoparse_colorcalc_rule
        )
    }
    print('Blockset generation finished!\n')

    # Finally, save blockset data as JSON
    raise NotImplementedError
    print('Blockset data saved as {OUTPUT_PATH + ".json"}')
