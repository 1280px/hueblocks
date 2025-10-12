<script setup lang="ts">
import type { ColorbarSeg } from '@/types/simpleview'

import { defineEmits, defineProps } from 'vue'

import ColorPicker from '@/components/ColorPicker.vue'
import { overlayShow } from '@/overlay'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'
import BlockPickColor from '@/views/SimpleView/BlockPick/BlockPickColor.vue'

const { side } = defineProps<{
    side: 'left' | 'right',
}>()

const emit = defineEmits<{
    done: [],
}>()

const SimpleViewStore = useSimpleViewStore()

const cbRefIdx = (side === 'left' ? 0 : (SimpleViewStore.colorbarData.length - 1))
const cbRefItem = SimpleViewStore.colorbarData[cbRefIdx]

const cbNewItem: ColorbarSeg = {
    color: [...cbRefItem.color],
    blockRef: cbRefItem.blockRef,
    steps: cbRefItem.steps,
}

function addCbItem() {
    if (side === 'left') {
        SimpleViewStore.colorbarData.unshift(cbNewItem)
    }
    else {
        // Since last steps segment is defined by not the latest but
        // second to last cbItem, we need to change its steps as well:
        SimpleViewStore.colorbarData[cbRefIdx].steps = cbRefItem.steps
        SimpleViewStore.colorbarData.push(cbNewItem)
    }

    emit('done')
}
</script>

<template>
    <div class="popover-content">
        <label class="popover-item">Length:&nbsp;
            <input
                v-model="cbNewItem.steps"
                type="number" min="3" max="999"
            >
        </label>

        <label class="popover-item">Colour:&nbsp;
            <ColorPicker
                v-model="cbNewItem"
                :colorpick="() => overlayShow([
                    BlockPickColor, { },
                ])"
            />
        </label>

        <div class="popover-item">
            <button type="submit" @click.prevent="addCbItem">
                Add!
            </button>
        </div>
    </div>
</template>

<style lang="scss">
    @use '@/assets/popovers' as *;
</style>
