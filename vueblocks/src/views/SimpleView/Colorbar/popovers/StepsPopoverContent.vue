<script setup lang="ts">
import type { ColorRGB } from '@/types/colors'
import type { ColorbarSeg } from '@/types/simpleview'

import { defineEmits, defineProps } from 'vue'

import Icon from '@/components/Icon.vue'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const { cbIdx } = defineProps<{
    cbIdx: number,
}>()

const emit = defineEmits<{
    done: [],
}>()

const SimpleViewStore = useSimpleViewStore()

function splitCbItem() {
    const half = Math.floor(SimpleViewStore.colorbarData[cbIdx].steps / 2)

    SimpleViewStore.colorbarData[cbIdx].steps -= half

    const newItem: ColorbarSeg = {
        color: (SimpleViewStore.colorbarData[cbIdx].color).map(
            (c, i) => Math.floor((c / 2) + (SimpleViewStore.colorbarData[cbIdx + 1].color[i] / 2)),
        ) as ColorRGB,
        blockRef: null,
        steps: half,
    }

    SimpleViewStore.colorbarData.splice(cbIdx + 1, 0, newItem)
}
</script>

<template>
    <div class="popover-content">
        <div class="popover-item">
            <button
                :title="SimpleViewStore.colorbarData[cbIdx].steps > 5
                    ? 'Insert colour tag in between' : 'Length too short to be splittable in between'
                "
                :disabled="SimpleViewStore.colorbarData[cbIdx].steps <= 5"
                @click="splitCbItem"
            >
                <Icon name="colortag" />
            </button>

            <hr>

            <label class="popover-item">Length:
                <input
                    v-model="SimpleViewStore.colorbarData[cbIdx].steps"
                    type="number" min="3" max="999"
                >
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
