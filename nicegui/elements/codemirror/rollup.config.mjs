import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";

export default {
  input: "./editor.mjs",
  output: {
    dir: "./lib/",
    format: "es",
  },
  plugins: [
    nodeResolve(),
    terser({
      mangle: true,
    }),
  ],
};
