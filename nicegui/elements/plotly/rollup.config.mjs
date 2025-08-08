import nodeResolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import terser from "@rollup/plugin-terser";

export default {
  input: "./src/index.mjs",
  output: {
    dir: "./dist/",
    format: "es",
  },
  plugins: [
    nodeResolve({
      preferBuiltins: false,
      browser: true,
    }),
    commonjs({
      include: ["node_modules/**"],
    }),
    terser({
      mangle: true,
    }),
  ],
};
