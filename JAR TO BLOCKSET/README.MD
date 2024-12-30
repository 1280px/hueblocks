# jar2blockset

A simple Python script to extract assets from MCJE .jar file and then generate blockset description for them. Successor to blox2rgb.py from legacy HueBlocks versions.

**Only MCJE 1.5+ versions are supproted, and I have no plans to add other editions support!**

**If you wish to use Programmer's Art textures, please swtich the version down to 1.13.2, as this is the last version they were used and updated (except for glowing obsidian texture).**

### Usage

1. Go to wherever your MCJE launcher stores versions (default is `~/.minecraft/version`) and grab a .jar of version you're interested in

2. Make sure you have Python and required modules installed: `pip3 install -r requirements.txt`

3. Run like this: `python3 ./jar2blockset.py YOUR_MCJE_VER.jar`

4. By default, the script behaviour is:

    - $A:$ Filter out blocks with ANY transparency (plants, glass, doors, etc.),
    - $B:$ DON'T filter out animated assets (instead cropping them to just the first frame),
    - $C:$ Filter out blocks from blacklist, if needed (see `blacklist-default.cfg`), and
    - $D:$ Automatically determines blocks' sides and display names from their file names.

    If you wish to change this behaviour, run the script like this: `python3 ./jar2blockset.py YOUR_MCJE_VER.jar A B C D`, where $A,B$ are corresponding options (1 for True, 0 for False), and the last argument is the blacklist file path (if nothing is provided, `blacklist-default.cfg` will be used; to disable, pass `None` as argument).

### Output

A directory containing all the filtered textures, and a .json file with a list of data for each texture, structured like this:
```js
{
    'texture': 'cool_block_top.png', // Name of block texture with .png extension
    'name': 'Cool Block Top' // Block texture name, generated automatically
    'color': (123, 45, 67),  // Average color, computed by sum of squares
    'side': ['up'] // List of block texture sides, in OptiFine's CTM faces notation
}
```

Note that automatically parsed data, especially for older versions, might not be 100% correct, so it is recommended to re-check the blockset before using it in production.
