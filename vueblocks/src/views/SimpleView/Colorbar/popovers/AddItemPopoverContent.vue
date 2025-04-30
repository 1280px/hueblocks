<script setup>
    import {ref, computed, defineProps, defineEmits} from 'vue'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'
    import { hex2rgb, rgb2hex } from '@/colors'

    import ColorControls from '@/components/ColorControls.vue'
    import Icon from '@/components/Icon.vue'

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
    const cbRefColor = ref(rgb2hex(SimpleViewStore.colorbarData[cbRefIdx].color))
    const cbRefSteps = ref(SimpleViewStore.colorbarData[cbRefIdx].steps)

    const addCbItem = () => {
        const newCbItem = {
            color: hex2rgb(cbRefColor.value),
            blockRef: null,
            steps: cbRefSteps
        }

        if (side === 'left') {
            SimpleViewStore.colorbarData.unshift(newCbItem)
        }
        else {
            // Since last steps segment is defined by not the latest but
            // second to last cbItem, we need to change its steps as well:
            SimpleViewStore.colorbarData[cbRefIdx].steps = cbRefSteps
            SimpleViewStore.colorbarData.push(newCbItem)
        }

        emit('done')
    }
</script>

<template>
    <div class="popover-content">
        <label class="popover-item">Length:&nbsp;
            <input type="number"
                v-model="cbRefSteps" min=3 max=999
            >
        </label>
        <label class="popover-item">Colour:&nbsp;
            <ColorControls />
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
