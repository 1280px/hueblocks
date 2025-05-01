<script setup>
    import {ref, computed, defineProps, defineEmits} from 'vue'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'

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

    const splitCbItem = () => {
        const half = Math.floor(SimpleViewStore.colorbarData[cbIdx].steps / 2)

        SimpleViewStore.colorbarData[cbIdx].steps -= half

        const newItem = {
            color: (SimpleViewStore.colorbarData[cbIdx].color).map(
                (c, i) => Math.floor((c / 2) + (SimpleViewStore.colorbarData[cbIdx+1].color[i] / 2))
            ),
            blockRef: null,
            steps: half
        }

        SimpleViewStore.colorbarData.splice(cbIdx+1, 0, newItem)
    }
</script>

<template>
    <div class="popover-content">
        <div class="popover-item">
            <button @click="splitCbItem" title="Insert colour tag in between"
                :disabled="SimpleViewStore.colorbarData[cbIdx].steps <= 5"
            >
                <Icon name="colortag" />
            </button>
            <hr>
            <label class="popover-item">Length:
                <input type="number" min=3 max=999
                    v-model="SimpleViewStore.colorbarData[cbIdx].steps"
                >
            </label>
            <button type="submit" @click.prevent="emit('done')">OK</button>
        </div>
    </div>
</template>

<style lang="scss">
    @use '@/assets/popovers' as *;
</style>
