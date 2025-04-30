<script setup>
    import {watch, ref} from 'vue'

    const visible = ref(false)
    const innerComponent = ref(null), innerProps = ref({})
    let res = null

    const show = (newInnerComponent, newInnerProps = {}) => {
        innerComponent.value = newInnerComponent
        innerProps.value = newInnerProps
        visible.value = true

        return new Promise((resolve) => {
            res = resolve
        })
    }

    const done = (data) => {
        visible.value = false
        innerComponent.value = null
        innerProps.value = {}

        res?.(data ?? null)
    }

    const d = ref()

    watch(visible, async (v) => {
        if (v) {
            // Apparently setImmediate() is not supported in Vue?
            setTimeout(() => d.value?.showModal(), 1)
        }
    })

    defineExpose({ show })
</script>

<template>
    <Transition name="overlay">
        <dialog v-if="visible" ref="d" @cancel.prevent>
            {{ innerComponent }}
            {{ innerProps }}
            <component :is="innerComponent" v-bind="innerProps" @done="done" />
        </dialog>
    </Transition>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    dialog {
        margin: 32px 32px auto;
        background: none;
        border: none;
    }
    dialog::backdrop {
        background-color: $accent-dark_25;
        backdrop-filter: blur(4px);
    }
</style>
