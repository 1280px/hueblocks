<script setup>
    import {ref, defineModel, defineProps, useId} from 'vue'

    const value = defineModel()
    value.value = !value.value ? 'all' : value.value

    const id = useId()

    const facing = [
        // According to Optifine CTM, first two options should be the last;
        // however, chances are, they will actually be used the most :)
        { all: 'Any' },
        { sides: 'Sides' },
        { top: 'Top' },
        { bottom: 'Bottom' },
        { north: 'North' },
        { south: 'South' },
        { east: 'East' },
        { west: 'West' }
    ]
</script>

<template>
    <label :for="id">
        Side:
        <div class="side-picker__wrap">
            <div class="side-picker__image">
                <icon>{{ value }}</icon>
                <!-- <icon>🔻</icon> -->
            </div>
            <select class="side-picker__btn" v-model="value" :id="id">
                <option v-for="(face, i) in facing" :key="i"
                    :value="Object.keys(face)[0]"
                >{{ Object.values(face)[0] }}</option>
            </select>
        </div>
    </label>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .side-picker__wrap {
        position: relative;
    }
    
    .side-picker__btn {
        appearance: none;
        width: 40px; height: 40px;
        margin-left: 5px;
        background-color: $dark_20; color: $white; // We need to provide this to be used for DD menu background
        text-indent: -100%; // Remove selected text option from DD itself without affecting DD menu styles
        border: 2px solid $accent-light_50; border-radius: $BR_round;
        transition: $TR_regular;

        width: 64px; // TODO: Remove this temporary override after implementing actual icons

        &:hover {
        	border-color: $accent-light;
        }

        &:focus, :active {
            border: 4px solid $accent-light_50;
            background-color: $dark_60;
            transition: $TR_fast;
        }
    }

    .side-picker__image {
        @include flex-center;
        position: absolute;
        pointer-events: none;
        top: 0; left: 0;
        width: calc(100% - 5px); height: 100%;
        // background-color: #f008;
        margin-left: 5px;
        border-radius: $BR_round;
    }

    label {
        @include flex-center;
        font-weight: $FW_bold;
        user-select: none;
        cursor: unset;
    }
</style>
