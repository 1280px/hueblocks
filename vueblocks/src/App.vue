<script setup>
    import {ref, onMounted, defineAsyncComponent} from 'vue'
    import { useGlobalStore } from '@/stores/GlobalStore'

    import Header from './views/Header/index.vue'

    const SimpleView = defineAsyncComponent({
        loader: () => import('./views/SimpleView/index.vue'),
        loadingComponent: () => 'Loading SimpleView…', delay: 0, suspensible: false
    })

    const GlobalStore = useGlobalStore()

    onMounted(async () => {
        await GlobalStore.loadBlocksetsData()
        await GlobalStore.loadBlocksetBlockdata()
        await GlobalStore.loadBlocksetPalettes()
    })
</script>

<template>
    <Header />

    <SimpleView v-if="GlobalStore.viewMode === 'simple'" />

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
        text-align: center;
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
    // abbr {
    //     text-decoration: underline dotted 1px;
    // }
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
