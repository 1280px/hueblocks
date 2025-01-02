# jar2blockset

A simple Python script to extract assets from MCJE .jar file, filter only needed block textures, and then generate blockset description for them. Successor of blox2rgb.py from legacy HueBlocks versions.

**Only MCJE 1.5+ versions are supproted, and I have no plans to add support for other editions!**


## Usage

1. Go to wherever your MCJE launcher stores versions (default is `~/.minecraft/versions`) and grab a .jar of version you're interested in

2. Make sure you have Python and required modules installed: `pip3 install -r requirements.txt`

3. Run like this: `python3 ./jar2blockset.py YOUR_MCJE_VER.jar`

4. By default, the script behaviour is:

    - $A:$ Filter out blocks with ANY transparency (plants, glass, doors, etc.),
    - $B:$ DON'T filter out animated assets (instead cropping them to just the first frame),
    - $C:$ Filter out blacklisted blocks according to blacklist file, and
    - $D:$ Create blockset JSON, generating blocks' properties data according to autoparser rules file.

    If you wish to change this behaviour, run the script like this: `python3 ./jar2blockset.py YOUR_MCJE_VER.jar A B C D`, where $A,B$ are corresponding options (`1` for True, `0` for False), and $C,D$ are pathes to blacklist file and autoparser rules (if nothing is provided, tries to load default config files `blacklist-default.yml` and `autoparse-default.yml`)


## Output

A directory containing all the filtered textures, and a file with a JSON object of data about blockset and data for each parsed non-filtered texture, structured like this:
```js
{
    "name": "My Blockset", // Blockset name, generated automatically
    "dir": "./res/my-blockset", // Directory where blockset textures stored, allowing
                                // multiple blocksets to use shared directory (files, not
                                // included in blockset JSON data, will simply be ignored).
    "count": 42, // How many textures are in the blockset
    "data": [
        {
            "name": "Cool Block Top", // Block texture name, generated automatically
            "texture": "cool_block_top.png", // Name of block texture with .png extension
            "color": [123, 45, 67], // Average color, computed by sum of squares
            "sides": ["top"] // List of block texture sides in OptiFine CTM faces notation,
                             // excluding "all" and "sides" options for simplicity.
        },
        ...
    ]
}
```
Note that automatically parsed data, especially for older versions, might not be 100% correct, so it is recommended to re-check the blockset before using it in production. You also should NOT rely on default blacklist and autoparse rules if you're changing default parameters or/and using a blockset containing non-vanilla blocks — rather, use them as an example on how these config files work.
