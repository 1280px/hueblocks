<script setup>
    import {ref, computed, defineProps, defineEmits} from 'vue'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'
    import { hex2rgb, rgb2hex } from '@/colors'

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

    const cbItemColor = computed({
        get: () => {
            const rgb = SimpleViewStore.colorbarData[cbIdx].color
            return rgb2hex(rgb)
        },
        set: (hex) => {
            const rgb = hex2rgb(hex)
            SimpleViewStore.colorbarData[cbIdx].color = rgb
        }
    })

    const deleteCbItem = () => {
        if (cbIdx > 0) {
            SimpleViewStore.colorbarData[cbIdx-1].steps += SimpleViewStore.colorbarData[cbIdx].steps
        }
        SimpleViewStore.colorbarData.splice(cbIdx, 1)

        emit('done')
    }
</script>

<template>
    <div class="popover-content">
        <div class="popover-item">
            <button @click="deleteCbItem()"
                :disabled="SimpleViewStore.colorbarData.length <= 2"
            >Delete</button>
            <hr>
            <label for="i">Color: </label>
            <input type="color" id="i"
                v-model="cbItemColor" placeholder="cbItemColor"
            >
            <button type="submit" @click.prevent="emit('done')">OK</button>
        </div>
    </div>
</template>

<style lang="sass">
    @use '@/assets/popovers' as *;
</style>
