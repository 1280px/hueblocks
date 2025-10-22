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
                <button
                    id="big-black-button"
                    :disabled="!GlobalStore.currBlocksetBlockdata"
                    @click="() => emit('bbbClick')"
                >
                    {{
                        GlobalStore.currBlocksetBlockdata
                            ? 'GENERATE BLOCK GRAIDENT'
                            : 'Loading blockdata, please wait…'
                    }}
                </button>
            </div>

            <div class="blockviz-controls__blob round">
                <SlottedButton
                    class="round"
                    title="Zoom out (0.5x)"
                    @click="GlobalStore.changeBlockSize(0.5)"
                >
                    <Icon name="zoom-out" />
                </SlottedButton>

                <SlottedButton
                    class="round"
                    title="Zoom in (2.0x)"
                    @click="GlobalStore.changeBlockSize(2.0)"
                >
                    <Icon name="zoom-in" />
                </SlottedButton>
            </div>
        </div>

        <small>
            tip: left click a block to hide it, right click to copy id
        </small>
    </section>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .blockviz-controls__wrap {
        background: linear-gradient(transparent 32px, #181818bb 32px, $dark_bg);
    }
    .blockviz-controls {
        @include flex-center;
        height: 64px;
        gap: 2vw; // 4vw;
    }
    .blockviz-controls__blob {
        @include flex-center;
        padding: 4px; gap: 4px;
        background: linear-gradient(#181818bb 50.5%, $trans 50.5%);
        border-radius: calc($BR_big + $BR_regular);

        &.round {
            border-radius: $BR_round;
        }
    }

    #big-black-button {
        appearance: none;
        height: 60px;
        padding: 0 20px;
        border-radius: $BR_big;
    }

    .side-picker__wrap {
        width: 84px; height: 40px;
    }
</style>
