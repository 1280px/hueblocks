<script setup lang="ts">
import { defineModel, useId } from 'vue'

import Icon from '@/components/Icon.vue'

const { isCompact = false } = defineProps<{
    isCompact?: boolean,
}>()

const currFace = defineModel()
currFace.value = !currFace.value ? 'all' : currFace.value

const id = useId()

// According to Optifine CTM, first two options should be the last;
// however, chances are, they will actually be used the most :)
const facing = ['all', 'sides', 'top', 'bottom', 'north', 'west', 'south', 'east']
</script>

<template>
    <label :for="id" class="side-picker__wrap" :class="[isCompact ? 'compact' : '']">
        <div class="side-picker__image">
            <!-- We're doing this so the icons won't blink when changed -->
            <template v-for="(face, i) in facing" :key="i">
                <Icon
                    v-show="currFace === face"
                    :name="`facing-${face}`"
                />
            </template>
            <Icon v-if="!isCompact" name="dd-arrow" />
        </div>
        <select
            :id="id" v-model="currFace" class="side-picker__btn"
            :title="`Filter by facing: ${currFace.charAt(0).toUpperCase() + currFace.slice(1)}`"
        >
            <option
                v-for="(face, i) in facing" :key="i"
                :value="face"
            >{{ face.charAt(0).toUpperCase() + face.slice(1) }}</option>
        </select>
    </label>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .side-picker__wrap {
        position: relative;
        border-radius: $BR_round;

        &.compact {
            width: 40px;
        }
    }

    .side-picker__btn {
        width: 100%; height: 100%;
        appearance: none;
        background-color: $dark_20; color: $white; // We need to provide this to be used for DD menu background
        text-indent: -100%; // Remove selected text option from DD itself without affecting DD menu styles
        border: 2px solid $accent-light_50; border-radius: $BR_round;
        transition: $TR_regular;

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
        width: calc(100% - 4px); height: 100%;
        padding-left: 4px; gap: 4px;
        border-radius: $BR_round;

        .compact & {
            padding-left: 2px;
        }
    }

    label {
        @include flex-center;
        font-weight: $FW_bold;
        user-select: none;
        cursor: unset;
    }
</style>
