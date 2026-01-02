<template>
    <button>
        <slot />
    </button>
</template>

<style lang="scss" scoped>
    @use '@/assets/variables' as *;

    button {
        appearance: none;
        height: 32px; min-width: 32px;
        padding: 2px;
        border: 2px solid $accent-light_50; border-radius: $BR_regular;
        background-color: $dark_20; color: $white;
        transition: $TR_regular;

        &:disabled {
            border: 4px solid $accent-light_50;
            background-color: $dark_20;
            opacity: .6;
        }

        &.round {
            height: 40px; min-width: 40px;
            border-radius: $BR_round;
        }

        &.trans {
            background-color: $trans;
            border: 0 solid $trans;

            &:disabled {
                opacity: .6;
            }
        }

        &:not(:disabled) {
            &:hover {
                border-color: $accent-light;

                &.trans {
                    background-color: $white_20; border-color: $trans;
                }
            }

            &:focus-visible, &:hover:active {
                padding: 0;
                background-color: $dark_60;
                border: 4px solid $accent-light_50;
                outline: none;
                transition: $TR_fast;

                &.trans {
                    background-color: $white_30;
                    border: 2px solid $white_20;
                    transition: $TR_fast;
                }
            }
        }
    }
</style>
