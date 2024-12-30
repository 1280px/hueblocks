# jar2blockset

A simple Python script to extract assets from MCJE .jar file, filter only needed block textures, and then generate blockset description for them. Successor of blox2rgb.py from legacy HueBlocks versions.

**Only MCJE 1.5+ versions are supproted, and I have no plans to add other editions support!**


## Usage

1. Go to wherever your MCJE launcher stores versions (default is `~/.minecraft/versions`) and grab a .jar of version you're interested in

2. Make sure you have Python and required modules installed: `pip3 install -r requirements.txt`

3. Run like this: `python3 ./jar2blockset.py YOUR_MCJE_VER.jar`

4. By default, the script behaviour is:

    - $A:$ Filter out blocks with ANY transparency (plants, glass, doors, etc.),
    - $B:$ DON'T filter out animated assets (instead cropping them to just the first frame),
    - $C:$ Filter out blacklisted blocks according to blacklist file, and
    - $D:$ Autogenerate texture names and facing according to autoparser rules file.

    If you wish to change this behaviour, run the script like this: `python3 ./jar2blockset.py YOUR_MCJE_VER.jar A B C BLACKLIST.txt`, where $A,B$ are corresponding options (1 for True, 0 for False), and $C,D$ are pathes to blacklist file and autoparser rules (uses `blacklist-default.cfg` and `autoparser-rules.cfg` if nothing is provided; to disable, pass `None` as arguments)


## Output

A directory containing all the filtered textures, and a .json file with a list of data for each texture, structured like this:
```js
{
    'texture': 'cool_block_top.png', // Name of block texture with .png extension
    'name': 'Cool Block Top' // Block texture name, generated automatically
    'color': (123, 45, 67),  // Average color, computed by sum of squares
    'side': ['up'] // List of block texture sides in OptiFine's CTM facing notation
}
```

Note that automatically parsed data, especially for older versions, might not be 100% correct, so it is recommended to re-check the blockset before using it in production.
