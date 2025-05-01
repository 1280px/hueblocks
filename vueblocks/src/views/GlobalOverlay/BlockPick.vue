<script setup>
    // This overlay inner component is put GO dir because it is
    // expected to be shared across different views and modes!
    import {ref, defineEmits} from 'vue'

    const emit = defineEmits([
        'done'
    ])
</script>

<template>
    <button @click="emit('done', {
        color: [123, 145, 189],
        blockRef: {
            name: 'Tuff (fr though)',
            texture: 'tuff.png'
        }
    })">done</button>
    <button @click="emit('done')">cancel</button>
</template>

<style lang="scss" scoped>

</style>
