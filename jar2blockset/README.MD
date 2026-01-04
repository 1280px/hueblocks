# jar2blockset

A modular Python script to extract assets from MCJE .jar file, filter only needed block textures, and then generate blockset description and palettes for them. Successor of blox2rgb.py from legacy HueBlocks versions.

**Only MCJE 1.5+ versions are supported, and I have no plans to add support for other editions!**


## Usage

1. Go to wherever your MCJE launcher stores versions (default is `~/.minecraft/versions`) and grab a .jar of version you're interested in

2. Make sure you have Python and required modules installed: `pip3 install -r requirements.txt`

3. Run like this: `python3 ./_main.py YOUR_MCJE_VER.jar`

4. By default (if ran like above), the script will behave like this:

    - $A:$ Filter out blocks with ANY transparency (plants, glass, doors, etc.);
    - $B:$ DON'T filter out animated assets (use mean of first and last frames instead);
    - $C:$ Use `blacklist-default.yml` for textures exclusion filter;
    - $D:$ Use `config-default.yml` settings for data, naming, and color configuration, and `facing-default.yml` to compute textures facing from their names;
    - $E:$ Use `palettes-default.yml` for texture palettes inclusing filter;
    - $F:$ Use `config-default.yml` settings for blockset's naming configuration.

    If you wish to change this behaviour, run the script like this: `python3 ./_main.py YOUR_MCJE_VER.jar c b f p`, where $c,b,f,p$ are pathes to config, blacklist, facing and palettes .yml files respectively. You can also use `None` to disable blacklist and facing parser and palettes, but providing valid config file is necessary; Every omitted option will use its default value instead.
    
    You can find more information about each file within default .ymls themselves.


## Output

1. `_blocksets.json` — a JSON file containing path, description, and metadata for each blockset:
    ```js
    {
        "name": "My Blockset", // Blockset name, generated automatically
        "dir": "./blocksets/my-blockset", // Relative path to where data & textures are stored
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
                "rgb": [123, 45, 67], // Mean texture color in RGB colorpsace (no alpha)
                "lab": [0.163, -0.106, 0.416], // Mean texture color in OkLAB colorspace
                "sides": ["top"] // List of applicable block texture sides in OptiFine CTM
                                 // faces notation, excluding "all" and "sides" options.
            },
            ...
        ]
        ```

    3. `_palettes.json` — a JSON list of objects containing palettes compiled for the blockset:
        ```js
        [
            "name": "My Palette", // Palette name from original palettes file
            "textures": [
                "cool_block_top.png", // List of all blocks included in the palette;
                                      // every block not in the palette will be ignored.
                ...
            ],
            "count": 12 // How many textures are included in the palette
        ]
        ```

Note that automatically parsed data, especially for older versions, might not be 100% correct, so it is recommended to re-check the blockset before using it in production. You also should NOT rely on default blacklist and autoparse rules if you're changing default parameters or/and using a blockset containing non-vanilla blocks — rather, use them as an example on how these config files work.


## jarfetcher

A small helper Python script that is used by CI/CD for getting two exact JAR files from Mojang's Piston Meta servers — the latest stable(!) version and 1.13.2 (the latest version to come with Programmer's Art textures as default). **You don't need to run it if you have obtained JAR files already**, but it can be helpful if you wish to automate MCJE versions fetching for your own needs as well.

Usage: `python3 _jarfetcher.py OUTPUT_DIR` (if $OUTPUT\_DIR$ is omitted, current dir will be used).
