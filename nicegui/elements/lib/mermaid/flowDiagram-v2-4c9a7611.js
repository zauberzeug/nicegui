import { p as parser, f as flowDb } from "./flowDb-88762a1f.js";
import { f as flowRendererV2, a as flowStyles } from "./styles-4fe3d1fc.js";
import { f as setConfig } from "./config-389b86ff.js";
import "d3";
import "./utils-d5eeff82.js";
import "@braintree/sanitize-url";
import "./setupGraphViewbox-e35e4124.js";
import "./commonDb-2ace122b.js";
import "lodash-es/memoize.js";
import "./mermaidAPI-0716c7c2.js";
import "stylis";
import "./errorRenderer-d05351b9.js";
import "dompurify";
import "lodash-es/isEmpty.js";
import "dagre-d3-es/src/graphlib/index.js";
import "./index-f9d09cc9.js";
import "dagre-d3-es/src/dagre/index.js";
import "dagre-d3-es/src/graphlib/json.js";
import "./edges-65da65dc.js";
import "./svgDraw-6a237a99.js";
import "dagre-d3-es/src/dagre-js/label/add-html-label.js";
import "dayjs";
import "khroma";
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
//# sourceMappingURL=flowDiagram-v2-4c9a7611.js.map
