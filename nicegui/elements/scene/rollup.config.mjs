import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";

// HACK: plugin to patch DragControls to handle non-Group objects
const patchDragControls = () => ({
  name: "patch-drag-controls",
  transform(code, id) {
    if (!id.includes("DragControls.js")) return null;
    const searchStr = "_selected = findGroup( _intersections[ 0 ].object )";
    if (!code.includes(searchStr)) throw new Error(`Expected to find "${searchStr}" in DragControls.js`);
    return { code: code.replace(searchStr, searchStr + " || _intersections[ 0 ].object"), map: null };
  },
});

export default {
  input: "./src/index.mjs",
  output: {
    dir: "./dist/",
    format: "es",
    sourcemap: true,
  },
  plugins: [
    nodeResolve(),
    patchDragControls(),
    terser({
      mangle: true,
    }),
  ],
};
