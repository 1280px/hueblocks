<script setup>
    import {ref, computed, defineProps, defineEmits} from 'vue'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'

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

        SimpleViewStore.colorbarData[cbIdx].steps -= half;

        const newItem = { ...SimpleViewStore.colorbarData[cbIdx], steps: half };
        SimpleViewStore.colorbarData.splice(cbIdx + 1, 0, newItem);
    }
</script>

<template>
    <div class="popover-content">
        <div class="popover-item">
            <button @click="splitCbItem()"
                :disabled="SimpleViewStore.colorbarData[cbIdx].steps <= 5"
            >Split</button>
            <hr>
            <label for="i">Length: </label>
            <input type="number" min=3 max=999 id="i"
                v-model="SimpleViewStore.colorbarData[cbIdx].steps"
            >
            <button type="submit" @click.prevent="emit('done')">OK</button>
        </div>
    </div>
</template>

<style lang="sass">
    @use '@/assets/popovers' as *;
</style>
