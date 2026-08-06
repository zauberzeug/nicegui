import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";

export default {
  input: "./src/index.mjs",
  output: {
    dir: "./dist/",
    format: "es",
    sourcemap: true,
  },
  // yjs core resolved at runtime via NiceGUI's shared _yjs_bundle ESM module.
  external: ["yjs"],
  plugins: [
    nodeResolve(),
    terser({
      mangle: true,
    }),
  ],
};
