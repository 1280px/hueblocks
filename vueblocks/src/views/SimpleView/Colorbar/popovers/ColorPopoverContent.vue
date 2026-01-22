<script setup lang="ts">
import type { ColorbarSeg } from '@/types/simpleview'

import ColorPicker from '@/components/ColorPicker.vue'
import Icon from '@/components/Icon.vue'
import SlottedButton from '@/components/SlottedButton.vue'
import { overlayShow } from '@/overlay'
import { useGlobalStore } from '@/stores/GlobalStore'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'
import BlockPickColor from '@/views/SimpleView/BlockPick/BlockPickColor.vue'

const { cbIdx } = defineProps<{
    cbIdx: number,
}>()

const emit = defineEmits<{
    done: [],
}>()

const SimpleViewStore = useSimpleViewStore()
const GlobalStore = useGlobalStore()

function deleteCbItem() {
    if (cbIdx > 0) {
        SimpleViewStore.colorbarData[cbIdx - 1].steps += SimpleViewStore.colorbarData[cbIdx].steps
    }
    SimpleViewStore.colorbarData.splice(cbIdx, 1)

    emit('done')
}

async function applyPickedBlock() {
    const res: ColorbarSeg = await overlayShow(
        [BlockPickColor, { originalFacing: GlobalStore.blockFacing }],
    )

    if (res) {
        SimpleViewStore.colorbarData[cbIdx].color = [...res.color]

        SimpleViewStore.colorbarData[cbIdx].blockRef = res.blockRef ? res.blockRef : null
    }
}
</script>

<template>
    <div class="popover-content">
        <div class="popover-item">
            <SlottedButton
                variant="black"
                :title="
                    SimpleViewStore.colorbarData.length > 2
                        ? 'Delete this colour tag'
                        : 'There should be at least 2 colours for a gradient'
                "
                :disabled="SimpleViewStore.colorbarData.length <= 2"
                @click="deleteCbItem"
            >
                <Icon name="colortag-del" />
            </SlottedButton>

            <hr>

            <label class="popover-item">Colour:
                <ColorPicker
                    v-model="SimpleViewStore.colorbarData[cbIdx].color"
                    colorpick-text="Pick colour from a block…" colorpick-icon="block"
                    @change="SimpleViewStore.colorbarData[cbIdx].blockRef = null"
                    @colorpick="applyPickedBlock"
                />
            </label>

            <SlottedButton
                variant="black"
                type="submit"
                @click.prevent="emit('done')"
            >
                <Icon name="check" />
            </SlottedButton>
        </div>
    </div>
</template>

<style lang="scss">
    @use '@/assets/popovers' as *;
</style>
