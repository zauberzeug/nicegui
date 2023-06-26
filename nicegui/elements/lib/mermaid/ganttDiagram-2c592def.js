import { s as nr, u as rr } from "./utils-aa888deb.js";
import { w as hn, x as mn, R as dn, C as gn, y as ir, z as ar, A as he, B as Be, D as Ze, E as sr, F as ee, G as or, H as _e, g as vt, I as nt, l as me, f as Wt, e as cr } from "./config-e567ef17.js";
import { m as ur } from "./mermaidAPI-04b5c286.js";
import { s as lr, g as fr, d as hr, e as mr, b as dr, a as gr, f as yr } from "./commonDb-4dc3d465.js";
import { c as pr } from "./setupGraphViewbox-a4603a92.js";
import { i as yn } from "./init-f9637058.js";
import "./errorRenderer-a3c4bedb.js";
function Ht(t, e) {
  return t == null || e == null ? NaN : t < e ? -1 : t > e ? 1 : t >= e ? 0 : NaN;
}
function kr(t, e) {
  return t == null || e == null ? NaN : e < t ? -1 : e > t ? 1 : e >= t ? 0 : NaN;
}
function Ae(t) {
  let e, r, n;
  t.length !== 2 ? (e = Ht, r = (c, g) => Ht(t(c), g), n = (c, g) => t(c) - g) : (e = t === Ht || t === kr ? t : vr, r = t, n = t);
  function i(c, g, l = 0, b = c.length) {
    if (l < b) {
      if (e(g, g) !== 0)
        return b;
      do {
        const v = l + b >>> 1;
        r(c[v], g) < 0 ? l = v + 1 : b = v;
      } while (l < b);
    }
    return l;
  }
  function a(c, g, l = 0, b = c.length) {
    if (l < b) {
      if (e(g, g) !== 0)
        return b;
      do {
        const v = l + b >>> 1;
        r(c[v], g) <= 0 ? l = v + 1 : b = v;
      } while (l < b);
    }
    return l;
  }
  function s(c, g, l = 0, b = c.length) {
    const v = i(c, g, l, b - 1);
    return v > l && n(c[v - 1], g) > -n(c[v], g) ? v - 1 : v;
  }
  return { left: i, center: s, right: a };
}
function vr() {
  return 0;
}
function Tr(t) {
  return t === null ? NaN : +t;
}
const xr = Ae(Ht), br = xr.right;
Ae(Tr).center;
const Mr = br;
var de = Math.sqrt(50), ge = Math.sqrt(10), ye = Math.sqrt(2);
function wr(t, e, r) {
  var n, i = -1, a, s, c;
  if (e = +e, t = +t, r = +r, t === e && r > 0)
    return [t];
  if ((n = e < t) && (a = t, t = e, e = a), (c = pn(t, e, r)) === 0 || !isFinite(c))
    return [];
  if (c > 0) {
    let g = Math.round(t / c), l = Math.round(e / c);
    for (g * c < t && ++g, l * c > e && --l, s = new Array(a = l - g + 1); ++i < a; )
      s[i] = (g + i) * c;
  } else {
    c = -c;
    let g = Math.round(t * c), l = Math.round(e * c);
    for (g / c < t && ++g, l / c > e && --l, s = new Array(a = l - g + 1); ++i < a; )
      s[i] = (g + i) / c;
  }
  return n && s.reverse(), s;
}
function pn(t, e, r) {
  var n = (e - t) / Math.max(0, r), i = Math.floor(Math.log(n) / Math.LN10), a = n / Math.pow(10, i);
  return i >= 0 ? (a >= de ? 10 : a >= ge ? 5 : a >= ye ? 2 : 1) * Math.pow(10, i) : -Math.pow(10, -i) / (a >= de ? 10 : a >= ge ? 5 : a >= ye ? 2 : 1);
}
function pe(t, e, r) {
  var n = Math.abs(e - t) / Math.max(0, r), i = Math.pow(10, Math.floor(Math.log(n) / Math.LN10)), a = n / i;
  return a >= de ? i *= 10 : a >= ge ? i *= 5 : a >= ye && (i *= 2), e < t ? -i : i;
}
function Cr(t, e) {
  let r;
  if (e === void 0)
    for (const n of t)
      n != null && (r < n || r === void 0 && n >= n) && (r = n);
  else {
    let n = -1;
    for (let i of t)
      (i = e(i, ++n, t)) != null && (r < i || r === void 0 && i >= i) && (r = i);
  }
  return r;
}
function Dr(t, e) {
  let r;
  if (e === void 0)
    for (const n of t)
      n != null && (r > n || r === void 0 && n >= n) && (r = n);
  else {
    let n = -1;
    for (let i of t)
      (i = e(i, ++n, t)) != null && (r > i || r === void 0 && i >= i) && (r = i);
  }
  return r;
}
function Sr(t) {
  return t;
}
var Pt = 1, ne = 2, ke = 3, zt = 4, je = 1e-6;
function _r(t) {
  return "translate(" + t + ",0)";
}
function Ar(t) {
  return "translate(0," + t + ")";
}
function Fr(t) {
  return (e) => +t(e);
}
function Yr(t, e) {
  return e = Math.max(0, t.bandwidth() - e * 2) / 2, t.round() && (e = Math.round(e)), (r) => +t(r) + e;
}
function Ur() {
  return !this.__axis;
}
function kn(t, e) {
  var r = [], n = null, i = null, a = 6, s = 6, c = 3, g = typeof window < "u" && window.devicePixelRatio > 1 ? 0 : 0.5, l = t === Pt || t === zt ? -1 : 1, b = t === zt || t === ne ? "x" : "y", v = t === Pt || t === ke ? _r : Ar;
  function y(p) {
    var I = n ?? (e.ticks ? e.ticks.apply(e, r) : e.domain()), C = i ?? (e.tickFormat ? e.tickFormat.apply(e, r) : Sr), _ = Math.max(a, 0) + c, E = e.range(), W = +E[0] + g, O = +E[E.length - 1] + g, R = (e.bandwidth ? Yr : Fr)(e.copy(), g), P = p.selection ? p.selection() : p, w = P.selectAll(".domain").data([null]), Y = P.selectAll(".tick").data(I, e).order(), B = Y.exit(), x = Y.enter().append("g").attr("class", "tick"), m = Y.select("line"), u = Y.select("text");
    w = w.merge(w.enter().insert("path", ".tick").attr("class", "domain").attr("stroke", "currentColor")), Y = Y.merge(x), m = m.merge(x.append("line").attr("stroke", "currentColor").attr(b + "2", l * a)), u = u.merge(x.append("text").attr("fill", "currentColor").attr(b, l * _).attr("dy", t === Pt ? "0em" : t === ke ? "0.71em" : "0.32em")), p !== P && (w = w.transition(p), Y = Y.transition(p), m = m.transition(p), u = u.transition(p), B = B.transition(p).attr("opacity", je).attr("transform", function(h) {
      return isFinite(h = R(h)) ? v(h + g) : this.getAttribute("transform");
    }), x.attr("opacity", je).attr("transform", function(h) {
      var T = this.parentNode.__axis;
      return v((T && isFinite(T = T(h)) ? T : R(h)) + g);
    })), B.remove(), w.attr("d", t === zt || t === ne ? s ? "M" + l * s + "," + W + "H" + g + "V" + O + "H" + l * s : "M" + g + "," + W + "V" + O : s ? "M" + W + "," + l * s + "V" + g + "H" + O + "V" + l * s : "M" + W + "," + g + "H" + O), Y.attr("opacity", 1).attr("transform", function(h) {
      return v(R(h) + g);
    }), m.attr(b + "2", l * a), u.attr(b, l * _).text(C), P.filter(Ur).attr("fill", "none").attr("font-size", 10).attr("font-family", "sans-serif").attr("text-anchor", t === ne ? "start" : t === zt ? "end" : "middle"), P.each(function() {
      this.__axis = R;
    });
  }
  return y.scale = function(p) {
    return arguments.length ? (e = p, y) : e;
  }, y.ticks = function() {
    return r = Array.from(arguments), y;
  }, y.tickArguments = function(p) {
    return arguments.length ? (r = p == null ? [] : Array.from(p), y) : r.slice();
  }, y.tickValues = function(p) {
    return arguments.length ? (n = p == null ? null : Array.from(p), y) : n && n.slice();
  }, y.tickFormat = function(p) {
    return arguments.length ? (i = p, y) : i;
  }, y.tickSize = function(p) {
    return arguments.length ? (a = s = +p, y) : a;
  }, y.tickSizeInner = function(p) {
    return arguments.length ? (a = +p, y) : a;
  }, y.tickSizeOuter = function(p) {
    return arguments.length ? (s = +p, y) : s;
  }, y.tickPadding = function(p) {
    return arguments.length ? (c = +p, y) : c;
  }, y.offset = function(p) {
    return arguments.length ? (g = +p, y) : g;
  }, y;
}
function Lr(t) {
  return kn(Pt, t);
}
function Er(t) {
  return kn(ke, t);
}
const Nr = Math.PI / 180, Ir = 180 / Math.PI, Bt = 18, vn = 0.96422, Tn = 1, xn = 0.82521, bn = 4 / 29, Tt = 6 / 29, Mn = 3 * Tt * Tt, Wr = Tt * Tt * Tt;
function wn(t) {
  if (t instanceof ot)
    return new ot(t.l, t.a, t.b, t.opacity);
  if (t instanceof ut)
    return Cn(t);
  t instanceof dn || (t = ir(t));
  var e = se(t.r), r = se(t.g), n = se(t.b), i = re((0.2225045 * e + 0.7168786 * r + 0.0606169 * n) / Tn), a, s;
  return e === r && r === n ? a = s = i : (a = re((0.4360747 * e + 0.3850649 * r + 0.1430804 * n) / vn), s = re((0.0139322 * e + 0.0971045 * r + 0.7141733 * n) / xn)), new ot(116 * i - 16, 500 * (a - i), 200 * (i - s), t.opacity);
}
function zr(t, e, r, n) {
  return arguments.length === 1 ? wn(t) : new ot(t, e, r, n ?? 1);
}
function ot(t, e, r, n) {
  this.l = +t, this.a = +e, this.b = +r, this.opacity = +n;
}
hn(ot, zr, mn(gn, {
  brighter(t) {
    return new ot(this.l + Bt * (t ?? 1), this.a, this.b, this.opacity);
  },
  darker(t) {
    return new ot(this.l - Bt * (t ?? 1), this.a, this.b, this.opacity);
  },
  rgb() {
    var t = (this.l + 16) / 116, e = isNaN(this.a) ? t : t + this.a / 500, r = isNaN(this.b) ? t : t - this.b / 200;
    return e = vn * ie(e), t = Tn * ie(t), r = xn * ie(r), new dn(
      ae(3.1338561 * e - 1.6168667 * t - 0.4906146 * r),
      ae(-0.9787684 * e + 1.9161415 * t + 0.033454 * r),
      ae(0.0719453 * e - 0.2289914 * t + 1.4052427 * r),
      this.opacity
    );
  }
}));
function re(t) {
  return t > Wr ? Math.pow(t, 1 / 3) : t / Mn + bn;
}
function ie(t) {
  return t > Tt ? t * t * t : Mn * (t - bn);
}
function ae(t) {
  return 255 * (t <= 31308e-7 ? 12.92 * t : 1.055 * Math.pow(t, 1 / 2.4) - 0.055);
}
function se(t) {
  return (t /= 255) <= 0.04045 ? t / 12.92 : Math.pow((t + 0.055) / 1.055, 2.4);
}
function Or(t) {
  if (t instanceof ut)
    return new ut(t.h, t.c, t.l, t.opacity);
  if (t instanceof ot || (t = wn(t)), t.a === 0 && t.b === 0)
    return new ut(NaN, 0 < t.l && t.l < 100 ? 0 : NaN, t.l, t.opacity);
  var e = Math.atan2(t.b, t.a) * Ir;
  return new ut(e < 0 ? e + 360 : e, Math.sqrt(t.a * t.a + t.b * t.b), t.l, t.opacity);
}
function ve(t, e, r, n) {
  return arguments.length === 1 ? Or(t) : new ut(t, e, r, n ?? 1);
}
function ut(t, e, r, n) {
  this.h = +t, this.c = +e, this.l = +r, this.opacity = +n;
}
function Cn(t) {
  if (isNaN(t.h))
    return new ot(t.l, 0, 0, t.opacity);
  var e = t.h * Nr;
  return new ot(t.l, Math.cos(e) * t.c, Math.sin(e) * t.c, t.opacity);
}
hn(ut, ve, mn(gn, {
  brighter(t) {
    return new ut(this.h, this.c, this.l + Bt * (t ?? 1), this.opacity);
  },
  darker(t) {
    return new ut(this.h, this.c, this.l - Bt * (t ?? 1), this.opacity);
  },
  rgb() {
    return Cn(this).rgb();
  }
}));
function Hr(t, e) {
  e || (e = []);
  var r = t ? Math.min(e.length, t.length) : 0, n = e.slice(), i;
  return function(a) {
    for (i = 0; i < r; ++i)
      n[i] = t[i] * (1 - a) + e[i] * a;
    return n;
  };
}
function Pr(t) {
  return ArrayBuffer.isView(t) && !(t instanceof DataView);
}
function Vr(t, e) {
  var r = e ? e.length : 0, n = t ? Math.min(r, t.length) : 0, i = new Array(n), a = new Array(r), s;
  for (s = 0; s < n; ++s)
    i[s] = Fe(t[s], e[s]);
  for (; s < r; ++s)
    a[s] = e[s];
  return function(c) {
    for (s = 0; s < n; ++s)
      a[s] = i[s](c);
    return a;
  };
}
function Rr(t, e) {
  var r = new Date();
  return t = +t, e = +e, function(n) {
    return r.setTime(t * (1 - n) + e * n), r;
  };
}
function Br(t, e) {
  var r = {}, n = {}, i;
  (t === null || typeof t != "object") && (t = {}), (e === null || typeof e != "object") && (e = {});
  for (i in e)
    i in t ? r[i] = Fe(t[i], e[i]) : n[i] = e[i];
  return function(a) {
    for (i in r)
      n[i] = r[i](a);
    return n;
  };
}
function Fe(t, e) {
  var r = typeof e, n;
  return e == null || r === "boolean" ? ar(e) : (r === "number" ? he : r === "string" ? (n = Be(e)) ? (e = n, Ze) : sr : e instanceof Be ? Ze : e instanceof Date ? Rr : Pr(e) ? Hr : Array.isArray(e) ? Vr : typeof e.valueOf != "function" && typeof e.toString != "function" || isNaN(e) ? Br : he)(t, e);
}
function Zr(t, e) {
  return t = +t, e = +e, function(r) {
    return Math.round(t * (1 - r) + e * r);
  };
}
function jr(t) {
  return function(e, r) {
    var n = t((e = ve(e)).h, (r = ve(r)).h), i = ee(e.c, r.c), a = ee(e.l, r.l), s = ee(e.opacity, r.opacity);
    return function(c) {
      return e.h = n(c), e.c = i(c), e.l = a(c), e.opacity = s(c), e + "";
    };
  };
}
const Xr = jr(or);
function qr(t) {
  return Math.abs(t = Math.round(t)) >= 1e21 ? t.toLocaleString("en").replace(/,/g, "") : t.toString(10);
}
function Zt(t, e) {
  if ((r = (t = e ? t.toExponential(e - 1) : t.toExponential()).indexOf("e")) < 0)
    return null;
  var r, n = t.slice(0, r);
  return [
    n.length > 1 ? n[0] + n.slice(2) : n,
    +t.slice(r + 1)
  ];
}
function bt(t) {
  return t = Zt(Math.abs(t)), t ? t[1] : NaN;
}
function Gr(t, e) {
  return function(r, n) {
    for (var i = r.length, a = [], s = 0, c = t[0], g = 0; i > 0 && c > 0 && (g + c + 1 > n && (c = Math.max(1, n - g)), a.push(r.substring(i -= c, i + c)), !((g += c + 1) > n)); )
      c = t[s = (s + 1) % t.length];
    return a.reverse().join(e);
  };
}
function $r(t) {
  return function(e) {
    return e.replace(/[0-9]/g, function(r) {
      return t[+r];
    });
  };
}
var Qr = /^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$/i;
function jt(t) {
  if (!(e = Qr.exec(t)))
    throw new Error("invalid format: " + t);
  var e;
  return new Ye({
    fill: e[1],
    align: e[2],
    sign: e[3],
    symbol: e[4],
    zero: e[5],
    width: e[6],
    comma: e[7],
    precision: e[8] && e[8].slice(1),
    trim: e[9],
    type: e[10]
  });
}
jt.prototype = Ye.prototype;
function Ye(t) {
  this.fill = t.fill === void 0 ? " " : t.fill + "", this.align = t.align === void 0 ? ">" : t.align + "", this.sign = t.sign === void 0 ? "-" : t.sign + "", this.symbol = t.symbol === void 0 ? "" : t.symbol + "", this.zero = !!t.zero, this.width = t.width === void 0 ? void 0 : +t.width, this.comma = !!t.comma, this.precision = t.precision === void 0 ? void 0 : +t.precision, this.trim = !!t.trim, this.type = t.type === void 0 ? "" : t.type + "";
}
Ye.prototype.toString = function() {
  return this.fill + this.align + this.sign + this.symbol + (this.zero ? "0" : "") + (this.width === void 0 ? "" : Math.max(1, this.width | 0)) + (this.comma ? "," : "") + (this.precision === void 0 ? "" : "." + Math.max(0, this.precision | 0)) + (this.trim ? "~" : "") + this.type;
};
function Jr(t) {
  t:
    for (var e = t.length, r = 1, n = -1, i; r < e; ++r)
      switch (t[r]) {
        case ".":
          n = i = r;
          break;
        case "0":
          n === 0 && (n = r), i = r;
          break;
        default:
          if (!+t[r])
            break t;
          n > 0 && (n = 0);
          break;
      }
  return n > 0 ? t.slice(0, n) + t.slice(i + 1) : t;
}
var Dn;
function Kr(t, e) {
  var r = Zt(t, e);
  if (!r)
    return t + "";
  var n = r[0], i = r[1], a = i - (Dn = Math.max(-8, Math.min(8, Math.floor(i / 3))) * 3) + 1, s = n.length;
  return a === s ? n : a > s ? n + new Array(a - s + 1).join("0") : a > 0 ? n.slice(0, a) + "." + n.slice(a) : "0." + new Array(1 - a).join("0") + Zt(t, Math.max(0, e + a - 1))[0];
}
function Xe(t, e) {
  var r = Zt(t, e);
  if (!r)
    return t + "";
  var n = r[0], i = r[1];
  return i < 0 ? "0." + new Array(-i).join("0") + n : n.length > i + 1 ? n.slice(0, i + 1) + "." + n.slice(i + 1) : n + new Array(i - n.length + 2).join("0");
}
const qe = {
  "%": (t, e) => (t * 100).toFixed(e),
  b: (t) => Math.round(t).toString(2),
  c: (t) => t + "",
  d: qr,
  e: (t, e) => t.toExponential(e),
  f: (t, e) => t.toFixed(e),
  g: (t, e) => t.toPrecision(e),
  o: (t) => Math.round(t).toString(8),
  p: (t, e) => Xe(t * 100, e),
  r: Xe,
  s: Kr,
  X: (t) => Math.round(t).toString(16).toUpperCase(),
  x: (t) => Math.round(t).toString(16)
};
function Ge(t) {
  return t;
}
var $e = Array.prototype.map, Qe = ["y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"];
function ti(t) {
  var e = t.grouping === void 0 || t.thousands === void 0 ? Ge : Gr($e.call(t.grouping, Number), t.thousands + ""), r = t.currency === void 0 ? "" : t.currency[0] + "", n = t.currency === void 0 ? "" : t.currency[1] + "", i = t.decimal === void 0 ? "." : t.decimal + "", a = t.numerals === void 0 ? Ge : $r($e.call(t.numerals, String)), s = t.percent === void 0 ? "%" : t.percent + "", c = t.minus === void 0 ? "−" : t.minus + "", g = t.nan === void 0 ? "NaN" : t.nan + "";
  function l(v) {
    v = jt(v);
    var y = v.fill, p = v.align, I = v.sign, C = v.symbol, _ = v.zero, E = v.width, W = v.comma, O = v.precision, R = v.trim, P = v.type;
    P === "n" ? (W = !0, P = "g") : qe[P] || (O === void 0 && (O = 12), R = !0, P = "g"), (_ || y === "0" && p === "=") && (_ = !0, y = "0", p = "=");
    var w = C === "$" ? r : C === "#" && /[boxX]/.test(P) ? "0" + P.toLowerCase() : "", Y = C === "$" ? n : /[%p]/.test(P) ? s : "", B = qe[P], x = /[defgprs%]/.test(P);
    O = O === void 0 ? 6 : /[gprs]/.test(P) ? Math.max(1, Math.min(21, O)) : Math.max(0, Math.min(20, O));
    function m(u) {
      var h = w, T = Y, o, F, f;
      if (P === "c")
        T = B(u) + T, u = "";
      else {
        u = +u;
        var A = u < 0 || 1 / u < 0;
        if (u = isNaN(u) ? g : B(Math.abs(u), O), R && (u = Jr(u)), A && +u == 0 && I !== "+" && (A = !1), h = (A ? I === "(" ? I : c : I === "-" || I === "(" ? "" : I) + h, T = (P === "s" ? Qe[8 + Dn / 3] : "") + T + (A && I === "(" ? ")" : ""), x) {
          for (o = -1, F = u.length; ++o < F; )
            if (f = u.charCodeAt(o), 48 > f || f > 57) {
              T = (f === 46 ? i + u.slice(o + 1) : u.slice(o)) + T, u = u.slice(0, o);
              break;
            }
        }
      }
      W && !_ && (u = e(u, 1 / 0));
      var Z = h.length + u.length + T.length, j = Z < E ? new Array(E - Z + 1).join(y) : "";
      switch (W && _ && (u = e(j + u, j.length ? E - T.length : 1 / 0), j = ""), p) {
        case "<":
          u = h + u + T + j;
          break;
        case "=":
          u = h + j + u + T;
          break;
        case "^":
          u = j.slice(0, Z = j.length >> 1) + h + u + T + j.slice(Z);
          break;
        default:
          u = j + h + u + T;
          break;
      }
      return a(u);
    }
    return m.toString = function() {
      return v + "";
    }, m;
  }
  function b(v, y) {
    var p = l((v = jt(v), v.type = "f", v)), I = Math.max(-8, Math.min(8, Math.floor(bt(y) / 3))) * 3, C = Math.pow(10, -I), _ = Qe[8 + I / 3];
    return function(E) {
      return p(C * E) + _;
    };
  }
  return {
    format: l,
    formatPrefix: b
  };
}
var Ot, Sn, _n;
ei({
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});
function ei(t) {
  return Ot = ti(t), Sn = Ot.format, _n = Ot.formatPrefix, Ot;
}
function ni(t) {
  return Math.max(0, -bt(Math.abs(t)));
}
function ri(t, e) {
  return Math.max(0, Math.max(-8, Math.min(8, Math.floor(bt(e) / 3))) * 3 - bt(Math.abs(t)));
}
function ii(t, e) {
  return t = Math.abs(t), e = Math.abs(e) - t, Math.max(0, bt(e) - bt(t)) + 1;
}
function ai(t) {
  return function() {
    return t;
  };
}
function si(t) {
  return +t;
}
var Je = [0, 1];
function kt(t) {
  return t;
}
function Te(t, e) {
  return (e -= t = +t) ? function(r) {
    return (r - t) / e;
  } : ai(isNaN(e) ? NaN : 0.5);
}
function oi(t, e) {
  var r;
  return t > e && (r = t, t = e, e = r), function(n) {
    return Math.max(t, Math.min(e, n));
  };
}
function ci(t, e, r) {
  var n = t[0], i = t[1], a = e[0], s = e[1];
  return i < n ? (n = Te(i, n), a = r(s, a)) : (n = Te(n, i), a = r(a, s)), function(c) {
    return a(n(c));
  };
}
function ui(t, e, r) {
  var n = Math.min(t.length, e.length) - 1, i = new Array(n), a = new Array(n), s = -1;
  for (t[n] < t[0] && (t = t.slice().reverse(), e = e.slice().reverse()); ++s < n; )
    i[s] = Te(t[s], t[s + 1]), a[s] = r(e[s], e[s + 1]);
  return function(c) {
    var g = Mr(t, c, 1, n) - 1;
    return a[g](i[g](c));
  };
}
function An(t, e) {
  return e.domain(t.domain()).range(t.range()).interpolate(t.interpolate()).clamp(t.clamp()).unknown(t.unknown());
}
function li() {
  var t = Je, e = Je, r = Fe, n, i, a, s = kt, c, g, l;
  function b() {
    var y = Math.min(t.length, e.length);
    return s !== kt && (s = oi(t[0], t[y - 1])), c = y > 2 ? ui : ci, g = l = null, v;
  }
  function v(y) {
    return y == null || isNaN(y = +y) ? a : (g || (g = c(t.map(n), e, r)))(n(s(y)));
  }
  return v.invert = function(y) {
    return s(i((l || (l = c(e, t.map(n), he)))(y)));
  }, v.domain = function(y) {
    return arguments.length ? (t = Array.from(y, si), b()) : t.slice();
  }, v.range = function(y) {
    return arguments.length ? (e = Array.from(y), b()) : e.slice();
  }, v.rangeRound = function(y) {
    return e = Array.from(y), r = Zr, b();
  }, v.clamp = function(y) {
    return arguments.length ? (s = y ? !0 : kt, b()) : s !== kt;
  }, v.interpolate = function(y) {
    return arguments.length ? (r = y, b()) : r;
  }, v.unknown = function(y) {
    return arguments.length ? (a = y, v) : a;
  }, function(y, p) {
    return n = y, i = p, b();
  };
}
function Fn() {
  return li()(kt, kt);
}
function fi(t, e, r, n) {
  var i = pe(t, e, r), a;
  switch (n = jt(n ?? ",f"), n.type) {
    case "s": {
      var s = Math.max(Math.abs(t), Math.abs(e));
      return n.precision == null && !isNaN(a = ri(i, s)) && (n.precision = a), _n(n, s);
    }
    case "":
    case "e":
    case "g":
    case "p":
    case "r": {
      n.precision == null && !isNaN(a = ii(i, Math.max(Math.abs(t), Math.abs(e)))) && (n.precision = a - (n.type === "e"));
      break;
    }
    case "f":
    case "%": {
      n.precision == null && !isNaN(a = ni(i)) && (n.precision = a - (n.type === "%") * 2);
      break;
    }
  }
  return Sn(n);
}
function hi(t) {
  var e = t.domain;
  return t.ticks = function(r) {
    var n = e();
    return wr(n[0], n[n.length - 1], r ?? 10);
  }, t.tickFormat = function(r, n) {
    var i = e();
    return fi(i[0], i[i.length - 1], r ?? 10, n);
  }, t.nice = function(r) {
    r == null && (r = 10);
    var n = e(), i = 0, a = n.length - 1, s = n[i], c = n[a], g, l, b = 10;
    for (c < s && (l = s, s = c, c = l, l = i, i = a, a = l); b-- > 0; ) {
      if (l = pn(s, c, r), l === g)
        return n[i] = s, n[a] = c, e(n);
      if (l > 0)
        s = Math.floor(s / l) * l, c = Math.ceil(c / l) * l;
      else if (l < 0)
        s = Math.ceil(s * l) / l, c = Math.floor(c * l) / l;
      else
        break;
      g = l;
    }
    return t;
  }, t;
}
function Yn() {
  var t = Fn();
  return t.copy = function() {
    return An(t, Yn());
  }, yn.apply(t, arguments), hi(t);
}
function mi(t, e) {
  t = t.slice();
  var r = 0, n = t.length - 1, i = t[r], a = t[n], s;
  return a < i && (s = r, r = n, n = s, s = i, i = a, a = s), t[r] = e.floor(i), t[n] = e.ceil(a), t;
}
var oe = new Date(), ce = new Date();
function tt(t, e, r, n) {
  function i(a) {
    return t(a = arguments.length === 0 ? new Date() : new Date(+a)), a;
  }
  return i.floor = function(a) {
    return t(a = new Date(+a)), a;
  }, i.ceil = function(a) {
    return t(a = new Date(a - 1)), e(a, 1), t(a), a;
  }, i.round = function(a) {
    var s = i(a), c = i.ceil(a);
    return a - s < c - a ? s : c;
  }, i.offset = function(a, s) {
    return e(a = new Date(+a), s == null ? 1 : Math.floor(s)), a;
  }, i.range = function(a, s, c) {
    var g = [], l;
    if (a = i.ceil(a), c = c == null ? 1 : Math.floor(c), !(a < s) || !(c > 0))
      return g;
    do
      g.push(l = new Date(+a)), e(a, c), t(a);
    while (l < a && a < s);
    return g;
  }, i.filter = function(a) {
    return tt(function(s) {
      if (s >= s)
        for (; t(s), !a(s); )
          s.setTime(s - 1);
    }, function(s, c) {
      if (s >= s)
        if (c < 0)
          for (; ++c <= 0; )
            for (; e(s, -1), !a(s); )
              ;
        else
          for (; --c >= 0; )
            for (; e(s, 1), !a(s); )
              ;
    });
  }, r && (i.count = function(a, s) {
    return oe.setTime(+a), ce.setTime(+s), t(oe), t(ce), Math.floor(r(oe, ce));
  }, i.every = function(a) {
    return a = Math.floor(a), !isFinite(a) || !(a > 0) ? null : a > 1 ? i.filter(n ? function(s) {
      return n(s) % a === 0;
    } : function(s) {
      return i.count(0, s) % a === 0;
    }) : i;
  }), i;
}
var Xt = tt(function() {
}, function(t, e) {
  t.setTime(+t + e);
}, function(t, e) {
  return e - t;
});
Xt.every = function(t) {
  return t = Math.floor(t), !isFinite(t) || !(t > 0) ? null : t > 1 ? tt(function(e) {
    e.setTime(Math.floor(e / t) * t);
  }, function(e, r) {
    e.setTime(+e + r * t);
  }, function(e, r) {
    return (r - e) / t;
  }) : Xt;
};
const di = Xt;
Xt.range;
const lt = 1e3, it = lt * 60, ft = it * 60, mt = ft * 24, Ue = mt * 7, Ke = mt * 30, ue = mt * 365;
var Un = tt(function(t) {
  t.setTime(t - t.getMilliseconds());
}, function(t, e) {
  t.setTime(+t + e * lt);
}, function(t, e) {
  return (e - t) / lt;
}, function(t) {
  return t.getUTCSeconds();
});
const Lt = Un;
Un.range;
var Ln = tt(function(t) {
  t.setTime(t - t.getMilliseconds() - t.getSeconds() * lt);
}, function(t, e) {
  t.setTime(+t + e * it);
}, function(t, e) {
  return (e - t) / it;
}, function(t) {
  return t.getMinutes();
});
const qt = Ln;
Ln.range;
var En = tt(function(t) {
  t.setTime(t - t.getMilliseconds() - t.getSeconds() * lt - t.getMinutes() * it);
}, function(t, e) {
  t.setTime(+t + e * ft);
}, function(t, e) {
  return (e - t) / ft;
}, function(t) {
  return t.getHours();
});
const Gt = En;
En.range;
var Nn = tt(
  (t) => t.setHours(0, 0, 0, 0),
  (t, e) => t.setDate(t.getDate() + e),
  (t, e) => (e - t - (e.getTimezoneOffset() - t.getTimezoneOffset()) * it) / mt,
  (t) => t.getDate() - 1
);
const Mt = Nn;
Nn.range;
function gt(t) {
  return tt(function(e) {
    e.setDate(e.getDate() - (e.getDay() + 7 - t) % 7), e.setHours(0, 0, 0, 0);
  }, function(e, r) {
    e.setDate(e.getDate() + r * 7);
  }, function(e, r) {
    return (r - e - (r.getTimezoneOffset() - e.getTimezoneOffset()) * it) / Ue;
  });
}
var wt = gt(0), $t = gt(1), gi = gt(2), yi = gt(3), Ct = gt(4), pi = gt(5), ki = gt(6);
wt.range;
$t.range;
gi.range;
yi.range;
Ct.range;
pi.range;
ki.range;
var In = tt(function(t) {
  t.setDate(1), t.setHours(0, 0, 0, 0);
}, function(t, e) {
  t.setMonth(t.getMonth() + e);
}, function(t, e) {
  return e.getMonth() - t.getMonth() + (e.getFullYear() - t.getFullYear()) * 12;
}, function(t) {
  return t.getMonth();
});
const Qt = In;
In.range;
var Le = tt(function(t) {
  t.setMonth(0, 1), t.setHours(0, 0, 0, 0);
}, function(t, e) {
  t.setFullYear(t.getFullYear() + e);
}, function(t, e) {
  return e.getFullYear() - t.getFullYear();
}, function(t) {
  return t.getFullYear();
});
Le.every = function(t) {
  return !isFinite(t = Math.floor(t)) || !(t > 0) ? null : tt(function(e) {
    e.setFullYear(Math.floor(e.getFullYear() / t) * t), e.setMonth(0, 1), e.setHours(0, 0, 0, 0);
  }, function(e, r) {
    e.setFullYear(e.getFullYear() + r * t);
  });
};
const dt = Le;
Le.range;
var Wn = tt(function(t) {
  t.setUTCSeconds(0, 0);
}, function(t, e) {
  t.setTime(+t + e * it);
}, function(t, e) {
  return (e - t) / it;
}, function(t) {
  return t.getUTCMinutes();
});
const vi = Wn;
Wn.range;
var zn = tt(function(t) {
  t.setUTCMinutes(0, 0, 0);
}, function(t, e) {
  t.setTime(+t + e * ft);
}, function(t, e) {
  return (e - t) / ft;
}, function(t) {
  return t.getUTCHours();
});
const Ti = zn;
zn.range;
var On = tt(function(t) {
  t.setUTCHours(0, 0, 0, 0);
}, function(t, e) {
  t.setUTCDate(t.getUTCDate() + e);
}, function(t, e) {
  return (e - t) / mt;
}, function(t) {
  return t.getUTCDate() - 1;
});
const Ee = On;
On.range;
function yt(t) {
  return tt(function(e) {
    e.setUTCDate(e.getUTCDate() - (e.getUTCDay() + 7 - t) % 7), e.setUTCHours(0, 0, 0, 0);
  }, function(e, r) {
    e.setUTCDate(e.getUTCDate() + r * 7);
  }, function(e, r) {
    return (r - e) / Ue;
  });
}
var Ne = yt(0), Jt = yt(1), xi = yt(2), bi = yt(3), Dt = yt(4), Mi = yt(5), wi = yt(6);
Ne.range;
Jt.range;
xi.range;
bi.range;
Dt.range;
Mi.range;
wi.range;
var Hn = tt(function(t) {
  t.setUTCDate(1), t.setUTCHours(0, 0, 0, 0);
}, function(t, e) {
  t.setUTCMonth(t.getUTCMonth() + e);
}, function(t, e) {
  return e.getUTCMonth() - t.getUTCMonth() + (e.getUTCFullYear() - t.getUTCFullYear()) * 12;
}, function(t) {
  return t.getUTCMonth();
});
const Ci = Hn;
Hn.range;
var Ie = tt(function(t) {
  t.setUTCMonth(0, 1), t.setUTCHours(0, 0, 0, 0);
}, function(t, e) {
  t.setUTCFullYear(t.getUTCFullYear() + e);
}, function(t, e) {
  return e.getUTCFullYear() - t.getUTCFullYear();
}, function(t) {
  return t.getUTCFullYear();
});
Ie.every = function(t) {
  return !isFinite(t = Math.floor(t)) || !(t > 0) ? null : tt(function(e) {
    e.setUTCFullYear(Math.floor(e.getUTCFullYear() / t) * t), e.setUTCMonth(0, 1), e.setUTCHours(0, 0, 0, 0);
  }, function(e, r) {
    e.setUTCFullYear(e.getUTCFullYear() + r * t);
  });
};
const St = Ie;
Ie.range;
function Pn(t, e, r, n, i, a) {
  const s = [
    [Lt, 1, lt],
    [Lt, 5, 5 * lt],
    [Lt, 15, 15 * lt],
    [Lt, 30, 30 * lt],
    [a, 1, it],
    [a, 5, 5 * it],
    [a, 15, 15 * it],
    [a, 30, 30 * it],
    [i, 1, ft],
    [i, 3, 3 * ft],
    [i, 6, 6 * ft],
    [i, 12, 12 * ft],
    [n, 1, mt],
    [n, 2, 2 * mt],
    [r, 1, Ue],
    [e, 1, Ke],
    [e, 3, 3 * Ke],
    [t, 1, ue]
  ];
  function c(l, b, v) {
    const y = b < l;
    y && ([l, b] = [b, l]);
    const p = v && typeof v.range == "function" ? v : g(l, b, v), I = p ? p.range(l, +b + 1) : [];
    return y ? I.reverse() : I;
  }
  function g(l, b, v) {
    const y = Math.abs(b - l) / v, p = Ae(([, , _]) => _).right(s, y);
    if (p === s.length)
      return t.every(pe(l / ue, b / ue, v));
    if (p === 0)
      return di.every(Math.max(pe(l, b, v), 1));
    const [I, C] = s[y / s[p - 1][2] < s[p][2] / y ? p - 1 : p];
    return I.every(C);
  }
  return [c, g];
}
Pn(St, Ci, Ne, Ee, Ti, vi);
const [Di, Si] = Pn(dt, Qt, wt, Mt, Gt, qt);
function le(t) {
  if (0 <= t.y && t.y < 100) {
    var e = new Date(-1, t.m, t.d, t.H, t.M, t.S, t.L);
    return e.setFullYear(t.y), e;
  }
  return new Date(t.y, t.m, t.d, t.H, t.M, t.S, t.L);
}
function fe(t) {
  if (0 <= t.y && t.y < 100) {
    var e = new Date(Date.UTC(-1, t.m, t.d, t.H, t.M, t.S, t.L));
    return e.setUTCFullYear(t.y), e;
  }
  return new Date(Date.UTC(t.y, t.m, t.d, t.H, t.M, t.S, t.L));
}
function Ft(t, e, r) {
  return { y: t, m: e, d: r, H: 0, M: 0, S: 0, L: 0 };
}
function _i(t) {
  var e = t.dateTime, r = t.date, n = t.time, i = t.periods, a = t.days, s = t.shortDays, c = t.months, g = t.shortMonths, l = Yt(i), b = Ut(i), v = Yt(a), y = Ut(a), p = Yt(s), I = Ut(s), C = Yt(c), _ = Ut(c), E = Yt(g), W = Ut(g), O = {
    a: A,
    A: Z,
    b: j,
    B: k,
    c: null,
    d: sn,
    e: sn,
    f: Qi,
    g: oa,
    G: ua,
    H: qi,
    I: Gi,
    j: $i,
    L: Vn,
    m: Ji,
    M: Ki,
    p: U,
    q: S,
    Q: un,
    s: ln,
    S: ta,
    u: ea,
    U: na,
    V: ra,
    w: ia,
    W: aa,
    x: null,
    X: null,
    y: sa,
    Y: ca,
    Z: la,
    "%": cn
  }, R = {
    a: V,
    A: q,
    b: z,
    B: H,
    c: null,
    d: on,
    e: on,
    f: da,
    g: wa,
    G: Da,
    H: fa,
    I: ha,
    j: ma,
    L: Bn,
    m: ga,
    M: ya,
    p: ht,
    q: $,
    Q: un,
    s: ln,
    S: pa,
    u: ka,
    U: va,
    V: Ta,
    w: xa,
    W: ba,
    x: null,
    X: null,
    y: Ma,
    Y: Ca,
    Z: Sa,
    "%": cn
  }, P = {
    a: m,
    A: u,
    b: h,
    B: T,
    c: o,
    d: rn,
    e: rn,
    f: Bi,
    g: nn,
    G: en,
    H: an,
    I: an,
    j: Hi,
    L: Ri,
    m: Oi,
    M: Pi,
    p: x,
    q: zi,
    Q: ji,
    s: Xi,
    S: Vi,
    u: Li,
    U: Ei,
    V: Ni,
    w: Ui,
    W: Ii,
    x: F,
    X: f,
    y: nn,
    Y: en,
    Z: Wi,
    "%": Zi
  };
  O.x = w(r, O), O.X = w(n, O), O.c = w(e, O), R.x = w(r, R), R.X = w(n, R), R.c = w(e, R);
  function w(M, D) {
    return function(L) {
      var d = [], G = -1, N = 0, Q = M.length, J, at, rt;
      for (L instanceof Date || (L = new Date(+L)); ++G < Q; )
        M.charCodeAt(G) === 37 && (d.push(M.slice(N, G)), (at = tn[J = M.charAt(++G)]) != null ? J = M.charAt(++G) : at = J === "e" ? " " : "0", (rt = D[J]) && (J = rt(L, at)), d.push(J), N = G + 1);
      return d.push(M.slice(N, G)), d.join("");
    };
  }
  function Y(M, D) {
    return function(L) {
      var d = Ft(1900, void 0, 1), G = B(d, M, L += "", 0), N, Q;
      if (G != L.length)
        return null;
      if ("Q" in d)
        return new Date(d.Q);
      if ("s" in d)
        return new Date(d.s * 1e3 + ("L" in d ? d.L : 0));
      if (D && !("Z" in d) && (d.Z = 0), "p" in d && (d.H = d.H % 12 + d.p * 12), d.m === void 0 && (d.m = "q" in d ? d.q : 0), "V" in d) {
        if (d.V < 1 || d.V > 53)
          return null;
        "w" in d || (d.w = 1), "Z" in d ? (N = fe(Ft(d.y, 0, 1)), Q = N.getUTCDay(), N = Q > 4 || Q === 0 ? Jt.ceil(N) : Jt(N), N = Ee.offset(N, (d.V - 1) * 7), d.y = N.getUTCFullYear(), d.m = N.getUTCMonth(), d.d = N.getUTCDate() + (d.w + 6) % 7) : (N = le(Ft(d.y, 0, 1)), Q = N.getDay(), N = Q > 4 || Q === 0 ? $t.ceil(N) : $t(N), N = Mt.offset(N, (d.V - 1) * 7), d.y = N.getFullYear(), d.m = N.getMonth(), d.d = N.getDate() + (d.w + 6) % 7);
      } else
        ("W" in d || "U" in d) && ("w" in d || (d.w = "u" in d ? d.u % 7 : "W" in d ? 1 : 0), Q = "Z" in d ? fe(Ft(d.y, 0, 1)).getUTCDay() : le(Ft(d.y, 0, 1)).getDay(), d.m = 0, d.d = "W" in d ? (d.w + 6) % 7 + d.W * 7 - (Q + 5) % 7 : d.w + d.U * 7 - (Q + 6) % 7);
      return "Z" in d ? (d.H += d.Z / 100 | 0, d.M += d.Z % 100, fe(d)) : le(d);
    };
  }
  function B(M, D, L, d) {
    for (var G = 0, N = D.length, Q = L.length, J, at; G < N; ) {
      if (d >= Q)
        return -1;
      if (J = D.charCodeAt(G++), J === 37) {
        if (J = D.charAt(G++), at = P[J in tn ? D.charAt(G++) : J], !at || (d = at(M, L, d)) < 0)
          return -1;
      } else if (J != L.charCodeAt(d++))
        return -1;
    }
    return d;
  }
  function x(M, D, L) {
    var d = l.exec(D.slice(L));
    return d ? (M.p = b.get(d[0].toLowerCase()), L + d[0].length) : -1;
  }
  function m(M, D, L) {
    var d = p.exec(D.slice(L));
    return d ? (M.w = I.get(d[0].toLowerCase()), L + d[0].length) : -1;
  }
  function u(M, D, L) {
    var d = v.exec(D.slice(L));
    return d ? (M.w = y.get(d[0].toLowerCase()), L + d[0].length) : -1;
  }
  function h(M, D, L) {
    var d = E.exec(D.slice(L));
    return d ? (M.m = W.get(d[0].toLowerCase()), L + d[0].length) : -1;
  }
  function T(M, D, L) {
    var d = C.exec(D.slice(L));
    return d ? (M.m = _.get(d[0].toLowerCase()), L + d[0].length) : -1;
  }
  function o(M, D, L) {
    return B(M, e, D, L);
  }
  function F(M, D, L) {
    return B(M, r, D, L);
  }
  function f(M, D, L) {
    return B(M, n, D, L);
  }
  function A(M) {
    return s[M.getDay()];
  }
  function Z(M) {
    return a[M.getDay()];
  }
  function j(M) {
    return g[M.getMonth()];
  }
  function k(M) {
    return c[M.getMonth()];
  }
  function U(M) {
    return i[+(M.getHours() >= 12)];
  }
  function S(M) {
    return 1 + ~~(M.getMonth() / 3);
  }
  function V(M) {
    return s[M.getUTCDay()];
  }
  function q(M) {
    return a[M.getUTCDay()];
  }
  function z(M) {
    return g[M.getUTCMonth()];
  }
  function H(M) {
    return c[M.getUTCMonth()];
  }
  function ht(M) {
    return i[+(M.getUTCHours() >= 12)];
  }
  function $(M) {
    return 1 + ~~(M.getUTCMonth() / 3);
  }
  return {
    format: function(M) {
      var D = w(M += "", O);
      return D.toString = function() {
        return M;
      }, D;
    },
    parse: function(M) {
      var D = Y(M += "", !1);
      return D.toString = function() {
        return M;
      }, D;
    },
    utcFormat: function(M) {
      var D = w(M += "", R);
      return D.toString = function() {
        return M;
      }, D;
    },
    utcParse: function(M) {
      var D = Y(M += "", !0);
      return D.toString = function() {
        return M;
      }, D;
    }
  };
}
var tn = { "-": "", _: " ", 0: "0" }, et = /^\s*\d+/, Ai = /^%/, Fi = /[\\^$*+?|[\]().{}]/g;
function X(t, e, r) {
  var n = t < 0 ? "-" : "", i = (n ? -t : t) + "", a = i.length;
  return n + (a < r ? new Array(r - a + 1).join(e) + i : i);
}
function Yi(t) {
  return t.replace(Fi, "\\$&");
}
function Yt(t) {
  return new RegExp("^(?:" + t.map(Yi).join("|") + ")", "i");
}
function Ut(t) {
  return new Map(t.map((e, r) => [e.toLowerCase(), r]));
}
function Ui(t, e, r) {
  var n = et.exec(e.slice(r, r + 1));
  return n ? (t.w = +n[0], r + n[0].length) : -1;
}
function Li(t, e, r) {
  var n = et.exec(e.slice(r, r + 1));
  return n ? (t.u = +n[0], r + n[0].length) : -1;
}
function Ei(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.U = +n[0], r + n[0].length) : -1;
}
function Ni(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.V = +n[0], r + n[0].length) : -1;
}
function Ii(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.W = +n[0], r + n[0].length) : -1;
}
function en(t, e, r) {
  var n = et.exec(e.slice(r, r + 4));
  return n ? (t.y = +n[0], r + n[0].length) : -1;
}
function nn(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.y = +n[0] + (+n[0] > 68 ? 1900 : 2e3), r + n[0].length) : -1;
}
function Wi(t, e, r) {
  var n = /^(Z)|([+-]\d\d)(?::?(\d\d))?/.exec(e.slice(r, r + 6));
  return n ? (t.Z = n[1] ? 0 : -(n[2] + (n[3] || "00")), r + n[0].length) : -1;
}
function zi(t, e, r) {
  var n = et.exec(e.slice(r, r + 1));
  return n ? (t.q = n[0] * 3 - 3, r + n[0].length) : -1;
}
function Oi(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.m = n[0] - 1, r + n[0].length) : -1;
}
function rn(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.d = +n[0], r + n[0].length) : -1;
}
function Hi(t, e, r) {
  var n = et.exec(e.slice(r, r + 3));
  return n ? (t.m = 0, t.d = +n[0], r + n[0].length) : -1;
}
function an(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.H = +n[0], r + n[0].length) : -1;
}
function Pi(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.M = +n[0], r + n[0].length) : -1;
}
function Vi(t, e, r) {
  var n = et.exec(e.slice(r, r + 2));
  return n ? (t.S = +n[0], r + n[0].length) : -1;
}
function Ri(t, e, r) {
  var n = et.exec(e.slice(r, r + 3));
  return n ? (t.L = +n[0], r + n[0].length) : -1;
}
function Bi(t, e, r) {
  var n = et.exec(e.slice(r, r + 6));
  return n ? (t.L = Math.floor(n[0] / 1e3), r + n[0].length) : -1;
}
function Zi(t, e, r) {
  var n = Ai.exec(e.slice(r, r + 1));
  return n ? r + n[0].length : -1;
}
function ji(t, e, r) {
  var n = et.exec(e.slice(r));
  return n ? (t.Q = +n[0], r + n[0].length) : -1;
}
function Xi(t, e, r) {
  var n = et.exec(e.slice(r));
  return n ? (t.s = +n[0], r + n[0].length) : -1;
}
function sn(t, e) {
  return X(t.getDate(), e, 2);
}
function qi(t, e) {
  return X(t.getHours(), e, 2);
}
function Gi(t, e) {
  return X(t.getHours() % 12 || 12, e, 2);
}
function $i(t, e) {
  return X(1 + Mt.count(dt(t), t), e, 3);
}
function Vn(t, e) {
  return X(t.getMilliseconds(), e, 3);
}
function Qi(t, e) {
  return Vn(t, e) + "000";
}
function Ji(t, e) {
  return X(t.getMonth() + 1, e, 2);
}
function Ki(t, e) {
  return X(t.getMinutes(), e, 2);
}
function ta(t, e) {
  return X(t.getSeconds(), e, 2);
}
function ea(t) {
  var e = t.getDay();
  return e === 0 ? 7 : e;
}
function na(t, e) {
  return X(wt.count(dt(t) - 1, t), e, 2);
}
function Rn(t) {
  var e = t.getDay();
  return e >= 4 || e === 0 ? Ct(t) : Ct.ceil(t);
}
function ra(t, e) {
  return t = Rn(t), X(Ct.count(dt(t), t) + (dt(t).getDay() === 4), e, 2);
}
function ia(t) {
  return t.getDay();
}
function aa(t, e) {
  return X($t.count(dt(t) - 1, t), e, 2);
}
function sa(t, e) {
  return X(t.getFullYear() % 100, e, 2);
}
function oa(t, e) {
  return t = Rn(t), X(t.getFullYear() % 100, e, 2);
}
function ca(t, e) {
  return X(t.getFullYear() % 1e4, e, 4);
}
function ua(t, e) {
  var r = t.getDay();
  return t = r >= 4 || r === 0 ? Ct(t) : Ct.ceil(t), X(t.getFullYear() % 1e4, e, 4);
}
function la(t) {
  var e = t.getTimezoneOffset();
  return (e > 0 ? "-" : (e *= -1, "+")) + X(e / 60 | 0, "0", 2) + X(e % 60, "0", 2);
}
function on(t, e) {
  return X(t.getUTCDate(), e, 2);
}
function fa(t, e) {
  return X(t.getUTCHours(), e, 2);
}
function ha(t, e) {
  return X(t.getUTCHours() % 12 || 12, e, 2);
}
function ma(t, e) {
  return X(1 + Ee.count(St(t), t), e, 3);
}
function Bn(t, e) {
  return X(t.getUTCMilliseconds(), e, 3);
}
function da(t, e) {
  return Bn(t, e) + "000";
}
function ga(t, e) {
  return X(t.getUTCMonth() + 1, e, 2);
}
function ya(t, e) {
  return X(t.getUTCMinutes(), e, 2);
}
function pa(t, e) {
  return X(t.getUTCSeconds(), e, 2);
}
function ka(t) {
  var e = t.getUTCDay();
  return e === 0 ? 7 : e;
}
function va(t, e) {
  return X(Ne.count(St(t) - 1, t), e, 2);
}
function Zn(t) {
  var e = t.getUTCDay();
  return e >= 4 || e === 0 ? Dt(t) : Dt.ceil(t);
}
function Ta(t, e) {
  return t = Zn(t), X(Dt.count(St(t), t) + (St(t).getUTCDay() === 4), e, 2);
}
function xa(t) {
  return t.getUTCDay();
}
function ba(t, e) {
  return X(Jt.count(St(t) - 1, t), e, 2);
}
function Ma(t, e) {
  return X(t.getUTCFullYear() % 100, e, 2);
}
function wa(t, e) {
  return t = Zn(t), X(t.getUTCFullYear() % 100, e, 2);
}
function Ca(t, e) {
  return X(t.getUTCFullYear() % 1e4, e, 4);
}
function Da(t, e) {
  var r = t.getUTCDay();
  return t = r >= 4 || r === 0 ? Dt(t) : Dt.ceil(t), X(t.getUTCFullYear() % 1e4, e, 4);
}
function Sa() {
  return "+0000";
}
function cn() {
  return "%";
}
function un(t) {
  return +t;
}
function ln(t) {
  return Math.floor(+t / 1e3);
}
var pt, Kt;
_a({
  dateTime: "%x, %X",
  date: "%-m/%-d/%Y",
  time: "%-I:%M:%S %p",
  periods: ["AM", "PM"],
  days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
  shortDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
  shortMonths: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
});
function _a(t) {
  return pt = _i(t), Kt = pt.format, pt.parse, pt.utcFormat, pt.utcParse, pt;
}
function Aa(t) {
  return new Date(t);
}
function Fa(t) {
  return t instanceof Date ? +t : +new Date(+t);
}
function jn(t, e, r, n, i, a, s, c, g, l) {
  var b = Fn(), v = b.invert, y = b.domain, p = l(".%L"), I = l(":%S"), C = l("%I:%M"), _ = l("%I %p"), E = l("%a %d"), W = l("%b %d"), O = l("%B"), R = l("%Y");
  function P(w) {
    return (g(w) < w ? p : c(w) < w ? I : s(w) < w ? C : a(w) < w ? _ : n(w) < w ? i(w) < w ? E : W : r(w) < w ? O : R)(w);
  }
  return b.invert = function(w) {
    return new Date(v(w));
  }, b.domain = function(w) {
    return arguments.length ? y(Array.from(w, Fa)) : y().map(Aa);
  }, b.ticks = function(w) {
    var Y = y();
    return t(Y[0], Y[Y.length - 1], w ?? 10);
  }, b.tickFormat = function(w, Y) {
    return Y == null ? P : l(Y);
  }, b.nice = function(w) {
    var Y = y();
    return (!w || typeof w.range != "function") && (w = e(Y[0], Y[Y.length - 1], w ?? 10)), w ? y(mi(Y, w)) : b;
  }, b.copy = function() {
    return An(b, jn(t, e, r, n, i, a, s, c, g, l));
  }, b;
}
function Ya() {
  return yn.apply(jn(Di, Si, dt, Qt, wt, Mt, Gt, qt, Lt, Kt).domain([new Date(2e3, 0, 1), new Date(2e3, 0, 2)]), arguments);
}
var xe = function() {
  var t = function(B, x, m, u) {
    for (m = m || {}, u = B.length; u--; m[B[u]] = x)
      ;
    return m;
  }, e = [1, 3], r = [1, 5], n = [7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 25, 26, 28, 35, 40], i = [1, 15], a = [1, 16], s = [1, 17], c = [1, 18], g = [1, 19], l = [1, 20], b = [1, 21], v = [1, 22], y = [1, 23], p = [1, 24], I = [1, 25], C = [1, 26], _ = [1, 27], E = [1, 29], W = [1, 31], O = [1, 34], R = [5, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 25, 26, 28, 35, 40], P = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, directive: 4, gantt: 5, document: 6, EOF: 7, line: 8, SPACE: 9, statement: 10, NL: 11, dateFormat: 12, inclusiveEndDates: 13, topAxis: 14, axisFormat: 15, tickInterval: 16, excludes: 17, includes: 18, todayMarker: 19, title: 20, acc_title: 21, acc_title_value: 22, acc_descr: 23, acc_descr_value: 24, acc_descr_multiline_value: 25, section: 26, clickStatement: 27, taskTxt: 28, taskData: 29, openDirective: 30, typeDirective: 31, closeDirective: 32, ":": 33, argDirective: 34, click: 35, callbackname: 36, callbackargs: 37, href: 38, clickStatementDebug: 39, open_directive: 40, type_directive: 41, arg_directive: 42, close_directive: 43, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 5: "gantt", 7: "EOF", 9: "SPACE", 11: "NL", 12: "dateFormat", 13: "inclusiveEndDates", 14: "topAxis", 15: "axisFormat", 16: "tickInterval", 17: "excludes", 18: "includes", 19: "todayMarker", 20: "title", 21: "acc_title", 22: "acc_title_value", 23: "acc_descr", 24: "acc_descr_value", 25: "acc_descr_multiline_value", 26: "section", 28: "taskTxt", 29: "taskData", 33: ":", 35: "click", 36: "callbackname", 37: "callbackargs", 38: "href", 40: "open_directive", 41: "type_directive", 42: "arg_directive", 43: "close_directive" },
    productions_: [0, [3, 2], [3, 3], [6, 0], [6, 2], [8, 2], [8, 1], [8, 1], [8, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 2], [10, 2], [10, 1], [10, 1], [10, 1], [10, 2], [10, 1], [4, 4], [4, 6], [27, 2], [27, 3], [27, 3], [27, 4], [27, 3], [27, 4], [27, 2], [39, 2], [39, 3], [39, 3], [39, 4], [39, 3], [39, 4], [39, 2], [30, 1], [31, 1], [34, 1], [32, 1]],
    performAction: function(x, m, u, h, T, o, F) {
      var f = o.length - 1;
      switch (T) {
        case 2:
          return o[f - 1];
        case 3:
          this.$ = [];
          break;
        case 4:
          o[f - 1].push(o[f]), this.$ = o[f - 1];
          break;
        case 5:
        case 6:
          this.$ = o[f];
          break;
        case 7:
        case 8:
          this.$ = [];
          break;
        case 9:
          h.setDateFormat(o[f].substr(11)), this.$ = o[f].substr(11);
          break;
        case 10:
          h.enableInclusiveEndDates(), this.$ = o[f].substr(18);
          break;
        case 11:
          h.TopAxis(), this.$ = o[f].substr(8);
          break;
        case 12:
          h.setAxisFormat(o[f].substr(11)), this.$ = o[f].substr(11);
          break;
        case 13:
          h.setTickInterval(o[f].substr(13)), this.$ = o[f].substr(13);
          break;
        case 14:
          h.setExcludes(o[f].substr(9)), this.$ = o[f].substr(9);
          break;
        case 15:
          h.setIncludes(o[f].substr(9)), this.$ = o[f].substr(9);
          break;
        case 16:
          h.setTodayMarker(o[f].substr(12)), this.$ = o[f].substr(12);
          break;
        case 17:
          h.setDiagramTitle(o[f].substr(6)), this.$ = o[f].substr(6);
          break;
        case 18:
          this.$ = o[f].trim(), h.setAccTitle(this.$);
          break;
        case 19:
        case 20:
          this.$ = o[f].trim(), h.setAccDescription(this.$);
          break;
        case 21:
          h.addSection(o[f].substr(8)), this.$ = o[f].substr(8);
          break;
        case 23:
          h.addTask(o[f - 1], o[f]), this.$ = "task";
          break;
        case 27:
          this.$ = o[f - 1], h.setClickEvent(o[f - 1], o[f], null);
          break;
        case 28:
          this.$ = o[f - 2], h.setClickEvent(o[f - 2], o[f - 1], o[f]);
          break;
        case 29:
          this.$ = o[f - 2], h.setClickEvent(o[f - 2], o[f - 1], null), h.setLink(o[f - 2], o[f]);
          break;
        case 30:
          this.$ = o[f - 3], h.setClickEvent(o[f - 3], o[f - 2], o[f - 1]), h.setLink(o[f - 3], o[f]);
          break;
        case 31:
          this.$ = o[f - 2], h.setClickEvent(o[f - 2], o[f], null), h.setLink(o[f - 2], o[f - 1]);
          break;
        case 32:
          this.$ = o[f - 3], h.setClickEvent(o[f - 3], o[f - 1], o[f]), h.setLink(o[f - 3], o[f - 2]);
          break;
        case 33:
          this.$ = o[f - 1], h.setLink(o[f - 1], o[f]);
          break;
        case 34:
        case 40:
          this.$ = o[f - 1] + " " + o[f];
          break;
        case 35:
        case 36:
        case 38:
          this.$ = o[f - 2] + " " + o[f - 1] + " " + o[f];
          break;
        case 37:
        case 39:
          this.$ = o[f - 3] + " " + o[f - 2] + " " + o[f - 1] + " " + o[f];
          break;
        case 41:
          h.parseDirective("%%{", "open_directive");
          break;
        case 42:
          h.parseDirective(o[f], "type_directive");
          break;
        case 43:
          o[f] = o[f].trim().replace(/'/g, '"'), h.parseDirective(o[f], "arg_directive");
          break;
        case 44:
          h.parseDirective("}%%", "close_directive", "gantt");
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: e, 30: 4, 40: r }, { 1: [3] }, { 3: 6, 4: 2, 5: e, 30: 4, 40: r }, t(n, [2, 3], { 6: 7 }), { 31: 8, 41: [1, 9] }, { 41: [2, 41] }, { 1: [2, 1] }, { 4: 30, 7: [1, 10], 8: 11, 9: [1, 12], 10: 13, 11: [1, 14], 12: i, 13: a, 14: s, 15: c, 16: g, 17: l, 18: b, 19: v, 20: y, 21: p, 23: I, 25: C, 26: _, 27: 28, 28: E, 30: 4, 35: W, 40: r }, { 32: 32, 33: [1, 33], 43: O }, t([33, 43], [2, 42]), t(n, [2, 8], { 1: [2, 2] }), t(n, [2, 4]), { 4: 30, 10: 35, 12: i, 13: a, 14: s, 15: c, 16: g, 17: l, 18: b, 19: v, 20: y, 21: p, 23: I, 25: C, 26: _, 27: 28, 28: E, 30: 4, 35: W, 40: r }, t(n, [2, 6]), t(n, [2, 7]), t(n, [2, 9]), t(n, [2, 10]), t(n, [2, 11]), t(n, [2, 12]), t(n, [2, 13]), t(n, [2, 14]), t(n, [2, 15]), t(n, [2, 16]), t(n, [2, 17]), { 22: [1, 36] }, { 24: [1, 37] }, t(n, [2, 20]), t(n, [2, 21]), t(n, [2, 22]), { 29: [1, 38] }, t(n, [2, 24]), { 36: [1, 39], 38: [1, 40] }, { 11: [1, 41] }, { 34: 42, 42: [1, 43] }, { 11: [2, 44] }, t(n, [2, 5]), t(n, [2, 18]), t(n, [2, 19]), t(n, [2, 23]), t(n, [2, 27], { 37: [1, 44], 38: [1, 45] }), t(n, [2, 33], { 36: [1, 46] }), t(R, [2, 25]), { 32: 47, 43: O }, { 43: [2, 43] }, t(n, [2, 28], { 38: [1, 48] }), t(n, [2, 29]), t(n, [2, 31], { 37: [1, 49] }), { 11: [1, 50] }, t(n, [2, 30]), t(n, [2, 32]), t(R, [2, 26])],
    defaultActions: { 5: [2, 41], 6: [2, 1], 34: [2, 44], 43: [2, 43] },
    parseError: function(x, m) {
      if (m.recoverable)
        this.trace(x);
      else {
        var u = new Error(x);
        throw u.hash = m, u;
      }
    },
    parse: function(x) {
      var m = this, u = [0], h = [], T = [null], o = [], F = this.table, f = "", A = 0, Z = 0, j = 2, k = 1, U = o.slice.call(arguments, 1), S = Object.create(this.lexer), V = { yy: {} };
      for (var q in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, q) && (V.yy[q] = this.yy[q]);
      S.setInput(x, V.yy), V.yy.lexer = S, V.yy.parser = this, typeof S.yylloc > "u" && (S.yylloc = {});
      var z = S.yylloc;
      o.push(z);
      var H = S.options && S.options.ranges;
      typeof V.yy.parseError == "function" ? this.parseError = V.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function ht() {
        var rt;
        return rt = h.pop() || S.lex() || k, typeof rt != "number" && (rt instanceof Array && (h = rt, rt = h.pop()), rt = m.symbols_[rt] || rt), rt;
      }
      for (var $, M, D, L, d = {}, G, N, Q, J; ; ) {
        if (M = u[u.length - 1], this.defaultActions[M] ? D = this.defaultActions[M] : (($ === null || typeof $ > "u") && ($ = ht()), D = F[M] && F[M][$]), typeof D > "u" || !D.length || !D[0]) {
          var at = "";
          J = [];
          for (G in F[M])
            this.terminals_[G] && G > j && J.push("'" + this.terminals_[G] + "'");
          S.showPosition ? at = "Parse error on line " + (A + 1) + `:
` + S.showPosition() + `
Expecting ` + J.join(", ") + ", got '" + (this.terminals_[$] || $) + "'" : at = "Parse error on line " + (A + 1) + ": Unexpected " + ($ == k ? "end of input" : "'" + (this.terminals_[$] || $) + "'"), this.parseError(at, {
            text: S.match,
            token: this.terminals_[$] || $,
            line: S.yylineno,
            loc: z,
            expected: J
          });
        }
        if (D[0] instanceof Array && D.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + M + ", token: " + $);
        switch (D[0]) {
          case 1:
            u.push($), T.push(S.yytext), o.push(S.yylloc), u.push(D[1]), $ = null, Z = S.yyleng, f = S.yytext, A = S.yylineno, z = S.yylloc;
            break;
          case 2:
            if (N = this.productions_[D[1]][1], d.$ = T[T.length - N], d._$ = {
              first_line: o[o.length - (N || 1)].first_line,
              last_line: o[o.length - 1].last_line,
              first_column: o[o.length - (N || 1)].first_column,
              last_column: o[o.length - 1].last_column
            }, H && (d._$.range = [
              o[o.length - (N || 1)].range[0],
              o[o.length - 1].range[1]
            ]), L = this.performAction.apply(d, [
              f,
              Z,
              A,
              V.yy,
              D[1],
              T,
              o
            ].concat(U)), typeof L < "u")
              return L;
            N && (u = u.slice(0, -1 * N * 2), T = T.slice(0, -1 * N), o = o.slice(0, -1 * N)), u.push(this.productions_[D[1]][0]), T.push(d.$), o.push(d._$), Q = F[u[u.length - 2]][u[u.length - 1]], u.push(Q);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, w = function() {
    var B = {
      EOF: 1,
      parseError: function(m, u) {
        if (this.yy.parser)
          this.yy.parser.parseError(m, u);
        else
          throw new Error(m);
      },
      // resets the lexer, sets new input
      setInput: function(x, m) {
        return this.yy = m || this.yy || {}, this._input = x, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var x = this._input[0];
        this.yytext += x, this.yyleng++, this.offset++, this.match += x, this.matched += x;
        var m = x.match(/(?:\r\n?|\n).*/g);
        return m ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), x;
      },
      // unshifts one char (or a string) into the input
      unput: function(x) {
        var m = x.length, u = x.split(/(?:\r\n?|\n)/g);
        this._input = x + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - m), this.offset -= m;
        var h = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), u.length - 1 && (this.yylineno -= u.length - 1);
        var T = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: u ? (u.length === h.length ? this.yylloc.first_column : 0) + h[h.length - u.length].length - u[0].length : this.yylloc.first_column - m
        }, this.options.ranges && (this.yylloc.range = [T[0], T[0] + this.yyleng - m]), this.yyleng = this.yytext.length, this;
      },
      // When called from action, caches matched text and appends it on next action
      more: function() {
        return this._more = !0, this;
      },
      // When called from action, signals the lexer that this rule fails to match the input, so the next matching rule (regex) should be tested instead.
      reject: function() {
        if (this.options.backtrack_lexer)
          this._backtrack = !0;
        else
          return this.parseError("Lexical error on line " + (this.yylineno + 1) + `. You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).
` + this.showPosition(), {
            text: "",
            token: null,
            line: this.yylineno
          });
        return this;
      },
      // retain first n characters of the match
      less: function(x) {
        this.unput(this.match.slice(x));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var x = this.matched.substr(0, this.matched.length - this.match.length);
        return (x.length > 20 ? "..." : "") + x.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var x = this.match;
        return x.length < 20 && (x += this._input.substr(0, 20 - x.length)), (x.substr(0, 20) + (x.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var x = this.pastInput(), m = new Array(x.length + 1).join("-");
        return x + this.upcomingInput() + `
` + m + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(x, m) {
        var u, h, T;
        if (this.options.backtrack_lexer && (T = {
          yylineno: this.yylineno,
          yylloc: {
            first_line: this.yylloc.first_line,
            last_line: this.last_line,
            first_column: this.yylloc.first_column,
            last_column: this.yylloc.last_column
          },
          yytext: this.yytext,
          match: this.match,
          matches: this.matches,
          matched: this.matched,
          yyleng: this.yyleng,
          offset: this.offset,
          _more: this._more,
          _input: this._input,
          yy: this.yy,
          conditionStack: this.conditionStack.slice(0),
          done: this.done
        }, this.options.ranges && (T.yylloc.range = this.yylloc.range.slice(0))), h = x[0].match(/(?:\r\n?|\n).*/g), h && (this.yylineno += h.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: h ? h[h.length - 1].length - h[h.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + x[0].length
        }, this.yytext += x[0], this.match += x[0], this.matches = x, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(x[0].length), this.matched += x[0], u = this.performAction.call(this, this.yy, this, m, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), u)
          return u;
        if (this._backtrack) {
          for (var o in T)
            this[o] = T[o];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var x, m, u, h;
        this._more || (this.yytext = "", this.match = "");
        for (var T = this._currentRules(), o = 0; o < T.length; o++)
          if (u = this._input.match(this.rules[T[o]]), u && (!m || u[0].length > m[0].length)) {
            if (m = u, h = o, this.options.backtrack_lexer) {
              if (x = this.test_match(u, T[o]), x !== !1)
                return x;
              if (this._backtrack) {
                m = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return m ? (x = this.test_match(m, T[h]), x !== !1 ? x : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
` + this.showPosition(), {
          text: "",
          token: null,
          line: this.yylineno
        });
      },
      // return next match that has a token
      lex: function() {
        var m = this.next();
        return m || this.lex();
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function(m) {
        this.conditionStack.push(m);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function() {
        var m = this.conditionStack.length - 1;
        return m > 0 ? this.conditionStack.pop() : this.conditionStack[0];
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function() {
        return this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1] ? this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules : this.conditions.INITIAL.rules;
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function(m) {
        return m = this.conditionStack.length - 1 - Math.abs(m || 0), m >= 0 ? this.conditionStack[m] : "INITIAL";
      },
      // alias for begin(condition)
      pushState: function(m) {
        this.begin(m);
      },
      // return the number of states currently on the stack
      stateStackSize: function() {
        return this.conditionStack.length;
      },
      options: { "case-insensitive": !0 },
      performAction: function(m, u, h, T) {
        switch (h) {
          case 0:
            return this.begin("open_directive"), 40;
          case 1:
            return this.begin("type_directive"), 41;
          case 2:
            return this.popState(), this.begin("arg_directive"), 33;
          case 3:
            return this.popState(), this.popState(), 43;
          case 4:
            return 42;
          case 5:
            return this.begin("acc_title"), 21;
          case 6:
            return this.popState(), "acc_title_value";
          case 7:
            return this.begin("acc_descr"), 23;
          case 8:
            return this.popState(), "acc_descr_value";
          case 9:
            this.begin("acc_descr_multiline");
            break;
          case 10:
            this.popState();
            break;
          case 11:
            return "acc_descr_multiline_value";
          case 12:
            break;
          case 13:
            break;
          case 14:
            break;
          case 15:
            return 11;
          case 16:
            break;
          case 17:
            break;
          case 18:
            break;
          case 19:
            this.begin("href");
            break;
          case 20:
            this.popState();
            break;
          case 21:
            return 38;
          case 22:
            this.begin("callbackname");
            break;
          case 23:
            this.popState();
            break;
          case 24:
            this.popState(), this.begin("callbackargs");
            break;
          case 25:
            return 36;
          case 26:
            this.popState();
            break;
          case 27:
            return 37;
          case 28:
            this.begin("click");
            break;
          case 29:
            this.popState();
            break;
          case 30:
            return 35;
          case 31:
            return 5;
          case 32:
            return 12;
          case 33:
            return 13;
          case 34:
            return 14;
          case 35:
            return 15;
          case 36:
            return 16;
          case 37:
            return 18;
          case 38:
            return 17;
          case 39:
            return 19;
          case 40:
            return "date";
          case 41:
            return 20;
          case 42:
            return "accDescription";
          case 43:
            return 26;
          case 44:
            return 28;
          case 45:
            return 29;
          case 46:
            return 33;
          case 47:
            return 7;
          case 48:
            return "INVALID";
        }
      },
      rules: [/^(?:%%\{)/i, /^(?:((?:(?!\}%%)[^:.])*))/i, /^(?::)/i, /^(?:\}%%)/i, /^(?:((?:(?!\}%%).|\n)*))/i, /^(?:accTitle\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*:\s*)/i, /^(?:(?!\n||)*[^\n]*)/i, /^(?:accDescr\s*\{\s*)/i, /^(?:[\}])/i, /^(?:[^\}]*)/i, /^(?:%%(?!\{)*[^\n]*)/i, /^(?:[^\}]%%*[^\n]*)/i, /^(?:%%*[^\n]*[\n]*)/i, /^(?:[\n]+)/i, /^(?:\s+)/i, /^(?:#[^\n]*)/i, /^(?:%[^\n]*)/i, /^(?:href[\s]+["])/i, /^(?:["])/i, /^(?:[^"]*)/i, /^(?:call[\s]+)/i, /^(?:\([\s]*\))/i, /^(?:\()/i, /^(?:[^(]*)/i, /^(?:\))/i, /^(?:[^)]*)/i, /^(?:click[\s]+)/i, /^(?:[\s\n])/i, /^(?:[^\s\n]*)/i, /^(?:gantt\b)/i, /^(?:dateFormat\s[^#\n;]+)/i, /^(?:inclusiveEndDates\b)/i, /^(?:topAxis\b)/i, /^(?:axisFormat\s[^#\n;]+)/i, /^(?:tickInterval\s[^#\n;]+)/i, /^(?:includes\s[^#\n;]+)/i, /^(?:excludes\s[^#\n;]+)/i, /^(?:todayMarker\s[^\n;]+)/i, /^(?:\d\d\d\d-\d\d-\d\d\b)/i, /^(?:title\s[^#\n;]+)/i, /^(?:accDescription\s[^#\n;]+)/i, /^(?:section\s[^#:\n;]+)/i, /^(?:[^#:\n;]+)/i, /^(?::[^#\n;]+)/i, /^(?::)/i, /^(?:$)/i, /^(?:.)/i],
      conditions: { acc_descr_multiline: { rules: [10, 11], inclusive: !1 }, acc_descr: { rules: [8], inclusive: !1 }, acc_title: { rules: [6], inclusive: !1 }, close_directive: { rules: [], inclusive: !1 }, arg_directive: { rules: [3, 4], inclusive: !1 }, type_directive: { rules: [2, 3], inclusive: !1 }, open_directive: { rules: [1], inclusive: !1 }, callbackargs: { rules: [26, 27], inclusive: !1 }, callbackname: { rules: [23, 24, 25], inclusive: !1 }, href: { rules: [20, 21], inclusive: !1 }, click: { rules: [29, 30], inclusive: !1 }, INITIAL: { rules: [0, 5, 7, 9, 12, 13, 14, 15, 16, 17, 18, 19, 22, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48], inclusive: !0 } }
    };
    return B;
  }();
  P.lexer = w;
  function Y() {
    this.yy = {};
  }
  return Y.prototype = P, P.Parser = Y, new Y();
}();
xe.parser = xe;
const Ua = xe;
var be = {}, La = {
  get exports() {
    return be;
  },
  set exports(t) {
    be = t;
  }
};
(function(t, e) {
  (function(r, n) {
    t.exports = n();
  })(_e, function() {
    var r = "day";
    return function(n, i, a) {
      var s = function(l) {
        return l.add(4 - l.isoWeekday(), r);
      }, c = i.prototype;
      c.isoWeekYear = function() {
        return s(this).year();
      }, c.isoWeek = function(l) {
        if (!this.$utils().u(l))
          return this.add(7 * (l - this.isoWeek()), r);
        var b, v, y, p, I = s(this), C = (b = this.isoWeekYear(), v = this.$u, y = (v ? a.utc : a)().year(b).startOf("year"), p = 4 - y.isoWeekday(), y.isoWeekday() > 4 && (p += 7), y.add(p, r));
        return I.diff(C, "week") + 1;
      }, c.isoWeekday = function(l) {
        return this.$utils().u(l) ? this.day() || 7 : this.day(this.day() % 7 ? l : l - 7);
      };
      var g = c.startOf;
      c.startOf = function(l, b) {
        var v = this.$utils(), y = !!v.u(b) || b;
        return v.p(l) === "isoweek" ? y ? this.date(this.date() - (this.isoWeekday() - 1)).startOf("day") : this.date(this.date() - 1 - (this.isoWeekday() - 1) + 7).endOf("day") : g.bind(this)(l, b);
      };
    };
  });
})(La);
const Ea = be;
var Me = {}, Na = {
  get exports() {
    return Me;
  },
  set exports(t) {
    Me = t;
  }
};
(function(t, e) {
  (function(r, n) {
    t.exports = n();
  })(_e, function() {
    var r = { LTS: "h:mm:ss A", LT: "h:mm A", L: "MM/DD/YYYY", LL: "MMMM D, YYYY", LLL: "MMMM D, YYYY h:mm A", LLLL: "dddd, MMMM D, YYYY h:mm A" }, n = /(\[[^[]*\])|([-_:/.,()\s]+)|(A|a|YYYY|YY?|MM?M?M?|Do|DD?|hh?|HH?|mm?|ss?|S{1,3}|z|ZZ?)/g, i = /\d\d/, a = /\d\d?/, s = /\d*[^-_:/,()\s\d]+/, c = {}, g = function(C) {
      return (C = +C) + (C > 68 ? 1900 : 2e3);
    }, l = function(C) {
      return function(_) {
        this[C] = +_;
      };
    }, b = [/[+-]\d\d:?(\d\d)?|Z/, function(C) {
      (this.zone || (this.zone = {})).offset = function(_) {
        if (!_ || _ === "Z")
          return 0;
        var E = _.match(/([+-]|\d\d)/g), W = 60 * E[1] + (+E[2] || 0);
        return W === 0 ? 0 : E[0] === "+" ? -W : W;
      }(C);
    }], v = function(C) {
      var _ = c[C];
      return _ && (_.indexOf ? _ : _.s.concat(_.f));
    }, y = function(C, _) {
      var E, W = c.meridiem;
      if (W) {
        for (var O = 1; O <= 24; O += 1)
          if (C.indexOf(W(O, 0, _)) > -1) {
            E = O > 12;
            break;
          }
      } else
        E = C === (_ ? "pm" : "PM");
      return E;
    }, p = { A: [s, function(C) {
      this.afternoon = y(C, !1);
    }], a: [s, function(C) {
      this.afternoon = y(C, !0);
    }], S: [/\d/, function(C) {
      this.milliseconds = 100 * +C;
    }], SS: [i, function(C) {
      this.milliseconds = 10 * +C;
    }], SSS: [/\d{3}/, function(C) {
      this.milliseconds = +C;
    }], s: [a, l("seconds")], ss: [a, l("seconds")], m: [a, l("minutes")], mm: [a, l("minutes")], H: [a, l("hours")], h: [a, l("hours")], HH: [a, l("hours")], hh: [a, l("hours")], D: [a, l("day")], DD: [i, l("day")], Do: [s, function(C) {
      var _ = c.ordinal, E = C.match(/\d+/);
      if (this.day = E[0], _)
        for (var W = 1; W <= 31; W += 1)
          _(W).replace(/\[|\]/g, "") === C && (this.day = W);
    }], M: [a, l("month")], MM: [i, l("month")], MMM: [s, function(C) {
      var _ = v("months"), E = (v("monthsShort") || _.map(function(W) {
        return W.slice(0, 3);
      })).indexOf(C) + 1;
      if (E < 1)
        throw new Error();
      this.month = E % 12 || E;
    }], MMMM: [s, function(C) {
      var _ = v("months").indexOf(C) + 1;
      if (_ < 1)
        throw new Error();
      this.month = _ % 12 || _;
    }], Y: [/[+-]?\d+/, l("year")], YY: [i, function(C) {
      this.year = g(C);
    }], YYYY: [/\d{4}/, l("year")], Z: b, ZZ: b };
    function I(C) {
      var _, E;
      _ = C, E = c && c.formats;
      for (var W = (C = _.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g, function(x, m, u) {
        var h = u && u.toUpperCase();
        return m || E[u] || r[u] || E[h].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g, function(T, o, F) {
          return o || F.slice(1);
        });
      })).match(n), O = W.length, R = 0; R < O; R += 1) {
        var P = W[R], w = p[P], Y = w && w[0], B = w && w[1];
        W[R] = B ? { regex: Y, parser: B } : P.replace(/^\[|\]$/g, "");
      }
      return function(x) {
        for (var m = {}, u = 0, h = 0; u < O; u += 1) {
          var T = W[u];
          if (typeof T == "string")
            h += T.length;
          else {
            var o = T.regex, F = T.parser, f = x.slice(h), A = o.exec(f)[0];
            F.call(m, A), x = x.replace(A, "");
          }
        }
        return function(Z) {
          var j = Z.afternoon;
          if (j !== void 0) {
            var k = Z.hours;
            j ? k < 12 && (Z.hours += 12) : k === 12 && (Z.hours = 0), delete Z.afternoon;
          }
        }(m), m;
      };
    }
    return function(C, _, E) {
      E.p.customParseFormat = !0, C && C.parseTwoDigitYear && (g = C.parseTwoDigitYear);
      var W = _.prototype, O = W.parse;
      W.parse = function(R) {
        var P = R.date, w = R.utc, Y = R.args;
        this.$u = w;
        var B = Y[1];
        if (typeof B == "string") {
          var x = Y[2] === !0, m = Y[3] === !0, u = x || m, h = Y[2];
          m && (h = Y[2]), c = this.$locale(), !x && h && (c = E.Ls[h]), this.$d = function(f, A, Z) {
            try {
              if (["x", "X"].indexOf(A) > -1)
                return new Date((A === "X" ? 1e3 : 1) * f);
              var j = I(A)(f), k = j.year, U = j.month, S = j.day, V = j.hours, q = j.minutes, z = j.seconds, H = j.milliseconds, ht = j.zone, $ = new Date(), M = S || (k || U ? 1 : $.getDate()), D = k || $.getFullYear(), L = 0;
              k && !U || (L = U > 0 ? U - 1 : $.getMonth());
              var d = V || 0, G = q || 0, N = z || 0, Q = H || 0;
              return ht ? new Date(Date.UTC(D, L, M, d, G, N, Q + 60 * ht.offset * 1e3)) : Z ? new Date(Date.UTC(D, L, M, d, G, N, Q)) : new Date(D, L, M, d, G, N, Q);
            } catch {
              return new Date("");
            }
          }(P, B, w), this.init(), h && h !== !0 && (this.$L = this.locale(h).$L), u && P != this.format(B) && (this.$d = new Date("")), c = {};
        } else if (B instanceof Array)
          for (var T = B.length, o = 1; o <= T; o += 1) {
            Y[1] = B[o - 1];
            var F = E.apply(this, Y);
            if (F.isValid()) {
              this.$d = F.$d, this.$L = F.$L, this.init();
              break;
            }
            o === T && (this.$d = new Date(""));
          }
        else
          O.call(this, R);
      };
    };
  });
})(Na);
const Ia = Me;
var we = {}, Wa = {
  get exports() {
    return we;
  },
  set exports(t) {
    we = t;
  }
};
(function(t, e) {
  (function(r, n) {
    t.exports = n();
  })(_e, function() {
    return function(r, n) {
      var i = n.prototype, a = i.format;
      i.format = function(s) {
        var c = this, g = this.$locale();
        if (!this.isValid())
          return a.bind(this)(s);
        var l = this.$utils(), b = (s || "YYYY-MM-DDTHH:mm:ssZ").replace(/\[([^\]]+)]|Q|wo|ww|w|WW|W|zzz|z|gggg|GGGG|Do|X|x|k{1,2}|S/g, function(v) {
          switch (v) {
            case "Q":
              return Math.ceil((c.$M + 1) / 3);
            case "Do":
              return g.ordinal(c.$D);
            case "gggg":
              return c.weekYear();
            case "GGGG":
              return c.isoWeekYear();
            case "wo":
              return g.ordinal(c.week(), "W");
            case "w":
            case "ww":
              return l.s(c.week(), v === "w" ? 1 : 2, "0");
            case "W":
            case "WW":
              return l.s(c.isoWeek(), v === "W" ? 1 : 2, "0");
            case "k":
            case "kk":
              return l.s(String(c.$H === 0 ? 24 : c.$H), v === "k" ? 1 : 2, "0");
            case "X":
              return Math.floor(c.$d.getTime() / 1e3);
            case "x":
              return c.$d.getTime();
            case "z":
              return "[" + c.offsetName() + "]";
            case "zzz":
              return "[" + c.offsetName("long") + "]";
            default:
              return v;
          }
        });
        return a.bind(this)(b);
      };
    };
  });
})(Wa);
const za = we;
nt.extend(Ea);
nt.extend(Ia);
nt.extend(za);
let st = "", We = "", ze, Oe = "", Et = [], Nt = [], He = {}, Pe = [], te = [], _t = "";
const Xn = ["active", "done", "crit", "milestone"];
let Ve = [], It = !1, Re = !1, Ce = 0;
const Oa = function(t, e, r) {
  ur.parseDirective(this, t, e, r);
}, Ha = function() {
  Pe = [], te = [], _t = "", Ve = [], Vt = 0, Se = void 0, Rt = void 0, K = [], st = "", We = "", ze = void 0, Oe = "", Et = [], Nt = [], It = !1, Re = !1, Ce = 0, He = {}, yr();
}, Pa = function(t) {
  We = t;
}, Va = function() {
  return We;
}, Ra = function(t) {
  ze = t;
}, Ba = function() {
  return ze;
}, Za = function(t) {
  Oe = t;
}, ja = function() {
  return Oe;
}, Xa = function(t) {
  st = t;
}, qa = function() {
  It = !0;
}, Ga = function() {
  return It;
}, $a = function() {
  Re = !0;
}, Qa = function() {
  return Re;
}, Ja = function() {
  return st;
}, Ka = function(t) {
  Et = t.toLowerCase().split(/[\s,]+/);
}, ts = function() {
  return Et;
}, es = function(t) {
  Nt = t.toLowerCase().split(/[\s,]+/);
}, ns = function() {
  return Nt;
}, rs = function() {
  return He;
}, is = function(t) {
  _t = t, Pe.push(t);
}, as = function() {
  return Pe;
}, ss = function() {
  let t = fn();
  const e = 10;
  let r = 0;
  for (; !t && r < e; )
    t = fn(), r++;
  return te = K, te;
}, qn = function(t, e, r, n) {
  return n.includes(t.format(e.trim())) ? !1 : t.isoWeekday() >= 6 && r.includes("weekends") || r.includes(t.format("dddd").toLowerCase()) ? !0 : r.includes(t.format(e.trim()));
}, Gn = function(t, e, r, n) {
  if (!r.length || t.manualEndTime)
    return;
  let i;
  t.startTime instanceof Date ? i = nt(t.startTime) : i = nt(t.startTime, e, !0), i = i.add(1, "d");
  let a;
  t.endTime instanceof Date ? a = nt(t.endTime) : a = nt(t.endTime, e, !0);
  const [s, c] = os(
    i,
    a,
    e,
    r,
    n
  );
  t.endTime = s.toDate(), t.renderEndTime = c;
}, os = function(t, e, r, n, i) {
  let a = !1, s = null;
  for (; t <= e; )
    a || (s = e.toDate()), a = qn(t, r, n, i), a && (e = e.add(1, "d")), t = t.add(1, "d");
  return [e, s];
}, De = function(t, e, r) {
  r = r.trim();
  const i = /^after\s+([\d\w- ]+)/.exec(r.trim());
  if (i !== null) {
    let s = null;
    if (i[1].split(" ").forEach(function(c) {
      let g = At(c);
      g !== void 0 && (s ? g.endTime > s.endTime && (s = g) : s = g);
    }), s)
      return s.endTime;
    {
      const c = new Date();
      return c.setHours(0, 0, 0, 0), c;
    }
  }
  let a = nt(r, e.trim(), !0);
  if (a.isValid())
    return a.toDate();
  {
    me.debug("Invalid date:" + r), me.debug("With date format:" + e.trim());
    const s = new Date(r);
    if (s === void 0 || isNaN(s.getTime()))
      throw new Error("Invalid date:" + r);
    return s;
  }
}, $n = function(t) {
  const e = /^(\d+(?:\.\d+)?)([Mdhmswy]|ms)$/.exec(t.trim());
  return e !== null ? [Number.parseFloat(e[1]), e[2]] : [NaN, "ms"];
}, Qn = function(t, e, r, n = !1) {
  r = r.trim();
  let i = nt(r, e.trim(), !0);
  if (i.isValid())
    return n && (i = i.add(1, "d")), i.toDate();
  let a = nt(t);
  const [s, c] = $n(r);
  if (!Number.isNaN(s)) {
    const g = a.add(s, c);
    g.isValid() && (a = g);
  }
  return a.toDate();
};
let Vt = 0;
const xt = function(t) {
  return t === void 0 ? (Vt = Vt + 1, "task" + Vt) : t;
}, cs = function(t, e) {
  let r;
  e.substr(0, 1) === ":" ? r = e.substr(1, e.length) : r = e;
  const n = r.split(","), i = {};
  er(n, i, Xn);
  for (let s = 0; s < n.length; s++)
    n[s] = n[s].trim();
  let a = "";
  switch (n.length) {
    case 1:
      i.id = xt(), i.startTime = t.endTime, a = n[0];
      break;
    case 2:
      i.id = xt(), i.startTime = De(void 0, st, n[0]), a = n[1];
      break;
    case 3:
      i.id = xt(n[0]), i.startTime = De(void 0, st, n[1]), a = n[2];
      break;
  }
  return a && (i.endTime = Qn(i.startTime, st, a, It), i.manualEndTime = nt(a, "YYYY-MM-DD", !0).isValid(), Gn(i, st, Nt, Et)), i;
}, us = function(t, e) {
  let r;
  e.substr(0, 1) === ":" ? r = e.substr(1, e.length) : r = e;
  const n = r.split(","), i = {};
  er(n, i, Xn);
  for (let a = 0; a < n.length; a++)
    n[a] = n[a].trim();
  switch (n.length) {
    case 1:
      i.id = xt(), i.startTime = {
        type: "prevTaskEnd",
        id: t
      }, i.endTime = {
        data: n[0]
      };
      break;
    case 2:
      i.id = xt(), i.startTime = {
        type: "getStartDate",
        startData: n[0]
      }, i.endTime = {
        data: n[1]
      };
      break;
    case 3:
      i.id = xt(n[0]), i.startTime = {
        type: "getStartDate",
        startData: n[1]
      }, i.endTime = {
        data: n[2]
      };
      break;
  }
  return i;
};
let Se, Rt, K = [];
const Jn = {}, ls = function(t, e) {
  const r = {
    section: _t,
    type: _t,
    processed: !1,
    manualEndTime: !1,
    renderEndTime: null,
    raw: { data: e },
    task: t,
    classes: []
  }, n = us(Rt, e);
  r.raw.startTime = n.startTime, r.raw.endTime = n.endTime, r.id = n.id, r.prevTaskId = Rt, r.active = n.active, r.done = n.done, r.crit = n.crit, r.milestone = n.milestone, r.order = Ce, Ce++;
  const i = K.push(r);
  Rt = r.id, Jn[r.id] = i - 1;
}, At = function(t) {
  const e = Jn[t];
  return K[e];
}, fs = function(t, e) {
  const r = {
    section: _t,
    type: _t,
    description: t,
    task: t,
    classes: []
  }, n = cs(Se, e);
  r.startTime = n.startTime, r.endTime = n.endTime, r.id = n.id, r.active = n.active, r.done = n.done, r.crit = n.crit, r.milestone = n.milestone, Se = r, te.push(r);
}, fn = function() {
  const t = function(r) {
    const n = K[r];
    let i = "";
    switch (K[r].raw.startTime.type) {
      case "prevTaskEnd": {
        const a = At(n.prevTaskId);
        n.startTime = a.endTime;
        break;
      }
      case "getStartDate":
        i = De(void 0, st, K[r].raw.startTime.startData), i && (K[r].startTime = i);
        break;
    }
    return K[r].startTime && (K[r].endTime = Qn(
      K[r].startTime,
      st,
      K[r].raw.endTime.data,
      It
    ), K[r].endTime && (K[r].processed = !0, K[r].manualEndTime = nt(
      K[r].raw.endTime.data,
      "YYYY-MM-DD",
      !0
    ).isValid(), Gn(K[r], st, Nt, Et))), K[r].processed;
  };
  let e = !0;
  for (const [r, n] of K.entries())
    t(r), e = e && n.processed;
  return e;
}, hs = function(t, e) {
  let r = e;
  vt().securityLevel !== "loose" && (r = nr(e)), t.split(",").forEach(function(n) {
    At(n) !== void 0 && (tr(n, () => {
      window.open(r, "_self");
    }), He[n] = r);
  }), Kn(t, "clickable");
}, Kn = function(t, e) {
  t.split(",").forEach(function(r) {
    let n = At(r);
    n !== void 0 && n.classes.push(e);
  });
}, ms = function(t, e, r) {
  if (vt().securityLevel !== "loose" || e === void 0)
    return;
  let n = [];
  if (typeof r == "string") {
    n = r.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
    for (let a = 0; a < n.length; a++) {
      let s = n[a].trim();
      s.charAt(0) === '"' && s.charAt(s.length - 1) === '"' && (s = s.substr(1, s.length - 2)), n[a] = s;
    }
  }
  n.length === 0 && n.push(t), At(t) !== void 0 && tr(t, () => {
    rr.runFunc(e, ...n);
  });
}, tr = function(t, e) {
  Ve.push(
    function() {
      const r = document.querySelector(`[id="${t}"]`);
      r !== null && r.addEventListener("click", function() {
        e();
      });
    },
    function() {
      const r = document.querySelector(`[id="${t}-text"]`);
      r !== null && r.addEventListener("click", function() {
        e();
      });
    }
  );
}, ds = function(t, e, r) {
  t.split(",").forEach(function(n) {
    ms(n, e, r);
  }), Kn(t, "clickable");
}, gs = function(t) {
  Ve.forEach(function(e) {
    e(t);
  });
}, ys = {
  parseDirective: Oa,
  getConfig: () => vt().gantt,
  clear: Ha,
  setDateFormat: Xa,
  getDateFormat: Ja,
  enableInclusiveEndDates: qa,
  endDatesAreInclusive: Ga,
  enableTopAxis: $a,
  topAxisEnabled: Qa,
  setAxisFormat: Pa,
  getAxisFormat: Va,
  setTickInterval: Ra,
  getTickInterval: Ba,
  setTodayMarker: Za,
  getTodayMarker: ja,
  setAccTitle: lr,
  getAccTitle: fr,
  setDiagramTitle: hr,
  getDiagramTitle: mr,
  setAccDescription: dr,
  getAccDescription: gr,
  addSection: is,
  getSections: as,
  getTasks: ss,
  addTask: ls,
  findTaskById: At,
  addTaskOrg: fs,
  setIncludes: Ka,
  getIncludes: ts,
  setExcludes: es,
  getExcludes: ns,
  setClickEvent: ds,
  setLink: hs,
  getLinks: rs,
  bindFunctions: gs,
  parseDuration: $n,
  isInvalidDate: qn
};
function er(t, e, r) {
  let n = !0;
  for (; n; )
    n = !1, r.forEach(function(i) {
      const a = "^\\s*" + i + "\\s*$", s = new RegExp(a);
      t[0].match(s) && (e[i] = !0, t.shift(1), n = !0);
    });
}
const ps = function() {
  me.debug("Something is calling, setConf, remove the call");
};
let ct;
const ks = function(t, e, r, n) {
  const i = vt().gantt, a = vt().securityLevel;
  let s;
  a === "sandbox" && (s = Wt("#i" + e));
  const c = a === "sandbox" ? Wt(s.nodes()[0].contentDocument.body) : Wt("body"), g = a === "sandbox" ? s.nodes()[0].contentDocument : document, l = g.getElementById(e);
  ct = l.parentElement.offsetWidth, ct === void 0 && (ct = 1200), i.useWidth !== void 0 && (ct = i.useWidth);
  const b = n.db.getTasks(), v = b.length * (i.barHeight + i.barGap) + 2 * i.topPadding;
  l.setAttribute("viewBox", "0 0 " + ct + " " + v);
  const y = c.select(`[id="${e}"]`), p = Ya().domain([
    Dr(b, function(m) {
      return m.startTime;
    }),
    Cr(b, function(m) {
      return m.endTime;
    })
  ]).rangeRound([0, ct - i.leftPadding - i.rightPadding]);
  let I = [];
  for (const m of b)
    I.push(m.type);
  const C = I;
  I = Y(I);
  function _(m, u) {
    const h = m.startTime, T = u.startTime;
    let o = 0;
    return h > T ? o = 1 : h < T && (o = -1), o;
  }
  b.sort(_), E(b, ct, v), pr(y, v, ct, i.useMaxWidth), y.append("text").text(n.db.getDiagramTitle()).attr("x", ct / 2).attr("y", i.titleTopMargin).attr("class", "titleText");
  function E(m, u, h) {
    const T = i.barHeight, o = T + i.barGap, F = i.topPadding, f = i.leftPadding, A = Yn().domain([0, I.length]).range(["#00B9FA", "#F95002"]).interpolate(Xr);
    O(
      o,
      F,
      f,
      u,
      h,
      m,
      n.db.getExcludes(),
      n.db.getIncludes()
    ), R(f, F, u, h), W(m, o, F, f, T, A, u), P(o, F), w(f, F, u, h);
  }
  function W(m, u, h, T, o, F, f) {
    y.append("g").selectAll("rect").data(m).enter().append("rect").attr("x", 0).attr("y", function(k, U) {
      return U = k.order, U * u + h - 2;
    }).attr("width", function() {
      return f - i.rightPadding / 2;
    }).attr("height", u).attr("class", function(k) {
      for (const [U, S] of I.entries())
        if (k.type === S)
          return "section section" + U % i.numberSectionStyles;
      return "section section0";
    });
    const A = y.append("g").selectAll("rect").data(m).enter(), Z = n.db.getLinks();
    if (A.append("rect").attr("id", function(k) {
      return k.id;
    }).attr("rx", 3).attr("ry", 3).attr("x", function(k) {
      return k.milestone ? p(k.startTime) + T + 0.5 * (p(k.endTime) - p(k.startTime)) - 0.5 * o : p(k.startTime) + T;
    }).attr("y", function(k, U) {
      return U = k.order, U * u + h;
    }).attr("width", function(k) {
      return k.milestone ? o : p(k.renderEndTime || k.endTime) - p(k.startTime);
    }).attr("height", o).attr("transform-origin", function(k, U) {
      return U = k.order, (p(k.startTime) + T + 0.5 * (p(k.endTime) - p(k.startTime))).toString() + "px " + (U * u + h + 0.5 * o).toString() + "px";
    }).attr("class", function(k) {
      const U = "task";
      let S = "";
      k.classes.length > 0 && (S = k.classes.join(" "));
      let V = 0;
      for (const [z, H] of I.entries())
        k.type === H && (V = z % i.numberSectionStyles);
      let q = "";
      return k.active ? k.crit ? q += " activeCrit" : q = " active" : k.done ? k.crit ? q = " doneCrit" : q = " done" : k.crit && (q += " crit"), q.length === 0 && (q = " task"), k.milestone && (q = " milestone " + q), q += V, q += " " + S, U + q;
    }), A.append("text").attr("id", function(k) {
      return k.id + "-text";
    }).text(function(k) {
      return k.task;
    }).attr("font-size", i.fontSize).attr("x", function(k) {
      let U = p(k.startTime), S = p(k.renderEndTime || k.endTime);
      k.milestone && (U += 0.5 * (p(k.endTime) - p(k.startTime)) - 0.5 * o), k.milestone && (S = U + o);
      const V = this.getBBox().width;
      return V > S - U ? S + V + 1.5 * i.leftPadding > f ? U + T - 5 : S + T + 5 : (S - U) / 2 + U + T;
    }).attr("y", function(k, U) {
      return U = k.order, U * u + i.barHeight / 2 + (i.fontSize / 2 - 2) + h;
    }).attr("text-height", o).attr("class", function(k) {
      const U = p(k.startTime);
      let S = p(k.endTime);
      k.milestone && (S = U + o);
      const V = this.getBBox().width;
      let q = "";
      k.classes.length > 0 && (q = k.classes.join(" "));
      let z = 0;
      for (const [ht, $] of I.entries())
        k.type === $ && (z = ht % i.numberSectionStyles);
      let H = "";
      return k.active && (k.crit ? H = "activeCritText" + z : H = "activeText" + z), k.done ? k.crit ? H = H + " doneCritText" + z : H = H + " doneText" + z : k.crit && (H = H + " critText" + z), k.milestone && (H += " milestoneText"), V > S - U ? S + V + 1.5 * i.leftPadding > f ? q + " taskTextOutsideLeft taskTextOutside" + z + " " + H : q + " taskTextOutsideRight taskTextOutside" + z + " " + H + " width-" + V : q + " taskText taskText" + z + " " + H + " width-" + V;
    }), vt().securityLevel === "sandbox") {
      let k;
      k = Wt("#i" + e);
      const U = k.nodes()[0].contentDocument;
      A.filter(function(S) {
        return Z[S.id] !== void 0;
      }).each(function(S) {
        var V = U.querySelector("#" + S.id), q = U.querySelector("#" + S.id + "-text");
        const z = V.parentNode;
        var H = U.createElement("a");
        H.setAttribute("xlink:href", Z[S.id]), H.setAttribute("target", "_top"), z.appendChild(H), H.appendChild(V), H.appendChild(q);
      });
    }
  }
  function O(m, u, h, T, o, F, f, A) {
    const Z = F.reduce(
      (z, { startTime: H }) => z ? Math.min(z, H) : H,
      0
    ), j = F.reduce((z, { endTime: H }) => z ? Math.max(z, H) : H, 0), k = n.db.getDateFormat();
    if (!Z || !j)
      return;
    const U = [];
    let S = null, V = nt(Z);
    for (; V.valueOf() <= j; )
      n.db.isInvalidDate(V, k, f, A) ? S ? S.end = V : S = {
        start: V,
        end: V
      } : S && (U.push(S), S = null), V = V.add(1, "d");
    y.append("g").selectAll("rect").data(U).enter().append("rect").attr("id", function(z) {
      return "exclude-" + z.start.format("YYYY-MM-DD");
    }).attr("x", function(z) {
      return p(z.start) + h;
    }).attr("y", i.gridLineStartPadding).attr("width", function(z) {
      const H = z.end.add(1, "day");
      return p(H) - p(z.start);
    }).attr("height", o - u - i.gridLineStartPadding).attr("transform-origin", function(z, H) {
      return (p(z.start) + h + 0.5 * (p(z.end) - p(z.start))).toString() + "px " + (H * m + 0.5 * o).toString() + "px";
    }).attr("class", "exclude-range");
  }
  function R(m, u, h, T) {
    let o = Er(p).tickSize(-T + u + i.gridLineStartPadding).tickFormat(Kt(n.db.getAxisFormat() || i.axisFormat || "%Y-%m-%d"));
    const f = /^([1-9]\d*)(minute|hour|day|week|month)$/.exec(
      n.db.getTickInterval() || i.tickInterval
    );
    if (f !== null) {
      const A = f[1];
      switch (f[2]) {
        case "minute":
          o.ticks(qt.every(A));
          break;
        case "hour":
          o.ticks(Gt.every(A));
          break;
        case "day":
          o.ticks(Mt.every(A));
          break;
        case "week":
          o.ticks(wt.every(A));
          break;
        case "month":
          o.ticks(Qt.every(A));
          break;
      }
    }
    if (y.append("g").attr("class", "grid").attr("transform", "translate(" + m + ", " + (T - 50) + ")").call(o).selectAll("text").style("text-anchor", "middle").attr("fill", "#000").attr("stroke", "none").attr("font-size", 10).attr("dy", "1em"), n.db.topAxisEnabled() || i.topAxis) {
      let A = Lr(p).tickSize(-T + u + i.gridLineStartPadding).tickFormat(Kt(n.db.getAxisFormat() || i.axisFormat || "%Y-%m-%d"));
      if (f !== null) {
        const Z = f[1];
        switch (f[2]) {
          case "minute":
            A.ticks(qt.every(Z));
            break;
          case "hour":
            A.ticks(Gt.every(Z));
            break;
          case "day":
            A.ticks(Mt.every(Z));
            break;
          case "week":
            A.ticks(wt.every(Z));
            break;
          case "month":
            A.ticks(Qt.every(Z));
            break;
        }
      }
      y.append("g").attr("class", "grid").attr("transform", "translate(" + m + ", " + u + ")").call(A).selectAll("text").style("text-anchor", "middle").attr("fill", "#000").attr("stroke", "none").attr("font-size", 10);
    }
  }
  function P(m, u) {
    const h = [];
    let T = 0;
    for (const [o, F] of I.entries())
      h[o] = [F, x(F, C)];
    y.append("g").selectAll("text").data(h).enter().append(function(o) {
      const F = o[0].split(cr.lineBreakRegex), f = -(F.length - 1) / 2, A = g.createElementNS("http://www.w3.org/2000/svg", "text");
      A.setAttribute("dy", f + "em");
      for (const [Z, j] of F.entries()) {
        const k = g.createElementNS("http://www.w3.org/2000/svg", "tspan");
        k.setAttribute("alignment-baseline", "central"), k.setAttribute("x", "10"), Z > 0 && k.setAttribute("dy", "1em"), k.textContent = j, A.appendChild(k);
      }
      return A;
    }).attr("x", 10).attr("y", function(o, F) {
      if (F > 0)
        for (let f = 0; f < F; f++)
          return T += h[F - 1][1], o[1] * m / 2 + T * m + u;
      else
        return o[1] * m / 2 + u;
    }).attr("font-size", i.sectionFontSize).attr("font-size", i.sectionFontSize).attr("class", function(o) {
      for (const [F, f] of I.entries())
        if (o[0] === f)
          return "sectionTitle sectionTitle" + F % i.numberSectionStyles;
      return "sectionTitle";
    });
  }
  function w(m, u, h, T) {
    const o = n.db.getTodayMarker();
    if (o === "off")
      return;
    const F = y.append("g").attr("class", "today"), f = new Date(), A = F.append("line");
    A.attr("x1", p(f) + m).attr("x2", p(f) + m).attr("y1", i.titleTopMargin).attr("y2", T - i.titleTopMargin).attr("class", "today"), o !== "" && A.attr("style", o.replace(/,/g, ";"));
  }
  function Y(m) {
    const u = {}, h = [];
    for (let T = 0, o = m.length; T < o; ++T)
      Object.prototype.hasOwnProperty.call(u, m[T]) || (u[m[T]] = !0, h.push(m[T]));
    return h;
  }
  function B(m) {
    let u = m.length;
    const h = {};
    for (; u; )
      h[m[--u]] = (h[m[u]] || 0) + 1;
    return h;
  }
  function x(m, u) {
    return B(u)[m] || 0;
  }
}, vs = {
  setConf: ps,
  draw: ks
}, Ts = (t) => `
  .mermaid-main-font {
    font-family: "trebuchet ms", verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);
  }
  .exclude-range {
    fill: ${t.excludeBkgColor};
  }

  .section {
    stroke: none;
    opacity: 0.2;
  }

  .section0 {
    fill: ${t.sectionBkgColor};
  }

  .section2 {
    fill: ${t.sectionBkgColor2};
  }

  .section1,
  .section3 {
    fill: ${t.altSectionBkgColor};
    opacity: 0.2;
  }

  .sectionTitle0 {
    fill: ${t.titleColor};
  }

  .sectionTitle1 {
    fill: ${t.titleColor};
  }

  .sectionTitle2 {
    fill: ${t.titleColor};
  }

  .sectionTitle3 {
    fill: ${t.titleColor};
  }

  .sectionTitle {
    text-anchor: start;
    // font-size: ${t.ganttFontSize};
    // text-height: 14px;
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);

  }


  /* Grid and axis */

  .grid .tick {
    stroke: ${t.gridColor};
    opacity: 0.8;
    shape-rendering: crispEdges;
    text {
      font-family: ${t.fontFamily};
      fill: ${t.textColor};
    }
  }

  .grid path {
    stroke-width: 0;
  }


  /* Today line */

  .today {
    fill: none;
    stroke: ${t.todayLineColor};
    stroke-width: 2px;
  }


  /* Task styling */

  /* Default task */

  .task {
    stroke-width: 2;
  }

  .taskText {
    text-anchor: middle;
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);
  }

  // .taskText:not([font-size]) {
  //   font-size: ${t.ganttFontSize};
  // }

  .taskTextOutsideRight {
    fill: ${t.taskTextDarkColor};
    text-anchor: start;
    // font-size: ${t.ganttFontSize};
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);

  }

  .taskTextOutsideLeft {
    fill: ${t.taskTextDarkColor};
    text-anchor: end;
    // font-size: ${t.ganttFontSize};
  }

  /* Special case clickable */
  .task.clickable {
    cursor: pointer;
  }
  .taskText.clickable {
    cursor: pointer;
    fill: ${t.taskTextClickableColor} !important;
    font-weight: bold;
  }

  .taskTextOutsideLeft.clickable {
    cursor: pointer;
    fill: ${t.taskTextClickableColor} !important;
    font-weight: bold;
  }

  .taskTextOutsideRight.clickable {
    cursor: pointer;
    fill: ${t.taskTextClickableColor} !important;
    font-weight: bold;
  }

  /* Specific task settings for the sections*/

  .taskText0,
  .taskText1,
  .taskText2,
  .taskText3 {
    fill: ${t.taskTextColor};
  }

  .task0,
  .task1,
  .task2,
  .task3 {
    fill: ${t.taskBkgColor};
    stroke: ${t.taskBorderColor};
  }

  .taskTextOutside0,
  .taskTextOutside2
  {
    fill: ${t.taskTextOutsideColor};
  }

  .taskTextOutside1,
  .taskTextOutside3 {
    fill: ${t.taskTextOutsideColor};
  }


  /* Active task */

  .active0,
  .active1,
  .active2,
  .active3 {
    fill: ${t.activeTaskBkgColor};
    stroke: ${t.activeTaskBorderColor};
  }

  .activeText0,
  .activeText1,
  .activeText2,
  .activeText3 {
    fill: ${t.taskTextDarkColor} !important;
  }


  /* Completed task */

  .done0,
  .done1,
  .done2,
  .done3 {
    stroke: ${t.doneTaskBorderColor};
    fill: ${t.doneTaskBkgColor};
    stroke-width: 2;
  }

  .doneText0,
  .doneText1,
  .doneText2,
  .doneText3 {
    fill: ${t.taskTextDarkColor} !important;
  }


  /* Tasks on the critical line */

  .crit0,
  .crit1,
  .crit2,
  .crit3 {
    stroke: ${t.critBorderColor};
    fill: ${t.critBkgColor};
    stroke-width: 2;
  }

  .activeCrit0,
  .activeCrit1,
  .activeCrit2,
  .activeCrit3 {
    stroke: ${t.critBorderColor};
    fill: ${t.activeTaskBkgColor};
    stroke-width: 2;
  }

  .doneCrit0,
  .doneCrit1,
  .doneCrit2,
  .doneCrit3 {
    stroke: ${t.critBorderColor};
    fill: ${t.doneTaskBkgColor};
    stroke-width: 2;
    cursor: pointer;
    shape-rendering: crispEdges;
  }

  .milestone {
    transform: rotate(45deg) scale(0.8,0.8);
  }

  .milestoneText {
    font-style: italic;
  }
  .doneCritText0,
  .doneCritText1,
  .doneCritText2,
  .doneCritText3 {
    fill: ${t.taskTextDarkColor} !important;
  }

  .activeCritText0,
  .activeCritText1,
  .activeCritText2,
  .activeCritText3 {
    fill: ${t.taskTextDarkColor} !important;
  }

  .titleText {
    text-anchor: middle;
    font-size: 18px;
    fill: ${t.textColor}    ;
    font-family: 'trebuchet ms', verdana, arial, sans-serif;
    font-family: var(--mermaid-font-family);
  }
`, xs = Ts, As = {
  parser: Ua,
  db: ys,
  renderer: vs,
  styles: xs
};
export {
  As as diagram
};
//# sourceMappingURL=ganttDiagram-2c592def.js.map
