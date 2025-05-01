<script setup>
    import {ref, computed, defineProps, defineEmits} from 'vue'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'

    import ColorControls from '@/components/ColorControls.vue'
    import Icon from '@/components/Icon.vue'

    const SimpleViewStore = useSimpleViewStore()
    const {cbIdx} = defineProps({
        cbIdx: {
            type: Number,
            required: true
        }
    })
    const emit = defineEmits([
        'done'
    ])

    const deleteCbItem = () => {
        if (cbIdx > 0) {
            SimpleViewStore.colorbarData[cbIdx-1].steps
            += SimpleViewStore.colorbarData[cbIdx].steps
        }
        SimpleViewStore.colorbarData.splice(cbIdx, 1)

        emit('done')
    }
</script>

<template>
    <div class="popover-content">
        <div class="popover-item">
            <button @click="deleteCbItem" title="Delete this colour tag"
                :disabled="SimpleViewStore.colorbarData.length <= 2"
            >
                <Icon name="colortag-del" />
            </button>
            <hr>
            <label class="popover-item">Colour:
                <ColorControls v-model="SimpleViewStore.colorbarData[cbIdx]"
                    @change="SimpleViewStore.colorbarData[cbIdx].blockRef = null"
                />
            </label>
            <button type="submit" @click.prevent="emit('done')">OK</button>
        </div>
    </div>
</template>

<style lang="scss">
    @use '@/assets/popovers' as *;
</style>
