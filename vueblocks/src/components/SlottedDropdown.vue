<script setup lang="ts">
import { computed, useId } from 'vue'

import Icon from '@/components/Icon.vue'

const { names, variant = 'default' } = defineProps<{
    names: string[],
    variant?: 'default' | 'black',
}>()

const value = defineModel<number>({ default: 0 })

const ibValue = computed<number>({
    get: () => value.value >= names.length ? names.length - 1 : value.value < 0 ? 0 : value.value,
    set: (i: number) => value.value = (i >= names.length ? names.length - 1 : i < 0 ? 0 : i),
})

const id = useId()
</script>

<template>
    <label :for="id">
        <slot />
        <select
            :id="id" v-model="ibValue"
            :disabled="names?.length < 2"
            :class="{ black: variant === 'black' }"
        >
            <component
                :is="name !== '<hr>' ? 'option' : 'hr'"
                v-for="(name, i) in names" :key="i" :value="i"
            >
                {{ name }}
            </component>
        </select>
        <div
            class="select__arrow"
            :class="{ inactive: names.length < 2, black: variant === 'black' }"
        >
            <Icon name="dd-arrow" />
        </div>
    </label>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    select {
        appearance: none;
        width: 200px; height: 28px;
        margin-left: 5px; padding: 0 8px 1px 8px;
        background-color: $dark_20; color: $white;
        border: 2px solid $accent-light_50; border-radius: $BR_round;
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
                padding: 0 6px 1px 6px;
                background-color: $dark_60;
                border: 4px solid $accent-light_50;
                transition: $TR_fast;

                &.black {
                    background-color: $accent-dark; border-color: $accent-light_50;
                }
            }
        }
    }

    .select__arrow {
        @include flex-center;
        margin-left: -44px; padding-left: 20px;
        width: 20px; height: 20px;
        background: linear-gradient(90deg, $trans, $dark_bg 50%); color: $white_80;
        border-radius: 0 $BR_round $BR_round 0;
        pointer-events: none;

        &.black {
            background: transparent;
        }

        &.inactive {
            color: $white_50 !important;
        }
    }

    label {
        @include flex-center;
        font-weight: $FW_bold;
        user-select: none;
        cursor: unset;
    }
</style>
