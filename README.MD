> [!TIP]
> This version is still in development and, while is already very usable, it still might be not as stable and lacks a few features from previous version. If you wish to use legacy version of HueBlocks, [click here](https://1280px.github.io/hueblocks).

<p align=center>
  <a href="https://1280px.github.io/hueblocks-new/">
    <img src='readme-pic.png'><br>
  </a>
  <i>Create beautiful block gradients in a few clicks!</i>
</p>


<b>HueBlocks is an online Minecraft block gradients generator.</b>
<br>It's simple to use: pick colours or blocks you want, set amount of blocks between them, press the Big Black Button and voila!

Additionally, you can:
- Choose Minecraft Java Edition version which blocks you're interested in
- Select a palette to generate gradients using only specific set of blocks, or even create your own palettes and share them with others using palette JSON import/export tool
- Filter textures by applicable block size (for example, if you're building a house wall, you're probably not really interested in blocks that only have fitting textures on their top side)
<!-- - Upload and use custom textures right from your browser, without any need to mess with backend! -->
- Switch between RGB and CIELAB colourspaces
<!-- - Choose blocks noise threshold, allowing to filter too "smooth" (like concrete) or, more commonly, too "noisy" blocks (crafting tables, glazed terracotta, TNT, you name it) -->
- *and more!*

By default, HB comes with block from **latest stable MCJE** (1.21.11 as of Jan '26) and **MCJE 1.13.2** (last version to have Programmer's Art by default). If you need some other version, you can either fork a repo and host an instance with your own blocksets (see below), or just DM me and I consider adding it here *(as long as it is vanilla Java Edition version availabe from Mojang Studios servers)*.

***Please note that not every single texture is included!*** All blocks with fully transparent pixels (i.e. flowers or trapdoors — but not semi-opaque blocks like stained glass), biome-/foliage-affected (such as grass and leaves), and overly-similar looking blocks were scrapped for the sake of better gradient appearance. All of these paramaters, as well as palette presets, are fully configurable on backend side, so you can easily tweak it for your need on your instance.


# Technical Details

HueBlocks consists of two parts — a Vue SPA web app (`vueblocks`) and a Python blocksets data generator (`jar2blockset`). Just like the legacy version, it has no actual back-end — all textures are downloaded, extracted and processed using Github Actions after every push, and then stored on their servers instead.

For each of these parts, there is a separate README with more details and documentation. So:
- If you want to create blocksets from your own textures or change generation configs (i.e. to include semi-transparent blocks, use custom palettes or edit textures blacklist) — [check this](https://github.com/1280px/hueblocks-new/tree/master/jar2blockset#readme),
- And if you want to mess with web app (it's very modular by design, so, if you know Vue 3, even something as creating a whole new separate mode shouldn't take much time) — [check that](https://github.com/1280px/hueblocks-new/tree/master/vueblocks#readme).


# Legal Notice

All the textures data provided by the Github Pages version are live extracted and processed from client JAR files live downloaded from Mojang's [Piston Meta servers API](https://gist.github.com/skyrising/95a8e6a7287634e097ecafa2f21c240f) using HTTP calls, and NOT provided in the repository itself. All rights on both the JAR files and the textures belong to Mojang Studios, and used for demonstration purposes only!
