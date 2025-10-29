import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";

export default {
  input: "./src/index.mjs",
  output: {
    dir: "./dist/",
    format: "es",
    sourcemap: true,
  },
  plugins: [
    nodeResolve(),
    { name: "strip-trailing-whitespace", transform: (code) => ({ code: code.replace(/[ \t]+$/gm, ""), map: null }) },
    terser({
      mangle: true,
    }),
  ],
};
