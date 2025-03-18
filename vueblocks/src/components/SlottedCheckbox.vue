<script setup>
    import {ref, defineModel, useId} from 'vue'

    const value = defineModel()
    const id = useId()
</script>

<template>
    <label :for="id">
    <input type="checkbox" v-model="value" :id="id">
        <slot></slot>
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
            background-color: $white_30;
            border-color: $white_80;

            &:active {
                background-color: $white_50;
                border-color: $white;
                box-shadow: inset 0 0 0 2px $white;
                // transition: $TR_fast;
            }
        }

        &:checked {
            background-color: $white_80;
            border-color: $trans;

            &:hover {
                background-color: $white;

                &:active {
                    background-color: $white_80;
                    border-color: $accent-dark_25;
                    box-shadow: inset 0 0 0 2px $accent-dark_25;
                }
            }
        }
    }

    label {
        @include flex-center;
        font-weight: 700;
        user-select: none;
    }
</style>
