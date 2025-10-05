<script setup>
import { defineEmits, defineProps } from 'vue'

import Icon from '@/components/Icon.vue'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'

const { cbIdx } = defineProps({
    cbIdx: {
        type: Number,
        required: true,
    },
})

const emit = defineEmits([
    'done',
])

const SimpleViewStore = useSimpleViewStore()

function splitCbItem() {
    const half = Math.floor(SimpleViewStore.colorbarData[cbIdx].steps / 2)

    SimpleViewStore.colorbarData[cbIdx].steps -= half

    const newItem = {
        color: (SimpleViewStore.colorbarData[cbIdx].color).map(
            (c, i) => Math.floor((c / 2) + (SimpleViewStore.colorbarData[cbIdx + 1].color[i] / 2)),
        ),
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
                title="Insert colour tag in between" :disabled="SimpleViewStore.colorbarData[cbIdx].steps <= 5"
                @click="splitCbItem"
            >
                <Icon name="colortag" />
            </button>
            <hr>
            <label class="popover-item">Length:
                <input
                    v-model="SimpleViewStore.colorbarData[cbIdx].steps" type="number" min="3"
                    max="999"
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
