import { defineConfig } from "vite";

export default defineConfig({
  build: {
    lib: {
      entry: "./src/index.mjs",
      name: "NiceGUIEChart",
      fileName: "index",
      formats: ["es"],
    },
    target: "es2015",
    minify: "terser",
    sourcemap: true,
  },
  define: { "process.env.NODE_ENV": JSON.stringify("production") },
});
