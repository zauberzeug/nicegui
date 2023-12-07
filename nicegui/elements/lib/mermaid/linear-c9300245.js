import { a0 as cn, a1 as D, a2 as Y, a3 as Z, a4 as hn } from "./mermaid-5f2d2ec5.js";
import { i as sn } from "./init-f9637058.js";
function $(n, t) {
  return n == null || t == null ? NaN : n < t ? -1 : n > t ? 1 : n >= t ? 0 : NaN;
}
function mn(n, t) {
  return n == null || t == null ? NaN : t < n ? -1 : t > n ? 1 : t >= n ? 0 : NaN;
}
function nn(n) {
  let t, e, r;
  n.length !== 2 ? (t = $, e = (u, h) => $(n(u), h), r = (u, h) => n(u) - h) : (t = n === $ || n === mn ? n : ln, e = n, r = n);
  function i(u, h, f = 0, l = u.length) {
    if (f < l) {
      if (t(h, h) !== 0)
        return l;
      do {
        const c = f + l >>> 1;
        e(u[c], h) < 0 ? f = c + 1 : l = c;
      } while (f < l);
    }
    return f;
  }
  function a(u, h, f = 0, l = u.length) {
    if (f < l) {
      if (t(h, h) !== 0)
        return l;
      do {
        const c = f + l >>> 1;
        e(u[c], h) <= 0 ? f = c + 1 : l = c;
      } while (f < l);
    }
    return f;
  }
  function o(u, h, f = 0, l = u.length) {
    const c = i(u, h, f, l - 1);
    return c > f && r(u[c - 1], h) > -r(u[c], h) ? c - 1 : c;
  }
  return { left: i, center: o, right: a };
}
function ln() {
  return 0;
}
function dn(n) {
  return n === null ? NaN : +n;
}
const gn = nn($), Mn = gn.right;
nn(dn).center;
const yn = Mn;
var T = Math.sqrt(50), I = Math.sqrt(10), q = Math.sqrt(2);
function pn(n, t, e) {
  var r, i = -1, a, o, u;
  if (t = +t, n = +n, e = +e, n === t && e > 0)
    return [n];
  if ((r = t < n) && (a = n, n = t, t = a), (u = tn(n, t, e)) === 0 || !isFinite(u))
    return [];
  if (u > 0) {
    let h = Math.round(n / u), f = Math.round(t / u);
    for (h * u < n && ++h, f * u > t && --f, o = new Array(a = f - h + 1); ++i < a; )
      o[i] = (h + i) * u;
  } else {
    u = -u;
    let h = Math.round(n * u), f = Math.round(t * u);
    for (h / u < n && ++h, f / u > t && --f, o = new Array(a = f - h + 1); ++i < a; )
      o[i] = (h + i) / u;
  }
  return r && o.reverse(), o;
}
function tn(n, t, e) {
  var r = (t - n) / Math.max(0, e), i = Math.floor(Math.log(r) / Math.LN10), a = r / Math.pow(10, i);
  return i >= 0 ? (a >= T ? 10 : a >= I ? 5 : a >= q ? 2 : 1) * Math.pow(10, i) : -Math.pow(10, -i) / (a >= T ? 10 : a >= I ? 5 : a >= q ? 2 : 1);
}
function wn(n, t, e) {
  var r = Math.abs(t - n) / Math.max(0, e), i = Math.pow(10, Math.floor(Math.log(r) / Math.LN10)), a = r / i;
  return a >= T ? i *= 10 : a >= I ? i *= 5 : a >= q && (i *= 2), t < n ? -i : i;
}
function Nn(n, t) {
  t || (t = []);
  var e = n ? Math.min(t.length, n.length) : 0, r = t.slice(), i;
  return function(a) {
    for (i = 0; i < e; ++i)
      r[i] = n[i] * (1 - a) + t[i] * a;
    return r;
  };
}
function kn(n) {
  return ArrayBuffer.isView(n) && !(n instanceof DataView);
}
function vn(n, t) {
  var e = t ? t.length : 0, r = n ? Math.min(e, n.length) : 0, i = new Array(r), a = new Array(e), o;
  for (o = 0; o < r; ++o)
    i[o] = B(n[o], t[o]);
  for (; o < e; ++o)
    a[o] = t[o];
  return function(u) {
    for (o = 0; o < r; ++o)
      a[o] = i[o](u);
    return a;
  };
}
function xn(n, t) {
  var e = /* @__PURE__ */ new Date();
  return n = +n, t = +t, function(r) {
    return e.setTime(n * (1 - r) + t * r), e;
  };
}
function An(n, t) {
  var e = {}, r = {}, i;
  (n === null || typeof n != "object") && (n = {}), (t === null || typeof t != "object") && (t = {});
  for (i in t)
    i in n ? e[i] = B(n[i], t[i]) : r[i] = t[i];
  return function(a) {
    for (i in e)
      r[i] = e[i](a);
    return r;
  };
}
function B(n, t) {
  var e = typeof t, r;
  return t == null || e === "boolean" ? cn(t) : (e === "number" ? D : e === "string" ? (r = Y(t)) ? (t = r, Z) : hn : t instanceof Y ? Z : t instanceof Date ? xn : kn(t) ? Nn : Array.isArray(t) ? vn : typeof t.valueOf != "function" && typeof t.toString != "function" || isNaN(t) ? An : D)(n, t);
}
function Sn(n, t) {
  return n = +n, t = +t, function(e) {
    return Math.round(n * (1 - e) + t * e);
  };
}
function bn(n) {
  return Math.abs(n = Math.round(n)) >= 1e21 ? n.toLocaleString("en").replace(/,/g, "") : n.toString(10);
}
function R(n, t) {
  if ((e = (n = t ? n.toExponential(t - 1) : n.toExponential()).indexOf("e")) < 0)
    return null;
  var e, r = n.slice(0, e);
  return [
    r.length > 1 ? r[0] + r.slice(2) : r,
    +n.slice(e + 1)
  ];
}
function A(n) {
  return n = R(Math.abs(n)), n ? n[1] : NaN;
}
function jn(n, t) {
  return function(e, r) {
    for (var i = e.length, a = [], o = 0, u = n[0], h = 0; i > 0 && u > 0 && (h + u + 1 > r && (u = Math.max(1, r - h)), a.push(e.substring(i -= u, i + u)), !((h += u + 1) > r)); )
      u = n[o = (o + 1) % n.length];
    return a.reverse().join(t);
  };
}
function Pn(n) {
  return function(t) {
    return t.replace(/[0-9]/g, function(e) {
      return n[+e];
    });
  };
}
var zn = /^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$/i;
function E(n) {
  if (!(t = zn.exec(n)))
    throw new Error("invalid format: " + n);
  var t;
  return new G({
    fill: t[1],
    align: t[2],
    sign: t[3],
    symbol: t[4],
    zero: t[5],
    width: t[6],
    comma: t[7],
    precision: t[8] && t[8].slice(1),
    trim: t[9],
    type: t[10]
  });
}
E.prototype = G.prototype;
function G(n) {
  this.fill = n.fill === void 0 ? " " : n.fill + "", this.align = n.align === void 0 ? ">" : n.align + "", this.sign = n.sign === void 0 ? "-" : n.sign + "", this.symbol = n.symbol === void 0 ? "" : n.symbol + "", this.zero = !!n.zero, this.width = n.width === void 0 ? void 0 : +n.width, this.comma = !!n.comma, this.precision = n.precision === void 0 ? void 0 : +n.precision, this.trim = !!n.trim, this.type = n.type === void 0 ? "" : n.type + "";
}
G.prototype.toString = function() {
  return this.fill + this.align + this.sign + this.symbol + (this.zero ? "0" : "") + (this.width === void 0 ? "" : Math.max(1, this.width | 0)) + (this.comma ? "," : "") + (this.precision === void 0 ? "" : "." + Math.max(0, this.precision | 0)) + (this.trim ? "~" : "") + this.type;
};
function Fn(n) {
  n:
    for (var t = n.length, e = 1, r = -1, i; e < t; ++e)
      switch (n[e]) {
        case ".":
          r = i = e;
          break;
        case "0":
          r === 0 && (r = e), i = e;
          break;
        default:
          if (!+n[e])
            break n;
          r > 0 && (r = 0);
          break;
      }
  return r > 0 ? n.slice(0, r) + n.slice(i + 1) : n;
}
var rn;
function $n(n, t) {
  var e = R(n, t);
  if (!e)
    return n + "";
  var r = e[0], i = e[1], a = i - (rn = Math.max(-8, Math.min(8, Math.floor(i / 3))) * 3) + 1, o = r.length;
  return a === o ? r : a > o ? r + new Array(a - o + 1).join("0") : a > 0 ? r.slice(0, a) + "." + r.slice(a) : "0." + new Array(1 - a).join("0") + R(n, Math.max(0, t + a - 1))[0];
}
function H(n, t) {
  var e = R(n, t);
  if (!e)
    return n + "";
  var r = e[0], i = e[1];
  return i < 0 ? "0." + new Array(-i).join("0") + r : r.length > i + 1 ? r.slice(0, i + 1) + "." + r.slice(i + 1) : r + new Array(i - r.length + 2).join("0");
}
const J = {
  "%": (n, t) => (n * 100).toFixed(t),
  b: (n) => Math.round(n).toString(2),
  c: (n) => n + "",
  d: bn,
  e: (n, t) => n.toExponential(t),
  f: (n, t) => n.toFixed(t),
  g: (n, t) => n.toPrecision(t),
  o: (n) => Math.round(n).toString(8),
  p: (n, t) => H(n * 100, t),
  r: H,
  s: $n,
  X: (n) => Math.round(n).toString(16).toUpperCase(),
  x: (n) => Math.round(n).toString(16)
};
function K(n) {
  return n;
}
var Q = Array.prototype.map, W = ["y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"];
function Rn(n) {
  var t = n.grouping === void 0 || n.thousands === void 0 ? K : jn(Q.call(n.grouping, Number), n.thousands + ""), e = n.currency === void 0 ? "" : n.currency[0] + "", r = n.currency === void 0 ? "" : n.currency[1] + "", i = n.decimal === void 0 ? "." : n.decimal + "", a = n.numerals === void 0 ? K : Pn(Q.call(n.numerals, String)), o = n.percent === void 0 ? "%" : n.percent + "", u = n.minus === void 0 ? "−" : n.minus + "", h = n.nan === void 0 ? "NaN" : n.nan + "";
  function f(c) {
    c = E(c);
    var m = c.fill, p = c.align, M = c.sign, S = c.symbol, k = c.zero, b = c.width, L = c.comma, w = c.precision, O = c.trim, d = c.type;
    d === "n" ? (L = !0, d = "g") : J[d] || (w === void 0 && (w = 12), O = !0, d = "g"), (k || m === "0" && p === "=") && (k = !0, m = "0", p = "=");
    var on = S === "$" ? e : S === "#" && /[boxX]/.test(d) ? "0" + d.toLowerCase() : "", un = S === "$" ? r : /[%p]/.test(d) ? o : "", V = J[d], fn = /[defgprs%]/.test(d);
    w = w === void 0 ? 6 : /[gprs]/.test(d) ? Math.max(1, Math.min(21, w)) : Math.max(0, Math.min(20, w));
    function X(s) {
      var N = on, g = un, v, U, j;
      if (d === "c")
        g = V(s) + g, s = "";
      else {
        s = +s;
        var P = s < 0 || 1 / s < 0;
        if (s = isNaN(s) ? h : V(Math.abs(s), w), O && (s = Fn(s)), P && +s == 0 && M !== "+" && (P = !1), N = (P ? M === "(" ? M : u : M === "-" || M === "(" ? "" : M) + N, g = (d === "s" ? W[8 + rn / 3] : "") + g + (P && M === "(" ? ")" : ""), fn) {
          for (v = -1, U = s.length; ++v < U; )
            if (j = s.charCodeAt(v), 48 > j || j > 57) {
              g = (j === 46 ? i + s.slice(v + 1) : s.slice(v)) + g, s = s.slice(0, v);
              break;
            }
        }
      }
      L && !k && (s = t(s, 1 / 0));
      var z = N.length + s.length + g.length, y = z < b ? new Array(b - z + 1).join(m) : "";
      switch (L && k && (s = t(y + s, y.length ? b - g.length : 1 / 0), y = ""), p) {
        case "<":
          s = N + s + g + y;
          break;
        case "=":
          s = N + y + s + g;
          break;
        case "^":
          s = y.slice(0, z = y.length >> 1) + N + s + g + y.slice(z);
          break;
        default:
          s = y + N + s + g;
          break;
      }
      return a(s);
    }
    return X.toString = function() {
      return c + "";
    }, X;
  }
  function l(c, m) {
    var p = f((c = E(c), c.type = "f", c)), M = Math.max(-8, Math.min(8, Math.floor(A(m) / 3))) * 3, S = Math.pow(10, -M), k = W[8 + M / 3];
    return function(b) {
      return p(S * b) + k;
    };
  }
  return {
    format: f,
    formatPrefix: l
  };
}
var F, en, an;
En({
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});
function En(n) {
  return F = Rn(n), en = F.format, an = F.formatPrefix, F;
}
function Ln(n) {
  return Math.max(0, -A(Math.abs(n)));
}
function Dn(n, t) {
  return Math.max(0, Math.max(-8, Math.min(8, Math.floor(A(t) / 3))) * 3 - A(Math.abs(n)));
}
function Tn(n, t) {
  return n = Math.abs(n), t = Math.abs(t) - n, Math.max(0, A(t) - A(n)) + 1;
}
function In(n) {
  return function() {
    return n;
  };
}
function qn(n) {
  return +n;
}
var _ = [0, 1];
function x(n) {
  return n;
}
function C(n, t) {
  return (t -= n = +n) ? function(e) {
    return (e - n) / t;
  } : In(isNaN(t) ? NaN : 0.5);
}
function Cn(n, t) {
  var e;
  return n > t && (e = n, n = t, t = e), function(r) {
    return Math.max(n, Math.min(t, r));
  };
}
function Bn(n, t, e) {
  var r = n[0], i = n[1], a = t[0], o = t[1];
  return i < r ? (r = C(i, r), a = e(o, a)) : (r = C(r, i), a = e(a, o)), function(u) {
    return a(r(u));
  };
}
function Gn(n, t, e) {
  var r = Math.min(n.length, t.length) - 1, i = new Array(r), a = new Array(r), o = -1;
  for (n[r] < n[0] && (n = n.slice().reverse(), t = t.slice().reverse()); ++o < r; )
    i[o] = C(n[o], n[o + 1]), a[o] = e(t[o], t[o + 1]);
  return function(u) {
    var h = yn(n, u, 1, r) - 1;
    return a[h](i[h](u));
  };
}
function On(n, t) {
  return t.domain(n.domain()).range(n.range()).interpolate(n.interpolate()).clamp(n.clamp()).unknown(n.unknown());
}
function Vn() {
  var n = _, t = _, e = B, r, i, a, o = x, u, h, f;
  function l() {
    var m = Math.min(n.length, t.length);
    return o !== x && (o = Cn(n[0], n[m - 1])), u = m > 2 ? Gn : Bn, h = f = null, c;
  }
  function c(m) {
    return m == null || isNaN(m = +m) ? a : (h || (h = u(n.map(r), t, e)))(r(o(m)));
  }
  return c.invert = function(m) {
    return o(i((f || (f = u(t, n.map(r), D)))(m)));
  }, c.domain = function(m) {
    return arguments.length ? (n = Array.from(m, qn), l()) : n.slice();
  }, c.range = function(m) {
    return arguments.length ? (t = Array.from(m), l()) : t.slice();
  }, c.rangeRound = function(m) {
    return t = Array.from(m), e = Sn, l();
  }, c.clamp = function(m) {
    return arguments.length ? (o = m ? !0 : x, l()) : o !== x;
  }, c.interpolate = function(m) {
    return arguments.length ? (e = m, l()) : e;
  }, c.unknown = function(m) {
    return arguments.length ? (a = m, c) : a;
  }, function(m, p) {
    return r = m, i = p, l();
  };
}
function Xn() {
  return Vn()(x, x);
}
function Un(n, t, e, r) {
  var i = wn(n, t, e), a;
  switch (r = E(r ?? ",f"), r.type) {
    case "s": {
      var o = Math.max(Math.abs(n), Math.abs(t));
      return r.precision == null && !isNaN(a = Dn(i, o)) && (r.precision = a), an(r, o);
    }
    case "":
    case "e":
    case "g":
    case "p":
    case "r": {
      r.precision == null && !isNaN(a = Tn(i, Math.max(Math.abs(n), Math.abs(t)))) && (r.precision = a - (r.type === "e"));
      break;
    }
    case "f":
    case "%": {
      r.precision == null && !isNaN(a = Ln(i)) && (r.precision = a - (r.type === "%") * 2);
      break;
    }
  }
  return en(r);
}
function Yn(n) {
  var t = n.domain;
  return n.ticks = function(e) {
    var r = t();
    return pn(r[0], r[r.length - 1], e ?? 10);
  }, n.tickFormat = function(e, r) {
    var i = t();
    return Un(i[0], i[i.length - 1], e ?? 10, r);
  }, n.nice = function(e) {
    e == null && (e = 10);
    var r = t(), i = 0, a = r.length - 1, o = r[i], u = r[a], h, f, l = 10;
    for (u < o && (f = o, o = u, u = f, f = i, i = a, a = f); l-- > 0; ) {
      if (f = tn(o, u, e), f === h)
        return r[i] = o, r[a] = u, t(r);
      if (f > 0)
        o = Math.floor(o / f) * f, u = Math.ceil(u / f) * f;
      else if (f < 0)
        o = Math.ceil(o * f) / f, u = Math.floor(u * f) / f;
      else
        break;
      h = f;
    }
    return n;
  }, n;
}
function Zn() {
  var n = Xn();
  return n.copy = function() {
    return On(n, Zn());
  }, sn.apply(n, arguments), Yn(n);
}
export {
  On as a,
  nn as b,
  Xn as c,
  Zn as l,
  wn as t
};
