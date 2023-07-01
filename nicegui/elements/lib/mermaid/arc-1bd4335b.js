import { c as Q, p as sn } from "./constant-2fe7eae5.js";
import { J as en, K as X, N as I, O as rn, P as y, I as ln, Q as z, R as b, T as un, V as t, W as an, X as on, Y as tn } from "./utils-aa888deb.js";
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
function pn(l, x, w, O, h, v, S, r) {
  var s = w - l, n = O - x, m = S - h, i = r - v, u = i * s - m * n;
  if (!(u * u < y))
    return u = (m * (x - v) - i * (l - h)) / u, [l + u * s, x + u * n];
}
function H(l, x, w, O, h, v, S) {
  var r = l - w, s = x - O, n = (S ? v : -v) / z(r * r + s * s), m = n * s, i = -n * r, u = l + m, f = x + i, c = w + m, D = O + i, o = (u + c) / 2, E = (f + D) / 2, p = c - u, g = D - f, R = p * p + g * g, J = h - v, P = u * D - c * f, K = (g < 0 ? -1 : 1) * z(tn(0, J * J * R - P * P)), N = (P * g - p * K) / R, d = (-P * p - g * K) / R, A = (P * g + p * K) / R, T = (-P * p + g * K) / R, e = N - o, a = d - E, V = A - o, W = T - E;
  return e * e + a * a > V * V + W * W && (N = A, d = T), {
    cx: N,
    cy: d,
    x01: -m,
    y01: -i,
    x11: N * (h / J - 1),
    y11: d * (h / J - 1)
  };
}
function hn() {
  var l = fn, x = cn, w = Q(0), O = null, h = yn, v = gn, S = mn, r = null;
  function s() {
    var n, m, i = +l.apply(this, arguments), u = +x.apply(this, arguments), f = h.apply(this, arguments) - rn, c = v.apply(this, arguments) - rn, D = un(c - f), o = c > f;
    if (r || (r = n = sn()), u < i && (m = u, u = i, i = m), !(u > y))
      r.moveTo(0, 0);
    else if (D > ln - y)
      r.moveTo(u * X(f), u * I(f)), r.arc(0, 0, u, f, c, !o), i > y && (r.moveTo(i * X(c), i * I(c)), r.arc(0, 0, i, c, f, o));
    else {
      var E = f, p = c, g = f, R = c, J = D, P = D, K = S.apply(this, arguments) / 2, N = K > y && (O ? +O.apply(this, arguments) : z(i * i + u * u)), d = b(un(u - i) / 2, +w.apply(this, arguments)), A = d, T = d, e, a;
      if (N > y) {
        var V = an(N / i * I(K)), W = an(N / u * I(K));
        (J -= V * 2) > y ? (V *= o ? 1 : -1, g += V, R -= V) : (J = 0, g = R = (f + c) / 2), (P -= W * 2) > y ? (W *= o ? 1 : -1, E += W, p -= W) : (P = 0, E = p = (f + c) / 2);
      }
      var Y = u * X(E), j = u * I(E), B = i * X(R), C = i * I(R);
      if (d > y) {
        var F = u * X(p), G = u * I(p), L = i * X(g), M = i * I(g), q;
        if (D < en && (q = pn(Y, j, L, M, F, G, B, C))) {
          var U = Y - q[0], Z = j - q[1], $ = F - q[0], k = G - q[1], _ = 1 / I(on((U * $ + Z * k) / (z(U * U + Z * Z) * z($ * $ + k * k))) / 2), nn = z(q[0] * q[0] + q[1] * q[1]);
          A = b(d, (i - nn) / (_ - 1)), T = b(d, (u - nn) / (_ + 1));
        }
      }
      P > y ? T > y ? (e = H(L, M, Y, j, u, T, o), a = H(F, G, B, C, u, T, o), r.moveTo(e.cx + e.x01, e.cy + e.y01), T < d ? r.arc(e.cx, e.cy, T, t(e.y01, e.x01), t(a.y01, a.x01), !o) : (r.arc(e.cx, e.cy, T, t(e.y01, e.x01), t(e.y11, e.x11), !o), r.arc(0, 0, u, t(e.cy + e.y11, e.cx + e.x11), t(a.cy + a.y11, a.cx + a.x11), !o), r.arc(a.cx, a.cy, T, t(a.y11, a.x11), t(a.y01, a.x01), !o))) : (r.moveTo(Y, j), r.arc(0, 0, u, E, p, !o)) : r.moveTo(Y, j), !(i > y) || !(J > y) ? r.lineTo(B, C) : A > y ? (e = H(B, C, F, G, i, -A, o), a = H(Y, j, L, M, i, -A, o), r.lineTo(e.cx + e.x01, e.cy + e.y01), A < d ? r.arc(e.cx, e.cy, A, t(e.y01, e.x01), t(a.y01, a.x01), !o) : (r.arc(e.cx, e.cy, A, t(e.y01, e.x01), t(e.y11, e.x11), !o), r.arc(0, 0, i, t(e.cy + e.y11, e.cx + e.x11), t(a.cy + a.y11, a.cx + a.x11), o), r.arc(a.cx, a.cy, A, t(a.y11, a.x11), t(a.y01, a.x01), !o))) : r.arc(0, 0, i, R, g, o);
    }
    if (r.closePath(), n)
      return r = null, n + "" || null;
  }
  return s.centroid = function() {
    var n = (+l.apply(this, arguments) + +x.apply(this, arguments)) / 2, m = (+h.apply(this, arguments) + +v.apply(this, arguments)) / 2 - en / 2;
    return [X(m) * n, I(m) * n];
  }, s.innerRadius = function(n) {
    return arguments.length ? (l = typeof n == "function" ? n : Q(+n), s) : l;
  }, s.outerRadius = function(n) {
    return arguments.length ? (x = typeof n == "function" ? n : Q(+n), s) : x;
  }, s.cornerRadius = function(n) {
    return arguments.length ? (w = typeof n == "function" ? n : Q(+n), s) : w;
  }, s.padRadius = function(n) {
    return arguments.length ? (O = n == null ? null : typeof n == "function" ? n : Q(+n), s) : O;
  }, s.startAngle = function(n) {
    return arguments.length ? (h = typeof n == "function" ? n : Q(+n), s) : h;
  }, s.endAngle = function(n) {
    return arguments.length ? (v = typeof n == "function" ? n : Q(+n), s) : v;
  }, s.padAngle = function(n) {
    return arguments.length ? (S = typeof n == "function" ? n : Q(+n), s) : S;
  }, s.context = function(n) {
    return arguments.length ? (r = n ?? null, s) : r;
  }, s;
}
export {
  hn as d
};
//# sourceMappingURL=arc-1bd4335b.js.map
