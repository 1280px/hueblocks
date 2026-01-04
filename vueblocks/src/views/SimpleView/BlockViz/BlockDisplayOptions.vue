<script setup lang="ts">
import SlottedCheckbox from '@/components/SlottedCheckbox.vue'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const SimpleViewStore = useSimpleViewStore()
</script>

<template>
    <section class="blockviz-options">
        <small>
            left click on a colour tag to change it, right click to copy its hex;<br>
            click or scroll a label between tags to change length between them.
        </small>

        <SlottedCheckbox v-model="SimpleViewStore.blockDisplayCfg.hideDuplicates">
            Hide duplicates
        </SlottedCheckbox>

        <SlottedCheckbox v-model="SimpleViewStore.blockDisplayCfg.resultsInOneRow">
            Results in one row
        </SlottedCheckbox>

        <SlottedCheckbox v-model="SimpleViewStore.blockDisplayCfg.keepPrevResults">
            Keep previous results
        </SlottedCheckbox>

        <SlottedCheckbox v-model="SimpleViewStore.blockFilteringCfg.useOkLAB">
            <abbr
                title="Use colourspace closer to how human eyes perceive colour. Results in more vibrant and natural looking, but often less saturated (&quot;washed-out&quot;) and contrast gradients."
            >
                Use&nbsp;OkLAB
            </abbr>
        </SlottedCheckbox>
    </section>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .blockviz-options {
        @include flex-center;
        flex-wrap: wrap;
        gap: 8px 16px;
        margin: 4px auto 24px; padding: 0 12px;

        & small {
            width: 100%;
            margin-bottom: 12px;
            text-align: center;
        }
    }
</style>
