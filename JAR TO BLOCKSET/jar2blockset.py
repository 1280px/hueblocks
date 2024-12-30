import zipfile
import os
import shutil
import sys
import numpy as np
from PIL import Image
import datetime


def extract_blocks_from_jar(jar_path, output_path):
    with zipfile.ZipFile(jar_path, 'r') as jar:
        for file in jar.namelist():
            if (
                file.startswith('assets/minecraft/textures/block') # 1.13+
                or file.startswith('assets/minecraft/textures/blocks') # 1.6.1--1.12.2
                or file.startswith('textures/blocks') # 1.5--1.6
            ):
                fname = os.path.basename(file)

                if fname: # Exclude directories themselves
                    with jar.open(file) as source, open(os.path.join(output_path, fname), 'wb') as target:
                        # Note that we intentionally do not exclude .txt/.mcmeta files,
                        # as they'll be useful later to determine whether the texture
                        # is actually animated or just has an irregular non-square shape!
                        target.write(source.read())
    return


def get_blacklisted_blocks(blacklist_path, blocks_path):
    blocks_names = sorted(os.listdir(blocks_path))
    blacklist = []

    with open(blacklist_path, 'r') as blist:
        for line_raw in blist:
            # Skip comments and empty lines
            if line_raw.startswith('#') or line_raw == '\n':
                continue

            line = line_raw.strip('\n')
            line_star = line.find('*')

            # Exclude wildcard-only filter, just in case
            if line == '*':
                print('Wildcard filter "*" is not allowed -- like, why would you want to remove EVERYTHING from blockset?')
                continue

            if line_star == -1: # No wildcard
                blacklist.append(line)
                continue

            elif line_star == len(line)-1: # Prefix wildcard
                for block_name in blocks_names:
                    if block_name.startswith(line.split('*')[0]):
                        blacklist.append(block_name)

            elif line_star == 0: # Suffix wildcard
                for block_name in blocks_names:
                    if block_name.endswith(line.split('*')[1]):
                        blacklist.append(block_name)
    return blacklist



def get_autoparse_rules(autoparse_path):
    return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Not enough arguments! See README for help.')
        sys.exit(0)
    JAR_PATH = sys.argv[1]
    EXCLUDE_ALPHA = (sys.argv[2] == '1') if len(sys.argv) >= 3 else True
    EXCLUDE_ANIMATED = (sys.argv[3] == '1') if len(sys.argv) >= 4 else True
    BLACKLIST_PATH = (
        (sys.argv[4] if (sys.argv[4] != 'None') else None)
        if len(sys.argv) >= 5 else 'blacklist-default.cfg'
    )
    AUTOPARSE_PATH = (
        (sys.argv[5] if (sys.argv[5] != 'None') else None)
        if len(sys.argv) >= 6 else 'autoparser-rules.cfg'
    )
    # print(JAR_PATH, EXCLUDE_ALPHA, EXCLUDE_ANIMATED, BLACKLIST_PATH, AUTOPARSE_PATH)
    OUTPUT_PATH = os.path.splitext(JAR_PATH)[0]

    # Ask what to do if output directory already exists
    if os.path.isdir(OUTPUT_PATH):
        if input(f'Output dir "{OUTPUT_PATH}" already exists! Type Y to replace: ').upper() == 'Y':
            shutil.rmtree(OUTPUT_PATH)
    os.mkdir(OUTPUT_PATH)


    # Extract block texture assets from jar
    extract_blocks_from_jar(JAR_PATH, OUTPUT_PATH)

    # Populate list of blacklisted blocks
    blacklist = get_blacklisted_blocks(BLACKLIST_PATH, OUTPUT_PATH)


    print('')

    # Now let's go through every extracted file and remove the unwanted ones
    for fname in sorted(os.listdir(OUTPUT_PATH)):
        if fname.endswith('.png'):
            img = Image.open(os.path.join(OUTPUT_PATH, fname))
            img_np = np.asarray(img)

            # (A) Exclude textures containing alpha channel
            if EXCLUDE_ALPHA:
                # Older textures used P onlu for textures without alpha and RBGA only
                # for ones with alpha. However, some newer textures also use P even
                # though they use alpha, so, we have to check it as well to be sure.
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
                # (B) Exclude textures with .txt/.mcmeta is option is true;
                # otherwise, use blend of first & last frames as a new texture
                if EXCLUDE_ANIMATED:
                    os.remove(os.path.join(OUTPUT_PATH, fname))
                    # print('Excluded', fname, '(B)')
                else:
                    img_first_frame = img.convert("RGBA").crop((0, 0, img_np.shape[1], img_np.shape[1]))
                    img_last_frame = img.convert("RGBA").crop((0, img_np.shape[0]-img_np.shape[1], img_np.shape[1], img_np.shape[0]))

                    img_new = Image.blend(img_first_frame, img_last_frame, alpha=0.5)
                    img_new.save(os.path.join(OUTPUT_PATH, fname))
                    # img_new.show()
                    # print('Modified', fname, '(B)')

            # (C) Exclude textures from the blacklist
            if fname in blacklist:
                try:
                    os.remove(os.path.join(OUTPUT_PATH, fname))
                    # print('Excluded', fname, '(C)')
                except:  # In case teh file was deleted already,
                    pass # or didn't even exist in the first place 

            img.close()

    # Remove animation metadata crap because we don't need it anymore
    for fname in sorted(os.listdir(OUTPUT_PATH)):
        if fname.endswith('.mcmeta') or fname.endswith('.txt'):
            os.remove(os.path.join(OUTPUT_PATH, fname))


    # (D) TODO: Finally, generate file with data about each texture
    # auroparse = get_autoparse_rules(AUTOPARSE_PATH)
    # blockset_data = []

    # for fname in sorted(os.listdir(OUTPUT_PATH)):
    #     texture_data = generate_texture_data(fname, OUTPUT_PATH, auroparse.naming, auroparse.facing)
    #     blockset_data.append(texture_data)


