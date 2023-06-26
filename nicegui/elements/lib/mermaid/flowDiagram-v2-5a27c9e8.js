import { p as parser, f as flowDb } from "./add-html-label-3fd8c466.js";
import { f as flowRendererV2, a as flowStyles } from "./styles-719792c5.js";
import { h as setConfig } from "./config-b4fa35bb.js";
import "./utils-872dfc50.js";
import "./setupGraphViewbox-16a0ba81.js";
import "./commonDb-7f40ab5a.js";
import "./mermaidAPI-6f22a815.js";
import "./errorRenderer-ebf63d74.js";
import "./isPlainObject-91dd8bc9.js";
import "./array-b7dcf730.js";
import "./constant-b644328d.js";
import "./layout-4663fc19.js";
import "./index-a1a98052.js";
import "./edges-62a01f73.js";
import "./svgDraw-9e97e6db.js";
import "./selectAll-b147441f.js";
const diagram = {
  parser,
  db: flowDb,
  renderer: flowRendererV2,
  styles: flowStyles,
  init: (cnf) => {
    if (!cnf.flowchart) {
      cnf.flowchart = {};
    }
    cnf.flowchart.arrowMarkerAbsolute = cnf.arrowMarkerAbsolute;
    setConfig({ flowchart: { arrowMarkerAbsolute: cnf.arrowMarkerAbsolute } });
    flowRendererV2.setConf(cnf.flowchart);
    flowDb.clear();
    flowDb.setGen("gen-2");
  }
};
export {
  diagram
};
//# sourceMappingURL=flowDiagram-v2-5a27c9e8.js.map
