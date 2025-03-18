<script setup>
    import {ref, defineModel, defineProps, useId} from 'vue'

    const value = defineModel()
    value.value = !value.value ? 'all' : value.value

    const id = useId()

    const facing = [
        // According to Optifine CTM, first two options should be the last;
        // however, I suppose they'll actually end up being used the most
        { all: 'Any' },
        { sides: 'Sides' },
        { top: 'Top' },
        { bottom: 'Bottom' },
        { north: 'North' },
        { south: 'South' },
        { east: 'East' },
        { west: 'West' }
    ]
</script>

<template>
    <div class="side-picker">
        <select class="side-picker__btn" v-model="value" :id="id">
            <option v-for="(face, i) in facing" :key="i"
                :value="Object.keys(face)[0]"
            >{{ Object.values(face)[0] }}</option>
        </select>
        
        <div class="side-picker__image" :title="face">
            <!-- <icon>{{ facing[value] }}</icon> -->
        </div>
    </div>
</template>

<style lang="scss" scoped>

</style>
