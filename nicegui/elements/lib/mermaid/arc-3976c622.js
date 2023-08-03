import { c as H, p as sn } from "./constant-2fe7eae5.js";
import { aC as en, aD as y, S as ln, aE as M, aF as D, aG as j, aH as b, aI as an, aJ as rn, aK as t, aL as un, aM as on, aN as tn } from "./mermaid-be6aa4a6.js";
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
function pn(l, x, S, E, h, v, J, a) {
  var s = S - l, n = E - x, m = J - h, i = a - v, r = i * s - m * n;
  if (!(r * r < y))
    return r = (m * (x - v) - i * (l - h)) / r, [l + r * s, x + r * n];
}
function V(l, x, S, E, h, v, J) {
  var a = l - S, s = x - E, n = (J ? v : -v) / j(a * a + s * s), m = n * s, i = -n * a, r = l + m, f = x + i, c = S + m, q = E + i, o = (r + c) / 2, w = (f + q) / 2, p = c - r, g = q - f, A = p * p + g * g, C = h - v, P = r * q - c * f, F = (g < 0 ? -1 : 1) * j(tn(0, C * C * A - P * P)), G = (P * g - p * F) / A, d = (-P * p - g * F) / A, R = (P * g + p * F) / A, T = (-P * p + g * F) / A, e = G - o, u = d - w, K = R - o, L = T - w;
  return e * e + u * u > K * K + L * L && (G = R, d = T), {
    cx: G,
    cy: d,
    x01: -m,
    y01: -i,
    x11: G * (h / C - 1),
    y11: d * (h / C - 1)
  };
}
function hn() {
  var l = fn, x = cn, S = H(0), E = null, h = yn, v = gn, J = mn, a = null;
  function s() {
    var n, m, i = +l.apply(this, arguments), r = +x.apply(this, arguments), f = h.apply(this, arguments) - en, c = v.apply(this, arguments) - en, q = an(c - f), o = c > f;
    if (a || (a = n = sn()), r < i && (m = r, r = i, i = m), !(r > y))
      a.moveTo(0, 0);
    else if (q > ln - y)
      a.moveTo(r * M(f), r * D(f)), a.arc(0, 0, r, f, c, !o), i > y && (a.moveTo(i * M(c), i * D(c)), a.arc(0, 0, i, c, f, o));
    else {
      var w = f, p = c, g = f, A = c, C = q, P = q, F = J.apply(this, arguments) / 2, G = F > y && (E ? +E.apply(this, arguments) : j(i * i + r * r)), d = b(an(r - i) / 2, +S.apply(this, arguments)), R = d, T = d, e, u;
      if (G > y) {
        var K = un(G / i * D(F)), L = un(G / r * D(F));
        (C -= K * 2) > y ? (K *= o ? 1 : -1, g += K, A -= K) : (C = 0, g = A = (f + c) / 2), (P -= L * 2) > y ? (L *= o ? 1 : -1, w += L, p -= L) : (P = 0, w = p = (f + c) / 2);
      }
      var N = r * M(w), O = r * D(w), z = i * M(A), B = i * D(A);
      if (d > y) {
        var Q = r * M(p), U = r * D(p), W = i * M(g), X = i * D(g), I;
        if (q < rn && (I = pn(N, O, W, X, Q, U, z, B))) {
          var Y = N - I[0], Z = O - I[1], $ = Q - I[0], k = U - I[1], _ = 1 / D(on((Y * $ + Z * k) / (j(Y * Y + Z * Z) * j($ * $ + k * k))) / 2), nn = j(I[0] * I[0] + I[1] * I[1]);
          R = b(d, (i - nn) / (_ - 1)), T = b(d, (r - nn) / (_ + 1));
        }
      }
      P > y ? T > y ? (e = V(W, X, N, O, r, T, o), u = V(Q, U, z, B, r, T, o), a.moveTo(e.cx + e.x01, e.cy + e.y01), T < d ? a.arc(e.cx, e.cy, T, t(e.y01, e.x01), t(u.y01, u.x01), !o) : (a.arc(e.cx, e.cy, T, t(e.y01, e.x01), t(e.y11, e.x11), !o), a.arc(0, 0, r, t(e.cy + e.y11, e.cx + e.x11), t(u.cy + u.y11, u.cx + u.x11), !o), a.arc(u.cx, u.cy, T, t(u.y11, u.x11), t(u.y01, u.x01), !o))) : (a.moveTo(N, O), a.arc(0, 0, r, w, p, !o)) : a.moveTo(N, O), !(i > y) || !(C > y) ? a.lineTo(z, B) : R > y ? (e = V(z, B, Q, U, i, -R, o), u = V(N, O, W, X, i, -R, o), a.lineTo(e.cx + e.x01, e.cy + e.y01), R < d ? a.arc(e.cx, e.cy, R, t(e.y01, e.x01), t(u.y01, u.x01), !o) : (a.arc(e.cx, e.cy, R, t(e.y01, e.x01), t(e.y11, e.x11), !o), a.arc(0, 0, i, t(e.cy + e.y11, e.cx + e.x11), t(u.cy + u.y11, u.cx + u.x11), o), a.arc(u.cx, u.cy, R, t(u.y11, u.x11), t(u.y01, u.x01), !o))) : a.arc(0, 0, i, A, g, o);
    }
    if (a.closePath(), n)
      return a = null, n + "" || null;
  }
  return s.centroid = function() {
    var n = (+l.apply(this, arguments) + +x.apply(this, arguments)) / 2, m = (+h.apply(this, arguments) + +v.apply(this, arguments)) / 2 - rn / 2;
    return [M(m) * n, D(m) * n];
  }, s.innerRadius = function(n) {
    return arguments.length ? (l = typeof n == "function" ? n : H(+n), s) : l;
  }, s.outerRadius = function(n) {
    return arguments.length ? (x = typeof n == "function" ? n : H(+n), s) : x;
  }, s.cornerRadius = function(n) {
    return arguments.length ? (S = typeof n == "function" ? n : H(+n), s) : S;
  }, s.padRadius = function(n) {
    return arguments.length ? (E = n == null ? null : typeof n == "function" ? n : H(+n), s) : E;
  }, s.startAngle = function(n) {
    return arguments.length ? (h = typeof n == "function" ? n : H(+n), s) : h;
  }, s.endAngle = function(n) {
    return arguments.length ? (v = typeof n == "function" ? n : H(+n), s) : v;
  }, s.padAngle = function(n) {
    return arguments.length ? (J = typeof n == "function" ? n : H(+n), s) : J;
  }, s.context = function(n) {
    return arguments.length ? (a = n ?? null, s) : a;
  }, s;
}
export {
  hn as d
};
