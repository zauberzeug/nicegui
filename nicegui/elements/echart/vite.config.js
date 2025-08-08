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
  },
  define: { "process.env.NODE_ENV": JSON.stringify("production") },
});
