<script setup>
    import {ref, defineModel, useId} from 'vue'

    const value = defineModel()
    const id = useId()
</script>

<template>
        <input type="checkbox" v-model="value" :id="id">

        <label class="tumbler__wrap" :for="id">
            <span class="tumbler__text" :class="{ 'active': value }">
                <slot name="left"></slot>
            </span>

            <label :for="id" class="tumbler" :class="{ 'active': value }">
                <!-- "tumblers are essentially just a little fancier checkboxes" -- Me, 2020. -->
            </label>

            <span class="tumbler__text" :class="{ 'active': !value }">
                <slot name="right"></slot>
            </span>
        </label>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .tumbler__wrap {
        @include flex-center;
    }

    input {
        display: none;
    }

    .tumbler__text {
        color: $white;
        font-weight: $FW_bold;
        transition: $TR_regular;

        &.active {
	        color: $white_50;
        }
    }    

    .tumbler {
        display: inline-block;
        position: relative;
        width: 48px; height: 2px;
        background: $white_30;
        margin: 0 12px -4px;

        &::before {
            content: '';
            position: absolute;
            left: 2px; top: -6px;
            width: 10px; height: 10px;
            background-color: $white;
            border: 2px solid $dark_border; border-radius: $BR_round;
            box-shadow: 0px 0px 0px 2px $white_50;
            transition: $TR_slow cubic-bezier(.77, 0, .18, 1);
        }

        .tumbler__wrap:hover & {
            &::before {
                background-color: $white;
                border-color: $accent-light;
                box-shadow: 0px 0px 0px 2px $white;
            }
        }

        .tumbler__wrap:hover:active & {
            &::before {
                background-color: $white_80;
                border-color: $white;
                box-shadow: 0px 0px 0px 2px $accent-light_50;
            }
        }

        &.active {
            &::before {
                transform: translateX(32px);
            }
        }
    }
</style>
