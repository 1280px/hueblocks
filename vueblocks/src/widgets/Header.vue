<script setup lang="ts">
import Cookies from 'js-cookie'

import { ref } from 'vue'
import SlottedMsgbox from '@/components/SlottedMsgbox.vue'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const SimpleViewStore = useSimpleViewStore()

function toggleDebugMode() {
    SimpleViewStore.blockDisplayCfg.showColorsDebug
        = !SimpleViewStore.blockDisplayCfg.showColorsDebug

    if (SimpleViewStore.blockDisplayCfg.showColorsDebug) {
        // eslint-disable-next-line no-alert
        alert('Colour debug toggled, re-generate a gradient to see effect.')
    }
}

const welcomeIsShown = ref<boolean>(!Cookies.get('nowelcome'))

function welcomeHide() {
    Cookies.set('nowelcome', 'true')
    welcomeIsShown.value = false
}
</script>

<template>
    <header>
        <h1 @dblclick.prevent="toggleDebugMode">
            HueBlocks<sup><sub><sup>NEW</sup></sub></sup>
        </h1>

        <h3>Create beautiful block gradients in a few clicks!</h3>

        <small>
            <!-- <a href="" @click="">language: en</a> •  -->
            <a href="https://github.com/1280px/hueblocks/">source code</a> •
            <a href="https://github.com/1280px/hueblocks/graphs/contributors/">contributors</a> •
            <a href="https://1280px.github.io/hueblocks-legacy">legacy version</a>
        </small>

        <SlottedMsgbox v-if="welcomeIsShown" :timeout="15">
            <h3>Welcome to the new version of Hueblocks 🎉</h3>
            <span>
                Starting January 15th, HueBlocks New is now an upstream version.<br>
                <a href="https://github.com/1280px/hueblocks#list-of-changes">
                    Click here to read the full list of changes and additions</a>, or
                <a href="#" @click.prevent="welcomeHide">
                    here</a>
                to never show this box again.
            </span>
            <span>
                If you wish to continue using legacy version anyway,
                use the "legacy version" link above.
            </span>
        </SlottedMsgbox>
    </header>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    header {
        display: flex; flex-direction: column;
        text-align: center;
        margin: 80px 0 38px; // Account 2px used by links underline
        gap: 12px;
    }
</style>
