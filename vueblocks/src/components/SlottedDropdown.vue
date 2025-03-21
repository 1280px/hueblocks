<script setup>
    import {ref, defineModel, defineProps, useId} from 'vue'

    const props = defineProps({
        names: {
            type: Array,
            required: true
        },
        default: {
            type: Number,
            required: false
        }
    })

    const value = defineModel()
    value.value = (props?.default || 0)
    // TODO: reset value to .default if out of bounds (use computed?)

    const id = useId()
</script>

<template>
    <label :for="id">
        <slot></slot>
        <select v-model="value" :id="id" :disabled="names.length < 2">
            <option v-for="(name, i) in names" :key="i" :value="i">{{ name }}</option>
        </select>
        <div class="select__arrow">
            <icon>🔻</icon>
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

        &:not(:disabled) {
            &:hover {
                border-color: $accent-light;
            }
            &:focus, :active {
                padding: 0 6px 1px 6px;
                background-color: $dark_60;
                border: 4px solid $accent-light_50;
                transition: $TR_fast;
            }
        }

        &:disabled {
            border-color: $white_20;
            background-color: $dark_20; color: $white_50;
        }
    }

    .select__arrow {
        @include flex-center;
        margin-left: -44px; padding-left: 20px;
        width: 20px; height: 20px;
        background: linear-gradient(90deg, $trans, $dark_bg 50%);
        border-radius: 0 $BR_round $BR_round 0;
        pointer-events: none;
    }

    label {
        @include flex-center;
        font-weight: $FW_bold;
        user-select: none;
        cursor: unset;
    }
</style>
