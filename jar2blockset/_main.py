import os
import sys

from datetime import datetime, timezone
from json import load, dump
from PIL import Image
import numpy as np
from shutil import rmtree
from yaml import safe_load
import zipfile

import blockdata
import palettes


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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('\nNot enough arguments! See README for help.')
        sys.exit(1)

    JAR_PATH = sys.argv[1]
    CONFIG_PATH = (
        (sys.argv[2] if (len(sys.argv) >= 3) and (sys.argv[2] != 'None') else 'config-default.yml')
    )
    FACING_PATH = (
        (sys.argv[3] if (sys.argv[3] != 'None') else None)
        if len(sys.argv) >= 5 else 'facing-default.yml'
    )
    BLACKLIST_PATH = (
        (sys.argv[4] if (sys.argv[4] != 'None') else None)
        if len(sys.argv) >= 5 else 'blacklist-default.yml'
    )
    PALETTES_PATH = (
        (sys.argv[5] if (sys.argv[5] != 'None') else None)
        if len(sys.argv) >= 6 else 'palettes-default.yml'
    )

    OUTPUT_PATH = os.path.splitext(JAR_PATH)[0]
    BLOCKSETS_PATH = os.path.dirname(JAR_PATH)


    # Load teh config file
    configs = {
        'exclude-alpha': None,
        'exclude-animated': None,
        'colorcalc': None,
        'naming': {
            'textures': None,
            'blockset': None,
        }
    }
    try:
        with open(CONFIG_PATH, 'r') as config_f:
            configs = safe_load(config_f)
    except:
        print('\nFailed to load config yml! Are you sure the file exists?')
        sys.exit(1)

    # Ask what to do if generated blockset files already exist
    if os.path.isdir(OUTPUT_PATH):
        if input(f'\nOutput dir "{OUTPUT_PATH}" already exists! Type Y to overwrite: ').upper() == 'Y':
            rmtree(OUTPUT_PATH)
    os.mkdir(OUTPUT_PATH)

    # Extract block texture assets from jar
    extract_blocks_from_jar(JAR_PATH, OUTPUT_PATH)
    print(f'\nExtracted {len(os.listdir(OUTPUT_PATH))} assets from JAR\n')

    # Populate list of blacklisted block textures
    if BLACKLIST_PATH:
        blacklist = blockdata.get_blacklisted_blocks(BLACKLIST_PATH, OUTPUT_PATH)


    # Now let's go through every extracted file and remove the unwanted ones
    for fname in sorted(os.listdir(OUTPUT_PATH)):
        if fname.endswith('.png'): # Exclude .mcmeta and crap like this
            img = Image.open(os.path.join(OUTPUT_PATH, fname))
            img_np = np.asarray(img)

            # (A) Exclude textures containing alpha channel
            if configs['exclude-alpha'] != 'none':
                # Older textures used P onlu for textures without alpha and RBGA
                # only for ones with alpha. However, some newer textures also use P
                # even though they use alpha, and since 1.21.6 some textures use L
                # or LA (or even RGB somehow for fire!) to the extent of some glass
                # textures being LA and some RGBA... thank Mojang for this mess.
                img_rgba = img.convert('RGBA')
                img_rgba_np = np.asarray(img_rgba)

                alpha_threshold = 255 if (configs['exclude-alpha'] == 'full') else 1

                if (img_rgba_np[:, :, 3].min()) < alpha_threshold:
                    os.remove(os.path.join(OUTPUT_PATH, fname))
                    # print(f'Excluded {fname} by found alpha ({img.mode})')
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
                if configs['exclude-animated']:
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
            if BLACKLIST_PATH and fname in blacklist:
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
    print(f'Filtered assets down to {len(os.listdir(OUTPUT_PATH))} textures\n')


    # (D) Generate blockdata for each texture, save as JSON
    facing_rules = blockdata.get_facing_rules(FACING_PATH, OUTPUT_PATH)
    print('Computed autoparser rules, processing textures data...\n')

    blockdata_res = blockdata.generate_textures_data(
        OUTPUT_PATH,
        facing_rules,
        configs['naming']['textures'],
        configs['colorcalc']
    )

    # Add generation timestamp (like it used to be in older HB)
    blockdata_res.insert(0,
        'Generated at: ' + str(datetime.now(timezone.utc)).split('.')[0] + ' UTC'
    )

    with open(os.path.join(OUTPUT_PATH, '_blockdata.json'), 'w') as blockdata_f:
        dump(blockdata_res, blockdata_f, indent=2, ensure_ascii=True)
    print(f'Blockdata generation finished, saved as {os.path.join(OUTPUT_PATH, '_blockdata.json')}\n')


    # (E) Compute palettes for the blockset, save as JSON
    if PALETTES_PATH:
        palettes_res = palettes.get_palettes_data(
            PALETTES_PATH, OUTPUT_PATH
        )

        with open(os.path.join(OUTPUT_PATH, '_palettes.json'), 'w') as palettes_f:
            dump(palettes_res, palettes_f, indent=2, ensure_ascii=True)
        print(f'Palettes computation finished, saved as {os.path.join(OUTPUT_PATH, '_palettes.json')}\n')


    # (F) Finally, generate blockset description, write/append as JSON
    descriptions = []
    if os.path.isfile(os.path.join(BLOCKSETS_PATH, '_blocksets.json')):
        with open(os.path.join(BLOCKSETS_PATH, '_blocksets.json'), 'r') as blocksets_f:
            descriptions = load(blocksets_f)
        print('Found existing blocksets data file! ')

        # Make sure we don't have multiple entries with the same dir
        # (also helps easily update data if existing JAR file was changed)
        descriptions = [desc for desc in descriptions if desc['dir'] != OUTPUT_PATH]

    description_res = {
        'name': blockdata.generate_naming(
            os.path.split(JAR_PATH)[-1],
            configs['naming']['blockset']
        ),
        'dir': OUTPUT_PATH,
        'count': len(os.listdir(OUTPUT_PATH))
    }
    descriptions.append(description_res)

    with open(os.path.join(BLOCKSETS_PATH, '_blocksets.json'), 'w') as blocksets_f:
        dump(descriptions, blocksets_f, indent=2, ensure_ascii=True)
    print(f'Updated blocksets data saved as {os.path.join(BLOCKSETS_PATH, '_blocksets.json')}\n')


    print('Done!!!1 :DDD')
    sys.exit(0)
