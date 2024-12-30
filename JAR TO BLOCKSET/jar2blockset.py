import zipfile
import os
import sys
import numpy as np
from PIL import Image
import datetime


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Not enough arguments! See README for help.')
        sys.exit(0)

    JAR_PATH = sys.argv[1]
    EXCLUDE_ALPHA = (sys.argv[2] == '1') if len(sys.argv) >= 3 else True
    EXCLUDE_ANIMATED = (sys.argv[3] == '1') if len(sys.argv) >= 4 else True
    AUTOPARSER = (sys.argv[4] == '1') if len(sys.argv) >= 5 else True
    BLACKLIST_PATH = (
        (sys.argv[5] if (sys.argv[5] != 'None') else None)
        if len(sys.argv) >= 6 else 'blacklist-default.cfg'
    )

    print(JAR_PATH, EXCLUDE_ALPHA, EXCLUDE_ANIMATED, AUTOPARSER, BLACKLIST_PATH)


    # Extract block assets from jar
    OUTPUT_PATH = os.path.splitext(JAR_PATH)[0]

    with zipfile.ZipFile(JAR_PATH, 'r') as jar:
        os.mkdir(OUTPUT_PATH)

        for file in jar.namelist():
            if (
                file.startswith('assets/minecraft/textures/block') # 1.13+
                or file.startswith('assets/minecraft/textures/blocks') # 1.6.1--1.12.2
                or file.startswith('textures/blocks') # 1.5--1.6
            ):
                fname = os.path.basename(file)

                if fname: # Exclude directories themselves
                    with jar.open(file) as source, open(os.path.join(OUTPUT_PATH, fname), 'wb') as target:
                        # Note that we intentionally do not exclude .txt/.mcmeta files,
                        # as they'll be useful later to determine whether the texture
                        # is actually animated or just has an irregular non-square shape!
                        target.write(source.read())


    # Now let's go through every extracted file and remove the unwanted ones
    for file in sorted(os.listdir(OUTPUT_PATH)):
        if file.endswith('.png'):
            img = Image.open(os.path.join(OUTPUT_PATH, file))
            img_np = np.asarray(img)

            # (A) Exclude textures containing alpha channel
            if EXCLUDE_ALPHA:
                if img_np.shape[2] == 4:
                    if (img_np[:, :, 3].min()) < 255:
                        os.remove(os.path.join(OUTPUT_PATH, file))
                        continue

            fname_noext = os.path.splitext(file)[0]

            if fname_noext == 'lava':
                print('i am lava!!!1')
                print(fname_noext + '.mcmeta')

            if (
                os.path.isfile(os.path.join(OUTPUT_PATH, fname_noext + '.mcmeta'))
                or os.path.isfile(os.path.join(OUTPUT_PATH, fname_noext + '.txt'))
            ):
                # (B) Exclude textures with .txt/.mcmeta provided
                if EXCLUDE_ANIMATED:
                    os.remove(os.path.join(OUTPUT_PATH, file))

                # Otherwise, use blend of first & last frames as texture
                else:
                    img_first_frame = img.crop((0, 0, img_np.shape[1], img_np.shape[1]))
                    img_last_frame = img.crop((0, img_np.shape[0]-img_np.shape[1], img_np.shape[1], img_np.shape[0]))

                    img_new = Image.blend(img_first_frame, img_last_frame, alpha=0.5)
                    img_new.save(os.path.join(OUTPUT_PATH, file))
                    # img_new.show()

                # Remove animation metadata crap as well
                if os.path.isfile(os.path.join(OUTPUT_PATH, fname_noext + '.mcmeta')):
                    os.remove(os.path.join(OUTPUT_PATH, fname_noext + '.mcmeta'))
                if os.path.isfile(os.path.join(OUTPUT_PATH, fname_noext + '.txt')):
                    os.remove(os.path.join(OUTPUT_PATH, fname_noext + '.txt'))
                continue

            # TODO: Exclude textures from the blacklist
            if BLACKLIST_PATH is not None:
                pass

        img.close()


    # TODO: Finally, generate file with data for each texture
