import {
  stateDb_default,
  stateDiagram_default,
  stateRenderer_v3_unified_default,
  styles_default
} from "./chunk-63NMYVOQ.mjs";
import "./chunk-GVMN75T7.mjs";
import "./chunk-HKQCUR3C.mjs";
import "./chunk-M7N4Q5GZ.mjs";
import "./chunk-C6CSAIDW.mjs";
import "./chunk-KW7S66XI.mjs";
import "./chunk-YP6PVJQ3.mjs";
import "./chunk-I7ZFS43C.mjs";
import "./chunk-GKOISANM.mjs";
import "./chunk-DD37ZF33.mjs";
import "./chunk-HD3LK5B5.mjs";
import {
  __name
} from "./chunk-DLQEHMXD.mjs";

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
