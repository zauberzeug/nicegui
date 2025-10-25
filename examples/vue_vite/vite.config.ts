import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import checker from 'vite-plugin-checker';

export default defineConfig({
  plugins: [
    vue({}),
    checker({ vueTsc: true, typescript: true })
  ],
  build: {
    cssCodeSplit: true,
    outDir: './vue_vite/components',
    lib: {
      entry: {
        'CounterOptions': './js/CounterOptions.vue',
        'CounterComposition': './js/CounterComposition.vue',
      },
      formats: ['es'],
      fileName: (format, entryName) => `${entryName}.js`,
      name: 'vue_vite',
    },
    minify: false,
    rollupOptions: {
      external: ['vue'],
      output: {
        entryFileNames: `[name].js`,
        chunkFileNames: `[name].js`,
        assetFileNames: `[name].[ext]`,
      },
    },
  }
});
