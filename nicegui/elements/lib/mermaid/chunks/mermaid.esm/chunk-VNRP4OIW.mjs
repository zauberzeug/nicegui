import {
  getConfig2 as getConfig,
  select_default
} from "./chunk-DD37ZF33.mjs";
import {
  __name
} from "./chunk-DLQEHMXD.mjs";

// src/rendering-util/selectSvgElement.ts
var selectSvgElement = /* @__PURE__ */ __name((id) => {
  const { securityLevel } = getConfig();
  let root = select_default("body");
  if (securityLevel === "sandbox") {
    const sandboxElement = select_default(`#i${id}`);
    const doc = sandboxElement.node()?.contentDocument ?? document;
    root = select_default(doc.body);
  }
  const svg = root.select(`#${id}`);
  return svg;
}, "selectSvgElement");

export {
  selectSvgElement
};
