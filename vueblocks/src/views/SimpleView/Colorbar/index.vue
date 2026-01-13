<script setup lang="ts">
import type { ColorRGB } from '@/types/colors'
import type { ColorbarPopoverData } from '@/types/simpleview'

import { computed, ref } from 'vue'
import { Wowerlay } from 'wowerlay'

import { getRandomRbg, rgb2hex } from '@/colors'
import Icon from '@/components/Icon.vue'
import SlottedButton from '@/components/SlottedButton.vue'
import { overlayIsShown } from '@/overlay'
import { useSimpleViewStore } from '@/stores/SimpleViewStore'
import AddItemButton from './AddItemButton.vue'
import ColorSegment from './ColorSegment.vue'
import AddItemPopoverContent from './popovers/AddItemPopoverContent.vue'
import ColorPopoverContent from './popovers/ColorPopoverContent.vue'
import StepsPopoverContent from './popovers/StepsPopoverContent.vue'
import StepsSegment from './StepsSegment.vue'

const SimpleViewStore = useSimpleViewStore()

// Colorbar aside buttons

function colorbarSwap() {
    SimpleViewStore.colorbarData = [...SimpleViewStore.colorbarData].reverse()

    // We also want to reverse all the lengths, which is why
    // we need to shift the unused last length back to the end:
    for (const cbIdx in SimpleViewStore.colorbarData) {
        SimpleViewStore.colorbarData[cbIdx].steps = (
            SimpleViewStore.colorbarData[+cbIdx + 1]
                ? SimpleViewStore.colorbarData[+cbIdx + 1].steps
                : 5
        )
    }
}

function colorbarRandom() {
    // We only want to randomize colors, not lengths
    for (const cbItem of SimpleViewStore.colorbarData) {
        cbItem.blockRef = null
        // cbItem.color = getRandomRbg(0.33)
        cbItem.color = getRandomRbg(Math.random() > 0.75 ? 0.96 : 1.12)
    }
}

// Colorbar quick actions

function changeLenOnScroll(e: WheelEvent, cbIdx: number) {
    if (e.deltaY > 0) {
        SimpleViewStore.colorbarData[cbIdx].steps = (
            SimpleViewStore.colorbarData[cbIdx].steps > 3
                ? SimpleViewStore.colorbarData[cbIdx].steps - 1
                : 3
        )
    }
    else {
        SimpleViewStore.colorbarData[cbIdx].steps = (
            SimpleViewStore.colorbarData[cbIdx].steps < 99
                ? SimpleViewStore.colorbarData[cbIdx].steps + 1
                : 99
        )
    }
}

function copyColorTagHex(rgb: ColorRGB) {
    navigator.clipboard.writeText(rgb2hex(rgb))
}

// Wowerlay popover

const popoverTarget = ref<EventTarget | null>(null)
const popoverData = ref<ColorbarPopoverData>()

function popoverShow(e: Event, data: ColorbarPopoverData) {
    if (popoverTarget.value === e.currentTarget) {
        popoverTarget.value = null
    }
    else {
        popoverData.value = data
        popoverTarget.value = e.currentTarget
    }
}

const popoverIsShown = computed({
    get: () => {
        return !!popoverTarget.value
    },
    set: () => {
        if (overlayIsShown.value) { return }

        popoverTarget.value = null
    },
})
</script>

<template>
    <section class="colorbar">
        <SlottedButton
            variant="trans"
            title="Swap left to right"
            @click="colorbarSwap"
        >
            <Icon name="swap" />
        </SlottedButton>

        <AddItemButton
            side="left" title="Add new color to the left"
            @click="(e: MouseEvent) => popoverShow(e, { mode: 'addItem', side: 'left' })"
        />
        <div class="colorbar__inner">
            <template v-for="(cbItem, cbIdx) in SimpleViewStore.colorbarData" :key="cbIdx">
                <ColorSegment
                    :color="cbItem.color" :block-ref="cbItem.blockRef"
                    @click="(e: MouseEvent) => popoverShow(e, { mode: 'color', cbIdx })"
                    @contextmenu.prevent="copyColorTagHex(cbItem.color)"
                />
                <StepsSegment
                    v-if="cbIdx !== SimpleViewStore.colorbarData.length - 1"
                    :value="cbItem.steps"
                    :bg="[
                        SimpleViewStore.colorbarData[cbIdx]?.color,
                        SimpleViewStore.colorbarData[cbIdx + 1]?.color,
                    ]"
                    @click="(e: MouseEvent) => popoverShow(e, { mode: 'steps', cbIdx })"
                    @wheel.prevent="(e: WheelEvent) => changeLenOnScroll(e, cbIdx)"
                />
            </template>
        </div>
        <AddItemButton
            side="right" title="Add new color to the right"
            @click="(e: MouseEvent) => popoverShow(e, { mode: 'addItem', side: 'right' })"
        />

        <SlottedButton
            variant="trans"
            title="Randomize colours"
            @click="colorbarRandom"
        >
            <Icon name="random" />
        </SlottedButton>
    </section>

    <Wowerlay
        v-model:visible="popoverIsShown" :target="(popoverTarget as (HTMLElement | null))" :gap="12"
        class="popover"
    >
        <template #arrow="{ side }">
            <div class="popover-arrow" :class="`${side}`" />
        </template>

        <ColorPopoverContent
            v-if="popoverData?.mode === 'color'"
            :cb-idx="popoverData.cbIdx" @done="popoverTarget = null"
        />
        <StepsPopoverContent
            v-else-if="popoverData?.mode === 'steps'"
            :cb-idx="popoverData.cbIdx" @done="popoverTarget = null"
        />
        <AddItemPopoverContent
            v-else-if="popoverData?.mode === 'addItem'"
            :side="popoverData.side" @done="popoverTarget = null"
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
