import { l as h } from "./config-e567ef17.js";
const a = function(n, o) {
  for (let t of o)
    n.attr(t[0], t[1]);
}, x = function(n, o, t) {
  let s = /* @__PURE__ */ new Map();
  return t ? (s.set("width", "100%"), s.set("style", `max-width: ${o}px;`)) : (s.set("height", n), s.set("width", o)), s;
}, $ = function(n, o, t, s) {
  const e = x(o, t, s);
  a(n, e);
}, w = function(n, o, t, s) {
  const e = o.node().getBBox(), r = e.width, u = e.height;
  h.info(`SVG bounds: ${r}x${u}`, e);
  let i = 0, c = 0;
  h.info(`Graph bounds: ${i}x${c}`, n), i = r + t * 2, c = u + t * 2, h.info(`Calculated bounds: ${i}x${c}`), $(o, c, i, s);
  const f = `${e.x - t} ${e.y - t} ${e.width + 2 * t} ${e.height + 2 * t}`;
  o.attr("viewBox", f);
};
export {
  $ as c,
  w as s
};
//# sourceMappingURL=setupGraphViewbox-a4603a92.js.map
