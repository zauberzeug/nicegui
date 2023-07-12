import { p as parser, f as flowDb } from "./flowDb-cec399e2.js";
import { f as flowRendererV2, g as flowStyles } from "./styles-452f304a.js";
import { u as setConfig } from "./mermaid-bf016224.js";
import "./layout-de394db2.js";
import "./index-e316e81a.js";
import "./edges-1a997dfb.js";
import "./createText-f11497a7.js";
import "./svgDraw-3835dd7e.js";
import "./line-cdde0d11.js";
import "./array-b7dcf730.js";
import "./constant-b644328d.js";
import "./selectAll-8725692e.js";
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
