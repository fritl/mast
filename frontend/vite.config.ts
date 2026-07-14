import { defineConfig } from 'vite';
import solidPlugin from 'vite-plugin-solid';
import devtools from 'solid-devtools/vite';

export default defineConfig({
    plugins: [devtools(), solidPlugin()],
    server: {
        proxy: {
            "/api": "http://backend:8000"
        },
        port: 5173,
    },
    build: {
        target: 'esnext',
    },
});
