<script setup>
    import SlottedMsgbox from '@/components/SlottedMsgbox.vue'
    // import ModeSwitcher from './ModeSwitcher.vue'
</script>

<template>
    <header>
        <h1>HueBlocks<sup><sub><sup>NEW</sup></sub></sup></h1>
        <h3>Create beautiful block gradients in a few clicks!</h3>

        <small>
            <!-- <a href="" @click="">language: en</a> •  -->
            <a href="https://github.com/1280px/hueblocks-new/">source code</a> • 
            <a href="https://github.com/1280px/hueblocks-new/graphs/contributors/">contributors</a> • 
            <a href="https://1280px.github.io/hueblocks">legacy version</a>
        </small>

        <SlottedMsgbox :duration="5">
            This is a new version of HueBlocks, still work in progress and missing some OG features! <br>
            If you wish to go to an older version of HB, click "legacy version" link above this message.
        </SlottedMsgbox>

        <!-- <ModeSwitcher /> -->
    </header>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    header {
        display: flex; flex-direction: column;
        text-align: center;
        margin: 80px 0 40px;
        gap: 12px;
    }

    box {
        margin-top: 12px;
        border-color: moccasin;
    }
</style>
