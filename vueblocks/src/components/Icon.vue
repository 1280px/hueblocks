<script setup lang="ts">
import { defineProps, onMounted, ref } from 'vue'

import { useGlobalStore } from '@/stores/GlobalStore'

const { name } = defineProps<{
    name: string,
}>()

const GlobalStore = useGlobalStore()

const iconData = ref(name)

onMounted(async () => {
    const response = await fetch(
        GlobalStore.getIconPath(name),
    )
    iconData.value = await response.text()
})
</script>

<!-- https://xhtml.ru/2020/css/un-repeat-svg-icon-fill-with-currentcolor/ -->

<template>
    <div class="icon" v-html="iconData" />
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .icon {
        @include flex-center;

        font-size: 0pt; // Don't show text when SVG isn't loaded
    }
</style>
