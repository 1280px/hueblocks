<script setup>
import { defineAsyncComponent, onMounted, ref, watch } from 'vue'

import { overlayBind, overlayIsShown } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { getCssRgb, getRandomRbg } from './colors'
import Header from './widgets/Header.vue'
import Overlay from './widgets/Overlay/index.vue'

const SimpleView = defineAsyncComponent({
    loader: () => import('./views/SimpleView/index.vue'),
    loadingComponent: () => 'Loading SimpleView…',
    delay: 0,
    suspensible: false,
})

const GlobalStore = useGlobalStore()

const overlayRef = ref() // We use this ref to bind overlay component

watch(overlayIsShown, (v) => {
    (v === true) ? document.body.classList.add('clip') : document.body.classList.remove('clip')
})

onMounted(async () => {
    document.querySelector('#app').style.background = (
        `linear-gradient(
        ${150 + Math.random() * 60}deg in oklab,
        ${getCssRgb(getRandomRbg(0.80))},
        ${getCssRgb(getRandomRbg(3.86))}
        )`
    )

    await GlobalStore.loadBlocksetsData()
    await GlobalStore.loadBlocksetBlockdata()
    await GlobalStore.loadBlocksetPalettes()

    await overlayBind(overlayRef.value)
})
</script>

<template>
    <Header />

    <SimpleView v-if="GlobalStore.viewMode === 'simple'" />

    <Overlay ref="overlayRef" />
</template>

<style lang="scss">
    @use '@/assets/variables' as *;

    html {
        display: flex;
        min-width: 100%; min-height: 100%;
        color-scheme: dark;
    }
    body, #app {
        flex: 1;
        display: flex; flex-direction: column;
        width: 100%; min-height: 100%;
        text-align: center;

        &.clip {
            overflow: hidden;
        }
    }
    #app {
        position: relative;
        // background: linear-gradient(#000628 20px, #282b58 420px);
        // background: linear-gradient(#080018 20px, #2d1e80 420px);
        // background: linear-gradient(#001b1d 20px, #099862 420px);
        color: $white;
        font-size: 16px; font-family: $FONTS;
    }

    h1 {
        margin: 0 !important;
        font-size: 3.0em !important;
        font-weight: $FW_bold;
    }
    h2 {
        margin: 0;
        font-size: 1.6em;
        font-weight: $FW_thin;
    }
    h3 {
        margin: 0;
        font-size: 1.2em;
        font-weight: $FW_thin;
    }
    a {
        color: inherit;
        transition: color $TR_regular;
    }
    a:hover {
        color: $white_80;
    }
    small {
        color: $white_30;
        font-size: .86em;
    }

    button, input[type=checkbox], input[type=radio], label, a, select, option {
        cursor: pointer;

        & :disabled {
            cursor: not-allowed;
        }
    }
</style>
