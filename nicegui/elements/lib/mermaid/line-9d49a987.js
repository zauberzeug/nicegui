import { a } from "./array-2ff2c7a6.js";
import { c as o, p as d } from "./constant-2fe7eae5.js";
import { n as h } from "./mermaid-5f2d2ec5.js";
function v(e) {
  return e[0];
}
function b(e) {
  return e[1];
}
function S(e, u) {
  var p = o(!0), i = null, l = h, r = null;
  e = typeof e == "function" ? e : e === void 0 ? v : o(e), u = typeof u == "function" ? u : u === void 0 ? b : o(u);
  function t(n) {
    var f, m = (n = a(n)).length, s, c = !1, g;
    for (i == null && (r = l(g = d())), f = 0; f <= m; ++f)
      !(f < m && p(s = n[f], f, n)) === c && ((c = !c) ? r.lineStart() : r.lineEnd()), c && r.point(+e(s, f, n), +u(s, f, n));
    if (g)
      return r = null, g + "" || null;
  }
  return t.x = function(n) {
    return arguments.length ? (e = typeof n == "function" ? n : o(+n), t) : e;
  }, t.y = function(n) {
    return arguments.length ? (u = typeof n == "function" ? n : o(+n), t) : u;
  }, t.defined = function(n) {
    return arguments.length ? (p = typeof n == "function" ? n : o(!!n), t) : p;
  }, t.curve = function(n) {
    return arguments.length ? (l = n, i != null && (r = l(i)), t) : l;
  }, t.context = function(n) {
    return arguments.length ? (n == null ? i = r = null : r = l(i = n), t) : i;
  }, t;
}
export {
  S as l
};
