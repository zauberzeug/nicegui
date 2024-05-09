import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";

export default {
  input: "./editor.mjs",
  output: {
    dir: "../../nicegui/elements/lib/codemirror/",
    format: "es",
  },
  plugins: [
    nodeResolve(),
    terser({
      // set this to false to prevent mangling, which can
      // be useful to look at the output code
      mangle: true,
    }),
  ],
};
