import {
  __name,
  getConfig2 as getConfig
} from "./chunk-O2AGWWWV.mjs";

// src/rendering-util/selectSvgElement.ts
import { select } from "d3";
var selectSvgElement = /* @__PURE__ */ __name((id) => {
  const { securityLevel } = getConfig();
  let root = select("body");
  if (securityLevel === "sandbox") {
    const sandboxElement = select(`#i${id}`);
    const doc = sandboxElement.node()?.contentDocument ?? document;
    root = select(doc.body);
  }
  const svg = root.select(`#${id}`);
  return svg;
}, "selectSvgElement");

export {
  selectSvgElement
};
