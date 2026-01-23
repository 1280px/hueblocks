<script setup lang="ts">
import { useId } from 'vue'

import Icon from '@/components/Icon.vue'

const value = defineModel<boolean>({ default: false })

const id = useId()
</script>

<template>
    <label :for="id">
        <input :id="id" v-model="value" type="checkbox">
        <Icon name="check" class="checkbox-check" :class="{ active: value }" />
        <slot />
    </label>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    input {
        appearance: none;
        width: 20px; height: 20px;
        margin-right: 5px;
        color: $accent-dark;
        border: 2px solid $white_80; border-radius: $BR_regular;
        box-shadow: inset 0 0 0 0px $white;
        transition: $TR_regular;

        &:hover {
            background-color: $white_30; border-color: $white_80;
        }

        &:focus-visible, &:hover:active {
            outline: none;
            background-color: $white_50; border-color: $white;
            box-shadow: inset 0 0 0 2px $white;
            // transition: $TR_fast;
        }

        &:checked {
            background-color: $white_80; border-color: $trans;

            &:hover {
                background-color: $white;
            }

            &:focus-visible, &:hover:active {
                outline: none;
                background-color: $white_80; border-color: $accent-dark_50;
                box-shadow: inset 0 0 0 2px $accent-dark_50;
            }
        }
    }

    .checkbox-check {
        position: absolute;
        left: 2px;
        color: $trans;
        transition: $TR_regular;
        opacity: .8;

        &.active {
            color: $accent-dark;
        }
    }

    label {
        @include flex-center;
        position: relative;
        font-weight: $FW_bold;
        user-select: none;
    }
</style>
