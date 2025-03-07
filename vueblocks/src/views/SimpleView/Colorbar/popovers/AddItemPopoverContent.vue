<script setup>
    import {ref, computed, defineProps, defineEmits} from 'vue'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'
    import { hex2rgb, rgb2hex } from '@/colors'

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
    <div class="popover-inner">
        <input type="number" min=3 max=999
            v-model="cbRefSteps"
        >
        <input type="color"
            v-model="cbRefColor" placeholder="cbRefColor"
        >
        <button type="submit" @click.prevent="addCbItem()">Add!</button>
    </div>
</template>
