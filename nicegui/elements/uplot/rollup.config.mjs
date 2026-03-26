import nodeResolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import terser from "@rollup/plugin-terser";
import postcss from 'rollup-plugin-postcss';

export default {
  input: "./src/index.mjs",
  output: {
    dir: './dist/',
    format: 'es',
    sourcemap: true,
  },
  plugins: [
    nodeResolve(),
    commonjs(),
    postcss(),
    terser({
      mangle: true,
    }),
  ],
};
