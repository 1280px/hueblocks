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
    </section>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .blockviz-options {
        @include flex-center;
        margin: 4px auto 24px;
        flex-wrap: wrap;
        gap: 0 16px;

        & small {
            width: 100%;
            text-align: center;
            margin-bottom: 20px;
        }
    }
</style>
