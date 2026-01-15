<script setup lang="ts">
import type { ColorRGB } from '@/types/colors'
import type { ColorbarSeg } from '@/types/simpleview'

import Icon from '@/components/Icon.vue'
import SlottedButton from '@/components/SlottedButton.vue'
import SlottedInput from '@/components/SlottedInput.vue'
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
            <SlottedButton
                variant="black"
                :title="SimpleViewStore.colorbarData[cbIdx].steps > 5
                    ? 'Insert colour tag in between' : 'Length too short to be splittable in between'
                "
                :disabled="SimpleViewStore.colorbarData[cbIdx].steps <= 5"
                @click="splitCbItem"
            >
                <Icon name="colortag" />
            </SlottedButton>

            <hr>

            <SlottedInput
                v-model="SimpleViewStore.colorbarData[cbIdx].steps"
                variant="black"
                type="number" min="3" max="999"
            >
                Length:
            </SlottedInput>

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
