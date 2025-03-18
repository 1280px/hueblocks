<script setup>
    import {ref, computed, defineAsyncComponent} from 'vue'
    import { Wowerlay } from 'wowerlay'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'
    
    import AddItemButton from './AddItemButton.vue'
    import StepsSegment from './StepsSegment.vue'
    import ColorSegment from './ColorSegment.vue'
    import SlottedButton from '@/components/SlottedButton.vue'

    const AddItemPopoverContent = defineAsyncComponent({
        loader: () => import('./popovers/AddItemPopoverContent.vue'),
        loadingComponent: () => 'Loading…', delay: 0, suspensible: false
    })
    const ColorPopoverContent = defineAsyncComponent({
        loader: () => import('./popovers/ColorPopoverContent.vue'),
        loadingComponent: () => 'Loading…', delay: 0, suspensible: false
    })
    const StepsPopoverContent = defineAsyncComponent({
        loader: () => import('./popovers/StepsPopoverContent.vue'),
        loadingComponent: () => 'Loading…', delay: 0, suspensible: false
    })
    
    const SimpleViewStore = useSimpleViewStore()

    // Colorbar button controls
    function colorbarSwap() {
        SimpleViewStore.colorbarData = SimpleViewStore.colorbarData.reverse()

        // We also want to reverse all the lengths, which is why
        // we need to shift the unused last length back to the end:
        for (const cbIdx in SimpleViewStore.colorbarData) {
            SimpleViewStore.colorbarData[cbIdx].steps = (
                SimpleViewStore.colorbarData[+cbIdx+1] ? SimpleViewStore.colorbarData[+cbIdx+1].steps : 5
            )
        }
    }
    function colorbarRandom() {
        // We only want to randomize colors, not lengths
        for (const cbItem of SimpleViewStore.colorbarData) {
            cbItem.blockRef = null
            cbItem.color = [
                parseInt(
                    Math.floor(0.3 + Math.random())*120
                    + Math.round(Math.random() * 2)*40
                    + (Math.random() * 56)
                ),
                parseInt(
                    Math.floor(0.3 + Math.random())*100
                    + Math.round(Math.random() * 4)*30
                    + (Math.random() * 16)
                ),
                parseInt(
                    Math.floor(0.3 + Math.random())*80
                    + Math.round(Math.random() * 2)*40
                    + (Math.random() * 96)
                )
            ]
            // console.log(cbItem.color[0], cbItem.color[1], cbItem.color[2])
        }
    }

    // Convert RGB to CSS color string
    function getCssRgb(rgb) {
        return `rgb(${rgb[0] || 0}, ${rgb[1] || 0}, ${rgb[2] || 0})`
    }

    // Wowerlay stuff
    const popoverTarget = ref(null)
    const popoverMode = ref(null)
    const popoverData = ref(null)

    const showPopover = (event, mode, data) => {
        if (popoverTarget.value === event.currentTarget) {
            popoverTarget.value = null
        }
        else {
            popoverMode.value = mode
            popoverData.value = data
            popoverTarget.value = event.currentTarget
        }
    }
</script>

<template>
    <section class="colorbar">
        <SlottedButton class="trans" @click="colorbarSwap" title="Swap left to right">
            <icon>🔁</icon>
        </SlottedButton>

        <AddItemButton side="left" title="Add new color to the left"
            @click="(e) => showPopover(e, 'addItem', 'left')"
            :disabled="SimpleViewStore.colorbarData.length > 21"
        />

        <div v-if="SimpleViewStore?.colorbarData" class="colorbar__inner">
            <template v-for="(cbItem, cbIdx) in SimpleViewStore.colorbarData" :key="cbIdx">
                <ColorSegment
                    :color="getCssRgb(cbItem.color)" :blockRef="cbItem.blockRef"
                    @click="(e) => showPopover(e, 'color', cbIdx)"
                />
                <StepsSegment v-if="cbIdx !== SimpleViewStore.colorbarData.length-1"
                    :value="cbItem.steps" :bg="[
                        getCssRgb(SimpleViewStore.colorbarData[cbIdx]?.color),
                        getCssRgb(SimpleViewStore.colorbarData[cbIdx+1]?.color)
                    ]"
                    @click="(e) => showPopover(e, 'steps', cbIdx)"
                />
            </template>
        </div>
        <span v-else class="colorbar__inner">
            — Loading, please wait… —
        </span>

        <AddItemButton side="right" title="Add new color to the right"
            @click="(e) => showPopover(e, 'addItem', 'right')"
            :disabled="SimpleViewStore.colorbarData.length > 21"
        />
        
        <SlottedButton class="trans" @click="colorbarRandom" title="Randomize colours">
            <icon>💥</icon>
        </SlottedButton>
    </section>

    <Wowerlay
        :target="popoverTarget" v-model:visible="popoverTarget"
        class="popover" :transition="popoverTransition"
    >
        <template #arrow>
            <div class="popover-arrow"></div>
        </template>

        <ColorPopoverContent v-if="popoverMode === 'color'"
            :cbIdx="popoverData" @done="popoverTarget = null"
        />
        <StepsPopoverContent v-else-if="popoverMode === 'steps'"
            :cbIdx="popoverData" @done="popoverTarget = null"
        />
        <AddItemPopoverContent v-else-if="popoverMode === 'addItem'"
            :side="popoverData" @done="popoverTarget = null"
        />
    </Wowerlay>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    .colorbar {
        flex: 1;
        display: flex;
        height: 40px;
        margin-bottom: 28px;
        border-radius: $BR_big;
        
        & button.trans {
            margin: 0 8px;
            align-self: center;
        }
    }
    
    .colorbar__inner {
        @include flex-center;
        flex: 1;
        align-items: stretch;
        background-color: $white_30;
        box-shadow: $SH_smooth;
    }
</style>
