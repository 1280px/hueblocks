<script setup>
    import {ref, defineProps} from 'vue'
    import { useGlobalStore } from '@/stores/GlobalStore'

    const {colorCss, blockRef} = defineProps({
        colorCss: {
            type: String,
            required: true
        },
        blockRef: {
            type: [Object, null],
            required: true
        },
    })
    const GlobalStore = useGlobalStore()
</script>

<!-- As if in "tea bag tag" :) -->
<template>
    <button class="colorbar__color-segment">
        <div class="colorbar__color-segment__tag">
            <div
                class="colorbar__color-segment__tag-inner"
                :style="{
                    'background-image': `url(${GlobalStore.getTexturePath(blockRef?.texture)})`,
                    'background-color': blockRef ? 'revert-layer' : colorCss
                }"
                :title="blockRef ? `${blockRef?.name} \n${colorCss}` : colorCss"
            ></div>
        </div>
    </button>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .colorbar__color-segment {
        background-color: $white;
        // Prevent browsers from distoring width on
        // non-100% scale using the border trick:
        width: 0; height: 100%;
        margin: 0; padding: 0;
        border: 0 solid $white; border-width: 0 1px 0 1px;
    }

    .colorbar__color-segment__tag {
        position: relative;
        left: -10px; bottom: calc(-100% + 2px);
        width: 20px; height: 20px;
        background-color: $white;
        border-radius: 3px 3px 4px 4px;
        box-shadow: $SH_regular;

        &::before {
            content: '';
            display: block;
            position: relative;
            top: -6px; left: 3px;
            width: 14px; height: 14px;
            transform: rotate(45deg);
            background-color: $white;
            border-radius: calc($BR_regular / 2);
        }
    }

    .colorbar__color-segment__tag-inner {
        width: 16px; height: 16px;
        position: relative;
        top: calc(-100% + 8px); left: 2px;
        background-color: $accent-light_50;
        background-position: center;
        background-size: contain;
        transition: $TR_regular;

        .colorbar__color-segment__tag:hover & {
            opacity: .8;
        }

        .colorbar__color-segment__tag:active & {
            transition: $TR_fast;
            opacity: .7;
        }
    }
</style>
