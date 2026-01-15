<script setup lang="ts">
import type { ColorbarSeg } from '@/types/simpleview'

import { ref } from 'vue'

import ColorPicker from '@/components/ColorPicker.vue'
import SlottedButton from '@/components/SlottedButton.vue'
import SlottedInput from '@/components/SlottedInput.vue'
import { overlayShow } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'
import BlockPickColor from '@/views/SimpleView/BlockPick/BlockPickColor.vue'

const { side } = defineProps<{
    side: 'left' | 'right',
}>()

const emit = defineEmits<{
    done: [],
}>()

const SimpleViewStore = useSimpleViewStore()
const GlobalStore = useGlobalStore()

const cbRefIdx = side === 'left'
    ? 0
    : (SimpleViewStore.colorbarData.length - 1)

const cbNewItem = ref<ColorbarSeg>({
    color: SimpleViewStore.colorbarData[cbRefIdx].color,
    blockRef: SimpleViewStore.colorbarData[cbRefIdx].blockRef,
    // The very last color tag's length should never be used
    steps: side === 'left'
        ? SimpleViewStore.colorbarData[cbRefIdx].steps
        : SimpleViewStore.colorbarData[cbRefIdx - 1].steps,
})

function addCbItem() {
    if (side === 'left') {
        SimpleViewStore.colorbarData.unshift({ ...cbNewItem.value })
    }
    else {
        SimpleViewStore.colorbarData[cbRefIdx].steps = cbNewItem.value.steps
        SimpleViewStore.colorbarData.push({ ...cbNewItem.value })
    }

    emit('done')
}

async function applyPickedBlock() {
    const res: ColorbarSeg = await overlayShow(
        [BlockPickColor, { originalFacing: GlobalStore.blockFacing }],
    )

    if (res) {
        cbNewItem.value.color = [...res.color]

        cbNewItem.value.blockRef = res.blockRef ? res.blockRef : null
    }
}
</script>

<template>
    <div class="popover-content">
        <SlottedInput
            v-model="cbNewItem.steps"
            variant="black"
            type="number" min="3" max="999"
        >
            Length:
        </SlottedInput>

        <label class="popover-item">Colour:&nbsp;
            <ColorPicker
                v-model="cbNewItem.color"
                colorpick-text="Pick colour from a block…" colorpick-icon="block"
                @colorpick="applyPickedBlock"
            />
        </label>

        <div class="popover-item">
            <SlottedButton
                variant="black"
                type="submit"
                @click.prevent="addCbItem"
            >
                Add!
            </SlottedButton>
        </div>
    </div>
</template>
