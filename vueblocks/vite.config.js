import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig(({ mode }) => ({
    plugins: [
        vue(),
        vueDevTools(),
    ],
    // Use base URL for GH Pages deploy, do not use it otherwise
    base: mode === 'development' ? '/' : '/hueblocks',
    publicDir: 'data',
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
}))
