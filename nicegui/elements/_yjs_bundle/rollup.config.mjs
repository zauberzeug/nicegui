import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";

export default {
  input: "./src/yjs.mjs",
  output: { dir: "./dist/", format: "es", sourcemap: true, entryFileNames: "index.js" },
  plugins: [nodeResolve(), terser({ mangle: true })],
};
