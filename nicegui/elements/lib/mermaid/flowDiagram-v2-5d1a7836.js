import { p as e, f as o } from "./flowDb-203d9d78.js";
import { f as t, g as a } from "./styles-081ce523.js";
import { t as s } from "./mermaid-5f2d2ec5.js";
import "./layout-1caf14c9.js";
import "./index-08d47d0a.js";
import "./edges-345e4ceb.js";
import "./createText-56dbee71.js";
import "./line-9d49a987.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
const k = {
  parser: e,
  db: o,
  renderer: t,
  styles: a,
  init: (r) => {
    r.flowchart || (r.flowchart = {}), r.flowchart.arrowMarkerAbsolute = r.arrowMarkerAbsolute, s({ flowchart: { arrowMarkerAbsolute: r.arrowMarkerAbsolute } }), t.setConf(r.flowchart), o.clear(), o.setGen("gen-2");
  }
};
export {
  k as diagram
};
