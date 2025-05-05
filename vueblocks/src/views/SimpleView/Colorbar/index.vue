<script setup>
    import {ref, computed, defineAsyncComponent} from 'vue'
    import {overlayIsShown} from '@/overlay'
    import { Wowerlay } from 'wowerlay'
    import { useSimpleViewStore } from '@/stores/SimpleViewStore'
    
    import AddItemButton from './AddItemButton.vue'
    import StepsSegment from './StepsSegment.vue'
    import ColorSegment from './ColorSegment.vue'
    import SlottedButton from '@/components/SlottedButton.vue'
    import Icon from '@/components/Icon.vue'

    import AddItemPopoverContent from './popovers/AddItemPopoverContent.vue'
    import ColorPopoverContent from './popovers/ColorPopoverContent.vue'
    import StepsPopoverContent from './popovers/StepsPopoverContent.vue'
    
    const SimpleViewStore = useSimpleViewStore()

    // Colorbar button controls
    function colorbarSwap() {
        SimpleViewStore.colorbarData = SimpleViewStore.colorbarData.reverse()

        // We also want to reverse all the lengths, which is why
        // we need to shift the unused last length back to the end:
        for (const cbIdx in SimpleViewStore.colorbarData) {
            SimpleViewStore.colorbarData[cbIdx].steps = (
                SimpleViewStore.colorbarData[+cbIdx+1]
                ? SimpleViewStore.colorbarData[+cbIdx+1].steps : 5
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

    const popoverShow = (event, mode, data) => {
        if (popoverTarget.value === event.currentTarget) {
            popoverTarget.value = null
        }
        else {
            popoverMode.value = mode
            popoverData.value = data
            popoverTarget.value = event.currentTarget
        }
    }

    const popoverIsShown = computed({
        get: () => {
            return !!popoverTarget.value
        },
        set: () => {
            if (overlayIsShown.value) {
                return
            }
            popoverTarget.value = null
        }
    })
</script>

<template>
    <section class="colorbar">
        <SlottedButton class="trans" @click="colorbarSwap" title="Swap left to right">
            <Icon name="swap" />
        </SlottedButton>

        <AddItemButton side="left" title="Add new color to the left"
            @click="(e) => popoverShow(e, 'addItem', 'left')"
        />
        <div class="colorbar__inner">
            <template v-for="(cbItem, cbIdx) in SimpleViewStore.colorbarData" :key="cbIdx">
                <ColorSegment
                    :colorCss="getCssRgb(cbItem.color)" :blockRef="cbItem.blockRef"
                    @click="(e) => popoverShow(e, 'color', cbIdx)"
                />
                <StepsSegment v-if="cbIdx !== SimpleViewStore.colorbarData.length-1"
                    :value="cbItem.steps" :bg="[
                        getCssRgb(SimpleViewStore.colorbarData[cbIdx]?.color),
                        getCssRgb(SimpleViewStore.colorbarData[cbIdx+1]?.color)
                    ]"
                    @click="(e) => popoverShow(e, 'steps', cbIdx)"
                />
            </template>
        </div>
        <AddItemButton side="right" title="Add new color to the right"
            @click="(e) => popoverShow(e, 'addItem', 'right')"
        />
        
        <SlottedButton class="trans" @click="colorbarRandom" title="Randomize colours">
            <Icon name="random" />
        </SlottedButton>
    </section>

    <Wowerlay
        class="popover" :target="popoverTarget" v-model:visible="popoverIsShown"
        :gap="12"
    >
        <template #arrow="{ side, placement }">
            <div class="popover-arrow" :class="`${side}`"></div>
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
            width: 32px;
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
