import nodeResolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import terser from "@rollup/plugin-terser";
import copy from "rollup-plugin-copy";

export default {
  input: "./src/index.mjs",
  output: {
    dir: "./dist/",
    format: "es",
    sourcemap: true,
  },
  plugins: [
    nodeResolve(),
    commonjs(),
    terser({
      mangle: true,
    }),
    copy({
      targets: [{ src: "node_modules/@xterm/xterm/css/xterm.css", dest: "dist" }],
    }),
  ],
};
