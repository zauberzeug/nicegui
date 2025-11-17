import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  build: {
    lib: {
      entry: "./src/index.js",
      name: "NiceGUIAudio",
      fileName: "audio.build",
      formats: ["es"],
    },
    target: "es2015",
    minify: "terser",
    sourcemap: true,
  },
  define: { "process.env.NODE_ENV": JSON.stringify("production") },
});
