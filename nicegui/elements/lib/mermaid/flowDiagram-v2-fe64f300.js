import { p as parser, f as flowDb } from "./flowDb-9e6c6aac.js";
import { f as flowRendererV2, a as flowStyles } from "./styles-7882abfe.js";
import { q as setConfig } from "./mermaid-aad43469.js";
import "d3";
import "dagre-d3-es/src/graphlib/index.js";
import "./index-1e7f2254.js";
import "dagre-d3-es/src/dagre/index.js";
import "dagre-d3-es/src/graphlib/json.js";
import "./edges-66ea8538.js";
import "./createText-a49d2d2a.js";
import "mdast-util-from-markdown";
import "ts-dedent";
import "./svgDraw-95adee0a.js";
import "dagre-d3-es/src/dagre-js/label/add-html-label.js";
import "khroma";
import "dayjs";
import "@braintree/sanitize-url";
import "dompurify";
import "lodash-es/memoize.js";
import "stylis";
import "lodash-es/isEmpty.js";
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
