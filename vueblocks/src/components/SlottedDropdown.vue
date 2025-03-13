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
    </label>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    select { 
        margin-left: 5px;
    }

    label {
        @include flex-center;
        // margin: 0 8px 8px;
        font-weight: 700;
        user-select: none;
    }
</style>
