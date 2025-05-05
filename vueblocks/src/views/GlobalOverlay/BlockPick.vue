<script setup>
    // This overlay inner component is put GO dir because it is
    // expected to be shared across many different views & modes!
    import {ref, defineEmits, onMounted} from 'vue'
    import {useGlobalStore} from '@/stores/GlobalStore'

    import SlottedButton from '@/components/SlottedButton.vue'
    import Block from '@/components/Block.vue'
    import Icon from '@/components/Icon.vue'

    const {mode} = defineProps({
        mode: {
            type: String,
            required: true
        }
    })
    const emit = defineEmits([
        'done'
    ])

    const GlobalStore = useGlobalStore()

    const blocksetIdx = ref(-1)
    const blockdataByAlphabet = ref({})

    onMounted(() => {
        blocksetIdx.value = GlobalStore.currBlocksetIdx

        // Separate all blocks by alphabet by their name
        for (const block of GlobalStore.currBlocksetBlockdata.sort(
            (b1, b2) => b1.name.localeCompare(b2.name)
        )) {
            if (!Object.hasOwn(blockdataByAlphabet.value, block.name[0])) {
                blockdataByAlphabet.value[block.name[0]] = []
            }

            blockdataByAlphabet.value[block.name[0]].push(block)
        }
    })
</script>

<template>
    <div class="overlay__inner">
        <main v-if="mode === 'palette'">
            <header>
                <h2>— &nbsp; Pick blocks you want to use as a palette… &nbsp; —</h2>
            </header>

        </main>

        <main v-else-if="mode == 'color'">
            <header>
                <h2>— &nbsp; Pick a block to use as a color reference… &nbsp; —</h2>
            </header>

            <section v-for="bdLetter of Object.keys(blockdataByAlphabet)" :key="bdLetter">
                <!-- {{ bdLetter }} -->
                <div v-for="(block, i) of blockdataByAlphabet[bdLetter]" :key="i"
                    class="block__click-wrap" @click="emit('done', {
                        color: block.rgb,
                        blockRef: {
                            name: block.name,
                            blocksetIdx: blocksetIdx,
                            texture: block.texture
                        }
                    })"
                >
                <Block 
                    :name="block.name" :blocksetIdx="blocksetIdx" :texture="block.texture"
                />
                </div>
            </section>
        </main>

        <aside>
            <SlottedButton class="round"
                @click="emit('done')"
            title="Cancel">
                <Icon name="close" />
            </SlottedButton>

            <SlottedButton class="round" v-if="mode === 'palette'"
                @click="emit('done', selectedBlockdata)"
                :disabled="selectedBlockdata.length < 3"
            :title="selectedBlockdata.length < 3 ? 'Please pick at least 3 blocks!' : 'Select'">
                <Icon name="check" />
            </SlottedButton>
        </aside>
    </div>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;
    .overlay__inner {
        @include responsive-width;

        position: relative;
        flex: 1;
        display: flex;
        margin: auto;
    }

    main {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    header {
        @include flex-center;

        width: 100%; height: 40px;
        margin-bottom: 32px;
    }
    section {
        display: flex;
        flex-wrap: wrap;
        width: 100%;
        margin: 4px 4px 20px;
    }

    aside {
        position: absolute;
        top: 0; right: 0;
        display: flex;
        flex-direction: column; align-items: flex-end;
        gap: 4px;
    }

    .block__click-wrap {
        width: fit-content; height: fit-content;
        transition: $TR_regular;

        &:hover, &:focus {
            box-shadow: 0 0 0 4px $white_50, 0 0 8px 4px #0002;
            z-index: 999;
            transition: $TR_fast;

            &:active {
                box-shadow: 0 0 0 2px $white_80, 0 0 4px 4px #0002;

                & .block {
                    transition: $TR_slow;
                    scale: 0.875;
                }
            }
        }

        &:checked .block {
            transition: $TR_slow;
            scale: 0.875;
        }
    }
</style>
