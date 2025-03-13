<script setup>
    import {ref, onMounted} from 'vue'
    import { useGlobalStore } from './stores/GlobalStore'

    import Header from './views/Header/index.vue'
    import SimpleView from './views/SimpleView/index.vue'

    const GlobalStore = useGlobalStore()

    onMounted(async () => {
        await GlobalStore.loadBlocksetsData()
        await GlobalStore.loadBlocksetBlockdata()
        await GlobalStore.loadBlocksetPalettes()
    })
</script>

<template>
    <Header />

    <SimpleView />
    <!-- <AdvancedView v-if="viewMode==='advanced'" />
    <SimpleView v-else /> -->

    <footer></footer>
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
    }
    #app {
        background: linear-gradient(#000628 20px, #282b58 420px);
        background: linear-gradient(#080018, #704070 420px);
        background: linear-gradient(#100418, #9c4848 400px);
        color: $white;
        font-size: 16px; font-family: $FONTS;
    }

    h1 {
        margin: 0;
        font-size: 3.0em;
        font-weight: 700;
    }
    h2 {
        margin: 0;
        font-size: 1.6em;
        font-weight: 300;
    }
    h3 {
        margin: 0;
        font-size: 1.2em;
        font-weight: 300;
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
    icon {
        background: $trans;
        margin: 0;
    }

    button, input[type=checkbox], input[type=radio], label, a, select, option {
        cursor: pointer;

        & :disabled {
            cursor: not-allowed;
        }
    }

    // TODO: Move popover styling to separate file
    .popover {
        margin-top: 12px; padding: 8px;
        background-color: $white; color: $black;
        border-radius: $BR_regular;
        box-shadow: $SH_smooth, $SH_subtle;
        font-size: 1em; font-family: $FONTS;
        animation: $TR_slow popover-pop;
    }
    .popover-inner {
        @include flex-center;
    }
    .popover-arrow {
        z-index: -1;
        top: -12px;
        width: 24px; height: 24px;
        margin-left: -0.5px;
        transform: rotate(45deg);
        background-color: $white;
        border-radius: calc($BR_regular / 2);
    }
    @keyframes popover-pop {
        0% {
            transform: translateY(8px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }
</style>
