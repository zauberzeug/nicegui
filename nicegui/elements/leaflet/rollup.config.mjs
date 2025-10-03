import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";
import copy from "rollup-plugin-copy";

const fixWhitespace = (buffer) => {
  let s = buffer.toString("utf8").replace(/\r\n/g, "\n");
  if (!s.endsWith("\n")) s += "\n";
  return s;
};

export default {
  input: "./src/index.mjs",
  output: {
    dir: "./dist/",
    format: "es",
    sourcemap: true,
  },
  plugins: [
    nodeResolve(),
    terser({ mangle: true }),
    copy({
      targets: [
        { src: "node_modules/leaflet/dist/leaflet.css", dest: "dist/leaflet", transform: fixWhitespace },
        { src: "node_modules/leaflet/dist/images/*", dest: "dist/leaflet/images" },
        { src: "node_modules/leaflet-draw/dist/leaflet.draw.css", dest: "dist/leaflet-draw", transform: fixWhitespace },
        { src: "node_modules/leaflet-draw/dist/images/*", dest: "dist/leaflet-draw/images" },
      ],
    }),
  ],
};
