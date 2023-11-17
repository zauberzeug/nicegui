import { c as X, p as sn } from "./constant-2fe7eae5.js";
import { aW as en, aX as j, aY as P, aZ as an, a_ as y, W as ln, a$ as C, b0 as k, b1 as rn, b2 as t, b3 as un, b4 as on, b5 as tn } from "./mermaid-5f2d2ec5.js";
function fn(l) {
  return l.innerRadius;
}
function cn(l) {
  return l.outerRadius;
}
function yn(l) {
  return l.startAngle;
}
function gn(l) {
  return l.endAngle;
}
function mn(l) {
  return l && l.padAngle;
}
function pn(l, x, w, W, h, v, Y, a) {
  var s = w - l, n = W - x, m = Y - h, i = a - v, r = i * s - m * n;
  if (!(r * r < y))
    return r = (m * (x - v) - i * (l - h)) / r, [l + r * s, x + r * n];
}
function K(l, x, w, W, h, v, Y) {
  var a = l - w, s = x - W, n = (Y ? v : -v) / C(a * a + s * s), m = n * s, i = -n * a, r = l + m, f = x + i, c = w + m, D = W + i, o = (r + c) / 2, E = (f + D) / 2, p = c - r, g = D - f, A = p * p + g * g, I = h - v, b = r * D - c * f, O = (g < 0 ? -1 : 1) * C(tn(0, I * I * A - b * b)), S = (b * g - p * O) / A, d = (-b * p - g * O) / A, R = (b * g + p * O) / A, T = (-b * p + g * O) / A, e = S - o, u = d - E, Z = R - o, $ = T - E;
  return e * e + u * u > Z * Z + $ * $ && (S = R, d = T), {
    cx: S,
    cy: d,
    x01: -m,
    y01: -i,
    x11: S * (h / I - 1),
    y11: d * (h / I - 1)
  };
}
function hn() {
  var l = fn, x = cn, w = X(0), W = null, h = yn, v = gn, Y = mn, a = null;
  function s() {
    var n, m, i = +l.apply(this, arguments), r = +x.apply(this, arguments), f = h.apply(this, arguments) - an, c = v.apply(this, arguments) - an, D = rn(c - f), o = c > f;
    if (a || (a = n = sn()), r < i && (m = r, r = i, i = m), !(r > y))
      a.moveTo(0, 0);
    else if (D > ln - y)
      a.moveTo(r * j(f), r * P(f)), a.arc(0, 0, r, f, c, !o), i > y && (a.moveTo(i * j(c), i * P(c)), a.arc(0, 0, i, c, f, o));
    else {
      var E = f, p = c, g = f, A = c, I = D, b = D, O = Y.apply(this, arguments) / 2, S = O > y && (W ? +W.apply(this, arguments) : C(i * i + r * r)), d = k(rn(r - i) / 2, +w.apply(this, arguments)), R = d, T = d, e, u;
      if (S > y) {
        var Z = un(S / i * P(O)), $ = un(S / r * P(O));
        (I -= Z * 2) > y ? (Z *= o ? 1 : -1, g += Z, A -= Z) : (I = 0, g = A = (f + c) / 2), (b -= $ * 2) > y ? ($ *= o ? 1 : -1, E += $, p -= $) : (b = 0, E = p = (f + c) / 2);
      }
      var z = r * j(E), B = r * P(E), F = i * j(A), G = i * P(A);
      if (d > y) {
        var H = r * j(p), J = r * P(p), L = i * j(g), M = i * P(g), q;
        if (D < en && (q = pn(z, B, L, M, H, J, F, G))) {
          var N = z - q[0], Q = B - q[1], U = H - q[0], V = J - q[1], _ = 1 / P(on((N * U + Q * V) / (C(N * N + Q * Q) * C(U * U + V * V))) / 2), nn = C(q[0] * q[0] + q[1] * q[1]);
          R = k(d, (i - nn) / (_ - 1)), T = k(d, (r - nn) / (_ + 1));
        }
      }
      b > y ? T > y ? (e = K(L, M, z, B, r, T, o), u = K(H, J, F, G, r, T, o), a.moveTo(e.cx + e.x01, e.cy + e.y01), T < d ? a.arc(e.cx, e.cy, T, t(e.y01, e.x01), t(u.y01, u.x01), !o) : (a.arc(e.cx, e.cy, T, t(e.y01, e.x01), t(e.y11, e.x11), !o), a.arc(0, 0, r, t(e.cy + e.y11, e.cx + e.x11), t(u.cy + u.y11, u.cx + u.x11), !o), a.arc(u.cx, u.cy, T, t(u.y11, u.x11), t(u.y01, u.x01), !o))) : (a.moveTo(z, B), a.arc(0, 0, r, E, p, !o)) : a.moveTo(z, B), !(i > y) || !(I > y) ? a.lineTo(F, G) : R > y ? (e = K(F, G, H, J, i, -R, o), u = K(z, B, L, M, i, -R, o), a.lineTo(e.cx + e.x01, e.cy + e.y01), R < d ? a.arc(e.cx, e.cy, R, t(e.y01, e.x01), t(u.y01, u.x01), !o) : (a.arc(e.cx, e.cy, R, t(e.y01, e.x01), t(e.y11, e.x11), !o), a.arc(0, 0, i, t(e.cy + e.y11, e.cx + e.x11), t(u.cy + u.y11, u.cx + u.x11), o), a.arc(u.cx, u.cy, R, t(u.y11, u.x11), t(u.y01, u.x01), !o))) : a.arc(0, 0, i, A, g, o);
    }
    if (a.closePath(), n)
      return a = null, n + "" || null;
  }
  return s.centroid = function() {
    var n = (+l.apply(this, arguments) + +x.apply(this, arguments)) / 2, m = (+h.apply(this, arguments) + +v.apply(this, arguments)) / 2 - en / 2;
    return [j(m) * n, P(m) * n];
  }, s.innerRadius = function(n) {
    return arguments.length ? (l = typeof n == "function" ? n : X(+n), s) : l;
  }, s.outerRadius = function(n) {
    return arguments.length ? (x = typeof n == "function" ? n : X(+n), s) : x;
  }, s.cornerRadius = function(n) {
    return arguments.length ? (w = typeof n == "function" ? n : X(+n), s) : w;
  }, s.padRadius = function(n) {
    return arguments.length ? (W = n == null ? null : typeof n == "function" ? n : X(+n), s) : W;
  }, s.startAngle = function(n) {
    return arguments.length ? (h = typeof n == "function" ? n : X(+n), s) : h;
  }, s.endAngle = function(n) {
    return arguments.length ? (v = typeof n == "function" ? n : X(+n), s) : v;
  }, s.padAngle = function(n) {
    return arguments.length ? (Y = typeof n == "function" ? n : X(+n), s) : Y;
  }, s.context = function(n) {
    return arguments.length ? (a = n ?? null, s) : a;
  }, s;
}
export {
  hn as d
};
