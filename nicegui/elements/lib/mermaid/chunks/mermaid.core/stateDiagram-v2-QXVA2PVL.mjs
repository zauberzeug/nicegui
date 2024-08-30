import {
  stateDb_default,
  stateDiagram_default,
  stateRenderer_v3_unified_default,
  styles_default
} from "./chunk-SVGOEX7Z.mjs";
import "./chunk-FUIDI54P.mjs";
import "./chunk-Z2VRG6XP.mjs";
import "./chunk-T3KDJ7CM.mjs";
import "./chunk-5CZSE4TR.mjs";
import "./chunk-TINLTEC2.mjs";
import "./chunk-OERGPBFJ.mjs";
import "./chunk-VKXSJROQ.mjs";
import {
  __name
} from "./chunk-O2AGWWWV.mjs";

// src/diagrams/state/stateDiagram-v2.ts
var diagram = {
  parser: stateDiagram_default,
  db: stateDb_default,
  renderer: stateRenderer_v3_unified_default,
  styles: styles_default,
  init: /* @__PURE__ */ __name((cnf) => {
    if (!cnf.state) {
      cnf.state = {};
    }
    cnf.state.arrowMarkerAbsolute = cnf.arrowMarkerAbsolute;
    stateDb_default.clear();
  }, "init")
};
export {
  diagram
};
