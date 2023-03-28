import { b as f, g as m } from "./config-e567ef17.js";
let n = "", e = "", c = "";
const o = (t) => f(t, m()), s = function() {
  n = "", c = "", e = "";
}, i = function(t) {
  n = o(t).replace(/^\s+/g, "");
}, a = function() {
  return n || e;
}, r = function(t) {
  c = o(t).replace(/\n\s+/g, `
`);
}, l = function() {
  return c;
}, g = function(t) {
  e = o(t);
}, u = function() {
  return e;
}, p = {
  setAccTitle: i,
  getAccTitle: a,
  setDiagramTitle: g,
  getDiagramTitle: u,
  getAccDescription: l,
  setAccDescription: r,
  clear: s
}, b = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  clear: s,
  default: p,
  getAccDescription: l,
  getAccTitle: a,
  getDiagramTitle: u,
  setAccDescription: r,
  setAccTitle: i,
  setDiagramTitle: g
}, Symbol.toStringTag, { value: "Module" }));
export {
  l as a,
  r as b,
  b as c,
  g as d,
  u as e,
  s as f,
  a as g,
  i as s
};
//# sourceMappingURL=commonDb-4dc3d465.js.map
