> [!IMPORTANT]
> This version is still in active development and, while it is already usable, it still might be not as stable and lacks some features from the previous version. If you wish to use legacy version of HueBlocks, [click here](https://1280px.github.io/hueblocks).

<p align=center>
  <a href="https://1280px.github.io/hueblocks-new/">
    <img src='readme-pic.png'><br>
  </a>
  <i>Create beautiful block gradients in a few clicks!</i>
</p>


<b>HueBlocks is an online Minecraft block gradients generator.</b>
<br>It's simple to use: you set colors (or blocks!) you want, amount of blocks between them, press the Big Black Button and voila!

Additionally, you can:
- Choose Minecraft Java Edition version which blocks you want to use;
- Select a palette if you want to generate a gradient using only specific set of blocks;
- Choose side of blocks to use (i.e. if you're building a house wall, you probably don't need top-only textures);
- ***[ᴡɪᴘ]*** Choose blocks noise threshold (i.e. if you need very smooth or very noisy-looking gradients);
- Switch between RGB and CIELAB colorspaces;
- *and more!*

By default, HB comes with **Minecraft Java Edition 1.21.5 and 1.13.2** blocks.
<br>***Please note that not every single texture is included!***
All non-opaque (like flowers or stained glass), biome-affected/foliage-affected (i.e. grass blocks), and overly-similar looking blocks were scrapped for the sake of better gradient generation quality.


# Technical Details

HueBlocks consists of two parts — a Vue SPA web app (`vueblocks`) and a Python blocksets data generator (`jar2blockset`).
Just like the legacy version, it has no actual back-end — all textures are downloaded, extracted and processed using Github Actions after every push, and then stored on their servers instead.

For each of these parts, there is a separate README with more details and documentation. So:
- If you want to create blocksets from your own textures or change generation configs (i.e. to include semi-transparent blocks, use custom palettes or edit textures blacklist) — [check this](https://github.com/1280px/hueblocks-new/tree/master/jar2blockset#readme),
- And if you want to mess with web app (it's very modular by design, so, if you know Vue 3, even something as creating a whole new separate mode shouldn't take much time) — [check that](https://github.com/1280px/hueblocks-new/tree/master/vueblocks#readme).


# Legal Notice

All the textures data provided by the Github Pages version are live extracted and processed from client JAR files 
live downloaded from Mojang's [Piston Meta servers API](https://gist.github.com/skyrising/95a8e6a7287634e097ecafa2f21c240f) using HTTP calls, and NOT provided in the repository itself. 
All rights on both the JAR files and the textures belong to Mojang Studios, and are used for demonstration purposes only!
