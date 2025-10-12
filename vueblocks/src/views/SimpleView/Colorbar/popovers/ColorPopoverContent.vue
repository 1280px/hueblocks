<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'

import ColorPicker from '@/components/ColorPicker.vue'
import Icon from '@/components/Icon.vue'
import { overlayShow } from '@/overlay'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'
import BlockPick from '@/widgets/Overlay/BlockPick.vue'

const { cbIdx } = defineProps<{
    cbIdx: number,
}>()

const emit = defineEmits<{
    done: [],
}>()

const SimpleViewStore = useSimpleViewStore()

function deleteCbItem() {
    if (cbIdx > 0) {
        SimpleViewStore.colorbarData[cbIdx - 1].steps += SimpleViewStore.colorbarData[cbIdx].steps
    }
    SimpleViewStore.colorbarData.splice(cbIdx, 1)

    emit('done')
}
</script>

<template>
    <div class="popover-content">
        <div class="popover-item">
            <button
                :title="SimpleViewStore.colorbarData.length > 2
                    ? 'Delete this colour tag' : 'There should be at least 2 colours for a gradient'
                "
                :disabled="SimpleViewStore.colorbarData.length <= 2"
                @click="deleteCbItem"
            >
                <Icon name="colortag-del" />
            </button>

            <hr>

            <label class="popover-item">Colour:
                <ColorPicker
                    v-model="SimpleViewStore.colorbarData[cbIdx]"
                    :blockpick="() => overlayShow({
                        content: BlockPick, props: { mode: 'color' },
                    })"
                    @change="SimpleViewStore.colorbarData[cbIdx].blockRef = null"
                />
            </label>

            <button type="submit" @click.prevent="emit('done')">
                OK
            </button>
        </div>
    </div>
</template>

<style lang="scss">
    @use '@/assets/popovers' as *;
</style>
