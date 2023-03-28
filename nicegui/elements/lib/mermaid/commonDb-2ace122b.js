import { b as sanitizeText$1, g as getConfig } from "./config-389b86ff.js";
let title = "";
let diagramTitle = "";
let description = "";
const sanitizeText = (txt) => sanitizeText$1(txt, getConfig());
const clear = function() {
  title = "";
  description = "";
  diagramTitle = "";
};
const setAccTitle = function(txt) {
  title = sanitizeText(txt).replace(/^\s+/g, "");
};
const getAccTitle = function() {
  return title || diagramTitle;
};
const setAccDescription = function(txt) {
  description = sanitizeText(txt).replace(/\n\s+/g, "\n");
};
const getAccDescription = function() {
  return description;
};
const setDiagramTitle = function(txt) {
  diagramTitle = sanitizeText(txt);
};
const getDiagramTitle = function() {
  return diagramTitle;
};
const commonDb = {
  setAccTitle,
  getAccTitle,
  setDiagramTitle,
  getDiagramTitle,
  getAccDescription,
  setAccDescription,
  clear
};
const commonDb$1 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  clear,
  default: commonDb,
  getAccDescription,
  getAccTitle,
  getDiagramTitle,
  setAccDescription,
  setAccTitle,
  setDiagramTitle
}, Symbol.toStringTag, { value: "Module" }));
export {
  getAccDescription as a,
  setAccDescription as b,
  commonDb$1 as c,
  setDiagramTitle as d,
  getDiagramTitle as e,
  clear as f,
  getAccTitle as g,
  setAccTitle as s
};
//# sourceMappingURL=commonDb-2ace122b.js.map
