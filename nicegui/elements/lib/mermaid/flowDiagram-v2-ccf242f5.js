import { p as e, f as o } from "./flowDb-5c3f1e8c.js";
import { f as t, g as a } from "./styles-41b45f07.js";
import { u as s } from "./mermaid-be6aa4a6.js";
import "./layout-b178bd1a.js";
import "./index-745c9ffe.js";
import "./edges-1ceb0db9.js";
import "./createText-7fe61f7a.js";
import "./svgDraw-51404f3b.js";
import "./line-d1abfd73.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
import "./selectAll-b44befab.js";
const A = {
  parser: e,
  db: o,
  renderer: t,
  styles: a,
  init: (r) => {
    r.flowchart || (r.flowchart = {}), r.flowchart.arrowMarkerAbsolute = r.arrowMarkerAbsolute, s({ flowchart: { arrowMarkerAbsolute: r.arrowMarkerAbsolute } }), t.setConf(r.flowchart), o.clear(), o.setGen("gen-2");
  }
};
export {
  A as diagram
};
