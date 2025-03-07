<template>
    <button>
        <slot></slot>
    </button>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    button {
        appearance: none;
        height: 32px; min-width: 32px;
        border: 2px solid $accent-light_50; border-radius: $BR_regular;

        &.round {
            height: 40px; min-width: 40px;
            border-radius: $BR_round;
        }

        &.trans {
            background-color: $trans;
            border: 0 solid $trans;
        }

        background-color: $dark_20; color: $white;
        transition: $TR_regular;

        &:hover {
        	border-color: $accent-light;

            &.trans {
                background-color: $white_20;
                border-color: $trans;
            }

            &:active {
                border: 4px solid $accent-light_50;
                background-color: $dark_60;
                transition: $TR_fast;

                &.trans {
                    background-color: $white_30;
                    border: 2px solid $white_20;
                }
            }
        }
    }
</style>
