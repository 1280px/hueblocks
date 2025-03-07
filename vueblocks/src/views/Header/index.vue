<script setup>
    import {ref} from 'vue'

    import MessageBox from '@/components/MessageBox.vue'
    // import ModeSwitcher from '@/components/ModeSwitcher.vue'
</script>

<template>
    <main>
        <!-- <h1>HueBlocks</h1>
        <h3>Create beautiful block gradients in a few clicks!</h3> -->
        <h1>hbve public ci/cd test</h1>

        <small>
            <!-- <a href="" @click="">language: en</a> •  -->
            <a href="https://github.com/1280px/hueblocks-new/">source code</a> • 
            <a href="https://github.com/1280px/hueblocks-new/graphs/contributors/">contributors</a> • 
            <a href="https://1280px.github.io/hueblocks">legacy version</a>
        </small>

        <MessageBox :duration="10">
            This is a newer version of HueBlocks, still work in progress and missing some features! <br>
            If you wish to go to original HueBlocks, click "legacy version" link above this message.
        </MessageBox>

        <!-- <ModeSwitcher /> -->
    </main>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    main {
        display: flex; flex-direction: column;
        text-align: center;
        margin: 80px 0 40px;
        gap: 12px;
    }

    box {
        margin-top: 12px;
        border-color: moccasin;
    }

    .warning-enter-active,
    .warning-leave-active {
        transition: opacity $TR_message ease;
    }

    .warning-enter-from,
    .warning-leave-to {
        opacity: 0;
    }
</style>
