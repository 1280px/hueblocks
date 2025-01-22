# jar2blockset

A modular Python script to extract assets from MCJE .jar file, filter only needed block textures, and then generate blockset description and palettes for them. Successor of blox2rgb.py from legacy HueBlocks versions.

**Only MCJE 1.5+ versions are supproted, and I have no plans to add support for other editions!**


## Usage

1. Go to wherever your MCJE launcher stores versions (default is `~/.minecraft/versions`) and grab a .jar of version you're interested in

2. Make sure you have Python and required modules installed: `pip3 install -r requirements.txt`

3. Run like this: `python3 ./_main.py YOUR_MCJE_VER.jar`

4. By default (if ran like above), the script will behave like this:

    - $A:$ Filter out blocks with ANY transparency (plants, glass, doors, etc.);
    - $B:$ DON'T filter out animated assets (use mean of first and last frames instead);
    - $C:$ Use `autoparser-default.yml` file for facing data, naming, and color generating configuration;
    - $D:$ Use `blacklist-default.yml` file for textures exclusion filter;
    - $E:$ Use `palettes-default.yml` file for texture palettes inclusing filter.

    If you wish to change this behaviour, run the script like this: `python3 ./_main.py YOUR_MCJE_VER.jar A B C D E`, where $A,B$ are corresponding options (`1` for True, `0` for False), and $C,D,E$ are pathes to .yml configuration files. You can also use 'None' to disable blacklist and palettes, but providing valid autoparser file is necessary; Every omitted option will use its default value instead. 


## Output

1. `blocksets.json` — a JSON file containing path, description, and metadata for each blockset:
    ```js
    {
        "name": "My Blockset", // Blockset name, generated automatically
        "dir": "./blocksets/my-blockset", // Directory where data & textures are stored
        "count": 42 // How many textures are in the blockset
    }
    ```
    (if the file already exists, it will be appended, allowing to easily batch multiple blocksets)

2. A directory with the same name as input JAR file, containing:

    1. All the filtered textures

    2. `_blockdata.json` — a JSON list of objects containing blockset data for each texture:
        ```js
        [
            {
                "name": "Cool Block Top", // Block texture name, generated automatically
                "texture": "cool_block_top.png", // Name of block texture with .png extension
                "color": [123, 45, 67], // Mean texture color, computed automatically
                "sides": ["top"] // List of block texture sides in OptiFine CTM faces notation,
                                // excluding "all" and "sides" options for simplicity.
            },
            ...
        ]
        ```

    3. `_palettes.json` — a JSON list of objects containing palettes compiled for the blockset:
        ```js
        [
            "name": "My Palette", // Palette name from original palettes file
            "count": 12, // How many textures are included in the palette
            "includes": [
                "cool_block_top.png", // List of all blocks included in the palette;
                                      // every block not in the palette will be ignored.
                ...
            ]
        ]
        ```

Note that automatically parsed data, especially for older versions, might not be 100% correct, so it is recommended to re-check the blockset before using it in production. You also should NOT rely on default blacklist and autoparse rules if you're changing default parameters or/and using a blockset containing non-vanilla blocks — rather, use them as an example on how these config files work.
