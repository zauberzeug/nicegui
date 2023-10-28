import { p as parser, f as flowDb } from "./flowDb-2e398966.js";
import { f as flowRendererV2, g as flowStyles } from "./styles-8234ce8b.js";
import { t as setConfig } from "./mermaid-f344f6a7.js";
import "./layout-8affc211.js";
import "./index-a53b5366.js";
import "./edges-32b26c0e.js";
import "./createText-53d25889.js";
import "./line-3d4ae7d1.js";
import "./array-b7dcf730.js";
import "./constant-b644328d.js";
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
