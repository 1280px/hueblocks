<script setup>
    import {ref, defineProps, defineAsyncComponent, onMounted} from 'vue'
    import { useGlobalStore } from '@/stores/GlobalStore'

    const {name} = defineProps({
        name: {
            type: String,
            required: true
        }
    })

    const iconData = ref(name)

    onMounted(async () => {
        const response = await fetch(
            GlobalStore.getIconPath(name)
        )
        iconData.value = await response.text()
    })

    const GlobalStore = useGlobalStore()
</script>

<!-- https://xhtml.ru/2020/css/un-repeat-svg-icon-fill-with-currentcolor/ -->

<template>
    <div class="icon" v-html="iconData"></div>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .icon {
        @include flex-center;
    }
</style>
