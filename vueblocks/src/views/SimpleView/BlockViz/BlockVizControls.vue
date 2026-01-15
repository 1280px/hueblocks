<script setup lang="ts">
import Icon from '@/components/Icon.vue'
import SidePicker from '@/components/SidePicker.vue'
import SlottedButton from '@/components/SlottedButton.vue'
import { useGlobalStore } from '@/stores/GlobalStore'

const emit = defineEmits<{
    bbbClick: [],
}>()

const GlobalStore = useGlobalStore()
</script>

<template>
    <section class="blockviz-controls__wrap">
        <div class="blockviz-controls">
            <div class="blockviz-controls__blob round">
                <SidePicker v-model="GlobalStore.blockFacing" />
            </div>

            <div class="blockviz-controls__blob">
                <SlottedButton
                    id="big-black-button"
                    :disabled="!GlobalStore.currBlocksetBlockdata"
                    @click="() => emit('bbbClick')"
                >
                    {{
                        GlobalStore.currBlocksetBlockdata
                            ? 'GENERATE BLOCK GRAIDENT'
                            : 'Loading blockdata, please wait…'
                    }}
                </SlottedButton>
            </div>

            <div class="blockviz-controls__blob round">
                <SlottedButton
                    round
                    title="Zoom out (0.5x)"
                    :disabled="Number.parseInt(GlobalStore.blockSize) <= 16"
                    @click="GlobalStore.changeBlockSize(0.5)"
                >
                    <Icon name="zoom-out" />
                </SlottedButton>

                <SlottedButton
                    round
                    title="Zoom in (2.0x)"
                    :disabled="Number.parseInt(GlobalStore.blockSize) >= 256"
                    @click="GlobalStore.changeBlockSize(2.0)"
                >
                    <Icon name="zoom-in" />
                </SlottedButton>
            </div>
        </div>

        <small>
            left click on a block to hide it, right click to copy id
        </small>
    </section>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .blockviz-controls__wrap {
        background: linear-gradient(transparent 32px, $dark_em 32px, $dark_bg);
    }
    .blockviz-controls {
        @include flex-center;
        height: 64px;
        gap: 2vw; // 4vw;
    }
    .blockviz-controls__blob {
        @include flex-center;
        padding: 4px; gap: 4px;
        background: linear-gradient($dark_em 50.5%, $trans 50.5%);
        border-radius: calc($BR_big + $BR_regular);

        &.round {
            border-radius: $BR_round;
        }
    }

    #big-black-button {
        height: 60px;
        padding: 0 20px;
        border-radius: $BR_big;
        font-weight: $FW_bold;
        box-shadow: inset 0 0 0 0px $white;

        &:not(:disabled) {
            &:hover {
                border-color: $white_80;
            }

            &:focus-visible, &:hover:active {
                // border-width: 4px;
                // padding: 2px 18px;
                border: 2px solid $white_80;
                box-shadow: inset 0 0 0 12px $trans;
                background-color: $white_30;
                transition: $TR_regular;
            }
        }
    }

    .side-picker__wrap {
        width: 84px; height: 40px;
    }
</style>
