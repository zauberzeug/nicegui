import { I as He, J as Ve, R as Pe, K as Re, L as Dn, M as Gt, N as Cn, O as de, P as me, c as pt, s as Mn, g as _n, z as Sn, A as Yn, b as Fn, a as Un, Q as nt, m as Ln, B as En, e as An, x as In, l as ae, j as It, k as Wn, f as On } from "./mermaid-be6aa4a6.js";
import { b as zn, t as Me, c as Nn, a as Hn, l as Vn } from "./linear-d8b7ca63.js";
import { i as Pn } from "./init-f9637058.js";
function Rn(t, e) {
  let n;
  if (e === void 0)
    for (const r of t)
      r != null && (n < r || n === void 0 && r >= r) && (n = r);
  else {
    let r = -1;
    for (let i of t)
      (i = e(i, ++r, t)) != null && (n < i || n === void 0 && i >= i) && (n = i);
  }
  return n;
}
function Bn(t, e) {
  let n;
  if (e === void 0)
    for (const r of t)
      r != null && (n > r || n === void 0 && r >= r) && (n = r);
  else {
    let r = -1;
    for (let i of t)
      (i = e(i, ++r, t)) != null && (n > i || n === void 0 && i >= i) && (n = i);
  }
  return n;
}
function Zn(t) {
  return t;
}
var Ot = 1, Qt = 2, oe = 3, Wt = 4, _e = 1e-6;
function Xn(t) {
  return "translate(" + t + ",0)";
}
function qn(t) {
  return "translate(0," + t + ")";
}
function jn(t) {
  return (e) => +t(e);
}
function Gn(t, e) {
  return e = Math.max(0, t.bandwidth() - e * 2) / 2, t.round() && (e = Math.round(e)), (n) => +t(n) + e;
}
function Qn() {
  return !this.__axis;
}
function Be(t, e) {
  var n = [], r = null, i = null, s = 6, o = 6, y = 3, M = typeof window < "u" && window.devicePixelRatio > 1 ? 0 : 0.5, p = t === Ot || t === Wt ? -1 : 1, C = t === Wt || t === Qt ? "x" : "y", S = t === Ot || t === oe ? Xn : qn;
  function w(b) {
    var P = r ?? (e.ticks ? e.ticks.apply(e, n) : e.domain()), g = i ?? (e.tickFormat ? e.tickFormat.apply(e, n) : Zn), F = Math.max(s, 0) + y, z = e.range(), O = +z[0] + M, H = +z[z.length - 1] + M, V = (e.bandwidth ? Gn : jn)(e.copy(), M), j = b.selection ? b.selection() : b, x = j.selectAll(".domain").data([null]), E = j.selectAll(".tick").data(P, e).order(), v = E.exit(), u = E.enter().append("g").attr("class", "tick"), f = E.select("line"), d = E.select("text");
    x = x.merge(x.enter().insert("path", ".tick").attr("class", "domain").attr("stroke", "currentColor")), E = E.merge(u), f = f.merge(u.append("line").attr("stroke", "currentColor").attr(C + "2", p * s)), d = d.merge(u.append("text").attr("fill", "currentColor").attr(C, p * F).attr("dy", t === Ot ? "0em" : t === oe ? "0.71em" : "0.32em")), b !== j && (x = x.transition(b), E = E.transition(b), f = f.transition(b), d = d.transition(b), v = v.transition(b).attr("opacity", _e).attr("transform", function(c) {
      return isFinite(c = V(c)) ? S(c + M) : this.getAttribute("transform");
    }), u.attr("opacity", _e).attr("transform", function(c) {
      var T = this.parentNode.__axis;
      return S((T && isFinite(T = T(c)) ? T : V(c)) + M);
    })), v.remove(), x.attr("d", t === Wt || t === Qt ? o ? "M" + p * o + "," + O + "H" + M + "V" + H + "H" + p * o : "M" + M + "," + O + "V" + H : o ? "M" + O + "," + p * o + "V" + M + "H" + H + "V" + p * o : "M" + O + "," + M + "H" + H), E.attr("opacity", 1).attr("transform", function(c) {
      return S(V(c) + M);
    }), f.attr(C + "2", p * s), d.attr(C, p * F).text(g), j.filter(Qn).attr("fill", "none").attr("font-size", 10).attr("font-family", "sans-serif").attr("text-anchor", t === Qt ? "start" : t === Wt ? "end" : "middle"), j.each(function() {
      this.__axis = V;
    });
  }
  return w.scale = function(b) {
    return arguments.length ? (e = b, w) : e;
  }, w.ticks = function() {
    return n = Array.from(arguments), w;
  }, w.tickArguments = function(b) {
    return arguments.length ? (n = b == null ? [] : Array.from(b), w) : n.slice();
  }, w.tickValues = function(b) {
    return arguments.length ? (r = b == null ? null : Array.from(b), w) : r && r.slice();
  }, w.tickFormat = function(b) {
    return arguments.length ? (i = b, w) : i;
  }, w.tickSize = function(b) {
    return arguments.length ? (s = o = +b, w) : s;
  }, w.tickSizeInner = function(b) {
    return arguments.length ? (s = +b, w) : s;
  }, w.tickSizeOuter = function(b) {
    return arguments.length ? (o = +b, w) : o;
  }, w.tickPadding = function(b) {
    return arguments.length ? (y = +b, w) : y;
  }, w.offset = function(b) {
    return arguments.length ? (M = +b, w) : M;
  }, w;
}
function Jn(t) {
  return Be(Ot, t);
}
function Kn(t) {
  return Be(oe, t);
}
const $n = Math.PI / 180, tr = 180 / Math.PI, Ht = 18, Ze = 0.96422, Xe = 1, qe = 0.82521, je = 4 / 29, vt = 6 / 29, Ge = 3 * vt * vt, er = vt * vt * vt;
function Qe(t) {
  if (t instanceof ot)
    return new ot(t.l, t.a, t.b, t.opacity);
  if (t instanceof ut)
    return Je(t);
  t instanceof Pe || (t = Dn(t));
  var e = te(t.r), n = te(t.g), r = te(t.b), i = Jt((0.2225045 * e + 0.7168786 * n + 0.0606169 * r) / Xe), s, o;
  return e === n && n === r ? s = o = i : (s = Jt((0.4360747 * e + 0.3850649 * n + 0.1430804 * r) / Ze), o = Jt((0.0139322 * e + 0.0971045 * n + 0.7141733 * r) / qe)), new ot(116 * i - 16, 500 * (s - i), 200 * (i - o), t.opacity);
}
function nr(t, e, n, r) {
  return arguments.length === 1 ? Qe(t) : new ot(t, e, n, r ?? 1);
}
function ot(t, e, n, r) {
  this.l = +t, this.a = +e, this.b = +n, this.opacity = +r;
}
He(ot, nr, Ve(Re, {
  brighter(t) {
    return new ot(this.l + Ht * (t ?? 1), this.a, this.b, this.opacity);
  },
  darker(t) {
    return new ot(this.l - Ht * (t ?? 1), this.a, this.b, this.opacity);
  },
  rgb() {
    var t = (this.l + 16) / 116, e = isNaN(this.a) ? t : t + this.a / 500, n = isNaN(this.b) ? t : t - this.b / 200;
    return e = Ze * Kt(e), t = Xe * Kt(t), n = qe * Kt(n), new Pe(
      $t(3.1338561 * e - 1.6168667 * t - 0.4906146 * n),
      $t(-0.9787684 * e + 1.9161415 * t + 0.033454 * n),
      $t(0.0719453 * e - 0.2289914 * t + 1.4052427 * n),
      this.opacity
    );
  }
}));
function Jt(t) {
  return t > er ? Math.pow(t, 1 / 3) : t / Ge + je;
}
function Kt(t) {
  return t > vt ? t * t * t : Ge * (t - je);
}
function $t(t) {
  return 255 * (t <= 31308e-7 ? 12.92 * t : 1.055 * Math.pow(t, 1 / 2.4) - 0.055);
}
function te(t) {
  return (t /= 255) <= 0.04045 ? t / 12.92 : Math.pow((t + 0.055) / 1.055, 2.4);
}
function rr(t) {
  if (t instanceof ut)
    return new ut(t.h, t.c, t.l, t.opacity);
  if (t instanceof ot || (t = Qe(t)), t.a === 0 && t.b === 0)
    return new ut(NaN, 0 < t.l && t.l < 100 ? 0 : NaN, t.l, t.opacity);
  var e = Math.atan2(t.b, t.a) * tr;
  return new ut(e < 0 ? e + 360 : e, Math.sqrt(t.a * t.a + t.b * t.b), t.l, t.opacity);
}
function ce(t, e, n, r) {
  return arguments.length === 1 ? rr(t) : new ut(t, e, n, r ?? 1);
}
function ut(t, e, n, r) {
  this.h = +t, this.c = +e, this.l = +n, this.opacity = +r;
}
function Je(t) {
  if (isNaN(t.h))
    return new ot(t.l, 0, 0, t.opacity);
  var e = t.h * $n;
  return new ot(t.l, Math.cos(e) * t.c, Math.sin(e) * t.c, t.opacity);
}
He(ut, ce, Ve(Re, {
  brighter(t) {
    return new ut(this.h, this.c, this.l + Ht * (t ?? 1), this.opacity);
  },
  darker(t) {
    return new ut(this.h, this.c, this.l - Ht * (t ?? 1), this.opacity);
  },
  rgb() {
    return Je(this).rgb();
  }
}));
function ir(t) {
  return function(e, n) {
    var r = t((e = ce(e)).h, (n = ce(n)).h), i = Gt(e.c, n.c), s = Gt(e.l, n.l), o = Gt(e.opacity, n.opacity);
    return function(y) {
      return e.h = r(y), e.c = i(y), e.l = s(y), e.opacity = o(y), e + "";
    };
  };
}
const sr = ir(Cn);
function ar(t, e) {
  t = t.slice();
  var n = 0, r = t.length - 1, i = t[n], s = t[r], o;
  return s < i && (o = n, n = r, r = o, o = i, i = s, s = o), t[n] = e.floor(i), t[r] = e.ceil(s), t;
}
var ee = /* @__PURE__ */ new Date(), ne = /* @__PURE__ */ new Date();
function et(t, e, n, r) {
  function i(s) {
    return t(s = arguments.length === 0 ? /* @__PURE__ */ new Date() : /* @__PURE__ */ new Date(+s)), s;
  }
  return i.floor = function(s) {
    return t(s = /* @__PURE__ */ new Date(+s)), s;
  }, i.ceil = function(s) {
    return t(s = new Date(s - 1)), e(s, 1), t(s), s;
  }, i.round = function(s) {
    var o = i(s), y = i.ceil(s);
    return s - o < y - s ? o : y;
  }, i.offset = function(s, o) {
    return e(s = /* @__PURE__ */ new Date(+s), o == null ? 1 : Math.floor(o)), s;
  }, i.range = function(s, o, y) {
    var M = [], p;
    if (s = i.ceil(s), y = y == null ? 1 : Math.floor(y), !(s < o) || !(y > 0))
      return M;
    do
      M.push(p = /* @__PURE__ */ new Date(+s)), e(s, y), t(s);
    while (p < s && s < o);
    return M;
  }, i.filter = function(s) {
    return et(function(o) {
      if (o >= o)
        for (; t(o), !s(o); )
          o.setTime(o - 1);
    }, function(o, y) {
      if (o >= o)
        if (y < 0)
          for (; ++y <= 0; )
            for (; e(o, -1), !s(o); )
              ;
        else
          for (; --y >= 0; )
            for (; e(o, 1), !s(o); )
              ;
    });
  }, n && (i.count = function(s, o) {
    return ee.setTime(+s), ne.setTime(+o), t(ee), t(ne), Math.floor(n(ee, ne));
  }, i.every = function(s) {
    return s = Math.floor(s), !isFinite(s) || !(s > 0) ? null : s > 1 ? i.filter(r ? function(o) {
      return r(o) % s === 0;
    } : function(o) {
      return i.count(0, o) % s === 0;
    }) : i;
  }), i;
}
var Vt = et(function() {
}, function(t, e) {
  t.setTime(+t + e);
}, function(t, e) {
  return e - t;
});
Vt.every = function(t) {
  return t = Math.floor(t), !isFinite(t) || !(t > 0) ? null : t > 1 ? et(function(e) {
    e.setTime(Math.floor(e / t) * t);
  }, function(e, n) {
    e.setTime(+e + n * t);
  }, function(e, n) {
    return (n - e) / t;
  }) : Vt;
};
const or = Vt;
Vt.range;
const lt = 1e3, st = lt * 60, ht = st * 60, dt = ht * 24, ge = dt * 7, Se = dt * 30, re = dt * 365;
var Ke = et(function(t) {
  t.setTime(t - t.getMilliseconds());
}, function(t, e) {
  t.setTime(+t + e * lt);
}, function(t, e) {
  return (e - t) / lt;
}, function(t) {
  return t.getUTCSeconds();
});
const Ft = Ke;
Ke.range;
var $e = et(function(t) {
  t.setTime(t - t.getMilliseconds() - t.getSeconds() * lt);
}, function(t, e) {
  t.setTime(+t + e * st);
}, function(t, e) {
  return (e - t) / st;
}, function(t) {
  return t.getMinutes();
});
const Pt = $e;
$e.range;
var tn = et(function(t) {
  t.setTime(t - t.getMilliseconds() - t.getSeconds() * lt - t.getMinutes() * st);
}, function(t, e) {
  t.setTime(+t + e * ht);
}, function(t, e) {
  return (e - t) / ht;
}, function(t) {
  return t.getHours();
});
const Rt = tn;
tn.range;
var en = et(
  (t) => t.setHours(0, 0, 0, 0),
  (t, e) => t.setDate(t.getDate() + e),
  (t, e) => (e - t - (e.getTimezoneOffset() - t.getTimezoneOffset()) * st) / dt,
  (t) => t.getDate() - 1
);
const xt = en;
en.range;
function gt(t) {
  return et(function(e) {
    e.setDate(e.getDate() - (e.getDay() + 7 - t) % 7), e.setHours(0, 0, 0, 0);
  }, function(e, n) {
    e.setDate(e.getDate() + n * 7);
  }, function(e, n) {
    return (n - e - (n.getTimezoneOffset() - e.getTimezoneOffset()) * st) / ge;
  });
}
var bt = gt(0), Bt = gt(1), cr = gt(2), ur = gt(3), wt = gt(4), lr = gt(5), fr = gt(6);
bt.range;
Bt.range;
cr.range;
ur.range;
wt.range;
lr.range;
fr.range;
var nn = et(function(t) {
  t.setDate(1), t.setHours(0, 0, 0, 0);
}, function(t, e) {
  t.setMonth(t.getMonth() + e);
}, function(t, e) {
  return e.getMonth() - t.getMonth() + (e.getFullYear() - t.getFullYear()) * 12;
}, function(t) {
  return t.getMonth();
});
const Zt = nn;
nn.range;
var ye = et(function(t) {
  t.setMonth(0, 1), t.setHours(0, 0, 0, 0);
}, function(t, e) {
  t.setFullYear(t.getFullYear() + e);
}, function(t, e) {
  return e.getFullYear() - t.getFullYear();
}, function(t) {
  return t.getFullYear();
});
ye.every = function(t) {
  return !isFinite(t = Math.floor(t)) || !(t > 0) ? null : et(function(e) {
    e.setFullYear(Math.floor(e.getFullYear() / t) * t), e.setMonth(0, 1), e.setHours(0, 0, 0, 0);
  }, function(e, n) {
    e.setFullYear(e.getFullYear() + n * t);
  });
};
const mt = ye;
ye.range;
var rn = et(function(t) {
  t.setUTCHours(0, 0, 0, 0);
}, function(t, e) {
  t.setUTCDate(t.getUTCDate() + e);
}, function(t, e) {
  return (e - t) / dt;
}, function(t) {
  return t.getUTCDate() - 1;
});
const sn = rn;
rn.range;
function yt(t) {
  return et(function(e) {
    e.setUTCDate(e.getUTCDate() - (e.getUTCDay() + 7 - t) % 7), e.setUTCHours(0, 0, 0, 0);
  }, function(e, n) {
    e.setUTCDate(e.getUTCDate() + n * 7);
  }, function(e, n) {
    return (n - e) / ge;
  });
}
var an = yt(0), Xt = yt(1), hr = yt(2), dr = yt(3), Dt = yt(4), mr = yt(5), gr = yt(6);
an.range;
Xt.range;
hr.range;
dr.range;
Dt.range;
mr.range;
gr.range;
var ke = et(function(t) {
  t.setUTCMonth(0, 1), t.setUTCHours(0, 0, 0, 0);
}, function(t, e) {
  t.setUTCFullYear(t.getUTCFullYear() + e);
}, function(t, e) {
  return e.getUTCFullYear() - t.getUTCFullYear();
}, function(t) {
  return t.getUTCFullYear();
});
ke.every = function(t) {
  return !isFinite(t = Math.floor(t)) || !(t > 0) ? null : et(function(e) {
    e.setUTCFullYear(Math.floor(e.getUTCFullYear() / t) * t), e.setUTCMonth(0, 1), e.setUTCHours(0, 0, 0, 0);
  }, function(e, n) {
    e.setUTCFullYear(e.getUTCFullYear() + n * t);
  });
};
const Ut = ke;
ke.range;
function yr(t, e, n, r, i, s) {
  const o = [
    [Ft, 1, lt],
    [Ft, 5, 5 * lt],
    [Ft, 15, 15 * lt],
    [Ft, 30, 30 * lt],
    [s, 1, st],
    [s, 5, 5 * st],
    [s, 15, 15 * st],
    [s, 30, 30 * st],
    [i, 1, ht],
    [i, 3, 3 * ht],
    [i, 6, 6 * ht],
    [i, 12, 12 * ht],
    [r, 1, dt],
    [r, 2, 2 * dt],
    [n, 1, ge],
    [e, 1, Se],
    [e, 3, 3 * Se],
    [t, 1, re]
  ];
  function y(p, C, S) {
    const w = C < p;
    w && ([p, C] = [C, p]);
    const b = S && typeof S.range == "function" ? S : M(p, C, S), P = b ? b.range(p, +C + 1) : [];
    return w ? P.reverse() : P;
  }
  function M(p, C, S) {
    const w = Math.abs(C - p) / S, b = zn(([, , F]) => F).right(o, w);
    if (b === o.length)
      return t.every(Me(p / re, C / re, S));
    if (b === 0)
      return or.every(Math.max(Me(p, C, S), 1));
    const [P, g] = o[w / o[b - 1][2] < o[b][2] / w ? b - 1 : b];
    return P.every(g);
  }
  return [y, M];
}
const [kr, pr] = yr(mt, Zt, bt, xt, Rt, Pt);
function ie(t) {
  if (0 <= t.y && t.y < 100) {
    var e = new Date(-1, t.m, t.d, t.H, t.M, t.S, t.L);
    return e.setFullYear(t.y), e;
  }
  return new Date(t.y, t.m, t.d, t.H, t.M, t.S, t.L);
}
function se(t) {
  if (0 <= t.y && t.y < 100) {
    var e = new Date(Date.UTC(-1, t.m, t.d, t.H, t.M, t.S, t.L));
    return e.setUTCFullYear(t.y), e;
  }
  return new Date(Date.UTC(t.y, t.m, t.d, t.H, t.M, t.S, t.L));
}
function _t(t, e, n) {
  return { y: t, m: e, d: n, H: 0, M: 0, S: 0, L: 0 };
}
function vr(t) {
  var e = t.dateTime, n = t.date, r = t.time, i = t.periods, s = t.days, o = t.shortDays, y = t.months, M = t.shortMonths, p = St(i), C = Yt(i), S = St(s), w = Yt(s), b = St(o), P = Yt(o), g = St(y), F = Yt(y), z = St(M), O = Yt(M), H = {
    a: B,
    A: Z,
    b: J,
    B: m,
    c: null,
    d: Ae,
    e: Ae,
    f: Pr,
    g: Kr,
    G: ti,
    H: Nr,
    I: Hr,
    j: Vr,
    L: on,
    m: Rr,
    M: Br,
    p: _,
    q: Y,
    Q: Oe,
    s: ze,
    S: Zr,
    u: Xr,
    U: qr,
    V: jr,
    w: Gr,
    W: Qr,
    x: null,
    X: null,
    y: Jr,
    Y: $r,
    Z: ei,
    "%": We
  }, V = {
    a: U,
    A: W,
    b: G,
    B: R,
    c: null,
    d: Ie,
    e: Ie,
    f: si,
    g: gi,
    G: ki,
    H: ni,
    I: ri,
    j: ii,
    L: un,
    m: ai,
    M: oi,
    p: ft,
    q,
    Q: Oe,
    s: ze,
    S: ci,
    u: ui,
    U: li,
    V: fi,
    w: hi,
    W: di,
    x: null,
    X: null,
    y: mi,
    Y: yi,
    Z: pi,
    "%": We
  }, j = {
    a: f,
    A: d,
    b: c,
    B: T,
    c: a,
    d: Le,
    e: Le,
    f: Ir,
    g: Ue,
    G: Fe,
    H: Ee,
    I: Ee,
    j: Ur,
    L: Ar,
    m: Fr,
    M: Lr,
    p: u,
    q: Yr,
    Q: Or,
    s: zr,
    S: Er,
    u: Dr,
    U: Cr,
    V: Mr,
    w: wr,
    W: _r,
    x: A,
    X: h,
    y: Ue,
    Y: Fe,
    Z: Sr,
    "%": Wr
  };
  H.x = x(n, H), H.X = x(r, H), H.c = x(e, H), V.x = x(n, V), V.X = x(r, V), V.c = x(e, V);
  function x(k, D) {
    return function(L) {
      var l = [], X = -1, I = 0, Q = k.length, K, it, rt;
      for (L instanceof Date || (L = /* @__PURE__ */ new Date(+L)); ++X < Q; )
        k.charCodeAt(X) === 37 && (l.push(k.slice(I, X)), (it = Ye[K = k.charAt(++X)]) != null ? K = k.charAt(++X) : it = K === "e" ? " " : "0", (rt = D[K]) && (K = rt(L, it)), l.push(K), I = X + 1);
      return l.push(k.slice(I, X)), l.join("");
    };
  }
  function E(k, D) {
    return function(L) {
      var l = _t(1900, void 0, 1), X = v(l, k, L += "", 0), I, Q;
      if (X != L.length)
        return null;
      if ("Q" in l)
        return new Date(l.Q);
      if ("s" in l)
        return new Date(l.s * 1e3 + ("L" in l ? l.L : 0));
      if (D && !("Z" in l) && (l.Z = 0), "p" in l && (l.H = l.H % 12 + l.p * 12), l.m === void 0 && (l.m = "q" in l ? l.q : 0), "V" in l) {
        if (l.V < 1 || l.V > 53)
          return null;
        "w" in l || (l.w = 1), "Z" in l ? (I = se(_t(l.y, 0, 1)), Q = I.getUTCDay(), I = Q > 4 || Q === 0 ? Xt.ceil(I) : Xt(I), I = sn.offset(I, (l.V - 1) * 7), l.y = I.getUTCFullYear(), l.m = I.getUTCMonth(), l.d = I.getUTCDate() + (l.w + 6) % 7) : (I = ie(_t(l.y, 0, 1)), Q = I.getDay(), I = Q > 4 || Q === 0 ? Bt.ceil(I) : Bt(I), I = xt.offset(I, (l.V - 1) * 7), l.y = I.getFullYear(), l.m = I.getMonth(), l.d = I.getDate() + (l.w + 6) % 7);
      } else
        ("W" in l || "U" in l) && ("w" in l || (l.w = "u" in l ? l.u % 7 : "W" in l ? 1 : 0), Q = "Z" in l ? se(_t(l.y, 0, 1)).getUTCDay() : ie(_t(l.y, 0, 1)).getDay(), l.m = 0, l.d = "W" in l ? (l.w + 6) % 7 + l.W * 7 - (Q + 5) % 7 : l.w + l.U * 7 - (Q + 6) % 7);
      return "Z" in l ? (l.H += l.Z / 100 | 0, l.M += l.Z % 100, se(l)) : ie(l);
    };
  }
  function v(k, D, L, l) {
    for (var X = 0, I = D.length, Q = L.length, K, it; X < I; ) {
      if (l >= Q)
        return -1;
      if (K = D.charCodeAt(X++), K === 37) {
        if (K = D.charAt(X++), it = j[K in Ye ? D.charAt(X++) : K], !it || (l = it(k, L, l)) < 0)
          return -1;
      } else if (K != L.charCodeAt(l++))
        return -1;
    }
    return l;
  }
  function u(k, D, L) {
    var l = p.exec(D.slice(L));
    return l ? (k.p = C.get(l[0].toLowerCase()), L + l[0].length) : -1;
  }
  function f(k, D, L) {
    var l = b.exec(D.slice(L));
    return l ? (k.w = P.get(l[0].toLowerCase()), L + l[0].length) : -1;
  }
  function d(k, D, L) {
    var l = S.exec(D.slice(L));
    return l ? (k.w = w.get(l[0].toLowerCase()), L + l[0].length) : -1;
  }
  function c(k, D, L) {
    var l = z.exec(D.slice(L));
    return l ? (k.m = O.get(l[0].toLowerCase()), L + l[0].length) : -1;
  }
  function T(k, D, L) {
    var l = g.exec(D.slice(L));
    return l ? (k.m = F.get(l[0].toLowerCase()), L + l[0].length) : -1;
  }
  function a(k, D, L) {
    return v(k, e, D, L);
  }
  function A(k, D, L) {
    return v(k, n, D, L);
  }
  function h(k, D, L) {
    return v(k, r, D, L);
  }
  function B(k) {
    return o[k.getDay()];
  }
  function Z(k) {
    return s[k.getDay()];
  }
  function J(k) {
    return M[k.getMonth()];
  }
  function m(k) {
    return y[k.getMonth()];
  }
  function _(k) {
    return i[+(k.getHours() >= 12)];
  }
  function Y(k) {
    return 1 + ~~(k.getMonth() / 3);
  }
  function U(k) {
    return o[k.getUTCDay()];
  }
  function W(k) {
    return s[k.getUTCDay()];
  }
  function G(k) {
    return M[k.getUTCMonth()];
  }
  function R(k) {
    return y[k.getUTCMonth()];
  }
  function ft(k) {
    return i[+(k.getUTCHours() >= 12)];
  }
  function q(k) {
    return 1 + ~~(k.getUTCMonth() / 3);
  }
  return {
    format: function(k) {
      var D = x(k += "", H);
      return D.toString = function() {
        return k;
      }, D;
    },
    parse: function(k) {
      var D = E(k += "", !1);
      return D.toString = function() {
        return k;
      }, D;
    },
    utcFormat: function(k) {
      var D = x(k += "", V);
      return D.toString = function() {
        return k;
      }, D;
    },
    utcParse: function(k) {
      var D = E(k += "", !0);
      return D.toString = function() {
        return k;
      }, D;
    }
  };
}
var Ye = { "-": "", _: " ", 0: "0" }, tt = /^\s*\d+/, Tr = /^%/, xr = /[\\^$*+?|[\]().{}]/g;
function N(t, e, n) {
  var r = t < 0 ? "-" : "", i = (r ? -t : t) + "", s = i.length;
  return r + (s < n ? new Array(n - s + 1).join(e) + i : i);
}
function br(t) {
  return t.replace(xr, "\\$&");
}
function St(t) {
  return new RegExp("^(?:" + t.map(br).join("|") + ")", "i");
}
function Yt(t) {
  return new Map(t.map((e, n) => [e.toLowerCase(), n]));
}
function wr(t, e, n) {
  var r = tt.exec(e.slice(n, n + 1));
  return r ? (t.w = +r[0], n + r[0].length) : -1;
}
function Dr(t, e, n) {
  var r = tt.exec(e.slice(n, n + 1));
  return r ? (t.u = +r[0], n + r[0].length) : -1;
}
function Cr(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.U = +r[0], n + r[0].length) : -1;
}
function Mr(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.V = +r[0], n + r[0].length) : -1;
}
function _r(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.W = +r[0], n + r[0].length) : -1;
}
function Fe(t, e, n) {
  var r = tt.exec(e.slice(n, n + 4));
  return r ? (t.y = +r[0], n + r[0].length) : -1;
}
function Ue(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.y = +r[0] + (+r[0] > 68 ? 1900 : 2e3), n + r[0].length) : -1;
}
function Sr(t, e, n) {
  var r = /^(Z)|([+-]\d\d)(?::?(\d\d))?/.exec(e.slice(n, n + 6));
  return r ? (t.Z = r[1] ? 0 : -(r[2] + (r[3] || "00")), n + r[0].length) : -1;
}
function Yr(t, e, n) {
  var r = tt.exec(e.slice(n, n + 1));
  return r ? (t.q = r[0] * 3 - 3, n + r[0].length) : -1;
}
function Fr(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.m = r[0] - 1, n + r[0].length) : -1;
}
function Le(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.d = +r[0], n + r[0].length) : -1;
}
function Ur(t, e, n) {
  var r = tt.exec(e.slice(n, n + 3));
  return r ? (t.m = 0, t.d = +r[0], n + r[0].length) : -1;
}
function Ee(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.H = +r[0], n + r[0].length) : -1;
}
function Lr(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.M = +r[0], n + r[0].length) : -1;
}
function Er(t, e, n) {
  var r = tt.exec(e.slice(n, n + 2));
  return r ? (t.S = +r[0], n + r[0].length) : -1;
}
function Ar(t, e, n) {
  var r = tt.exec(e.slice(n, n + 3));
  return r ? (t.L = +r[0], n + r[0].length) : -1;
}
function Ir(t, e, n) {
  var r = tt.exec(e.slice(n, n + 6));
  return r ? (t.L = Math.floor(r[0] / 1e3), n + r[0].length) : -1;
}
function Wr(t, e, n) {
  var r = Tr.exec(e.slice(n, n + 1));
  return r ? n + r[0].length : -1;
}
function Or(t, e, n) {
  var r = tt.exec(e.slice(n));
  return r ? (t.Q = +r[0], n + r[0].length) : -1;
}
function zr(t, e, n) {
  var r = tt.exec(e.slice(n));
  return r ? (t.s = +r[0], n + r[0].length) : -1;
}
function Ae(t, e) {
  return N(t.getDate(), e, 2);
}
function Nr(t, e) {
  return N(t.getHours(), e, 2);
}
function Hr(t, e) {
  return N(t.getHours() % 12 || 12, e, 2);
}
function Vr(t, e) {
  return N(1 + xt.count(mt(t), t), e, 3);
}
function on(t, e) {
  return N(t.getMilliseconds(), e, 3);
}
function Pr(t, e) {
  return on(t, e) + "000";
}
function Rr(t, e) {
  return N(t.getMonth() + 1, e, 2);
}
function Br(t, e) {
  return N(t.getMinutes(), e, 2);
}
function Zr(t, e) {
  return N(t.getSeconds(), e, 2);
}
function Xr(t) {
  var e = t.getDay();
  return e === 0 ? 7 : e;
}
function qr(t, e) {
  return N(bt.count(mt(t) - 1, t), e, 2);
}
function cn(t) {
  var e = t.getDay();
  return e >= 4 || e === 0 ? wt(t) : wt.ceil(t);
}
function jr(t, e) {
  return t = cn(t), N(wt.count(mt(t), t) + (mt(t).getDay() === 4), e, 2);
}
function Gr(t) {
  return t.getDay();
}
function Qr(t, e) {
  return N(Bt.count(mt(t) - 1, t), e, 2);
}
function Jr(t, e) {
  return N(t.getFullYear() % 100, e, 2);
}
function Kr(t, e) {
  return t = cn(t), N(t.getFullYear() % 100, e, 2);
}
function $r(t, e) {
  return N(t.getFullYear() % 1e4, e, 4);
}
function ti(t, e) {
  var n = t.getDay();
  return t = n >= 4 || n === 0 ? wt(t) : wt.ceil(t), N(t.getFullYear() % 1e4, e, 4);
}
function ei(t) {
  var e = t.getTimezoneOffset();
  return (e > 0 ? "-" : (e *= -1, "+")) + N(e / 60 | 0, "0", 2) + N(e % 60, "0", 2);
}
function Ie(t, e) {
  return N(t.getUTCDate(), e, 2);
}
function ni(t, e) {
  return N(t.getUTCHours(), e, 2);
}
function ri(t, e) {
  return N(t.getUTCHours() % 12 || 12, e, 2);
}
function ii(t, e) {
  return N(1 + sn.count(Ut(t), t), e, 3);
}
function un(t, e) {
  return N(t.getUTCMilliseconds(), e, 3);
}
function si(t, e) {
  return un(t, e) + "000";
}
function ai(t, e) {
  return N(t.getUTCMonth() + 1, e, 2);
}
function oi(t, e) {
  return N(t.getUTCMinutes(), e, 2);
}
function ci(t, e) {
  return N(t.getUTCSeconds(), e, 2);
}
function ui(t) {
  var e = t.getUTCDay();
  return e === 0 ? 7 : e;
}
function li(t, e) {
  return N(an.count(Ut(t) - 1, t), e, 2);
}
function ln(t) {
  var e = t.getUTCDay();
  return e >= 4 || e === 0 ? Dt(t) : Dt.ceil(t);
}
function fi(t, e) {
  return t = ln(t), N(Dt.count(Ut(t), t) + (Ut(t).getUTCDay() === 4), e, 2);
}
function hi(t) {
  return t.getUTCDay();
}
function di(t, e) {
  return N(Xt.count(Ut(t) - 1, t), e, 2);
}
function mi(t, e) {
  return N(t.getUTCFullYear() % 100, e, 2);
}
function gi(t, e) {
  return t = ln(t), N(t.getUTCFullYear() % 100, e, 2);
}
function yi(t, e) {
  return N(t.getUTCFullYear() % 1e4, e, 4);
}
function ki(t, e) {
  var n = t.getUTCDay();
  return t = n >= 4 || n === 0 ? Dt(t) : Dt.ceil(t), N(t.getUTCFullYear() % 1e4, e, 4);
}
function pi() {
  return "+0000";
}
function We() {
  return "%";
}
function Oe(t) {
  return +t;
}
function ze(t) {
  return Math.floor(+t / 1e3);
}
var kt, qt;
vi({
  dateTime: "%x, %X",
  date: "%-m/%-d/%Y",
  time: "%-I:%M:%S %p",
  periods: ["AM", "PM"],
  days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
  shortDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
  shortMonths: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
});
function vi(t) {
  return kt = vr(t), qt = kt.format, kt.parse, kt.utcFormat, kt.utcParse, kt;
}
function Ti(t) {
  return new Date(t);
}
function xi(t) {
  return t instanceof Date ? +t : +/* @__PURE__ */ new Date(+t);
}
function fn(t, e, n, r, i, s, o, y, M, p) {
  var C = Nn(), S = C.invert, w = C.domain, b = p(".%L"), P = p(":%S"), g = p("%I:%M"), F = p("%I %p"), z = p("%a %d"), O = p("%b %d"), H = p("%B"), V = p("%Y");
  function j(x) {
    return (M(x) < x ? b : y(x) < x ? P : o(x) < x ? g : s(x) < x ? F : r(x) < x ? i(x) < x ? z : O : n(x) < x ? H : V)(x);
  }
  return C.invert = function(x) {
    return new Date(S(x));
  }, C.domain = function(x) {
    return arguments.length ? w(Array.from(x, xi)) : w().map(Ti);
  }, C.ticks = function(x) {
    var E = w();
    return t(E[0], E[E.length - 1], x ?? 10);
  }, C.tickFormat = function(x, E) {
    return E == null ? j : p(E);
  }, C.nice = function(x) {
    var E = w();
    return (!x || typeof x.range != "function") && (x = e(E[0], E[E.length - 1], x ?? 10)), x ? w(ar(E, x)) : C;
  }, C.copy = function() {
    return Hn(C, fn(t, e, n, r, i, s, o, y, M, p));
  }, C;
}
function bi() {
  return Pn.apply(fn(kr, pr, mt, Zt, bt, xt, Rt, Pt, Ft, qt).domain([new Date(2e3, 0, 1), new Date(2e3, 0, 2)]), arguments);
}
var ue = function() {
  var t = function(v, u, f, d) {
    for (f = f || {}, d = v.length; d--; f[v[d]] = u)
      ;
    return f;
  }, e = [1, 3], n = [1, 5], r = [7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 25, 26, 28, 35, 40], i = [1, 15], s = [1, 16], o = [1, 17], y = [1, 18], M = [1, 19], p = [1, 20], C = [1, 21], S = [1, 22], w = [1, 23], b = [1, 24], P = [1, 25], g = [1, 26], F = [1, 27], z = [1, 29], O = [1, 31], H = [1, 34], V = [5, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 25, 26, 28, 35, 40], j = {
    trace: function() {
    },
    yy: {},
    symbols_: { error: 2, start: 3, directive: 4, gantt: 5, document: 6, EOF: 7, line: 8, SPACE: 9, statement: 10, NL: 11, dateFormat: 12, inclusiveEndDates: 13, topAxis: 14, axisFormat: 15, tickInterval: 16, excludes: 17, includes: 18, todayMarker: 19, title: 20, acc_title: 21, acc_title_value: 22, acc_descr: 23, acc_descr_value: 24, acc_descr_multiline_value: 25, section: 26, clickStatement: 27, taskTxt: 28, taskData: 29, openDirective: 30, typeDirective: 31, closeDirective: 32, ":": 33, argDirective: 34, click: 35, callbackname: 36, callbackargs: 37, href: 38, clickStatementDebug: 39, open_directive: 40, type_directive: 41, arg_directive: 42, close_directive: 43, $accept: 0, $end: 1 },
    terminals_: { 2: "error", 5: "gantt", 7: "EOF", 9: "SPACE", 11: "NL", 12: "dateFormat", 13: "inclusiveEndDates", 14: "topAxis", 15: "axisFormat", 16: "tickInterval", 17: "excludes", 18: "includes", 19: "todayMarker", 20: "title", 21: "acc_title", 22: "acc_title_value", 23: "acc_descr", 24: "acc_descr_value", 25: "acc_descr_multiline_value", 26: "section", 28: "taskTxt", 29: "taskData", 33: ":", 35: "click", 36: "callbackname", 37: "callbackargs", 38: "href", 40: "open_directive", 41: "type_directive", 42: "arg_directive", 43: "close_directive" },
    productions_: [0, [3, 2], [3, 3], [6, 0], [6, 2], [8, 2], [8, 1], [8, 1], [8, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 1], [10, 2], [10, 2], [10, 1], [10, 1], [10, 1], [10, 2], [10, 1], [4, 4], [4, 6], [27, 2], [27, 3], [27, 3], [27, 4], [27, 3], [27, 4], [27, 2], [39, 2], [39, 3], [39, 3], [39, 4], [39, 3], [39, 4], [39, 2], [30, 1], [31, 1], [34, 1], [32, 1]],
    performAction: function(u, f, d, c, T, a, A) {
      var h = a.length - 1;
      switch (T) {
        case 2:
          return a[h - 1];
        case 3:
          this.$ = [];
          break;
        case 4:
          a[h - 1].push(a[h]), this.$ = a[h - 1];
          break;
        case 5:
        case 6:
          this.$ = a[h];
          break;
        case 7:
        case 8:
          this.$ = [];
          break;
        case 9:
          c.setDateFormat(a[h].substr(11)), this.$ = a[h].substr(11);
          break;
        case 10:
          c.enableInclusiveEndDates(), this.$ = a[h].substr(18);
          break;
        case 11:
          c.TopAxis(), this.$ = a[h].substr(8);
          break;
        case 12:
          c.setAxisFormat(a[h].substr(11)), this.$ = a[h].substr(11);
          break;
        case 13:
          c.setTickInterval(a[h].substr(13)), this.$ = a[h].substr(13);
          break;
        case 14:
          c.setExcludes(a[h].substr(9)), this.$ = a[h].substr(9);
          break;
        case 15:
          c.setIncludes(a[h].substr(9)), this.$ = a[h].substr(9);
          break;
        case 16:
          c.setTodayMarker(a[h].substr(12)), this.$ = a[h].substr(12);
          break;
        case 17:
          c.setDiagramTitle(a[h].substr(6)), this.$ = a[h].substr(6);
          break;
        case 18:
          this.$ = a[h].trim(), c.setAccTitle(this.$);
          break;
        case 19:
        case 20:
          this.$ = a[h].trim(), c.setAccDescription(this.$);
          break;
        case 21:
          c.addSection(a[h].substr(8)), this.$ = a[h].substr(8);
          break;
        case 23:
          c.addTask(a[h - 1], a[h]), this.$ = "task";
          break;
        case 27:
          this.$ = a[h - 1], c.setClickEvent(a[h - 1], a[h], null);
          break;
        case 28:
          this.$ = a[h - 2], c.setClickEvent(a[h - 2], a[h - 1], a[h]);
          break;
        case 29:
          this.$ = a[h - 2], c.setClickEvent(a[h - 2], a[h - 1], null), c.setLink(a[h - 2], a[h]);
          break;
        case 30:
          this.$ = a[h - 3], c.setClickEvent(a[h - 3], a[h - 2], a[h - 1]), c.setLink(a[h - 3], a[h]);
          break;
        case 31:
          this.$ = a[h - 2], c.setClickEvent(a[h - 2], a[h], null), c.setLink(a[h - 2], a[h - 1]);
          break;
        case 32:
          this.$ = a[h - 3], c.setClickEvent(a[h - 3], a[h - 1], a[h]), c.setLink(a[h - 3], a[h - 2]);
          break;
        case 33:
          this.$ = a[h - 1], c.setLink(a[h - 1], a[h]);
          break;
        case 34:
        case 40:
          this.$ = a[h - 1] + " " + a[h];
          break;
        case 35:
        case 36:
        case 38:
          this.$ = a[h - 2] + " " + a[h - 1] + " " + a[h];
          break;
        case 37:
        case 39:
          this.$ = a[h - 3] + " " + a[h - 2] + " " + a[h - 1] + " " + a[h];
          break;
        case 41:
          c.parseDirective("%%{", "open_directive");
          break;
        case 42:
          c.parseDirective(a[h], "type_directive");
          break;
        case 43:
          a[h] = a[h].trim().replace(/'/g, '"'), c.parseDirective(a[h], "arg_directive");
          break;
        case 44:
          c.parseDirective("}%%", "close_directive", "gantt");
          break;
      }
    },
    table: [{ 3: 1, 4: 2, 5: e, 30: 4, 40: n }, { 1: [3] }, { 3: 6, 4: 2, 5: e, 30: 4, 40: n }, t(r, [2, 3], { 6: 7 }), { 31: 8, 41: [1, 9] }, { 41: [2, 41] }, { 1: [2, 1] }, { 4: 30, 7: [1, 10], 8: 11, 9: [1, 12], 10: 13, 11: [1, 14], 12: i, 13: s, 14: o, 15: y, 16: M, 17: p, 18: C, 19: S, 20: w, 21: b, 23: P, 25: g, 26: F, 27: 28, 28: z, 30: 4, 35: O, 40: n }, { 32: 32, 33: [1, 33], 43: H }, t([33, 43], [2, 42]), t(r, [2, 8], { 1: [2, 2] }), t(r, [2, 4]), { 4: 30, 10: 35, 12: i, 13: s, 14: o, 15: y, 16: M, 17: p, 18: C, 19: S, 20: w, 21: b, 23: P, 25: g, 26: F, 27: 28, 28: z, 30: 4, 35: O, 40: n }, t(r, [2, 6]), t(r, [2, 7]), t(r, [2, 9]), t(r, [2, 10]), t(r, [2, 11]), t(r, [2, 12]), t(r, [2, 13]), t(r, [2, 14]), t(r, [2, 15]), t(r, [2, 16]), t(r, [2, 17]), { 22: [1, 36] }, { 24: [1, 37] }, t(r, [2, 20]), t(r, [2, 21]), t(r, [2, 22]), { 29: [1, 38] }, t(r, [2, 24]), { 36: [1, 39], 38: [1, 40] }, { 11: [1, 41] }, { 34: 42, 42: [1, 43] }, { 11: [2, 44] }, t(r, [2, 5]), t(r, [2, 18]), t(r, [2, 19]), t(r, [2, 23]), t(r, [2, 27], { 37: [1, 44], 38: [1, 45] }), t(r, [2, 33], { 36: [1, 46] }), t(V, [2, 25]), { 32: 47, 43: H }, { 43: [2, 43] }, t(r, [2, 28], { 38: [1, 48] }), t(r, [2, 29]), t(r, [2, 31], { 37: [1, 49] }), { 11: [1, 50] }, t(r, [2, 30]), t(r, [2, 32]), t(V, [2, 26])],
    defaultActions: { 5: [2, 41], 6: [2, 1], 34: [2, 44], 43: [2, 43] },
    parseError: function(u, f) {
      if (f.recoverable)
        this.trace(u);
      else {
        var d = new Error(u);
        throw d.hash = f, d;
      }
    },
    parse: function(u) {
      var f = this, d = [0], c = [], T = [null], a = [], A = this.table, h = "", B = 0, Z = 0, J = 2, m = 1, _ = a.slice.call(arguments, 1), Y = Object.create(this.lexer), U = { yy: {} };
      for (var W in this.yy)
        Object.prototype.hasOwnProperty.call(this.yy, W) && (U.yy[W] = this.yy[W]);
      Y.setInput(u, U.yy), U.yy.lexer = Y, U.yy.parser = this, typeof Y.yylloc > "u" && (Y.yylloc = {});
      var G = Y.yylloc;
      a.push(G);
      var R = Y.options && Y.options.ranges;
      typeof U.yy.parseError == "function" ? this.parseError = U.yy.parseError : this.parseError = Object.getPrototypeOf(this).parseError;
      function ft() {
        var rt;
        return rt = c.pop() || Y.lex() || m, typeof rt != "number" && (rt instanceof Array && (c = rt, rt = c.pop()), rt = f.symbols_[rt] || rt), rt;
      }
      for (var q, k, D, L, l = {}, X, I, Q, K; ; ) {
        if (k = d[d.length - 1], this.defaultActions[k] ? D = this.defaultActions[k] : ((q === null || typeof q > "u") && (q = ft()), D = A[k] && A[k][q]), typeof D > "u" || !D.length || !D[0]) {
          var it = "";
          K = [];
          for (X in A[k])
            this.terminals_[X] && X > J && K.push("'" + this.terminals_[X] + "'");
          Y.showPosition ? it = "Parse error on line " + (B + 1) + `:
` + Y.showPosition() + `
Expecting ` + K.join(", ") + ", got '" + (this.terminals_[q] || q) + "'" : it = "Parse error on line " + (B + 1) + ": Unexpected " + (q == m ? "end of input" : "'" + (this.terminals_[q] || q) + "'"), this.parseError(it, {
            text: Y.match,
            token: this.terminals_[q] || q,
            line: Y.yylineno,
            loc: G,
            expected: K
          });
        }
        if (D[0] instanceof Array && D.length > 1)
          throw new Error("Parse Error: multiple actions possible at state: " + k + ", token: " + q);
        switch (D[0]) {
          case 1:
            d.push(q), T.push(Y.yytext), a.push(Y.yylloc), d.push(D[1]), q = null, Z = Y.yyleng, h = Y.yytext, B = Y.yylineno, G = Y.yylloc;
            break;
          case 2:
            if (I = this.productions_[D[1]][1], l.$ = T[T.length - I], l._$ = {
              first_line: a[a.length - (I || 1)].first_line,
              last_line: a[a.length - 1].last_line,
              first_column: a[a.length - (I || 1)].first_column,
              last_column: a[a.length - 1].last_column
            }, R && (l._$.range = [
              a[a.length - (I || 1)].range[0],
              a[a.length - 1].range[1]
            ]), L = this.performAction.apply(l, [
              h,
              Z,
              B,
              U.yy,
              D[1],
              T,
              a
            ].concat(_)), typeof L < "u")
              return L;
            I && (d = d.slice(0, -1 * I * 2), T = T.slice(0, -1 * I), a = a.slice(0, -1 * I)), d.push(this.productions_[D[1]][0]), T.push(l.$), a.push(l._$), Q = A[d[d.length - 2]][d[d.length - 1]], d.push(Q);
            break;
          case 3:
            return !0;
        }
      }
      return !0;
    }
  }, x = function() {
    var v = {
      EOF: 1,
      parseError: function(f, d) {
        if (this.yy.parser)
          this.yy.parser.parseError(f, d);
        else
          throw new Error(f);
      },
      // resets the lexer, sets new input
      setInput: function(u, f) {
        return this.yy = f || this.yy || {}, this._input = u, this._more = this._backtrack = this.done = !1, this.yylineno = this.yyleng = 0, this.yytext = this.matched = this.match = "", this.conditionStack = ["INITIAL"], this.yylloc = {
          first_line: 1,
          first_column: 0,
          last_line: 1,
          last_column: 0
        }, this.options.ranges && (this.yylloc.range = [0, 0]), this.offset = 0, this;
      },
      // consumes and returns one char from the input
      input: function() {
        var u = this._input[0];
        this.yytext += u, this.yyleng++, this.offset++, this.match += u, this.matched += u;
        var f = u.match(/(?:\r\n?|\n).*/g);
        return f ? (this.yylineno++, this.yylloc.last_line++) : this.yylloc.last_column++, this.options.ranges && this.yylloc.range[1]++, this._input = this._input.slice(1), u;
      },
      // unshifts one char (or a string) into the input
      unput: function(u) {
        var f = u.length, d = u.split(/(?:\r\n?|\n)/g);
        this._input = u + this._input, this.yytext = this.yytext.substr(0, this.yytext.length - f), this.offset -= f;
        var c = this.match.split(/(?:\r\n?|\n)/g);
        this.match = this.match.substr(0, this.match.length - 1), this.matched = this.matched.substr(0, this.matched.length - 1), d.length - 1 && (this.yylineno -= d.length - 1);
        var T = this.yylloc.range;
        return this.yylloc = {
          first_line: this.yylloc.first_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.first_column,
          last_column: d ? (d.length === c.length ? this.yylloc.first_column : 0) + c[c.length - d.length].length - d[0].length : this.yylloc.first_column - f
        }, this.options.ranges && (this.yylloc.range = [T[0], T[0] + this.yyleng - f]), this.yyleng = this.yytext.length, this;
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
      less: function(u) {
        this.unput(this.match.slice(u));
      },
      // displays already matched input, i.e. for error messages
      pastInput: function() {
        var u = this.matched.substr(0, this.matched.length - this.match.length);
        return (u.length > 20 ? "..." : "") + u.substr(-20).replace(/\n/g, "");
      },
      // displays upcoming input, i.e. for error messages
      upcomingInput: function() {
        var u = this.match;
        return u.length < 20 && (u += this._input.substr(0, 20 - u.length)), (u.substr(0, 20) + (u.length > 20 ? "..." : "")).replace(/\n/g, "");
      },
      // displays the character position where the lexing error occurred, i.e. for error messages
      showPosition: function() {
        var u = this.pastInput(), f = new Array(u.length + 1).join("-");
        return u + this.upcomingInput() + `
` + f + "^";
      },
      // test the lexed token: return FALSE when not a match, otherwise return token
      test_match: function(u, f) {
        var d, c, T;
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
        }, this.options.ranges && (T.yylloc.range = this.yylloc.range.slice(0))), c = u[0].match(/(?:\r\n?|\n).*/g), c && (this.yylineno += c.length), this.yylloc = {
          first_line: this.yylloc.last_line,
          last_line: this.yylineno + 1,
          first_column: this.yylloc.last_column,
          last_column: c ? c[c.length - 1].length - c[c.length - 1].match(/\r?\n?/)[0].length : this.yylloc.last_column + u[0].length
        }, this.yytext += u[0], this.match += u[0], this.matches = u, this.yyleng = this.yytext.length, this.options.ranges && (this.yylloc.range = [this.offset, this.offset += this.yyleng]), this._more = !1, this._backtrack = !1, this._input = this._input.slice(u[0].length), this.matched += u[0], d = this.performAction.call(this, this.yy, this, f, this.conditionStack[this.conditionStack.length - 1]), this.done && this._input && (this.done = !1), d)
          return d;
        if (this._backtrack) {
          for (var a in T)
            this[a] = T[a];
          return !1;
        }
        return !1;
      },
      // return next match in input
      next: function() {
        if (this.done)
          return this.EOF;
        this._input || (this.done = !0);
        var u, f, d, c;
        this._more || (this.yytext = "", this.match = "");
        for (var T = this._currentRules(), a = 0; a < T.length; a++)
          if (d = this._input.match(this.rules[T[a]]), d && (!f || d[0].length > f[0].length)) {
            if (f = d, c = a, this.options.backtrack_lexer) {
              if (u = this.test_match(d, T[a]), u !== !1)
                return u;
              if (this._backtrack) {
                f = !1;
                continue;
              } else
                return !1;
            } else if (!this.options.flex)
              break;
          }
        return f ? (u = this.test_match(f, T[c]), u !== !1 ? u : !1) : this._input === "" ? this.EOF : this.parseError("Lexical error on line " + (this.yylineno + 1) + `. Unrecognized text.
` + this.showPosition(), {
          text: "",
          token: null,
          line: this.yylineno
        });
      },
      // return next match that has a token
      lex: function() {
        var f = this.next();
        return f || this.lex();
      },
      // activates a new lexer condition state (pushes the new lexer condition state onto the condition stack)
      begin: function(f) {
        this.conditionStack.push(f);
      },
      // pop the previously active lexer condition state off the condition stack
      popState: function() {
        var f = this.conditionStack.length - 1;
        return f > 0 ? this.conditionStack.pop() : this.conditionStack[0];
      },
      // produce the lexer rule set which is active for the currently active lexer condition state
      _currentRules: function() {
        return this.conditionStack.length && this.conditionStack[this.conditionStack.length - 1] ? this.conditions[this.conditionStack[this.conditionStack.length - 1]].rules : this.conditions.INITIAL.rules;
      },
      // return the currently active lexer condition state; when an index argument is provided it produces the N-th previous condition state, if available
      topState: function(f) {
        return f = this.conditionStack.length - 1 - Math.abs(f || 0), f >= 0 ? this.conditionStack[f] : "INITIAL";
      },
      // alias for begin(condition)
      pushState: function(f) {
        this.begin(f);
      },
      // return the number of states currently on the stack
      stateStackSize: function() {
        return this.conditionStack.length;
      },
      options: { "case-insensitive": !0 },
      performAction: function(f, d, c, T) {
        switch (c) {
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
    return v;
  }();
  j.lexer = x;
  function E() {
    this.yy = {};
  }
  return E.prototype = j, j.Parser = E, new E();
}();
ue.parser = ue;
const wi = ue;
var hn = { exports: {} };
(function(t, e) {
  (function(n, r) {
    t.exports = r();
  })(de, function() {
    var n = "day";
    return function(r, i, s) {
      var o = function(p) {
        return p.add(4 - p.isoWeekday(), n);
      }, y = i.prototype;
      y.isoWeekYear = function() {
        return o(this).year();
      }, y.isoWeek = function(p) {
        if (!this.$utils().u(p))
          return this.add(7 * (p - this.isoWeek()), n);
        var C, S, w, b, P = o(this), g = (C = this.isoWeekYear(), S = this.$u, w = (S ? s.utc : s)().year(C).startOf("year"), b = 4 - w.isoWeekday(), w.isoWeekday() > 4 && (b += 7), w.add(b, n));
        return P.diff(g, "week") + 1;
      }, y.isoWeekday = function(p) {
        return this.$utils().u(p) ? this.day() || 7 : this.day(this.day() % 7 ? p : p - 7);
      };
      var M = y.startOf;
      y.startOf = function(p, C) {
        var S = this.$utils(), w = !!S.u(C) || C;
        return S.p(p) === "isoweek" ? w ? this.date(this.date() - (this.isoWeekday() - 1)).startOf("day") : this.date(this.date() - 1 - (this.isoWeekday() - 1) + 7).endOf("day") : M.bind(this)(p, C);
      };
    };
  });
})(hn);
var Di = hn.exports;
const Ci = /* @__PURE__ */ me(Di);
var dn = { exports: {} };
(function(t, e) {
  (function(n, r) {
    t.exports = r();
  })(de, function() {
    var n = { LTS: "h:mm:ss A", LT: "h:mm A", L: "MM/DD/YYYY", LL: "MMMM D, YYYY", LLL: "MMMM D, YYYY h:mm A", LLLL: "dddd, MMMM D, YYYY h:mm A" }, r = /(\[[^[]*\])|([-_:/.,()\s]+)|(A|a|YYYY|YY?|MM?M?M?|Do|DD?|hh?|HH?|mm?|ss?|S{1,3}|z|ZZ?)/g, i = /\d\d/, s = /\d\d?/, o = /\d*[^-_:/,()\s\d]+/, y = {}, M = function(g) {
      return (g = +g) + (g > 68 ? 1900 : 2e3);
    }, p = function(g) {
      return function(F) {
        this[g] = +F;
      };
    }, C = [/[+-]\d\d:?(\d\d)?|Z/, function(g) {
      (this.zone || (this.zone = {})).offset = function(F) {
        if (!F || F === "Z")
          return 0;
        var z = F.match(/([+-]|\d\d)/g), O = 60 * z[1] + (+z[2] || 0);
        return O === 0 ? 0 : z[0] === "+" ? -O : O;
      }(g);
    }], S = function(g) {
      var F = y[g];
      return F && (F.indexOf ? F : F.s.concat(F.f));
    }, w = function(g, F) {
      var z, O = y.meridiem;
      if (O) {
        for (var H = 1; H <= 24; H += 1)
          if (g.indexOf(O(H, 0, F)) > -1) {
            z = H > 12;
            break;
          }
      } else
        z = g === (F ? "pm" : "PM");
      return z;
    }, b = { A: [o, function(g) {
      this.afternoon = w(g, !1);
    }], a: [o, function(g) {
      this.afternoon = w(g, !0);
    }], S: [/\d/, function(g) {
      this.milliseconds = 100 * +g;
    }], SS: [i, function(g) {
      this.milliseconds = 10 * +g;
    }], SSS: [/\d{3}/, function(g) {
      this.milliseconds = +g;
    }], s: [s, p("seconds")], ss: [s, p("seconds")], m: [s, p("minutes")], mm: [s, p("minutes")], H: [s, p("hours")], h: [s, p("hours")], HH: [s, p("hours")], hh: [s, p("hours")], D: [s, p("day")], DD: [i, p("day")], Do: [o, function(g) {
      var F = y.ordinal, z = g.match(/\d+/);
      if (this.day = z[0], F)
        for (var O = 1; O <= 31; O += 1)
          F(O).replace(/\[|\]/g, "") === g && (this.day = O);
    }], M: [s, p("month")], MM: [i, p("month")], MMM: [o, function(g) {
      var F = S("months"), z = (S("monthsShort") || F.map(function(O) {
        return O.slice(0, 3);
      })).indexOf(g) + 1;
      if (z < 1)
        throw new Error();
      this.month = z % 12 || z;
    }], MMMM: [o, function(g) {
      var F = S("months").indexOf(g) + 1;
      if (F < 1)
        throw new Error();
      this.month = F % 12 || F;
    }], Y: [/[+-]?\d+/, p("year")], YY: [i, function(g) {
      this.year = M(g);
    }], YYYY: [/\d{4}/, p("year")], Z: C, ZZ: C };
    function P(g) {
      var F, z;
      F = g, z = y && y.formats;
      for (var O = (g = F.replace(/(\[[^\]]+])|(LTS?|l{1,4}|L{1,4})/g, function(u, f, d) {
        var c = d && d.toUpperCase();
        return f || z[d] || n[d] || z[c].replace(/(\[[^\]]+])|(MMMM|MM|DD|dddd)/g, function(T, a, A) {
          return a || A.slice(1);
        });
      })).match(r), H = O.length, V = 0; V < H; V += 1) {
        var j = O[V], x = b[j], E = x && x[0], v = x && x[1];
        O[V] = v ? { regex: E, parser: v } : j.replace(/^\[|\]$/g, "");
      }
      return function(u) {
        for (var f = {}, d = 0, c = 0; d < H; d += 1) {
          var T = O[d];
          if (typeof T == "string")
            c += T.length;
          else {
            var a = T.regex, A = T.parser, h = u.slice(c), B = a.exec(h)[0];
            A.call(f, B), u = u.replace(B, "");
          }
        }
        return function(Z) {
          var J = Z.afternoon;
          if (J !== void 0) {
            var m = Z.hours;
            J ? m < 12 && (Z.hours += 12) : m === 12 && (Z.hours = 0), delete Z.afternoon;
          }
        }(f), f;
      };
    }
    return function(g, F, z) {
      z.p.customParseFormat = !0, g && g.parseTwoDigitYear && (M = g.parseTwoDigitYear);
      var O = F.prototype, H = O.parse;
      O.parse = function(V) {
        var j = V.date, x = V.utc, E = V.args;
        this.$u = x;
        var v = E[1];
        if (typeof v == "string") {
          var u = E[2] === !0, f = E[3] === !0, d = u || f, c = E[2];
          f && (c = E[2]), y = this.$locale(), !u && c && (y = z.Ls[c]), this.$d = function(h, B, Z) {
            try {
              if (["x", "X"].indexOf(B) > -1)
                return new Date((B === "X" ? 1e3 : 1) * h);
              var J = P(B)(h), m = J.year, _ = J.month, Y = J.day, U = J.hours, W = J.minutes, G = J.seconds, R = J.milliseconds, ft = J.zone, q = /* @__PURE__ */ new Date(), k = Y || (m || _ ? 1 : q.getDate()), D = m || q.getFullYear(), L = 0;
              m && !_ || (L = _ > 0 ? _ - 1 : q.getMonth());
              var l = U || 0, X = W || 0, I = G || 0, Q = R || 0;
              return ft ? new Date(Date.UTC(D, L, k, l, X, I, Q + 60 * ft.offset * 1e3)) : Z ? new Date(Date.UTC(D, L, k, l, X, I, Q)) : new Date(D, L, k, l, X, I, Q);
            } catch {
              return /* @__PURE__ */ new Date("");
            }
          }(j, v, x), this.init(), c && c !== !0 && (this.$L = this.locale(c).$L), d && j != this.format(v) && (this.$d = /* @__PURE__ */ new Date("")), y = {};
        } else if (v instanceof Array)
          for (var T = v.length, a = 1; a <= T; a += 1) {
            E[1] = v[a - 1];
            var A = z.apply(this, E);
            if (A.isValid()) {
              this.$d = A.$d, this.$L = A.$L, this.init();
              break;
            }
            a === T && (this.$d = /* @__PURE__ */ new Date(""));
          }
        else
          H.call(this, V);
      };
    };
  });
})(dn);
var Mi = dn.exports;
const _i = /* @__PURE__ */ me(Mi);
var mn = { exports: {} };
(function(t, e) {
  (function(n, r) {
    t.exports = r();
  })(de, function() {
    return function(n, r) {
      var i = r.prototype, s = i.format;
      i.format = function(o) {
        var y = this, M = this.$locale();
        if (!this.isValid())
          return s.bind(this)(o);
        var p = this.$utils(), C = (o || "YYYY-MM-DDTHH:mm:ssZ").replace(/\[([^\]]+)]|Q|wo|ww|w|WW|W|zzz|z|gggg|GGGG|Do|X|x|k{1,2}|S/g, function(S) {
          switch (S) {
            case "Q":
              return Math.ceil((y.$M + 1) / 3);
            case "Do":
              return M.ordinal(y.$D);
            case "gggg":
              return y.weekYear();
            case "GGGG":
              return y.isoWeekYear();
            case "wo":
              return M.ordinal(y.week(), "W");
            case "w":
            case "ww":
              return p.s(y.week(), S === "w" ? 1 : 2, "0");
            case "W":
            case "WW":
              return p.s(y.isoWeek(), S === "W" ? 1 : 2, "0");
            case "k":
            case "kk":
              return p.s(String(y.$H === 0 ? 24 : y.$H), S === "k" ? 1 : 2, "0");
            case "X":
              return Math.floor(y.$d.getTime() / 1e3);
            case "x":
              return y.$d.getTime();
            case "z":
              return "[" + y.offsetName() + "]";
            case "zzz":
              return "[" + y.offsetName("long") + "]";
            default:
              return S;
          }
        });
        return s.bind(this)(C);
      };
    };
  });
})(mn);
var Si = mn.exports;
const Yi = /* @__PURE__ */ me(Si);
nt.extend(Ci);
nt.extend(_i);
nt.extend(Yi);
let at = "", pe = "", ve, Te = "", Lt = [], Et = [], xe = {}, be = [], jt = [], Ct = "", we = "";
const gn = ["active", "done", "crit", "milestone"];
let De = [], At = !1, Ce = !1, le = 0;
const Fi = function(t, e, n) {
  Ln.parseDirective(this, t, e, n);
}, Ui = function() {
  be = [], jt = [], Ct = "", De = [], zt = 0, he = void 0, Nt = void 0, $ = [], at = "", pe = "", we = "", ve = void 0, Te = "", Lt = [], Et = [], At = !1, Ce = !1, le = 0, xe = {}, En();
}, Li = function(t) {
  pe = t;
}, Ei = function() {
  return pe;
}, Ai = function(t) {
  ve = t;
}, Ii = function() {
  return ve;
}, Wi = function(t) {
  Te = t;
}, Oi = function() {
  return Te;
}, zi = function(t) {
  at = t;
}, Ni = function() {
  At = !0;
}, Hi = function() {
  return At;
}, Vi = function() {
  Ce = !0;
}, Pi = function() {
  return Ce;
}, Ri = function(t) {
  we = t;
}, Bi = function() {
  return we;
}, Zi = function() {
  return at;
}, Xi = function(t) {
  Lt = t.toLowerCase().split(/[\s,]+/);
}, qi = function() {
  return Lt;
}, ji = function(t) {
  Et = t.toLowerCase().split(/[\s,]+/);
}, Gi = function() {
  return Et;
}, Qi = function() {
  return xe;
}, Ji = function(t) {
  Ct = t, be.push(t);
}, Ki = function() {
  return be;
}, $i = function() {
  let t = Ne();
  const e = 10;
  let n = 0;
  for (; !t && n < e; )
    t = Ne(), n++;
  return jt = $, jt;
}, yn = function(t, e, n, r) {
  return r.includes(t.format(e.trim())) ? !1 : t.isoWeekday() >= 6 && n.includes("weekends") || n.includes(t.format("dddd").toLowerCase()) ? !0 : n.includes(t.format(e.trim()));
}, kn = function(t, e, n, r) {
  if (!n.length || t.manualEndTime)
    return;
  let i;
  t.startTime instanceof Date ? i = nt(t.startTime) : i = nt(t.startTime, e, !0), i = i.add(1, "d");
  let s;
  t.endTime instanceof Date ? s = nt(t.endTime) : s = nt(t.endTime, e, !0);
  const [o, y] = ts(
    i,
    s,
    e,
    n,
    r
  );
  t.endTime = o.toDate(), t.renderEndTime = y;
}, ts = function(t, e, n, r, i) {
  let s = !1, o = null;
  for (; t <= e; )
    s || (o = e.toDate()), s = yn(t, n, r, i), s && (e = e.add(1, "d")), t = t.add(1, "d");
  return [e, o];
}, fe = function(t, e, n) {
  n = n.trim();
  const i = /^after\s+([\d\w- ]+)/.exec(n.trim());
  if (i !== null) {
    let o = null;
    if (i[1].split(" ").forEach(function(y) {
      let M = Mt(y);
      M !== void 0 && (o ? M.endTime > o.endTime && (o = M) : o = M);
    }), o)
      return o.endTime;
    {
      const y = /* @__PURE__ */ new Date();
      return y.setHours(0, 0, 0, 0), y;
    }
  }
  let s = nt(n, e.trim(), !0);
  if (s.isValid())
    return s.toDate();
  {
    ae.debug("Invalid date:" + n), ae.debug("With date format:" + e.trim());
    const o = new Date(n);
    if (o === void 0 || isNaN(o.getTime()) || // WebKit browsers can mis-parse invalid dates to be ridiculously
    // huge numbers, e.g. new Date('202304') gets parsed as January 1, 202304.
    // This can cause virtually infinite loops while rendering, so for the
    // purposes of Gantt charts we'll just treat any date beyond 10,000 AD/BC as
    // invalid.
    o.getFullYear() < -1e4 || o.getFullYear() > 1e4)
      throw new Error("Invalid date:" + n);
    return o;
  }
}, pn = function(t) {
  const e = /^(\d+(?:\.\d+)?)([Mdhmswy]|ms)$/.exec(t.trim());
  return e !== null ? [Number.parseFloat(e[1]), e[2]] : [NaN, "ms"];
}, vn = function(t, e, n, r = !1) {
  n = n.trim();
  let i = nt(n, e.trim(), !0);
  if (i.isValid())
    return r && (i = i.add(1, "d")), i.toDate();
  let s = nt(t);
  const [o, y] = pn(n);
  if (!Number.isNaN(o)) {
    const M = s.add(o, y);
    M.isValid() && (s = M);
  }
  return s.toDate();
};
let zt = 0;
const Tt = function(t) {
  return t === void 0 ? (zt = zt + 1, "task" + zt) : t;
}, es = function(t, e) {
  let n;
  e.substr(0, 1) === ":" ? n = e.substr(1, e.length) : n = e;
  const r = n.split(","), i = {};
  wn(r, i, gn);
  for (let o = 0; o < r.length; o++)
    r[o] = r[o].trim();
  let s = "";
  switch (r.length) {
    case 1:
      i.id = Tt(), i.startTime = t.endTime, s = r[0];
      break;
    case 2:
      i.id = Tt(), i.startTime = fe(void 0, at, r[0]), s = r[1];
      break;
    case 3:
      i.id = Tt(r[0]), i.startTime = fe(void 0, at, r[1]), s = r[2];
      break;
  }
  return s && (i.endTime = vn(i.startTime, at, s, At), i.manualEndTime = nt(s, "YYYY-MM-DD", !0).isValid(), kn(i, at, Et, Lt)), i;
}, ns = function(t, e) {
  let n;
  e.substr(0, 1) === ":" ? n = e.substr(1, e.length) : n = e;
  const r = n.split(","), i = {};
  wn(r, i, gn);
  for (let s = 0; s < r.length; s++)
    r[s] = r[s].trim();
  switch (r.length) {
    case 1:
      i.id = Tt(), i.startTime = {
        type: "prevTaskEnd",
        id: t
      }, i.endTime = {
        data: r[0]
      };
      break;
    case 2:
      i.id = Tt(), i.startTime = {
        type: "getStartDate",
        startData: r[0]
      }, i.endTime = {
        data: r[1]
      };
      break;
    case 3:
      i.id = Tt(r[0]), i.startTime = {
        type: "getStartDate",
        startData: r[1]
      }, i.endTime = {
        data: r[2]
      };
      break;
  }
  return i;
};
let he, Nt, $ = [];
const Tn = {}, rs = function(t, e) {
  const n = {
    section: Ct,
    type: Ct,
    processed: !1,
    manualEndTime: !1,
    renderEndTime: null,
    raw: { data: e },
    task: t,
    classes: []
  }, r = ns(Nt, e);
  n.raw.startTime = r.startTime, n.raw.endTime = r.endTime, n.id = r.id, n.prevTaskId = Nt, n.active = r.active, n.done = r.done, n.crit = r.crit, n.milestone = r.milestone, n.order = le, le++;
  const i = $.push(n);
  Nt = n.id, Tn[n.id] = i - 1;
}, Mt = function(t) {
  const e = Tn[t];
  return $[e];
}, is = function(t, e) {
  const n = {
    section: Ct,
    type: Ct,
    description: t,
    task: t,
    classes: []
  }, r = es(he, e);
  n.startTime = r.startTime, n.endTime = r.endTime, n.id = r.id, n.active = r.active, n.done = r.done, n.crit = r.crit, n.milestone = r.milestone, he = n, jt.push(n);
}, Ne = function() {
  const t = function(n) {
    const r = $[n];
    let i = "";
    switch ($[n].raw.startTime.type) {
      case "prevTaskEnd": {
        const s = Mt(r.prevTaskId);
        r.startTime = s.endTime;
        break;
      }
      case "getStartDate":
        i = fe(void 0, at, $[n].raw.startTime.startData), i && ($[n].startTime = i);
        break;
    }
    return $[n].startTime && ($[n].endTime = vn(
      $[n].startTime,
      at,
      $[n].raw.endTime.data,
      At
    ), $[n].endTime && ($[n].processed = !0, $[n].manualEndTime = nt(
      $[n].raw.endTime.data,
      "YYYY-MM-DD",
      !0
    ).isValid(), kn($[n], at, Et, Lt))), $[n].processed;
  };
  let e = !0;
  for (const [n, r] of $.entries())
    t(n), e = e && r.processed;
  return e;
}, ss = function(t, e) {
  let n = e;
  pt().securityLevel !== "loose" && (n = An(e)), t.split(",").forEach(function(r) {
    Mt(r) !== void 0 && (bn(r, () => {
      window.open(n, "_self");
    }), xe[r] = n);
  }), xn(t, "clickable");
}, xn = function(t, e) {
  t.split(",").forEach(function(n) {
    let r = Mt(n);
    r !== void 0 && r.classes.push(e);
  });
}, as = function(t, e, n) {
  if (pt().securityLevel !== "loose" || e === void 0)
    return;
  let r = [];
  if (typeof n == "string") {
    r = n.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
    for (let s = 0; s < r.length; s++) {
      let o = r[s].trim();
      o.charAt(0) === '"' && o.charAt(o.length - 1) === '"' && (o = o.substr(1, o.length - 2)), r[s] = o;
    }
  }
  r.length === 0 && r.push(t), Mt(t) !== void 0 && bn(t, () => {
    In.runFunc(e, ...r);
  });
}, bn = function(t, e) {
  De.push(
    function() {
      const n = document.querySelector(`[id="${t}"]`);
      n !== null && n.addEventListener("click", function() {
        e();
      });
    },
    function() {
      const n = document.querySelector(`[id="${t}-text"]`);
      n !== null && n.addEventListener("click", function() {
        e();
      });
    }
  );
}, os = function(t, e, n) {
  t.split(",").forEach(function(r) {
    as(r, e, n);
  }), xn(t, "clickable");
}, cs = function(t) {
  De.forEach(function(e) {
    e(t);
  });
}, us = {
  parseDirective: Fi,
  getConfig: () => pt().gantt,
  clear: Ui,
  setDateFormat: zi,
  getDateFormat: Zi,
  enableInclusiveEndDates: Ni,
  endDatesAreInclusive: Hi,
  enableTopAxis: Vi,
  topAxisEnabled: Pi,
  setAxisFormat: Li,
  getAxisFormat: Ei,
  setTickInterval: Ai,
  getTickInterval: Ii,
  setTodayMarker: Wi,
  getTodayMarker: Oi,
  setAccTitle: Mn,
  getAccTitle: _n,
  setDiagramTitle: Sn,
  getDiagramTitle: Yn,
  setDisplayMode: Ri,
  getDisplayMode: Bi,
  setAccDescription: Fn,
  getAccDescription: Un,
  addSection: Ji,
  getSections: Ki,
  getTasks: $i,
  addTask: rs,
  findTaskById: Mt,
  addTaskOrg: is,
  setIncludes: Xi,
  getIncludes: qi,
  setExcludes: ji,
  getExcludes: Gi,
  setClickEvent: os,
  setLink: ss,
  getLinks: Qi,
  bindFunctions: cs,
  parseDuration: pn,
  isInvalidDate: yn
};
function wn(t, e, n) {
  let r = !0;
  for (; r; )
    r = !1, n.forEach(function(i) {
      const s = "^\\s*" + i + "\\s*$", o = new RegExp(s);
      t[0].match(o) && (e[i] = !0, t.shift(1), r = !0);
    });
}
const ls = function() {
  ae.debug("Something is calling, setConf, remove the call");
}, fs = (t, e) => {
  let n = [...t].map(() => -1 / 0), r = [...t].sort((s, o) => s.startTime - o.startTime || s.order - o.order), i = 0;
  for (const s of r)
    for (let o = 0; o < n.length; o++)
      if (s.startTime >= n[o]) {
        n[o] = s.endTime, s.order = o + e, o > i && (i = o);
        break;
      }
  return i;
};
let ct;
const hs = function(t, e, n, r) {
  const i = pt().gantt, s = pt().securityLevel;
  let o;
  s === "sandbox" && (o = It("#i" + e));
  const y = s === "sandbox" ? It(o.nodes()[0].contentDocument.body) : It("body"), M = s === "sandbox" ? o.nodes()[0].contentDocument : document, p = M.getElementById(e);
  ct = p.parentElement.offsetWidth, ct === void 0 && (ct = 1200), i.useWidth !== void 0 && (ct = i.useWidth);
  const C = r.db.getTasks();
  let S = [];
  for (const v of C)
    S.push(v.type);
  S = E(S);
  const w = {};
  let b = 2 * i.topPadding;
  if (r.db.getDisplayMode() === "compact" || i.displayMode === "compact") {
    const v = {};
    for (const f of C)
      v[f.section] === void 0 ? v[f.section] = [f] : v[f.section].push(f);
    let u = 0;
    for (const f of Object.keys(v)) {
      const d = fs(v[f], u) + 1;
      u += d, b += d * (i.barHeight + i.barGap), w[f] = d;
    }
  } else {
    b += C.length * (i.barHeight + i.barGap);
    for (const v of S)
      w[v] = C.filter((u) => u.type === v).length;
  }
  p.setAttribute("viewBox", "0 0 " + ct + " " + b);
  const P = y.select(`[id="${e}"]`), g = bi().domain([
    Bn(C, function(v) {
      return v.startTime;
    }),
    Rn(C, function(v) {
      return v.endTime;
    })
  ]).rangeRound([0, ct - i.leftPadding - i.rightPadding]);
  function F(v, u) {
    const f = v.startTime, d = u.startTime;
    let c = 0;
    return f > d ? c = 1 : f < d && (c = -1), c;
  }
  C.sort(F), z(C, ct, b), Wn(P, b, ct, i.useMaxWidth), P.append("text").text(r.db.getDiagramTitle()).attr("x", ct / 2).attr("y", i.titleTopMargin).attr("class", "titleText");
  function z(v, u, f) {
    const d = i.barHeight, c = d + i.barGap, T = i.topPadding, a = i.leftPadding, A = Vn().domain([0, S.length]).range(["#00B9FA", "#F95002"]).interpolate(sr);
    H(
      c,
      T,
      a,
      u,
      f,
      v,
      r.db.getExcludes(),
      r.db.getIncludes()
    ), V(a, T, u, f), O(v, c, T, a, d, A, u), j(c, T), x(a, T, u, f);
  }
  function O(v, u, f, d, c, T, a) {
    const h = [...new Set(v.map((m) => m.order))].map((m) => v.find((_) => _.order === m));
    P.append("g").selectAll("rect").data(h).enter().append("rect").attr("x", 0).attr("y", function(m, _) {
      return _ = m.order, _ * u + f - 2;
    }).attr("width", function() {
      return a - i.rightPadding / 2;
    }).attr("height", u).attr("class", function(m) {
      for (const [_, Y] of S.entries())
        if (m.type === Y)
          return "section section" + _ % i.numberSectionStyles;
      return "section section0";
    });
    const B = P.append("g").selectAll("rect").data(v).enter(), Z = r.db.getLinks();
    if (B.append("rect").attr("id", function(m) {
      return m.id;
    }).attr("rx", 3).attr("ry", 3).attr("x", function(m) {
      return m.milestone ? g(m.startTime) + d + 0.5 * (g(m.endTime) - g(m.startTime)) - 0.5 * c : g(m.startTime) + d;
    }).attr("y", function(m, _) {
      return _ = m.order, _ * u + f;
    }).attr("width", function(m) {
      return m.milestone ? c : g(m.renderEndTime || m.endTime) - g(m.startTime);
    }).attr("height", c).attr("transform-origin", function(m, _) {
      return _ = m.order, (g(m.startTime) + d + 0.5 * (g(m.endTime) - g(m.startTime))).toString() + "px " + (_ * u + f + 0.5 * c).toString() + "px";
    }).attr("class", function(m) {
      const _ = "task";
      let Y = "";
      m.classes.length > 0 && (Y = m.classes.join(" "));
      let U = 0;
      for (const [G, R] of S.entries())
        m.type === R && (U = G % i.numberSectionStyles);
      let W = "";
      return m.active ? m.crit ? W += " activeCrit" : W = " active" : m.done ? m.crit ? W = " doneCrit" : W = " done" : m.crit && (W += " crit"), W.length === 0 && (W = " task"), m.milestone && (W = " milestone " + W), W += U, W += " " + Y, _ + W;
    }), B.append("text").attr("id", function(m) {
      return m.id + "-text";
    }).text(function(m) {
      return m.task;
    }).attr("font-size", i.fontSize).attr("x", function(m) {
      let _ = g(m.startTime), Y = g(m.renderEndTime || m.endTime);
      m.milestone && (_ += 0.5 * (g(m.endTime) - g(m.startTime)) - 0.5 * c), m.milestone && (Y = _ + c);
      const U = this.getBBox().width;
      return U > Y - _ ? Y + U + 1.5 * i.leftPadding > a ? _ + d - 5 : Y + d + 5 : (Y - _) / 2 + _ + d;
    }).attr("y", function(m, _) {
      return _ = m.order, _ * u + i.barHeight / 2 + (i.fontSize / 2 - 2) + f;
    }).attr("text-height", c).attr("class", function(m) {
      const _ = g(m.startTime);
      let Y = g(m.endTime);
      m.milestone && (Y = _ + c);
      const U = this.getBBox().width;
      let W = "";
      m.classes.length > 0 && (W = m.classes.join(" "));
      let G = 0;
      for (const [ft, q] of S.entries())
        m.type === q && (G = ft % i.numberSectionStyles);
      let R = "";
      return m.active && (m.crit ? R = "activeCritText" + G : R = "activeText" + G), m.done ? m.crit ? R = R + " doneCritText" + G : R = R + " doneText" + G : m.crit && (R = R + " critText" + G), m.milestone && (R += " milestoneText"), U > Y - _ ? Y + U + 1.5 * i.leftPadding > a ? W + " taskTextOutsideLeft taskTextOutside" + G + " " + R : W + " taskTextOutsideRight taskTextOutside" + G + " " + R + " width-" + U : W + " taskText taskText" + G + " " + R + " width-" + U;
    }), pt().securityLevel === "sandbox") {
      let m;
      m = It("#i" + e);
      const _ = m.nodes()[0].contentDocument;
      B.filter(function(Y) {
        return Z[Y.id] !== void 0;
      }).each(function(Y) {
        var U = _.querySelector("#" + Y.id), W = _.querySelector("#" + Y.id + "-text");
        const G = U.parentNode;
        var R = _.createElement("a");
        R.setAttribute("xlink:href", Z[Y.id]), R.setAttribute("target", "_top"), G.appendChild(R), R.appendChild(U), R.appendChild(W);
      });
    }
  }
  function H(v, u, f, d, c, T, a, A) {
    const h = T.reduce(
      (U, { startTime: W }) => U ? Math.min(U, W) : W,
      0
    ), B = T.reduce((U, { endTime: W }) => U ? Math.max(U, W) : W, 0), Z = r.db.getDateFormat();
    if (!h || !B)
      return;
    const J = [];
    let m = null, _ = nt(h);
    for (; _.valueOf() <= B; )
      r.db.isInvalidDate(_, Z, a, A) ? m ? m.end = _ : m = {
        start: _,
        end: _
      } : m && (J.push(m), m = null), _ = _.add(1, "d");
    P.append("g").selectAll("rect").data(J).enter().append("rect").attr("id", function(U) {
      return "exclude-" + U.start.format("YYYY-MM-DD");
    }).attr("x", function(U) {
      return g(U.start) + f;
    }).attr("y", i.gridLineStartPadding).attr("width", function(U) {
      const W = U.end.add(1, "day");
      return g(W) - g(U.start);
    }).attr("height", c - u - i.gridLineStartPadding).attr("transform-origin", function(U, W) {
      return (g(U.start) + f + 0.5 * (g(U.end) - g(U.start))).toString() + "px " + (W * v + 0.5 * c).toString() + "px";
    }).attr("class", "exclude-range");
  }
  function V(v, u, f, d) {
    let c = Kn(g).tickSize(-d + u + i.gridLineStartPadding).tickFormat(qt(r.db.getAxisFormat() || i.axisFormat || "%Y-%m-%d"));
    const a = /^([1-9]\d*)(minute|hour|day|week|month)$/.exec(
      r.db.getTickInterval() || i.tickInterval
    );
    if (a !== null) {
      const A = a[1];
      switch (a[2]) {
        case "minute":
          c.ticks(Pt.every(A));
          break;
        case "hour":
          c.ticks(Rt.every(A));
          break;
        case "day":
          c.ticks(xt.every(A));
          break;
        case "week":
          c.ticks(bt.every(A));
          break;
        case "month":
          c.ticks(Zt.every(A));
          break;
      }
    }
    if (P.append("g").attr("class", "grid").attr("transform", "translate(" + v + ", " + (d - 50) + ")").call(c).selectAll("text").style("text-anchor", "middle").attr("fill", "#000").attr("stroke", "none").attr("font-size", 10).attr("dy", "1em"), r.db.topAxisEnabled() || i.topAxis) {
      let A = Jn(g).tickSize(-d + u + i.gridLineStartPadding).tickFormat(qt(r.db.getAxisFormat() || i.axisFormat || "%Y-%m-%d"));
      if (a !== null) {
        const h = a[1];
        switch (a[2]) {
          case "minute":
            A.ticks(Pt.every(h));
            break;
          case "hour":
            A.ticks(Rt.every(h));
            break;
          case "day":
            A.ticks(xt.every(h));
            break;
          case "week":
            A.ticks(bt.every(h));
            break;
          case "month":
            A.ticks(Zt.every(h));
            break;
        }
      }
      P.append("g").attr("class", "grid").attr("transform", "translate(" + v + ", " + u + ")").call(A).selectAll("text").style("text-anchor", "middle").attr("fill", "#000").attr("stroke", "none").attr("font-size", 10);
    }
  }
  function j(v, u) {
    let f = 0;
    const d = Object.keys(w).map((c) => [c, w[c]]);
    P.append("g").selectAll("text").data(d).enter().append(function(c) {
      const T = c[0].split(On.lineBreakRegex), a = -(T.length - 1) / 2, A = M.createElementNS("http://www.w3.org/2000/svg", "text");
      A.setAttribute("dy", a + "em");
      for (const [h, B] of T.entries()) {
        const Z = M.createElementNS("http://www.w3.org/2000/svg", "tspan");
        Z.setAttribute("alignment-baseline", "central"), Z.setAttribute("x", "10"), h > 0 && Z.setAttribute("dy", "1em"), Z.textContent = B, A.appendChild(Z);
      }
      return A;
    }).attr("x", 10).attr("y", function(c, T) {
      if (T > 0)
        for (let a = 0; a < T; a++)
          return f += d[T - 1][1], c[1] * v / 2 + f * v + u;
      else
        return c[1] * v / 2 + u;
    }).attr("font-size", i.sectionFontSize).attr("class", function(c) {
      for (const [T, a] of S.entries())
        if (c[0] === a)
          return "sectionTitle sectionTitle" + T % i.numberSectionStyles;
      return "sectionTitle";
    });
  }
  function x(v, u, f, d) {
    const c = r.db.getTodayMarker();
    if (c === "off")
      return;
    const T = P.append("g").attr("class", "today"), a = /* @__PURE__ */ new Date(), A = T.append("line");
    A.attr("x1", g(a) + v).attr("x2", g(a) + v).attr("y1", i.titleTopMargin).attr("y2", d - i.titleTopMargin).attr("class", "today"), c !== "" && A.attr("style", c.replace(/,/g, ";"));
  }
  function E(v) {
    const u = {}, f = [];
    for (let d = 0, c = v.length; d < c; ++d)
      Object.prototype.hasOwnProperty.call(u, v[d]) || (u[v[d]] = !0, f.push(v[d]));
    return f;
  }
}, ds = {
  setConf: ls,
  draw: hs
}, ms = (t) => `
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
`, gs = ms, vs = {
  parser: wi,
  db: us,
  renderer: ds,
  styles: gs
};
export {
  vs as diagram
};
