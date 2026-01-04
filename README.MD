> [!TIP]
> This version is still in development and, while is already very usable, it still might be not as stable and lacks a few features from previous version. If you wish to use legacy version of HueBlocks, [click here](https://1280px.github.io/hueblocks).

<p align=center>
  <a href="https://1280px.github.io/hueblocks-new/">
    <img src='readme-pic.png'><br>
  </a>
  <i>Create beautiful block gradients in a few clicks!</i>
</p>


<b>HueBlocks is an online Minecraft block gradients generator.</b>
<br>It's simple: pick colours or blocks you want, set amount of blocks between them, press the Big Black Button et voila!

Additionally, you can:
- Choose Minecraft Java Edition version which blocks you're interested in
- Use palettes to generate gradients using only specific sets of blocks, or even create your own palettes and share them with others via JSON import/export tool
- Filter textures by their facing (for example, if you're building a house wall, you're probably not that interested in blocks that only have a fitting texture on their top side)
- Switch between RGB and OkLAB colourspaces
- *and more!*
<!-- - Choose blocks noise threshold, allowing to filter out too "smooth" (like concrete) or, more commonly, too "noisy" blocks (crafting tables, glazed terracotta, TNT, you name it) -->
<!-- - Upload and use custom textures right from your browser, without any need to mess with backend -->

By default, HB comes with blocks from **latest stable MCJE** (1.21.11 as of Jan '26) and **MCJE 1.13.2** (last version to have Programmer's Art by default). *If you need some other version, you can either fork a repo and host an instance with your own blocksets (see below), or just DM me and I'll consider adding it here (as long as it is a vanilla Java Edition version available from Mojang Studios servers)*.

***Please note that not every single texture is included!*** All blocks with fully transparent pixels (i.e. flowers or trapdoors — but not semi-opaque blocks like stained glass), biome-/foliage-affected (such as grass and leaves), and overly-similar looking blocks were scrapped for the sake of better gradient appearance. *All of these paramaters, as well as palette presets, are fully configurable on backend side, so you can easily tweak it for your need on your instance.*


# Technical Details

HueBlocks consists of two parts — a Vue SPA web app (`vueblocks`) and a Python blocksets data generator (`jar2blockset`). Just like the legacy version, it has no actual back-end — all textures are downloaded, extracted and processed using Github Actions after every push, and then stored on their servers instead.

For each of these parts, there is a separate README with more details and documentation. So:
- If you want to create blocksets from your own textures or change generation configs (i.e. to include semi-transparent blocks, use custom palettes or edit textures blacklist) — [check this](https://github.com/1280px/hueblocks-new/tree/master/jar2blockset#readme),
- And if you want to mess with web app (it's very modular by design, so, if you know Vue 3, even something as creating a whole new separate mode shouldn't take much time) — [check that](https://github.com/1280px/hueblocks-new/tree/master/vueblocks#readme).

Additionally, if you're interested in color theory behind most of calculations, **I highly recommend  checking out Gneiss Name channel on YouTube**. His videos have greatly helped me refresh my memory on the basics, and also were great introductions to some topics I didn't understand before. 
<br>In particular, I recommend watching these episodes as sort of QnA:
- [What is OkLAB, and how is it different from (s)RGB?](https://www.youtube.com/watch?v=nJlZT5AE9zY)
  - [If you're very new to colourspaces, watch this first](https://www.youtube.com/watch?v=2kDuYv3ocxU)
- [What's the purpose of taking sqrt of squares for averaging block colour?](https://www.youtube.com/watch?v=e0HM_vfSuDw)
- [How exactly is block texture noise calculated?](https://www.youtube.com/watch?v=4meYZQZFuaA)
  - [Another technique of getting "denoised" texture averages](https://www.youtube.com/watch?v=HuW9qJbL0xM)

You can also check the j2bs source code for additional sources, commented right next to the code itself.


# Legal Notice

All the textures data provided by the Github Pages version are live extracted and processed from client JAR files live downloaded from Mojang's [Piston Meta servers API](https://gist.github.com/skyrising/95a8e6a7287634e097ecafa2f21c240f) using HTTP calls, and NOT provided in the repository itself. All rights on both the JAR files and the textures belong to Mojang Studios, and used for demonstration purposes only!
