<script setup lang="ts">
import { useId } from 'vue'

type SlottedInputType = 'email' | 'number' | 'password' | 'search' | 'tel' | 'text' | 'url' | 'week'

const { type = 'text', variant = 'default' } = defineProps<{
    type?: SlottedInputType,
    variant?: 'default' | 'black',
}>()

const value = defineModel<number | string>()

const id = useId()
</script>

<template>
    <label :for="id">
        <slot />
        <input
            :id="id" v-bind="$attrs" v-model="value"
            :class="{ black: variant === 'black' }"
            :type="type"
        >
    </label>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    input {
        appearance: none;
        flex: 1;
        height: 24px;
        margin-left: 5px; padding: 2px 4px;
        background-color: $dark_20; color: $white;
        border: 2px solid $accent-light_50; border-radius: $BR_big;
        transition: $TR_regular;
        outline: none;

        &:disabled {
            background-color: $dark_20; border-color: $white_20; color: $white_50;
        }

        &.black {
            background-color: $accent-dark_80; border-color: $accent-dark_25;

            &:disabled {
                background-color: $dark_em; border-color: $dark_60;
            }
        }

        &:not(:disabled) {
            &:hover {
                border-color: $accent-light;

                &.black {
                    border-color: $accent-dark_60;
                }
            }

            &:focus, &:active {
                box-shadow: inset 0 0 0 2px $white_50;
                background-color: $dark_60; border-color: $white_50;

                &.black {
                    background-color: $accent-dark; border-color: $white_50;
                }
            }
        }
    }

    label {
        @include flex-center;
        position: relative;
        user-select: none;
    }
</style>
