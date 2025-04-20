<script setup>
    import {ref, defineModel, useId} from 'vue'

    import Icon from '@/components/Icon.vue'

    const currFace = defineModel()
    currFace.value = !currFace.value ? 'all' : currFace.value

    const id = useId()

    // According to Optifine CTM, first two options should be the last;
    // however, chances are, they will actually be used the most :)
    const facing = [
        'all', 'sides', 'top', 'bottom', 'north', 'west', 'south', 'east'
    ]
</script>

<template>
    <label :for="id">
        <div class="side-picker__wrap">
            <div class="side-picker__image">
                <!-- We're doing this so the icons won't blink when changed -->
                <template v-for="(face, i) in facing" :key="i">
                    <Icon :name="'facing-' + face"
                        v-show="currFace === face"
                    />
                </template>
                <Icon name="dd-arrow" />
            </div>
            <select class="side-picker__btn" v-model="currFace" :id="id"
                :title="`Filter by facing: ${currFace.charAt(0).toUpperCase() + currFace.slice(1)}`"
            >
                <option v-for="(face, i) in facing" :key="i"
                    :value="face"
                >{{ face.charAt(0).toUpperCase() + face.slice(1) }}</option>
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
        width: calc(40px*2 + 4px); height: 40px;
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
        // background-color: #f008; // For debugging
        border-radius: $BR_round;
    }

    label {
        @include flex-center;
        font-weight: $FW_bold;
        user-select: none;
        cursor: unset;
    }
</style>
