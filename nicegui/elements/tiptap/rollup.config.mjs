import nodeResolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';

export default {
  input: './src/index.mjs',
  output: {
    dir: './dist/',
    format: 'es',
    sourcemap: true,
    entryFileNames: 'index.js',
  },
  plugins: [
    nodeResolve({ browser: true, preferBuiltins: false }),
    commonjs(),
    terser({ mangle: true }),
  ],
};
