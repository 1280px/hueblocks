<script setup>
import { defineProps } from 'vue'

import Icon from '@/components/Icon.vue'

const { side } = defineProps({
    side: {
        type: String,
        required: true,
    },
})
</script>

<template>
    <button class="colorbar__add-btn" :class="side">
        <Icon name="zoom-in" />
    </button>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    button {
        appearance: none;
        width: 40px;
        border: none;

        &.left {
            border-radius: $BR_big 0 0 $BR_big;
            border-right-color: $trans !important;
        }
        &.right {
            border-radius: 0 $BR_big $BR_big 0;
            border-left-color: $trans !important;
        }

        & > * {
            opacity: 1;
            transition: opacity $TR_regular;
        }

        background-color: $white_20;
        border: 0 solid $trans;
        box-shadow: $SH_smooth;
        transition: $TR_regular;

        &:not(:disabled):hover {
            background-color: $white_30;

            &:active {
                background-color: $white_50;
                border: 2px solid $white_30;
                transition: $TR_fast;
            }
        }

        &:disabled {
            width: 20px;
            background-color: $white_20;
            cursor: not-allowed;

            &.left {
                margin-left: 20px;
            }
            &.right {
                margin-right: 20px;
            }

            & > * {
                opacity: 0;
            }
        }
    }
</style>
