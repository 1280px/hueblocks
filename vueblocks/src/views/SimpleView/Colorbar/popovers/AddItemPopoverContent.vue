<script setup>
    import {ref, computed, defineProps, defineEmits} from 'vue'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'
    import { hex2rgb, rgb2hex } from '@/colors'

    import ColorControls from '@/components/ColorControls.vue'

    const SimpleViewStore = useSimpleViewStore()
    const {side} = defineProps({
        side: {
            type: String,
            required: true
        }
    })
    const emit = defineEmits([
        'done'
    ])

    const cbRefIdx = (side === 'left' ? 0 : (SimpleViewStore.colorbarData.length-1))
    const cbRefItem = SimpleViewStore.colorbarData[cbRefIdx]

    const cbNewItem = {
        color: cbRefItem.color,
        blockRef: cbRefItem.blockRef,
        steps: cbRefItem.steps
    }

    const addCbItem = () => {
        if (side === 'left') {
            SimpleViewStore.colorbarData.unshift(cbNewItem)
        }
        else {
            // Since last steps segment is defined by not the latest but
            // second to last cbItem, we need to change its steps as well:
            SimpleViewStore.colorbarData[cbRefIdx].steps = cbRefItem.value.steps
            SimpleViewStore.colorbarData.push(cbNewItem)
        }

        emit('done')
    }
</script>

<template>
    <div class="popover-content">
        <label class="popover-item">Length:&nbsp;
            <input type="number"
                v-model="cbRefItem.steps" min=3 max=999
            >
        </label>
        <label class="popover-item">Colour:&nbsp;
            <ColorControls v-model="cbNewItem" />
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
