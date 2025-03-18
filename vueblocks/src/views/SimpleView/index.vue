<script setup>
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'

    import SlottedCheckbox from '@/components/SlottedCheckbox.vue'
    import Colorbar from './Colorbar/index.vue'
    import BlockViz from './BlockViz/index.vue'

    const SimpleViewStore = useSimpleViewStore()
</script>

<template>
    <header>
        <section class="colorbar__wrap">
            <Colorbar />
        </section>

        <section class="blockviz-options--viz">
            <small>
                left click on a color tag to change it, right click to copy its hex;<br>
                click on a number between color tags to change length between them.
            </small>
            
            <SlottedCheckbox v-model="SimpleViewStore.blockVizCfg.hideDuplicates">
                Hide duplicates
            </SlottedCheckbox>
    
            <SlottedCheckbox v-model="SimpleViewStore.blockVizCfg.resultsInOneRow">
                Results in one row
            </SlottedCheckbox>
    
            <SlottedCheckbox v-model="SimpleViewStore.blockVizCfg.keepPrevResults">
                Keep previous results
            </SlottedCheckbox>
        </section>
    </header>

    <footer>
        <section class="blockviz__wrap">
            <BlockViz />
        </section>
    </footer>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    header {
        @include responsive-width;
        display: flex; flex-direction: column;
        margin: 0 auto;
    }
    footer {
        flex: 1;
        display: flex; flex-direction: column;
    }
    
    .colorbar__wrap {
        @include flex-center;
        align-items: baseline;
        gap: 4px;
    }

    .blockviz-options--viz {
        @include flex-center;
        margin: 4px auto 20px;
        flex-wrap: wrap;
        gap: 0 16px;

        & small {
            width: 100%;
            text-align: center;
            margin-bottom: 20px;
        }
    }

    .blockviz__wrap {
        flex: 1;
        display: flex; flex-direction: column;
    }
</style>
