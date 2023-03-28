import { a as m } from "./array-2ff2c7a6.js";
import { c, p as v } from "./constant-2fe7eae5.js";
import { x as j, h } from "./utils-aa888deb.js";
import { o as O, i as y } from "./mermaidAPI-04b5c286.js";
function P(n) {
  return n[0];
}
function d(n) {
  return n[1];
}
function z(n, r) {
  var o = c(!0), f = null, l = j, u = null;
  n = typeof n == "function" ? n : n === void 0 ? P : c(n), r = typeof r == "function" ? r : r === void 0 ? d : c(r);
  function e(t) {
    var i, g = (t = m(t)).length, s, a = !1, p;
    for (f == null && (u = l(p = v())), i = 0; i <= g; ++i)
      !(i < g && o(s = t[i], i, t)) === a && ((a = !a) ? u.lineStart() : u.lineEnd()), a && u.point(+n(s, i, t), +r(s, i, t));
    if (p)
      return u = null, p + "" || null;
  }
  return e.x = function(t) {
    return arguments.length ? (n = typeof t == "function" ? t : c(+t), e) : n;
  }, e.y = function(t) {
    return arguments.length ? (r = typeof t == "function" ? t : c(+t), e) : r;
  }, e.defined = function(t) {
    return arguments.length ? (o = typeof t == "function" ? t : c(!!t), e) : o;
  }, e.curve = function(t) {
    return arguments.length ? (l = t, f != null && (u = l(f)), e) : l;
  }, e.context = function(t) {
    return arguments.length ? (t == null ? f = u = null : u = l(f = t), e) : f;
  }, e;
}
var S = O(Object.getPrototypeOf, Object);
const T = S;
var w = "[object Object]", C = Function.prototype, L = Object.prototype, b = C.toString, k = L.hasOwnProperty, A = b.call(Object);
function B(n) {
  if (!y(n) || h(n) != w)
    return !1;
  var r = T(n);
  if (r === null)
    return !0;
  var o = k.call(r, "constructor") && r.constructor;
  return typeof o == "function" && o instanceof o && b.call(o) == A;
}
export {
  T as g,
  B as i,
  z as l
};
//# sourceMappingURL=isPlainObject-a5cb4071.js.map
