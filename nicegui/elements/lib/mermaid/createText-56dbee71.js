import { b6 as At, l as zt, aR as It } from "./mermaid-5f2d2ec5.js";
function Tt(n, r) {
  var { includeImageAlt: t = !0 } = r || {};
  return nt(n, t);
}
function nt(n, r) {
  return n && typeof n == "object" && // @ts-ignore looks like a literal.
  (n.value || // @ts-ignore looks like an image.
  (r ? n.alt : "") || // @ts-ignore looks like a parent.
  "children" in n && Hn(n.children, r) || Array.isArray(n) && Hn(n, r)) || "";
}
function Hn(n, r) {
  for (var t = [], e = -1; ++e < n.length; )
    t[e] = nt(n[e], r);
  return t.join("");
}
function en(n, r, t, e) {
  const u = n.length;
  let l = 0, i;
  if (r < 0 ? r = -r > u ? 0 : u + r : r = r > u ? u : r, t = t > 0 ? t : 0, e.length < 1e4)
    i = Array.from(e), i.unshift(r, t), [].splice.apply(n, i);
  else
    for (t && [].splice.apply(n, [r, t]); l < e.length; )
      i = e.slice(l, l + 1e4), i.unshift(r, 0), [].splice.apply(n, i), l += 1e4, r += 1e4;
}
function Z(n, r) {
  return n.length > 0 ? (en(n, n.length, 0, r), n) : r;
}
const Nn = {}.hasOwnProperty;
function Bt(n) {
  const r = {};
  let t = -1;
  for (; ++t < n.length; )
    Lt(r, n[t]);
  return r;
}
function Lt(n, r) {
  let t;
  for (t in r) {
    const u = (Nn.call(n, t) ? n[t] : void 0) || (n[t] = {}), l = r[t];
    let i;
    for (i in l) {
      Nn.call(u, i) || (u[i] = []);
      const a = l[i];
      Ot(
        // @ts-expect-error Looks like a list.
        u[i],
        Array.isArray(a) ? a : a ? [a] : []
      );
    }
  }
}
function Ot(n, r) {
  let t = -1;
  const e = [];
  for (; ++t < r.length; )
    (r[t].add === "after" ? n : e).push(r[t]);
  en(n, 0, 0, e);
}
const Dt = /[!-/:-@[-`{-~\u00A1\u00A7\u00AB\u00B6\u00B7\u00BB\u00BF\u037E\u0387\u055A-\u055F\u0589\u058A\u05BE\u05C0\u05C3\u05C6\u05F3\u05F4\u0609\u060A\u060C\u060D\u061B\u061E\u061F\u066A-\u066D\u06D4\u0700-\u070D\u07F7-\u07F9\u0830-\u083E\u085E\u0964\u0965\u0970\u09FD\u0A76\u0AF0\u0C77\u0C84\u0DF4\u0E4F\u0E5A\u0E5B\u0F04-\u0F12\u0F14\u0F3A-\u0F3D\u0F85\u0FD0-\u0FD4\u0FD9\u0FDA\u104A-\u104F\u10FB\u1360-\u1368\u1400\u166E\u169B\u169C\u16EB-\u16ED\u1735\u1736\u17D4-\u17D6\u17D8-\u17DA\u1800-\u180A\u1944\u1945\u1A1E\u1A1F\u1AA0-\u1AA6\u1AA8-\u1AAD\u1B5A-\u1B60\u1BFC-\u1BFF\u1C3B-\u1C3F\u1C7E\u1C7F\u1CC0-\u1CC7\u1CD3\u2010-\u2027\u2030-\u2043\u2045-\u2051\u2053-\u205E\u207D\u207E\u208D\u208E\u2308-\u230B\u2329\u232A\u2768-\u2775\u27C5\u27C6\u27E6-\u27EF\u2983-\u2998\u29D8-\u29DB\u29FC\u29FD\u2CF9-\u2CFC\u2CFE\u2CFF\u2D70\u2E00-\u2E2E\u2E30-\u2E4F\u2E52\u3001-\u3003\u3008-\u3011\u3014-\u301F\u3030\u303D\u30A0\u30FB\uA4FE\uA4FF\uA60D-\uA60F\uA673\uA67E\uA6F2-\uA6F7\uA874-\uA877\uA8CE\uA8CF\uA8F8-\uA8FA\uA8FC\uA92E\uA92F\uA95F\uA9C1-\uA9CD\uA9DE\uA9DF\uAA5C-\uAA5F\uAADE\uAADF\uAAF0\uAAF1\uABEB\uFD3E\uFD3F\uFE10-\uFE19\uFE30-\uFE52\uFE54-\uFE61\uFE63\uFE68\uFE6A\uFE6B\uFF01-\uFF03\uFF05-\uFF0A\uFF0C-\uFF0F\uFF1A\uFF1B\uFF1F\uFF20\uFF3B-\uFF3D\uFF3F\uFF5B\uFF5D\uFF5F-\uFF65]/, tn = sn(/[A-Za-z]/), An = sn(/\d/), Pt = sn(/[\dA-Fa-f]/), v = sn(/[\dA-Za-z]/), _t = sn(/[!-/:-@[-`{-~]/), Vn = sn(/[#-'*+\--9=?A-Z^-~]/);
function zn(n) {
  return (
    // Special whitespace codes (which have negative values), C0 and Control
    // character DEL
    n !== null && (n < 32 || n === 127)
  );
}
function Y(n) {
  return n !== null && (n < 0 || n === 32);
}
function C(n) {
  return n !== null && n < -2;
}
function q(n) {
  return n === -2 || n === -1 || n === 32;
}
const Mt = sn(/\s/), Rt = sn(Dt);
function sn(n) {
  return r;
  function r(t) {
    return t !== null && n.test(String.fromCharCode(t));
  }
}
function T(n, r, t, e) {
  const u = e ? e - 1 : Number.POSITIVE_INFINITY;
  let l = 0;
  return i;
  function i(c) {
    return q(c) ? (n.enter(t), a(c)) : r(c);
  }
  function a(c) {
    return q(c) && l++ < u ? (n.consume(c), a) : (n.exit(t), r(c));
  }
}
const jt = {
  tokenize: qt
};
function qt(n) {
  const r = n.attempt(
    this.parser.constructs.contentInitial,
    e,
    u
  );
  let t;
  return r;
  function e(a) {
    if (a === null) {
      n.consume(a);
      return;
    }
    return n.enter("lineEnding"), n.consume(a), n.exit("lineEnding"), T(n, r, "linePrefix");
  }
  function u(a) {
    return n.enter("paragraph"), l(a);
  }
  function l(a) {
    const c = n.enter("chunkText", {
      contentType: "text",
      previous: t
    });
    return t && (t.next = c), t = c, i(a);
  }
  function i(a) {
    if (a === null) {
      n.exit("chunkText"), n.exit("paragraph"), n.consume(a);
      return;
    }
    return C(a) ? (n.consume(a), n.exit("chunkText"), l) : (n.consume(a), i);
  }
}
const Ht = {
  tokenize: Nt
}, Wn = {
  tokenize: Vt
};
function Nt(n) {
  const r = this, t = [];
  let e = 0, u, l, i;
  return a;
  function a(F) {
    if (e < t.length) {
      const L = t[e];
      return r.containerState = L[1], n.attempt(
        L[0].continuation,
        c,
        p
      )(F);
    }
    return p(F);
  }
  function c(F) {
    if (e++, r.containerState._closeFlow) {
      r.containerState._closeFlow = void 0, u && _();
      const L = r.events.length;
      let O = L, d;
      for (; O--; )
        if (r.events[O][0] === "exit" && r.events[O][1].type === "chunkFlow") {
          d = r.events[O][1].end;
          break;
        }
      y(e);
      let P = L;
      for (; P < r.events.length; )
        r.events[P][1].end = Object.assign({}, d), P++;
      return en(
        r.events,
        O + 1,
        0,
        r.events.slice(L)
      ), r.events.length = P, p(F);
    }
    return a(F);
  }
  function p(F) {
    if (e === t.length) {
      if (!u)
        return g(F);
      if (u.currentConstruct && u.currentConstruct.concrete)
        return k(F);
      r.interrupt = !!(u.currentConstruct && !u._gfmTableDynamicInterruptHack);
    }
    return r.containerState = {}, n.check(
      Wn,
      h,
      x
    )(F);
  }
  function h(F) {
    return u && _(), y(e), g(F);
  }
  function x(F) {
    return r.parser.lazy[r.now().line] = e !== t.length, i = r.now().offset, k(F);
  }
  function g(F) {
    return r.containerState = {}, n.attempt(
      Wn,
      f,
      k
    )(F);
  }
  function f(F) {
    return e++, t.push([r.currentConstruct, r.containerState]), g(F);
  }
  function k(F) {
    if (F === null) {
      u && _(), y(0), n.consume(F);
      return;
    }
    return u = u || r.parser.flow(r.now()), n.enter("chunkFlow", {
      contentType: "flow",
      previous: l,
      _tokenizer: u
    }), B(F);
  }
  function B(F) {
    if (F === null) {
      D(n.exit("chunkFlow"), !0), y(0), n.consume(F);
      return;
    }
    return C(F) ? (n.consume(F), D(n.exit("chunkFlow")), e = 0, r.interrupt = void 0, a) : (n.consume(F), B);
  }
  function D(F, L) {
    const O = r.sliceStream(F);
    if (L && O.push(null), F.previous = l, l && (l.next = F), l = F, u.defineSkip(F.start), u.write(O), r.parser.lazy[F.start.line]) {
      let d = u.events.length;
      for (; d--; )
        if (
          // The token starts before the line ending…
          u.events[d][1].start.offset < i && // …and either is not ended yet…
          (!u.events[d][1].end || // …or ends after it.
          u.events[d][1].end.offset > i)
        )
          return;
      const P = r.events.length;
      let R = P, j, V;
      for (; R--; )
        if (r.events[R][0] === "exit" && r.events[R][1].type === "chunkFlow") {
          if (j) {
            V = r.events[R][1].end;
            break;
          }
          j = !0;
        }
      for (y(e), d = P; d < r.events.length; )
        r.events[d][1].end = Object.assign({}, V), d++;
      en(
        r.events,
        R + 1,
        0,
        r.events.slice(P)
      ), r.events.length = d;
    }
  }
  function y(F) {
    let L = t.length;
    for (; L-- > F; ) {
      const O = t[L];
      r.containerState = O[1], O[0].exit.call(r, n);
    }
    t.length = F;
  }
  function _() {
    u.write([null]), l = void 0, u = void 0, r.containerState._closeFlow = void 0;
  }
}
function Vt(n, r, t) {
  return T(
    n,
    n.attempt(this.parser.constructs.document, r, t),
    "linePrefix",
    this.parser.constructs.disable.null.includes("codeIndented") ? void 0 : 4
  );
}
function Qn(n) {
  if (n === null || Y(n) || Mt(n))
    return 1;
  if (Rt(n))
    return 2;
}
function Ln(n, r, t) {
  const e = [];
  let u = -1;
  for (; ++u < n.length; ) {
    const l = n[u].resolveAll;
    l && !e.includes(l) && (r = l(r, t), e.push(l));
  }
  return r;
}
const In = {
  name: "attention",
  tokenize: Qt,
  resolveAll: Wt
};
function Wt(n, r) {
  let t = -1, e, u, l, i, a, c, p, h;
  for (; ++t < n.length; )
    if (n[t][0] === "enter" && n[t][1].type === "attentionSequence" && n[t][1]._close) {
      for (e = t; e--; )
        if (n[e][0] === "exit" && n[e][1].type === "attentionSequence" && n[e][1]._open && // If the markers are the same:
        r.sliceSerialize(n[e][1]).charCodeAt(0) === r.sliceSerialize(n[t][1]).charCodeAt(0)) {
          if ((n[e][1]._close || n[t][1]._open) && (n[t][1].end.offset - n[t][1].start.offset) % 3 && !((n[e][1].end.offset - n[e][1].start.offset + n[t][1].end.offset - n[t][1].start.offset) % 3))
            continue;
          c = n[e][1].end.offset - n[e][1].start.offset > 1 && n[t][1].end.offset - n[t][1].start.offset > 1 ? 2 : 1;
          const x = Object.assign({}, n[e][1].end), g = Object.assign({}, n[t][1].start);
          Un(x, -c), Un(g, c), i = {
            type: c > 1 ? "strongSequence" : "emphasisSequence",
            start: x,
            end: Object.assign({}, n[e][1].end)
          }, a = {
            type: c > 1 ? "strongSequence" : "emphasisSequence",
            start: Object.assign({}, n[t][1].start),
            end: g
          }, l = {
            type: c > 1 ? "strongText" : "emphasisText",
            start: Object.assign({}, n[e][1].end),
            end: Object.assign({}, n[t][1].start)
          }, u = {
            type: c > 1 ? "strong" : "emphasis",
            start: Object.assign({}, i.start),
            end: Object.assign({}, a.end)
          }, n[e][1].end = Object.assign({}, i.start), n[t][1].start = Object.assign({}, a.end), p = [], n[e][1].end.offset - n[e][1].start.offset && (p = Z(p, [
            ["enter", n[e][1], r],
            ["exit", n[e][1], r]
          ])), p = Z(p, [
            ["enter", u, r],
            ["enter", i, r],
            ["exit", i, r],
            ["enter", l, r]
          ]), p = Z(
            p,
            Ln(
              r.parser.constructs.insideSpan.null,
              n.slice(e + 1, t),
              r
            )
          ), p = Z(p, [
            ["exit", l, r],
            ["enter", a, r],
            ["exit", a, r],
            ["exit", u, r]
          ]), n[t][1].end.offset - n[t][1].start.offset ? (h = 2, p = Z(p, [
            ["enter", n[t][1], r],
            ["exit", n[t][1], r]
          ])) : h = 0, en(n, e - 1, t - e + 3, p), t = e + p.length - h - 2;
          break;
        }
    }
  for (t = -1; ++t < n.length; )
    n[t][1].type === "attentionSequence" && (n[t][1].type = "data");
  return n;
}
function Qt(n, r) {
  const t = this.parser.constructs.attentionMarkers.null, e = this.previous, u = Qn(e);
  let l;
  return i;
  function i(c) {
    return n.enter("attentionSequence"), l = c, a(c);
  }
  function a(c) {
    if (c === l)
      return n.consume(c), a;
    const p = n.exit("attentionSequence"), h = Qn(c), x = !h || h === 2 && u || t.includes(c), g = !u || u === 2 && h || t.includes(e);
    return p._open = !!(l === 42 ? x : x && (u || !g)), p._close = !!(l === 42 ? g : g && (h || !x)), r(c);
  }
}
function Un(n, r) {
  n.column += r, n.offset += r, n._bufferIndex += r;
}
const Ut = {
  name: "autolink",
  tokenize: $t
};
function $t(n, r, t) {
  let e = 1;
  return u;
  function u(k) {
    return n.enter("autolink"), n.enter("autolinkMarker"), n.consume(k), n.exit("autolinkMarker"), n.enter("autolinkProtocol"), l;
  }
  function l(k) {
    return tn(k) ? (n.consume(k), i) : Vn(k) ? p(k) : t(k);
  }
  function i(k) {
    return k === 43 || k === 45 || k === 46 || v(k) ? a(k) : p(k);
  }
  function a(k) {
    return k === 58 ? (n.consume(k), c) : (k === 43 || k === 45 || k === 46 || v(k)) && e++ < 32 ? (n.consume(k), a) : p(k);
  }
  function c(k) {
    return k === 62 ? (n.exit("autolinkProtocol"), f(k)) : k === null || k === 32 || k === 60 || zn(k) ? t(k) : (n.consume(k), c);
  }
  function p(k) {
    return k === 64 ? (n.consume(k), e = 0, h) : Vn(k) ? (n.consume(k), p) : t(k);
  }
  function h(k) {
    return v(k) ? x(k) : t(k);
  }
  function x(k) {
    return k === 46 ? (n.consume(k), e = 0, h) : k === 62 ? (n.exit("autolinkProtocol").type = "autolinkEmail", f(k)) : g(k);
  }
  function g(k) {
    return (k === 45 || v(k)) && e++ < 63 ? (n.consume(k), k === 45 ? g : x) : t(k);
  }
  function f(k) {
    return n.enter("autolinkMarker"), n.consume(k), n.exit("autolinkMarker"), n.exit("autolink"), r;
  }
}
const Sn = {
  tokenize: Zt,
  partial: !0
};
function Zt(n, r, t) {
  return T(n, e, "linePrefix");
  function e(u) {
    return u === null || C(u) ? r(u) : t(u);
  }
}
const tt = {
  name: "blockQuote",
  tokenize: Yt,
  continuation: {
    tokenize: Gt
  },
  exit: Jt
};
function Yt(n, r, t) {
  const e = this;
  return u;
  function u(i) {
    if (i === 62) {
      const a = e.containerState;
      return a.open || (n.enter("blockQuote", {
        _container: !0
      }), a.open = !0), n.enter("blockQuotePrefix"), n.enter("blockQuoteMarker"), n.consume(i), n.exit("blockQuoteMarker"), l;
    }
    return t(i);
  }
  function l(i) {
    return q(i) ? (n.enter("blockQuotePrefixWhitespace"), n.consume(i), n.exit("blockQuotePrefixWhitespace"), n.exit("blockQuotePrefix"), r) : (n.exit("blockQuotePrefix"), r(i));
  }
}
function Gt(n, r, t) {
  return T(
    n,
    n.attempt(tt, r, t),
    "linePrefix",
    this.parser.constructs.disable.null.includes("codeIndented") ? void 0 : 4
  );
}
function Jt(n) {
  n.exit("blockQuote");
}
const et = {
  name: "characterEscape",
  tokenize: Kt
};
function Kt(n, r, t) {
  return e;
  function e(l) {
    return n.enter("characterEscape"), n.enter("escapeMarker"), n.consume(l), n.exit("escapeMarker"), u;
  }
  function u(l) {
    return _t(l) ? (n.enter("characterEscapeValue"), n.consume(l), n.exit("characterEscapeValue"), n.exit("characterEscape"), r) : t(l);
  }
}
const $n = document.createElement("i");
function On(n) {
  const r = "&" + n + ";";
  $n.innerHTML = r;
  const t = $n.textContent;
  return t.charCodeAt(t.length - 1) === 59 && n !== "semi" || t === r ? !1 : t;
}
const rt = {
  name: "characterReference",
  tokenize: Xt
};
function Xt(n, r, t) {
  const e = this;
  let u = 0, l, i;
  return a;
  function a(x) {
    return n.enter("characterReference"), n.enter("characterReferenceMarker"), n.consume(x), n.exit("characterReferenceMarker"), c;
  }
  function c(x) {
    return x === 35 ? (n.enter("characterReferenceMarkerNumeric"), n.consume(x), n.exit("characterReferenceMarkerNumeric"), p) : (n.enter("characterReferenceValue"), l = 31, i = v, h(x));
  }
  function p(x) {
    return x === 88 || x === 120 ? (n.enter("characterReferenceMarkerHexadecimal"), n.consume(x), n.exit("characterReferenceMarkerHexadecimal"), n.enter("characterReferenceValue"), l = 6, i = Pt, h) : (n.enter("characterReferenceValue"), l = 7, i = An, h(x));
  }
  function h(x) {
    let g;
    return x === 59 && u ? (g = n.exit("characterReferenceValue"), i === v && !On(e.sliceSerialize(g)) ? t(x) : (n.enter("characterReferenceMarker"), n.consume(x), n.exit("characterReferenceMarker"), n.exit("characterReference"), r)) : i(x) && u++ < l ? (n.consume(x), h) : t(x);
  }
}
const Zn = {
  name: "codeFenced",
  tokenize: vt,
  concrete: !0
};
function vt(n, r, t) {
  const e = this, u = {
    tokenize: O,
    partial: !0
  }, l = {
    tokenize: L,
    partial: !0
  }, i = this.events[this.events.length - 1], a = i && i[1].type === "linePrefix" ? i[2].sliceSerialize(i[1], !0).length : 0;
  let c = 0, p;
  return h;
  function h(d) {
    return n.enter("codeFenced"), n.enter("codeFencedFence"), n.enter("codeFencedFenceSequence"), p = d, x(d);
  }
  function x(d) {
    return d === p ? (n.consume(d), c++, x) : (n.exit("codeFencedFenceSequence"), c < 3 ? t(d) : T(n, g, "whitespace")(d));
  }
  function g(d) {
    return d === null || C(d) ? D(d) : (n.enter("codeFencedFenceInfo"), n.enter("chunkString", {
      contentType: "string"
    }), f(d));
  }
  function f(d) {
    return d === null || Y(d) ? (n.exit("chunkString"), n.exit("codeFencedFenceInfo"), T(n, k, "whitespace")(d)) : d === 96 && d === p ? t(d) : (n.consume(d), f);
  }
  function k(d) {
    return d === null || C(d) ? D(d) : (n.enter("codeFencedFenceMeta"), n.enter("chunkString", {
      contentType: "string"
    }), B(d));
  }
  function B(d) {
    return d === null || C(d) ? (n.exit("chunkString"), n.exit("codeFencedFenceMeta"), D(d)) : d === 96 && d === p ? t(d) : (n.consume(d), B);
  }
  function D(d) {
    return n.exit("codeFencedFence"), e.interrupt ? r(d) : y(d);
  }
  function y(d) {
    return d === null ? F(d) : C(d) ? n.attempt(
      l,
      n.attempt(
        u,
        F,
        a ? T(
          n,
          y,
          "linePrefix",
          a + 1
        ) : y
      ),
      F
    )(d) : (n.enter("codeFlowValue"), _(d));
  }
  function _(d) {
    return d === null || C(d) ? (n.exit("codeFlowValue"), y(d)) : (n.consume(d), _);
  }
  function F(d) {
    return n.exit("codeFenced"), r(d);
  }
  function L(d, P, R) {
    const j = this;
    return V;
    function V(E) {
      return d.enter("lineEnding"), d.consume(E), d.exit("lineEnding"), S;
    }
    function S(E) {
      return j.parser.lazy[j.now().line] ? R(E) : P(E);
    }
  }
  function O(d, P, R) {
    let j = 0;
    return T(
      d,
      V,
      "linePrefix",
      this.parser.constructs.disable.null.includes("codeIndented") ? void 0 : 4
    );
    function V(A) {
      return d.enter("codeFencedFence"), d.enter("codeFencedFenceSequence"), S(A);
    }
    function S(A) {
      return A === p ? (d.consume(A), j++, S) : j < c ? R(A) : (d.exit("codeFencedFenceSequence"), T(d, E, "whitespace")(A));
    }
    function E(A) {
      return A === null || C(A) ? (d.exit("codeFencedFence"), P(A)) : R(A);
    }
  }
}
const wn = {
  name: "codeIndented",
  tokenize: te
}, ne = {
  tokenize: ee,
  partial: !0
};
function te(n, r, t) {
  const e = this;
  return u;
  function u(p) {
    return n.enter("codeIndented"), T(n, l, "linePrefix", 4 + 1)(p);
  }
  function l(p) {
    const h = e.events[e.events.length - 1];
    return h && h[1].type === "linePrefix" && h[2].sliceSerialize(h[1], !0).length >= 4 ? i(p) : t(p);
  }
  function i(p) {
    return p === null ? c(p) : C(p) ? n.attempt(ne, i, c)(p) : (n.enter("codeFlowValue"), a(p));
  }
  function a(p) {
    return p === null || C(p) ? (n.exit("codeFlowValue"), i(p)) : (n.consume(p), a);
  }
  function c(p) {
    return n.exit("codeIndented"), r(p);
  }
}
function ee(n, r, t) {
  const e = this;
  return u;
  function u(i) {
    return e.parser.lazy[e.now().line] ? t(i) : C(i) ? (n.enter("lineEnding"), n.consume(i), n.exit("lineEnding"), u) : T(n, l, "linePrefix", 4 + 1)(i);
  }
  function l(i) {
    const a = e.events[e.events.length - 1];
    return a && a[1].type === "linePrefix" && a[2].sliceSerialize(a[1], !0).length >= 4 ? r(i) : C(i) ? u(i) : t(i);
  }
}
const re = {
  name: "codeText",
  tokenize: le,
  resolve: ie,
  previous: ue
};
function ie(n) {
  let r = n.length - 4, t = 3, e, u;
  if ((n[t][1].type === "lineEnding" || n[t][1].type === "space") && (n[r][1].type === "lineEnding" || n[r][1].type === "space")) {
    for (e = t; ++e < r; )
      if (n[e][1].type === "codeTextData") {
        n[t][1].type = "codeTextPadding", n[r][1].type = "codeTextPadding", t += 2, r -= 2;
        break;
      }
  }
  for (e = t - 1, r++; ++e <= r; )
    u === void 0 ? e !== r && n[e][1].type !== "lineEnding" && (u = e) : (e === r || n[e][1].type === "lineEnding") && (n[u][1].type = "codeTextData", e !== u + 2 && (n[u][1].end = n[e - 1][1].end, n.splice(u + 2, e - u - 2), r -= e - u - 2, e = u + 2), u = void 0);
  return n;
}
function ue(n) {
  return n !== 96 || this.events[this.events.length - 1][1].type === "characterEscape";
}
function le(n, r, t) {
  let e = 0, u, l;
  return i;
  function i(x) {
    return n.enter("codeText"), n.enter("codeTextSequence"), a(x);
  }
  function a(x) {
    return x === 96 ? (n.consume(x), e++, a) : (n.exit("codeTextSequence"), c(x));
  }
  function c(x) {
    return x === null ? t(x) : x === 96 ? (l = n.enter("codeTextSequence"), u = 0, h(x)) : x === 32 ? (n.enter("space"), n.consume(x), n.exit("space"), c) : C(x) ? (n.enter("lineEnding"), n.consume(x), n.exit("lineEnding"), c) : (n.enter("codeTextData"), p(x));
  }
  function p(x) {
    return x === null || x === 32 || x === 96 || C(x) ? (n.exit("codeTextData"), c(x)) : (n.consume(x), p);
  }
  function h(x) {
    return x === 96 ? (n.consume(x), u++, h) : u === e ? (n.exit("codeTextSequence"), n.exit("codeText"), r(x)) : (l.type = "codeTextData", p(x));
  }
}
function it(n) {
  const r = {};
  let t = -1, e, u, l, i, a, c, p;
  for (; ++t < n.length; ) {
    for (; t in r; )
      t = r[t];
    if (e = n[t], t && e[1].type === "chunkFlow" && n[t - 1][1].type === "listItemPrefix" && (c = e[1]._tokenizer.events, l = 0, l < c.length && c[l][1].type === "lineEndingBlank" && (l += 2), l < c.length && c[l][1].type === "content"))
      for (; ++l < c.length && c[l][1].type !== "content"; )
        c[l][1].type === "chunkText" && (c[l][1]._isInFirstContentOfListItem = !0, l++);
    if (e[0] === "enter")
      e[1].contentType && (Object.assign(r, ae(n, t)), t = r[t], p = !0);
    else if (e[1]._container) {
      for (l = t, u = void 0; l-- && (i = n[l], i[1].type === "lineEnding" || i[1].type === "lineEndingBlank"); )
        i[0] === "enter" && (u && (n[u][1].type = "lineEndingBlank"), i[1].type = "lineEnding", u = l);
      u && (e[1].end = Object.assign({}, n[u][1].start), a = n.slice(u, t), a.unshift(e), en(n, u, t - u + 1, a));
    }
  }
  return !p;
}
function ae(n, r) {
  const t = n[r][1], e = n[r][2];
  let u = r - 1;
  const l = [], i = t._tokenizer || e.parser[t.contentType](t.start), a = i.events, c = [], p = {};
  let h, x, g = -1, f = t, k = 0, B = 0;
  const D = [B];
  for (; f; ) {
    for (; n[++u][1] !== f; )
      ;
    l.push(u), f._tokenizer || (h = e.sliceStream(f), f.next || h.push(null), x && i.defineSkip(f.start), f._isInFirstContentOfListItem && (i._gfmTasklistFirstContentOfListItem = !0), i.write(h), f._isInFirstContentOfListItem && (i._gfmTasklistFirstContentOfListItem = void 0)), x = f, f = f.next;
  }
  for (f = t; ++g < a.length; )
    // Find a void token that includes a break.
    a[g][0] === "exit" && a[g - 1][0] === "enter" && a[g][1].type === a[g - 1][1].type && a[g][1].start.line !== a[g][1].end.line && (B = g + 1, D.push(B), f._tokenizer = void 0, f.previous = void 0, f = f.next);
  for (i.events = [], f ? (f._tokenizer = void 0, f.previous = void 0) : D.pop(), g = D.length; g--; ) {
    const y = a.slice(D[g], D[g + 1]), _ = l.pop();
    c.unshift([_, _ + y.length - 1]), en(n, _, 2, y);
  }
  for (g = -1; ++g < c.length; )
    p[k + c[g][0]] = k + c[g][1], k += c[g][1] - c[g][0] - 1;
  return p;
}
const oe = {
  tokenize: he,
  resolve: ce
}, se = {
  tokenize: pe,
  partial: !0
};
function ce(n) {
  return it(n), n;
}
function he(n, r) {
  let t;
  return e;
  function e(a) {
    return n.enter("content"), t = n.enter("chunkContent", {
      contentType: "content"
    }), u(a);
  }
  function u(a) {
    return a === null ? l(a) : C(a) ? n.check(
      se,
      i,
      l
    )(a) : (n.consume(a), u);
  }
  function l(a) {
    return n.exit("chunkContent"), n.exit("content"), r(a);
  }
  function i(a) {
    return n.consume(a), n.exit("chunkContent"), t.next = n.enter("chunkContent", {
      contentType: "content",
      previous: t
    }), t = t.next, u;
  }
}
function pe(n, r, t) {
  const e = this;
  return u;
  function u(i) {
    return n.exit("chunkContent"), n.enter("lineEnding"), n.consume(i), n.exit("lineEnding"), T(n, l, "linePrefix");
  }
  function l(i) {
    if (i === null || C(i))
      return t(i);
    const a = e.events[e.events.length - 1];
    return !e.parser.constructs.disable.null.includes("codeIndented") && a && a[1].type === "linePrefix" && a[2].sliceSerialize(a[1], !0).length >= 4 ? r(i) : n.interrupt(e.parser.constructs.flow, t, r)(i);
  }
}
function ut(n, r, t, e, u, l, i, a, c) {
  const p = c || Number.POSITIVE_INFINITY;
  let h = 0;
  return x;
  function x(y) {
    return y === 60 ? (n.enter(e), n.enter(u), n.enter(l), n.consume(y), n.exit(l), g) : y === null || y === 41 || zn(y) ? t(y) : (n.enter(e), n.enter(i), n.enter(a), n.enter("chunkString", {
      contentType: "string"
    }), B(y));
  }
  function g(y) {
    return y === 62 ? (n.enter(l), n.consume(y), n.exit(l), n.exit(u), n.exit(e), r) : (n.enter(a), n.enter("chunkString", {
      contentType: "string"
    }), f(y));
  }
  function f(y) {
    return y === 62 ? (n.exit("chunkString"), n.exit(a), g(y)) : y === null || y === 60 || C(y) ? t(y) : (n.consume(y), y === 92 ? k : f);
  }
  function k(y) {
    return y === 60 || y === 62 || y === 92 ? (n.consume(y), f) : f(y);
  }
  function B(y) {
    return y === 40 ? ++h > p ? t(y) : (n.consume(y), B) : y === 41 ? h-- ? (n.consume(y), B) : (n.exit("chunkString"), n.exit(a), n.exit(i), n.exit(e), r(y)) : y === null || Y(y) ? h ? t(y) : (n.exit("chunkString"), n.exit(a), n.exit(i), n.exit(e), r(y)) : zn(y) ? t(y) : (n.consume(y), y === 92 ? D : B);
  }
  function D(y) {
    return y === 40 || y === 41 || y === 92 ? (n.consume(y), B) : B(y);
  }
}
function lt(n, r, t, e, u, l) {
  const i = this;
  let a = 0, c;
  return p;
  function p(f) {
    return n.enter(e), n.enter(u), n.consume(f), n.exit(u), n.enter(l), h;
  }
  function h(f) {
    return f === null || f === 91 || f === 93 && !c || /* To do: remove in the future once we’ve switched from
     * `micromark-extension-footnote` to `micromark-extension-gfm-footnote`,
     * which doesn’t need this */
    /* Hidden footnotes hook */
    /* c8 ignore next 3 */
    f === 94 && !a && "_hiddenFootnoteSupport" in i.parser.constructs || a > 999 ? t(f) : f === 93 ? (n.exit(l), n.enter(u), n.consume(f), n.exit(u), n.exit(e), r) : C(f) ? (n.enter("lineEnding"), n.consume(f), n.exit("lineEnding"), h) : (n.enter("chunkString", {
      contentType: "string"
    }), x(f));
  }
  function x(f) {
    return f === null || f === 91 || f === 93 || C(f) || a++ > 999 ? (n.exit("chunkString"), h(f)) : (n.consume(f), c = c || !q(f), f === 92 ? g : x);
  }
  function g(f) {
    return f === 91 || f === 92 || f === 93 ? (n.consume(f), a++, x) : x(f);
  }
}
function at(n, r, t, e, u, l) {
  let i;
  return a;
  function a(g) {
    return n.enter(e), n.enter(u), n.consume(g), n.exit(u), i = g === 40 ? 41 : g, c;
  }
  function c(g) {
    return g === i ? (n.enter(u), n.consume(g), n.exit(u), n.exit(e), r) : (n.enter(l), p(g));
  }
  function p(g) {
    return g === i ? (n.exit(l), c(i)) : g === null ? t(g) : C(g) ? (n.enter("lineEnding"), n.consume(g), n.exit("lineEnding"), T(n, p, "linePrefix")) : (n.enter("chunkString", {
      contentType: "string"
    }), h(g));
  }
  function h(g) {
    return g === i || g === null || C(g) ? (n.exit("chunkString"), p(g)) : (n.consume(g), g === 92 ? x : h);
  }
  function x(g) {
    return g === i || g === 92 ? (n.consume(g), h) : h(g);
  }
}
function dn(n, r) {
  let t;
  return e;
  function e(u) {
    return C(u) ? (n.enter("lineEnding"), n.consume(u), n.exit("lineEnding"), t = !0, e) : q(u) ? T(
      n,
      e,
      t ? "linePrefix" : "lineSuffix"
    )(u) : r(u);
  }
}
function fn(n) {
  return n.replace(/[\t\n\r ]+/g, " ").replace(/^ | $/g, "").toLowerCase().toUpperCase();
}
const me = {
  name: "definition",
  tokenize: xe
}, fe = {
  tokenize: ge,
  partial: !0
};
function xe(n, r, t) {
  const e = this;
  let u;
  return l;
  function l(c) {
    return n.enter("definition"), lt.call(
      e,
      n,
      i,
      t,
      "definitionLabel",
      "definitionLabelMarker",
      "definitionLabelString"
    )(c);
  }
  function i(c) {
    return u = fn(
      e.sliceSerialize(e.events[e.events.length - 1][1]).slice(1, -1)
    ), c === 58 ? (n.enter("definitionMarker"), n.consume(c), n.exit("definitionMarker"), dn(
      n,
      ut(
        n,
        n.attempt(
          fe,
          T(n, a, "whitespace"),
          T(n, a, "whitespace")
        ),
        t,
        "definitionDestination",
        "definitionDestinationLiteral",
        "definitionDestinationLiteralMarker",
        "definitionDestinationRaw",
        "definitionDestinationString"
      )
    )) : t(c);
  }
  function a(c) {
    return c === null || C(c) ? (n.exit("definition"), e.parser.defined.includes(u) || e.parser.defined.push(u), r(c)) : t(c);
  }
}
function ge(n, r, t) {
  return e;
  function e(i) {
    return Y(i) ? dn(n, u)(i) : t(i);
  }
  function u(i) {
    return i === 34 || i === 39 || i === 40 ? at(
      n,
      T(n, l, "whitespace"),
      t,
      "definitionTitle",
      "definitionTitleMarker",
      "definitionTitleString"
    )(i) : t(i);
  }
  function l(i) {
    return i === null || C(i) ? r(i) : t(i);
  }
}
const ke = {
  name: "hardBreakEscape",
  tokenize: de
};
function de(n, r, t) {
  return e;
  function e(l) {
    return n.enter("hardBreakEscape"), n.enter("escapeMarker"), n.consume(l), u;
  }
  function u(l) {
    return C(l) ? (n.exit("escapeMarker"), n.exit("hardBreakEscape"), r(l)) : t(l);
  }
}
const be = {
  name: "headingAtx",
  tokenize: Se,
  resolve: ye
};
function ye(n, r) {
  let t = n.length - 2, e = 3, u, l;
  return n[e][1].type === "whitespace" && (e += 2), t - 2 > e && n[t][1].type === "whitespace" && (t -= 2), n[t][1].type === "atxHeadingSequence" && (e === t - 1 || t - 4 > e && n[t - 2][1].type === "whitespace") && (t -= e + 1 === t ? 2 : 4), t > e && (u = {
    type: "atxHeadingText",
    start: n[e][1].start,
    end: n[t][1].end
  }, l = {
    type: "chunkText",
    start: n[e][1].start,
    end: n[t][1].end,
    // @ts-expect-error Constants are fine to assign.
    contentType: "text"
  }, en(n, e, t - e + 1, [
    ["enter", u, r],
    ["enter", l, r],
    ["exit", l, r],
    ["exit", u, r]
  ])), n;
}
function Se(n, r, t) {
  const e = this;
  let u = 0;
  return l;
  function l(h) {
    return n.enter("atxHeading"), n.enter("atxHeadingSequence"), i(h);
  }
  function i(h) {
    return h === 35 && u++ < 6 ? (n.consume(h), i) : h === null || Y(h) ? (n.exit("atxHeadingSequence"), e.interrupt ? r(h) : a(h)) : t(h);
  }
  function a(h) {
    return h === 35 ? (n.enter("atxHeadingSequence"), c(h)) : h === null || C(h) ? (n.exit("atxHeading"), r(h)) : q(h) ? T(n, a, "whitespace")(h) : (n.enter("atxHeadingText"), p(h));
  }
  function c(h) {
    return h === 35 ? (n.consume(h), c) : (n.exit("atxHeadingSequence"), a(h));
  }
  function p(h) {
    return h === null || h === 35 || Y(h) ? (n.exit("atxHeadingText"), a(h)) : (n.consume(h), p);
  }
}
const Fe = [
  "address",
  "article",
  "aside",
  "base",
  "basefont",
  "blockquote",
  "body",
  "caption",
  "center",
  "col",
  "colgroup",
  "dd",
  "details",
  "dialog",
  "dir",
  "div",
  "dl",
  "dt",
  "fieldset",
  "figcaption",
  "figure",
  "footer",
  "form",
  "frame",
  "frameset",
  "h1",
  "h2",
  "h3",
  "h4",
  "h5",
  "h6",
  "head",
  "header",
  "hr",
  "html",
  "iframe",
  "legend",
  "li",
  "link",
  "main",
  "menu",
  "menuitem",
  "nav",
  "noframes",
  "ol",
  "optgroup",
  "option",
  "p",
  "param",
  "section",
  "summary",
  "table",
  "tbody",
  "td",
  "tfoot",
  "th",
  "thead",
  "title",
  "tr",
  "track",
  "ul"
], Yn = ["pre", "script", "style", "textarea"], Ee = {
  name: "htmlFlow",
  tokenize: Ae,
  resolveTo: Ce,
  concrete: !0
}, we = {
  tokenize: ze,
  partial: !0
};
function Ce(n) {
  let r = n.length;
  for (; r-- && !(n[r][0] === "enter" && n[r][1].type === "htmlFlow"); )
    ;
  return r > 1 && n[r - 2][1].type === "linePrefix" && (n[r][1].start = n[r - 2][1].start, n[r + 1][1].start = n[r - 2][1].start, n.splice(r - 2, 2)), n;
}
function Ae(n, r, t) {
  const e = this;
  let u, l, i, a, c;
  return p;
  function p(o) {
    return n.enter("htmlFlow"), n.enter("htmlFlowData"), n.consume(o), h;
  }
  function h(o) {
    return o === 33 ? (n.consume(o), x) : o === 47 ? (n.consume(o), k) : o === 63 ? (n.consume(o), u = 3, e.interrupt ? r : U) : tn(o) ? (n.consume(o), i = String.fromCharCode(o), l = !0, B) : t(o);
  }
  function x(o) {
    return o === 45 ? (n.consume(o), u = 2, g) : o === 91 ? (n.consume(o), u = 5, i = "CDATA[", a = 0, f) : tn(o) ? (n.consume(o), u = 4, e.interrupt ? r : U) : t(o);
  }
  function g(o) {
    return o === 45 ? (n.consume(o), e.interrupt ? r : U) : t(o);
  }
  function f(o) {
    return o === i.charCodeAt(a++) ? (n.consume(o), a === i.length ? e.interrupt ? r : S : f) : t(o);
  }
  function k(o) {
    return tn(o) ? (n.consume(o), i = String.fromCharCode(o), B) : t(o);
  }
  function B(o) {
    return o === null || o === 47 || o === 62 || Y(o) ? o !== 47 && l && Yn.includes(i.toLowerCase()) ? (u = 1, e.interrupt ? r(o) : S(o)) : Fe.includes(i.toLowerCase()) ? (u = 6, o === 47 ? (n.consume(o), D) : e.interrupt ? r(o) : S(o)) : (u = 7, e.interrupt && !e.parser.lazy[e.now().line] ? t(o) : l ? _(o) : y(o)) : o === 45 || v(o) ? (n.consume(o), i += String.fromCharCode(o), B) : t(o);
  }
  function D(o) {
    return o === 62 ? (n.consume(o), e.interrupt ? r : S) : t(o);
  }
  function y(o) {
    return q(o) ? (n.consume(o), y) : j(o);
  }
  function _(o) {
    return o === 47 ? (n.consume(o), j) : o === 58 || o === 95 || tn(o) ? (n.consume(o), F) : q(o) ? (n.consume(o), _) : j(o);
  }
  function F(o) {
    return o === 45 || o === 46 || o === 58 || o === 95 || v(o) ? (n.consume(o), F) : L(o);
  }
  function L(o) {
    return o === 61 ? (n.consume(o), O) : q(o) ? (n.consume(o), L) : _(o);
  }
  function O(o) {
    return o === null || o === 60 || o === 61 || o === 62 || o === 96 ? t(o) : o === 34 || o === 39 ? (n.consume(o), c = o, d) : q(o) ? (n.consume(o), O) : (c = null, P(o));
  }
  function d(o) {
    return o === null || C(o) ? t(o) : o === c ? (n.consume(o), R) : (n.consume(o), d);
  }
  function P(o) {
    return o === null || o === 34 || o === 39 || o === 60 || o === 61 || o === 62 || o === 96 || Y(o) ? L(o) : (n.consume(o), P);
  }
  function R(o) {
    return o === 47 || o === 62 || q(o) ? _(o) : t(o);
  }
  function j(o) {
    return o === 62 ? (n.consume(o), V) : t(o);
  }
  function V(o) {
    return q(o) ? (n.consume(o), V) : o === null || C(o) ? S(o) : t(o);
  }
  function S(o) {
    return o === 45 && u === 2 ? (n.consume(o), G) : o === 60 && u === 1 ? (n.consume(o), nn) : o === 62 && u === 4 ? (n.consume(o), H) : o === 63 && u === 3 ? (n.consume(o), U) : o === 93 && u === 5 ? (n.consume(o), W) : C(o) && (u === 6 || u === 7) ? n.check(
      we,
      H,
      E
    )(o) : o === null || C(o) ? E(o) : (n.consume(o), S);
  }
  function E(o) {
    return n.exit("htmlFlowData"), A(o);
  }
  function A(o) {
    return o === null ? s(o) : C(o) ? n.attempt(
      {
        tokenize: Q,
        partial: !0
      },
      A,
      s
    )(o) : (n.enter("htmlFlowData"), S(o));
  }
  function Q(o, cn, xn) {
    return hn;
    function hn(K) {
      return o.enter("lineEnding"), o.consume(K), o.exit("lineEnding"), N;
    }
    function N(K) {
      return e.parser.lazy[e.now().line] ? xn(K) : cn(K);
    }
  }
  function G(o) {
    return o === 45 ? (n.consume(o), U) : S(o);
  }
  function nn(o) {
    return o === 47 ? (n.consume(o), i = "", J) : S(o);
  }
  function J(o) {
    return o === 62 && Yn.includes(i.toLowerCase()) ? (n.consume(o), H) : tn(o) && i.length < 8 ? (n.consume(o), i += String.fromCharCode(o), J) : S(o);
  }
  function W(o) {
    return o === 93 ? (n.consume(o), U) : S(o);
  }
  function U(o) {
    return o === 62 ? (n.consume(o), H) : o === 45 && u === 2 ? (n.consume(o), U) : S(o);
  }
  function H(o) {
    return o === null || C(o) ? (n.exit("htmlFlowData"), s(o)) : (n.consume(o), H);
  }
  function s(o) {
    return n.exit("htmlFlow"), r(o);
  }
}
function ze(n, r, t) {
  return e;
  function e(u) {
    return n.exit("htmlFlowData"), n.enter("lineEndingBlank"), n.consume(u), n.exit("lineEndingBlank"), n.attempt(Sn, r, t);
  }
}
const Ie = {
  name: "htmlText",
  tokenize: Te
};
function Te(n, r, t) {
  const e = this;
  let u, l, i, a;
  return c;
  function c(s) {
    return n.enter("htmlText"), n.enter("htmlTextData"), n.consume(s), p;
  }
  function p(s) {
    return s === 33 ? (n.consume(s), h) : s === 47 ? (n.consume(s), P) : s === 63 ? (n.consume(s), O) : tn(s) ? (n.consume(s), V) : t(s);
  }
  function h(s) {
    return s === 45 ? (n.consume(s), x) : s === 91 ? (n.consume(s), l = "CDATA[", i = 0, D) : tn(s) ? (n.consume(s), L) : t(s);
  }
  function x(s) {
    return s === 45 ? (n.consume(s), g) : t(s);
  }
  function g(s) {
    return s === null || s === 62 ? t(s) : s === 45 ? (n.consume(s), f) : k(s);
  }
  function f(s) {
    return s === null || s === 62 ? t(s) : k(s);
  }
  function k(s) {
    return s === null ? t(s) : s === 45 ? (n.consume(s), B) : C(s) ? (a = k, W(s)) : (n.consume(s), k);
  }
  function B(s) {
    return s === 45 ? (n.consume(s), H) : k(s);
  }
  function D(s) {
    return s === l.charCodeAt(i++) ? (n.consume(s), i === l.length ? y : D) : t(s);
  }
  function y(s) {
    return s === null ? t(s) : s === 93 ? (n.consume(s), _) : C(s) ? (a = y, W(s)) : (n.consume(s), y);
  }
  function _(s) {
    return s === 93 ? (n.consume(s), F) : y(s);
  }
  function F(s) {
    return s === 62 ? H(s) : s === 93 ? (n.consume(s), F) : y(s);
  }
  function L(s) {
    return s === null || s === 62 ? H(s) : C(s) ? (a = L, W(s)) : (n.consume(s), L);
  }
  function O(s) {
    return s === null ? t(s) : s === 63 ? (n.consume(s), d) : C(s) ? (a = O, W(s)) : (n.consume(s), O);
  }
  function d(s) {
    return s === 62 ? H(s) : O(s);
  }
  function P(s) {
    return tn(s) ? (n.consume(s), R) : t(s);
  }
  function R(s) {
    return s === 45 || v(s) ? (n.consume(s), R) : j(s);
  }
  function j(s) {
    return C(s) ? (a = j, W(s)) : q(s) ? (n.consume(s), j) : H(s);
  }
  function V(s) {
    return s === 45 || v(s) ? (n.consume(s), V) : s === 47 || s === 62 || Y(s) ? S(s) : t(s);
  }
  function S(s) {
    return s === 47 ? (n.consume(s), H) : s === 58 || s === 95 || tn(s) ? (n.consume(s), E) : C(s) ? (a = S, W(s)) : q(s) ? (n.consume(s), S) : H(s);
  }
  function E(s) {
    return s === 45 || s === 46 || s === 58 || s === 95 || v(s) ? (n.consume(s), E) : A(s);
  }
  function A(s) {
    return s === 61 ? (n.consume(s), Q) : C(s) ? (a = A, W(s)) : q(s) ? (n.consume(s), A) : S(s);
  }
  function Q(s) {
    return s === null || s === 60 || s === 61 || s === 62 || s === 96 ? t(s) : s === 34 || s === 39 ? (n.consume(s), u = s, G) : C(s) ? (a = Q, W(s)) : q(s) ? (n.consume(s), Q) : (n.consume(s), u = void 0, J);
  }
  function G(s) {
    return s === u ? (n.consume(s), nn) : s === null ? t(s) : C(s) ? (a = G, W(s)) : (n.consume(s), G);
  }
  function nn(s) {
    return s === 62 || s === 47 || Y(s) ? S(s) : t(s);
  }
  function J(s) {
    return s === null || s === 34 || s === 39 || s === 60 || s === 61 || s === 96 ? t(s) : s === 62 || Y(s) ? S(s) : (n.consume(s), J);
  }
  function W(s) {
    return n.exit("htmlTextData"), n.enter("lineEnding"), n.consume(s), n.exit("lineEnding"), T(
      n,
      U,
      "linePrefix",
      e.parser.constructs.disable.null.includes("codeIndented") ? void 0 : 4
    );
  }
  function U(s) {
    return n.enter("htmlTextData"), a(s);
  }
  function H(s) {
    return s === 62 ? (n.consume(s), n.exit("htmlTextData"), n.exit("htmlText"), r) : t(s);
  }
}
const Dn = {
  name: "labelEnd",
  tokenize: _e,
  resolveTo: Pe,
  resolveAll: De
}, Be = {
  tokenize: Me
}, Le = {
  tokenize: Re
}, Oe = {
  tokenize: je
};
function De(n) {
  let r = -1, t;
  for (; ++r < n.length; )
    t = n[r][1], (t.type === "labelImage" || t.type === "labelLink" || t.type === "labelEnd") && (n.splice(r + 1, t.type === "labelImage" ? 4 : 2), t.type = "data", r++);
  return n;
}
function Pe(n, r) {
  let t = n.length, e = 0, u, l, i, a;
  for (; t--; )
    if (u = n[t][1], l) {
      if (u.type === "link" || u.type === "labelLink" && u._inactive)
        break;
      n[t][0] === "enter" && u.type === "labelLink" && (u._inactive = !0);
    } else if (i) {
      if (n[t][0] === "enter" && (u.type === "labelImage" || u.type === "labelLink") && !u._balanced && (l = t, u.type !== "labelLink")) {
        e = 2;
        break;
      }
    } else
      u.type === "labelEnd" && (i = t);
  const c = {
    type: n[l][1].type === "labelLink" ? "link" : "image",
    start: Object.assign({}, n[l][1].start),
    end: Object.assign({}, n[n.length - 1][1].end)
  }, p = {
    type: "label",
    start: Object.assign({}, n[l][1].start),
    end: Object.assign({}, n[i][1].end)
  }, h = {
    type: "labelText",
    start: Object.assign({}, n[l + e + 2][1].end),
    end: Object.assign({}, n[i - 2][1].start)
  };
  return a = [
    ["enter", c, r],
    ["enter", p, r]
  ], a = Z(a, n.slice(l + 1, l + e + 3)), a = Z(a, [["enter", h, r]]), a = Z(
    a,
    Ln(
      r.parser.constructs.insideSpan.null,
      n.slice(l + e + 4, i - 3),
      r
    )
  ), a = Z(a, [
    ["exit", h, r],
    n[i - 2],
    n[i - 1],
    ["exit", p, r]
  ]), a = Z(a, n.slice(i + 1)), a = Z(a, [["exit", c, r]]), en(n, l, n.length, a), n;
}
function _e(n, r, t) {
  const e = this;
  let u = e.events.length, l, i;
  for (; u--; )
    if ((e.events[u][1].type === "labelImage" || e.events[u][1].type === "labelLink") && !e.events[u][1]._balanced) {
      l = e.events[u][1];
      break;
    }
  return a;
  function a(h) {
    return l ? l._inactive ? p(h) : (i = e.parser.defined.includes(
      fn(
        e.sliceSerialize({
          start: l.end,
          end: e.now()
        })
      )
    ), n.enter("labelEnd"), n.enter("labelMarker"), n.consume(h), n.exit("labelMarker"), n.exit("labelEnd"), c) : t(h);
  }
  function c(h) {
    return h === 40 ? n.attempt(
      Be,
      r,
      i ? r : p
    )(h) : h === 91 ? n.attempt(
      Le,
      r,
      i ? n.attempt(Oe, r, p) : p
    )(h) : i ? r(h) : p(h);
  }
  function p(h) {
    return l._balanced = !0, t(h);
  }
}
function Me(n, r, t) {
  return e;
  function e(c) {
    return n.enter("resource"), n.enter("resourceMarker"), n.consume(c), n.exit("resourceMarker"), dn(n, u);
  }
  function u(c) {
    return c === 41 ? a(c) : ut(
      n,
      l,
      t,
      "resourceDestination",
      "resourceDestinationLiteral",
      "resourceDestinationLiteralMarker",
      "resourceDestinationRaw",
      "resourceDestinationString",
      32
    )(c);
  }
  function l(c) {
    return Y(c) ? dn(n, i)(c) : a(c);
  }
  function i(c) {
    return c === 34 || c === 39 || c === 40 ? at(
      n,
      dn(n, a),
      t,
      "resourceTitle",
      "resourceTitleMarker",
      "resourceTitleString"
    )(c) : a(c);
  }
  function a(c) {
    return c === 41 ? (n.enter("resourceMarker"), n.consume(c), n.exit("resourceMarker"), n.exit("resource"), r) : t(c);
  }
}
function Re(n, r, t) {
  const e = this;
  return u;
  function u(i) {
    return lt.call(
      e,
      n,
      l,
      t,
      "reference",
      "referenceMarker",
      "referenceString"
    )(i);
  }
  function l(i) {
    return e.parser.defined.includes(
      fn(
        e.sliceSerialize(e.events[e.events.length - 1][1]).slice(1, -1)
      )
    ) ? r(i) : t(i);
  }
}
function je(n, r, t) {
  return e;
  function e(l) {
    return n.enter("reference"), n.enter("referenceMarker"), n.consume(l), n.exit("referenceMarker"), u;
  }
  function u(l) {
    return l === 93 ? (n.enter("referenceMarker"), n.consume(l), n.exit("referenceMarker"), n.exit("reference"), r) : t(l);
  }
}
const qe = {
  name: "labelStartImage",
  tokenize: He,
  resolveAll: Dn.resolveAll
};
function He(n, r, t) {
  const e = this;
  return u;
  function u(a) {
    return n.enter("labelImage"), n.enter("labelImageMarker"), n.consume(a), n.exit("labelImageMarker"), l;
  }
  function l(a) {
    return a === 91 ? (n.enter("labelMarker"), n.consume(a), n.exit("labelMarker"), n.exit("labelImage"), i) : t(a);
  }
  function i(a) {
    return a === 94 && "_hiddenFootnoteSupport" in e.parser.constructs ? t(a) : r(a);
  }
}
const Ne = {
  name: "labelStartLink",
  tokenize: Ve,
  resolveAll: Dn.resolveAll
};
function Ve(n, r, t) {
  const e = this;
  return u;
  function u(i) {
    return n.enter("labelLink"), n.enter("labelMarker"), n.consume(i), n.exit("labelMarker"), n.exit("labelLink"), l;
  }
  function l(i) {
    return i === 94 && "_hiddenFootnoteSupport" in e.parser.constructs ? t(i) : r(i);
  }
}
const Cn = {
  name: "lineEnding",
  tokenize: We
};
function We(n, r) {
  return t;
  function t(e) {
    return n.enter("lineEnding"), n.consume(e), n.exit("lineEnding"), T(n, r, "linePrefix");
  }
}
const bn = {
  name: "thematicBreak",
  tokenize: Qe
};
function Qe(n, r, t) {
  let e = 0, u;
  return l;
  function l(c) {
    return n.enter("thematicBreak"), u = c, i(c);
  }
  function i(c) {
    return c === u ? (n.enter("thematicBreakSequence"), a(c)) : q(c) ? T(n, i, "whitespace")(c) : e < 3 || c !== null && !C(c) ? t(c) : (n.exit("thematicBreak"), r(c));
  }
  function a(c) {
    return c === u ? (n.consume(c), e++, a) : (n.exit("thematicBreakSequence"), i(c));
  }
}
const $ = {
  name: "list",
  tokenize: Ze,
  continuation: {
    tokenize: Ye
  },
  exit: Je
}, Ue = {
  tokenize: Ke,
  partial: !0
}, $e = {
  tokenize: Ge,
  partial: !0
};
function Ze(n, r, t) {
  const e = this, u = e.events[e.events.length - 1];
  let l = u && u[1].type === "linePrefix" ? u[2].sliceSerialize(u[1], !0).length : 0, i = 0;
  return a;
  function a(f) {
    const k = e.containerState.type || (f === 42 || f === 43 || f === 45 ? "listUnordered" : "listOrdered");
    if (k === "listUnordered" ? !e.containerState.marker || f === e.containerState.marker : An(f)) {
      if (e.containerState.type || (e.containerState.type = k, n.enter(k, {
        _container: !0
      })), k === "listUnordered")
        return n.enter("listItemPrefix"), f === 42 || f === 45 ? n.check(bn, t, p)(f) : p(f);
      if (!e.interrupt || f === 49)
        return n.enter("listItemPrefix"), n.enter("listItemValue"), c(f);
    }
    return t(f);
  }
  function c(f) {
    return An(f) && ++i < 10 ? (n.consume(f), c) : (!e.interrupt || i < 2) && (e.containerState.marker ? f === e.containerState.marker : f === 41 || f === 46) ? (n.exit("listItemValue"), p(f)) : t(f);
  }
  function p(f) {
    return n.enter("listItemMarker"), n.consume(f), n.exit("listItemMarker"), e.containerState.marker = e.containerState.marker || f, n.check(
      Sn,
      // Can’t be empty when interrupting.
      e.interrupt ? t : h,
      n.attempt(
        Ue,
        g,
        x
      )
    );
  }
  function h(f) {
    return e.containerState.initialBlankLine = !0, l++, g(f);
  }
  function x(f) {
    return q(f) ? (n.enter("listItemPrefixWhitespace"), n.consume(f), n.exit("listItemPrefixWhitespace"), g) : t(f);
  }
  function g(f) {
    return e.containerState.size = l + e.sliceSerialize(n.exit("listItemPrefix"), !0).length, r(f);
  }
}
function Ye(n, r, t) {
  const e = this;
  return e.containerState._closeFlow = void 0, n.check(Sn, u, l);
  function u(a) {
    return e.containerState.furtherBlankLines = e.containerState.furtherBlankLines || e.containerState.initialBlankLine, T(
      n,
      r,
      "listItemIndent",
      e.containerState.size + 1
    )(a);
  }
  function l(a) {
    return e.containerState.furtherBlankLines || !q(a) ? (e.containerState.furtherBlankLines = void 0, e.containerState.initialBlankLine = void 0, i(a)) : (e.containerState.furtherBlankLines = void 0, e.containerState.initialBlankLine = void 0, n.attempt($e, r, i)(a));
  }
  function i(a) {
    return e.containerState._closeFlow = !0, e.interrupt = void 0, T(
      n,
      n.attempt($, r, t),
      "linePrefix",
      e.parser.constructs.disable.null.includes("codeIndented") ? void 0 : 4
    )(a);
  }
}
function Ge(n, r, t) {
  const e = this;
  return T(
    n,
    u,
    "listItemIndent",
    e.containerState.size + 1
  );
  function u(l) {
    const i = e.events[e.events.length - 1];
    return i && i[1].type === "listItemIndent" && i[2].sliceSerialize(i[1], !0).length === e.containerState.size ? r(l) : t(l);
  }
}
function Je(n) {
  n.exit(this.containerState.type);
}
function Ke(n, r, t) {
  const e = this;
  return T(
    n,
    u,
    "listItemPrefixWhitespace",
    e.parser.constructs.disable.null.includes("codeIndented") ? void 0 : 4 + 1
  );
  function u(l) {
    const i = e.events[e.events.length - 1];
    return !q(l) && i && i[1].type === "listItemPrefixWhitespace" ? r(l) : t(l);
  }
}
const Gn = {
  name: "setextUnderline",
  tokenize: ve,
  resolveTo: Xe
};
function Xe(n, r) {
  let t = n.length, e, u, l;
  for (; t--; )
    if (n[t][0] === "enter") {
      if (n[t][1].type === "content") {
        e = t;
        break;
      }
      n[t][1].type === "paragraph" && (u = t);
    } else
      n[t][1].type === "content" && n.splice(t, 1), !l && n[t][1].type === "definition" && (l = t);
  const i = {
    type: "setextHeading",
    start: Object.assign({}, n[u][1].start),
    end: Object.assign({}, n[n.length - 1][1].end)
  };
  return n[u][1].type = "setextHeadingText", l ? (n.splice(u, 0, ["enter", i, r]), n.splice(l + 1, 0, ["exit", n[e][1], r]), n[e][1].end = Object.assign({}, n[l][1].end)) : n[e][1] = i, n.push(["exit", i, r]), n;
}
function ve(n, r, t) {
  const e = this;
  let u = e.events.length, l, i;
  for (; u--; )
    if (e.events[u][1].type !== "lineEnding" && e.events[u][1].type !== "linePrefix" && e.events[u][1].type !== "content") {
      i = e.events[u][1].type === "paragraph";
      break;
    }
  return a;
  function a(h) {
    return !e.parser.lazy[e.now().line] && (e.interrupt || i) ? (n.enter("setextHeadingLine"), n.enter("setextHeadingLineSequence"), l = h, c(h)) : t(h);
  }
  function c(h) {
    return h === l ? (n.consume(h), c) : (n.exit("setextHeadingLineSequence"), T(n, p, "lineSuffix")(h));
  }
  function p(h) {
    return h === null || C(h) ? (n.exit("setextHeadingLine"), r(h)) : t(h);
  }
}
const nr = {
  tokenize: tr
};
function tr(n) {
  const r = this, t = n.attempt(
    // Try to parse a blank line.
    Sn,
    e,
    // Try to parse initial flow (essentially, only code).
    n.attempt(
      this.parser.constructs.flowInitial,
      u,
      T(
        n,
        n.attempt(
          this.parser.constructs.flow,
          u,
          n.attempt(oe, u)
        ),
        "linePrefix"
      )
    )
  );
  return t;
  function e(l) {
    if (l === null) {
      n.consume(l);
      return;
    }
    return n.enter("lineEndingBlank"), n.consume(l), n.exit("lineEndingBlank"), r.currentConstruct = void 0, t;
  }
  function u(l) {
    if (l === null) {
      n.consume(l);
      return;
    }
    return n.enter("lineEnding"), n.consume(l), n.exit("lineEnding"), r.currentConstruct = void 0, t;
  }
}
const er = {
  resolveAll: st()
}, rr = ot("string"), ir = ot("text");
function ot(n) {
  return {
    tokenize: r,
    resolveAll: st(
      n === "text" ? ur : void 0
    )
  };
  function r(t) {
    const e = this, u = this.parser.constructs[n], l = t.attempt(u, i, a);
    return i;
    function i(h) {
      return p(h) ? l(h) : a(h);
    }
    function a(h) {
      if (h === null) {
        t.consume(h);
        return;
      }
      return t.enter("data"), t.consume(h), c;
    }
    function c(h) {
      return p(h) ? (t.exit("data"), l(h)) : (t.consume(h), c);
    }
    function p(h) {
      if (h === null)
        return !0;
      const x = u[h];
      let g = -1;
      if (x)
        for (; ++g < x.length; ) {
          const f = x[g];
          if (!f.previous || f.previous.call(e, e.previous))
            return !0;
        }
      return !1;
    }
  }
}
function st(n) {
  return r;
  function r(t, e) {
    let u = -1, l;
    for (; ++u <= t.length; )
      l === void 0 ? t[u] && t[u][1].type === "data" && (l = u, u++) : (!t[u] || t[u][1].type !== "data") && (u !== l + 2 && (t[l][1].end = t[u - 1][1].end, t.splice(l + 2, u - l - 2), u = l + 2), l = void 0);
    return n ? n(t, e) : t;
  }
}
function ur(n, r) {
  let t = 0;
  for (; ++t <= n.length; )
    if ((t === n.length || n[t][1].type === "lineEnding") && n[t - 1][1].type === "data") {
      const e = n[t - 1][1], u = r.sliceStream(e);
      let l = u.length, i = -1, a = 0, c;
      for (; l--; ) {
        const p = u[l];
        if (typeof p == "string") {
          for (i = p.length; p.charCodeAt(i - 1) === 32; )
            a++, i--;
          if (i)
            break;
          i = -1;
        } else if (p === -2)
          c = !0, a++;
        else if (p !== -1) {
          l++;
          break;
        }
      }
      if (a) {
        const p = {
          type: t === n.length || c || a < 2 ? "lineSuffix" : "hardBreakTrailing",
          start: {
            line: e.end.line,
            column: e.end.column - a,
            offset: e.end.offset - a,
            _index: e.start._index + l,
            _bufferIndex: l ? i : e.start._bufferIndex + i
          },
          end: Object.assign({}, e.end)
        };
        e.end = Object.assign({}, p.start), e.start.offset === e.end.offset ? Object.assign(e, p) : (n.splice(
          t,
          0,
          ["enter", p, r],
          ["exit", p, r]
        ), t += 2);
      }
      t++;
    }
  return n;
}
function lr(n, r, t) {
  let e = Object.assign(
    t ? Object.assign({}, t) : {
      line: 1,
      column: 1,
      offset: 0
    },
    {
      _index: 0,
      _bufferIndex: -1
    }
  );
  const u = {}, l = [];
  let i = [], a = [];
  const c = {
    consume: _,
    enter: F,
    exit: L,
    attempt: P(O),
    check: P(d),
    interrupt: P(d, {
      interrupt: !0
    })
  }, p = {
    previous: null,
    code: null,
    containerState: {},
    events: [],
    parser: n,
    sliceStream: f,
    sliceSerialize: g,
    now: k,
    defineSkip: B,
    write: x
  };
  let h = r.tokenize.call(p, c);
  return r.resolveAll && l.push(r), p;
  function x(S) {
    return i = Z(i, S), D(), i[i.length - 1] !== null ? [] : (R(r, 0), p.events = Ln(l, p.events, p), p.events);
  }
  function g(S, E) {
    return or(f(S), E);
  }
  function f(S) {
    return ar(i, S);
  }
  function k() {
    return Object.assign({}, e);
  }
  function B(S) {
    u[S.line] = S.column, V();
  }
  function D() {
    let S;
    for (; e._index < i.length; ) {
      const E = i[e._index];
      if (typeof E == "string")
        for (S = e._index, e._bufferIndex < 0 && (e._bufferIndex = 0); e._index === S && e._bufferIndex < E.length; )
          y(E.charCodeAt(e._bufferIndex));
      else
        y(E);
    }
  }
  function y(S) {
    h = h(S);
  }
  function _(S) {
    C(S) ? (e.line++, e.column = 1, e.offset += S === -3 ? 2 : 1, V()) : S !== -1 && (e.column++, e.offset++), e._bufferIndex < 0 ? e._index++ : (e._bufferIndex++, e._bufferIndex === i[e._index].length && (e._bufferIndex = -1, e._index++)), p.previous = S;
  }
  function F(S, E) {
    const A = E || {};
    return A.type = S, A.start = k(), p.events.push(["enter", A, p]), a.push(A), A;
  }
  function L(S) {
    const E = a.pop();
    return E.end = k(), p.events.push(["exit", E, p]), E;
  }
  function O(S, E) {
    R(S, E.from);
  }
  function d(S, E) {
    E.restore();
  }
  function P(S, E) {
    return A;
    function A(Q, G, nn) {
      let J, W, U, H;
      return Array.isArray(Q) ? (
        /* c8 ignore next 1 */
        o(Q)
      ) : "tokenize" in Q ? o([Q]) : s(Q);
      function s(N) {
        return K;
        function K(ln) {
          const pn = ln !== null && N[ln], mn = ln !== null && N.null, Fn = [
            // To do: add more extension tests.
            /* c8 ignore next 2 */
            ...Array.isArray(pn) ? pn : pn ? [pn] : [],
            ...Array.isArray(mn) ? mn : mn ? [mn] : []
          ];
          return o(Fn)(ln);
        }
      }
      function o(N) {
        return J = N, W = 0, N.length === 0 ? nn : cn(N[W]);
      }
      function cn(N) {
        return K;
        function K(ln) {
          return H = j(), U = N, N.partial || (p.currentConstruct = N), N.name && p.parser.constructs.disable.null.includes(N.name) ? hn() : N.tokenize.call(
            // If we do have fields, create an object w/ `context` as its
            // prototype.
            // This allows a “live binding”, which is needed for `interrupt`.
            E ? Object.assign(Object.create(p), E) : p,
            c,
            xn,
            hn
          )(ln);
        }
      }
      function xn(N) {
        return S(U, H), G;
      }
      function hn(N) {
        return H.restore(), ++W < J.length ? cn(J[W]) : nn;
      }
    }
  }
  function R(S, E) {
    S.resolveAll && !l.includes(S) && l.push(S), S.resolve && en(
      p.events,
      E,
      p.events.length - E,
      S.resolve(p.events.slice(E), p)
    ), S.resolveTo && (p.events = S.resolveTo(p.events, p));
  }
  function j() {
    const S = k(), E = p.previous, A = p.currentConstruct, Q = p.events.length, G = Array.from(a);
    return {
      restore: nn,
      from: Q
    };
    function nn() {
      e = S, p.previous = E, p.currentConstruct = A, p.events.length = Q, a = G, V();
    }
  }
  function V() {
    e.line in u && e.column < 2 && (e.column = u[e.line], e.offset += u[e.line] - 1);
  }
}
function ar(n, r) {
  const t = r.start._index, e = r.start._bufferIndex, u = r.end._index, l = r.end._bufferIndex;
  let i;
  return t === u ? i = [n[t].slice(e, l)] : (i = n.slice(t, u), e > -1 && (i[0] = i[0].slice(e)), l > 0 && i.push(n[u].slice(0, l))), i;
}
function or(n, r) {
  let t = -1;
  const e = [];
  let u;
  for (; ++t < n.length; ) {
    const l = n[t];
    let i;
    if (typeof l == "string")
      i = l;
    else
      switch (l) {
        case -5: {
          i = "\r";
          break;
        }
        case -4: {
          i = `
`;
          break;
        }
        case -3: {
          i = `\r
`;
          break;
        }
        case -2: {
          i = r ? " " : "	";
          break;
        }
        case -1: {
          if (!r && u)
            continue;
          i = " ";
          break;
        }
        default:
          i = String.fromCharCode(l);
      }
    u = l === -2, e.push(i);
  }
  return e.join("");
}
const sr = {
  [42]: $,
  [43]: $,
  [45]: $,
  [48]: $,
  [49]: $,
  [50]: $,
  [51]: $,
  [52]: $,
  [53]: $,
  [54]: $,
  [55]: $,
  [56]: $,
  [57]: $,
  [62]: tt
}, cr = {
  [91]: me
}, hr = {
  [-2]: wn,
  [-1]: wn,
  [32]: wn
}, pr = {
  [35]: be,
  [42]: bn,
  [45]: [Gn, bn],
  [60]: Ee,
  [61]: Gn,
  [95]: bn,
  [96]: Zn,
  [126]: Zn
}, mr = {
  [38]: rt,
  [92]: et
}, fr = {
  [-5]: Cn,
  [-4]: Cn,
  [-3]: Cn,
  [33]: qe,
  [38]: rt,
  [42]: In,
  [60]: [Ut, Ie],
  [91]: Ne,
  [92]: [ke, et],
  [93]: Dn,
  [95]: In,
  [96]: re
}, xr = {
  null: [In, er]
}, gr = {
  null: [42, 95]
}, kr = {
  null: []
}, dr = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  attentionMarkers: gr,
  contentInitial: cr,
  disable: kr,
  document: sr,
  flow: pr,
  flowInitial: hr,
  insideSpan: xr,
  string: mr,
  text: fr
}, Symbol.toStringTag, { value: "Module" }));
function br(n = {}) {
  const r = Bt(
    // @ts-expect-error Same as above.
    [dr].concat(n.extensions || [])
  ), t = {
    defined: [],
    lazy: {},
    constructs: r,
    content: e(jt),
    document: e(Ht),
    flow: e(nr),
    string: e(rr),
    text: e(ir)
  };
  return t;
  function e(u) {
    return l;
    function l(i) {
      return lr(t, u, i);
    }
  }
}
const Jn = /[\0\t\n\r]/g;
function yr() {
  let n = 1, r = "", t = !0, e;
  return u;
  function u(l, i, a) {
    const c = [];
    let p, h, x, g, f;
    for (l = r + l.toString(i), x = 0, r = "", t && (l.charCodeAt(0) === 65279 && x++, t = void 0); x < l.length; ) {
      if (Jn.lastIndex = x, p = Jn.exec(l), g = p && p.index !== void 0 ? p.index : l.length, f = l.charCodeAt(g), !p) {
        r = l.slice(x);
        break;
      }
      if (f === 10 && x === g && e)
        c.push(-3), e = void 0;
      else
        switch (e && (c.push(-5), e = void 0), x < g && (c.push(l.slice(x, g)), n += g - x), f) {
          case 0: {
            c.push(65533), n++;
            break;
          }
          case 9: {
            for (h = Math.ceil(n / 4) * 4, c.push(-2); n++ < h; )
              c.push(-1);
            break;
          }
          case 10: {
            c.push(-4), n = 1;
            break;
          }
          default:
            e = !0, n = 1;
        }
      x = g + 1;
    }
    return a && (e && c.push(-5), r && c.push(r), c.push(null)), c;
  }
}
function Sr(n) {
  for (; !it(n); )
    ;
  return n;
}
function ct(n, r) {
  const t = Number.parseInt(n, r);
  return (
    // C0 except for HT, LF, FF, CR, space
    t < 9 || t === 11 || t > 13 && t < 32 || // Control character (DEL) of the basic block and C1 controls.
    t > 126 && t < 160 || // Lone high surrogates and low surrogates.
    t > 55295 && t < 57344 || // Noncharacters.
    t > 64975 && t < 65008 || (t & 65535) === 65535 || (t & 65535) === 65534 || // Out of range
    t > 1114111 ? "�" : String.fromCharCode(t)
  );
}
const Fr = /\\([!-/:-@[-`{-~])|&(#(?:\d{1,7}|x[\da-f]{1,6})|[\da-z]{1,31});/gi;
function Er(n) {
  return n.replace(Fr, wr);
}
function wr(n, r, t) {
  if (r)
    return r;
  if (t.charCodeAt(0) === 35) {
    const u = t.charCodeAt(1), l = u === 120 || u === 88;
    return ct(t.slice(l ? 2 : 1), l ? 16 : 10);
  }
  return On(t) || n;
}
function yn(n) {
  return !n || typeof n != "object" ? "" : "position" in n || "type" in n ? Kn(n.position) : "start" in n || "end" in n ? Kn(n) : "line" in n || "column" in n ? Tn(n) : "";
}
function Tn(n) {
  return Xn(n && n.line) + ":" + Xn(n && n.column);
}
function Kn(n) {
  return Tn(n && n.start) + "-" + Tn(n && n.end);
}
function Xn(n) {
  return n && typeof n == "number" ? n : 1;
}
const ht = {}.hasOwnProperty, pt = (
  /**
   * @type {(
   *   ((value: Value, encoding: Encoding, options?: Options | null | undefined) => Root) &
   *   ((value: Value, options?: Options | null | undefined) => Root)
   * )}
   */
  /**
   * @param {Value} value
   * @param {Encoding | Options | null | undefined} [encoding]
   * @param {Options | null | undefined} [options]
   * @returns {Root}
   */
  function(n, r, t) {
    return typeof r != "string" && (t = r, r = void 0), Cr(t)(
      Sr(
        // @ts-expect-error: micromark types need to accept `null`.
        br(t).document().write(yr()(n, r, !0))
      )
    );
  }
);
function Cr(n) {
  const r = {
    transforms: [],
    canContainEols: ["emphasis", "fragment", "heading", "paragraph", "strong"],
    enter: {
      autolink: a(jn),
      autolinkProtocol: S,
      autolinkEmail: S,
      atxHeading: a(_n),
      blockQuote: a(Fn),
      characterEscape: S,
      characterReference: S,
      codeFenced: a(Pn),
      codeFencedFenceInfo: c,
      codeFencedFenceMeta: c,
      codeIndented: a(Pn, c),
      codeText: a(kt, c),
      codeTextData: S,
      data: S,
      codeFlowValue: S,
      definition: a(dt),
      definitionDestinationString: c,
      definitionLabelString: c,
      definitionTitleString: c,
      emphasis: a(bt),
      hardBreakEscape: a(Mn),
      hardBreakTrailing: a(Mn),
      htmlFlow: a(Rn, c),
      htmlFlowData: S,
      htmlText: a(Rn, c),
      htmlTextData: S,
      image: a(yt),
      label: c,
      link: a(jn),
      listItem: a(St),
      listItemValue: k,
      listOrdered: a(qn, f),
      listUnordered: a(qn),
      paragraph: a(Ft),
      reference: hn,
      referenceString: c,
      resourceDestinationString: c,
      resourceTitleString: c,
      setextHeading: a(_n),
      strong: a(Et),
      thematicBreak: a(Ct)
    },
    exit: {
      atxHeading: h(),
      atxHeadingSequence: P,
      autolink: h(),
      autolinkEmail: mn,
      autolinkProtocol: pn,
      blockQuote: h(),
      characterEscapeValue: E,
      characterReferenceMarkerHexadecimal: K,
      characterReferenceMarkerNumeric: K,
      characterReferenceValue: ln,
      codeFenced: h(_),
      codeFencedFence: y,
      codeFencedFenceInfo: B,
      codeFencedFenceMeta: D,
      codeFlowValue: E,
      codeIndented: h(F),
      codeText: h(J),
      codeTextData: E,
      data: E,
      definition: h(),
      definitionDestinationString: d,
      definitionLabelString: L,
      definitionTitleString: O,
      emphasis: h(),
      hardBreakEscape: h(Q),
      hardBreakTrailing: h(Q),
      htmlFlow: h(G),
      htmlFlowData: E,
      htmlText: h(nn),
      htmlTextData: E,
      image: h(U),
      label: s,
      labelText: H,
      lineEnding: A,
      link: h(W),
      listItem: h(),
      listOrdered: h(),
      listUnordered: h(),
      paragraph: h(),
      referenceString: N,
      resourceDestinationString: o,
      resourceTitleString: cn,
      resource: xn,
      setextHeading: h(V),
      setextHeadingLineSequence: j,
      setextHeadingText: R,
      strong: h(),
      thematicBreak: h()
    }
  };
  mt(r, (n || {}).mdastExtensions || []);
  const t = {};
  return e;
  function e(m) {
    let b = {
      type: "root",
      children: []
    };
    const w = {
      stack: [b],
      tokenStack: [],
      config: r,
      enter: p,
      exit: x,
      buffer: c,
      resume: g,
      setData: l,
      getData: i
    }, z = [];
    let I = -1;
    for (; ++I < m.length; )
      if (m[I][1].type === "listOrdered" || m[I][1].type === "listUnordered")
        if (m[I][0] === "enter")
          z.push(I);
        else {
          const X = z.pop();
          I = u(m, X, I);
        }
    for (I = -1; ++I < m.length; ) {
      const X = r[m[I][0]];
      ht.call(X, m[I][1].type) && X[m[I][1].type].call(
        Object.assign(
          {
            sliceSerialize: m[I][2].sliceSerialize
          },
          w
        ),
        m[I][1]
      );
    }
    if (w.tokenStack.length > 0) {
      const X = w.tokenStack[w.tokenStack.length - 1];
      (X[1] || vn).call(w, void 0, X[0]);
    }
    for (b.position = {
      start: on(
        m.length > 0 ? m[0][1].start : {
          line: 1,
          column: 1,
          offset: 0
        }
      ),
      end: on(
        m.length > 0 ? m[m.length - 2][1].end : {
          line: 1,
          column: 1,
          offset: 0
        }
      )
    }, I = -1; ++I < r.transforms.length; )
      b = r.transforms[I](b) || b;
    return b;
  }
  function u(m, b, w) {
    let z = b - 1, I = -1, X = !1, an, rn, gn, kn;
    for (; ++z <= w; ) {
      const M = m[z];
      if (M[1].type === "listUnordered" || M[1].type === "listOrdered" || M[1].type === "blockQuote" ? (M[0] === "enter" ? I++ : I--, kn = void 0) : M[1].type === "lineEndingBlank" ? M[0] === "enter" && (an && !kn && !I && !gn && (gn = z), kn = void 0) : M[1].type === "linePrefix" || M[1].type === "listItemValue" || M[1].type === "listItemMarker" || M[1].type === "listItemPrefix" || M[1].type === "listItemPrefixWhitespace" || (kn = void 0), !I && M[0] === "enter" && M[1].type === "listItemPrefix" || I === -1 && M[0] === "exit" && (M[1].type === "listUnordered" || M[1].type === "listOrdered")) {
        if (an) {
          let En = z;
          for (rn = void 0; En--; ) {
            const un = m[En];
            if (un[1].type === "lineEnding" || un[1].type === "lineEndingBlank") {
              if (un[0] === "exit")
                continue;
              rn && (m[rn][1].type = "lineEndingBlank", X = !0), un[1].type = "lineEnding", rn = En;
            } else if (!(un[1].type === "linePrefix" || un[1].type === "blockQuotePrefix" || un[1].type === "blockQuotePrefixWhitespace" || un[1].type === "blockQuoteMarker" || un[1].type === "listItemIndent"))
              break;
          }
          gn && (!rn || gn < rn) && (an._spread = !0), an.end = Object.assign(
            {},
            rn ? m[rn][1].start : M[1].end
          ), m.splice(rn || z, 0, ["exit", an, M[2]]), z++, w++;
        }
        M[1].type === "listItemPrefix" && (an = {
          type: "listItem",
          // @ts-expect-error Patched
          _spread: !1,
          start: Object.assign({}, M[1].start)
        }, m.splice(z, 0, ["enter", an, M[2]]), z++, w++, gn = void 0, kn = !0);
      }
    }
    return m[b][1]._spread = X, w;
  }
  function l(m, b) {
    t[m] = b;
  }
  function i(m) {
    return t[m];
  }
  function a(m, b) {
    return w;
    function w(z) {
      p.call(this, m(z), z), b && b.call(this, z);
    }
  }
  function c() {
    this.stack.push({
      type: "fragment",
      children: []
    });
  }
  function p(m, b, w) {
    return this.stack[this.stack.length - 1].children.push(m), this.stack.push(m), this.tokenStack.push([b, w]), m.position = {
      start: on(b.start)
    }, m;
  }
  function h(m) {
    return b;
    function b(w) {
      m && m.call(this, w), x.call(this, w);
    }
  }
  function x(m, b) {
    const w = this.stack.pop(), z = this.tokenStack.pop();
    if (z)
      z[0].type !== m.type && (b ? b.call(this, m, z[0]) : (z[1] || vn).call(this, m, z[0]));
    else
      throw new Error(
        "Cannot close `" + m.type + "` (" + yn({
          start: m.start,
          end: m.end
        }) + "): it’s not open"
      );
    return w.position.end = on(m.end), w;
  }
  function g() {
    return Tt(this.stack.pop());
  }
  function f() {
    l("expectingFirstListItemValue", !0);
  }
  function k(m) {
    if (i("expectingFirstListItemValue")) {
      const b = this.stack[this.stack.length - 2];
      b.start = Number.parseInt(this.sliceSerialize(m), 10), l("expectingFirstListItemValue");
    }
  }
  function B() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.lang = m;
  }
  function D() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.meta = m;
  }
  function y() {
    i("flowCodeInside") || (this.buffer(), l("flowCodeInside", !0));
  }
  function _() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.value = m.replace(/^(\r?\n|\r)|(\r?\n|\r)$/g, ""), l("flowCodeInside");
  }
  function F() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.value = m.replace(/(\r?\n|\r)$/g, "");
  }
  function L(m) {
    const b = this.resume(), w = this.stack[this.stack.length - 1];
    w.label = b, w.identifier = fn(
      this.sliceSerialize(m)
    ).toLowerCase();
  }
  function O() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.title = m;
  }
  function d() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.url = m;
  }
  function P(m) {
    const b = this.stack[this.stack.length - 1];
    if (!b.depth) {
      const w = this.sliceSerialize(m).length;
      b.depth = w;
    }
  }
  function R() {
    l("setextHeadingSlurpLineEnding", !0);
  }
  function j(m) {
    const b = this.stack[this.stack.length - 1];
    b.depth = this.sliceSerialize(m).charCodeAt(0) === 61 ? 1 : 2;
  }
  function V() {
    l("setextHeadingSlurpLineEnding");
  }
  function S(m) {
    const b = this.stack[this.stack.length - 1];
    let w = b.children[b.children.length - 1];
    (!w || w.type !== "text") && (w = wt(), w.position = {
      start: on(m.start)
    }, b.children.push(w)), this.stack.push(w);
  }
  function E(m) {
    const b = this.stack.pop();
    b.value += this.sliceSerialize(m), b.position.end = on(m.end);
  }
  function A(m) {
    const b = this.stack[this.stack.length - 1];
    if (i("atHardBreak")) {
      const w = b.children[b.children.length - 1];
      w.position.end = on(m.end), l("atHardBreak");
      return;
    }
    !i("setextHeadingSlurpLineEnding") && r.canContainEols.includes(b.type) && (S.call(this, m), E.call(this, m));
  }
  function Q() {
    l("atHardBreak", !0);
  }
  function G() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.value = m;
  }
  function nn() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.value = m;
  }
  function J() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.value = m;
  }
  function W() {
    const m = this.stack[this.stack.length - 1];
    if (i("inReference")) {
      const b = i("referenceType") || "shortcut";
      m.type += "Reference", m.referenceType = b, delete m.url, delete m.title;
    } else
      delete m.identifier, delete m.label;
    l("referenceType");
  }
  function U() {
    const m = this.stack[this.stack.length - 1];
    if (i("inReference")) {
      const b = i("referenceType") || "shortcut";
      m.type += "Reference", m.referenceType = b, delete m.url, delete m.title;
    } else
      delete m.identifier, delete m.label;
    l("referenceType");
  }
  function H(m) {
    const b = this.sliceSerialize(m), w = this.stack[this.stack.length - 2];
    w.label = Er(b), w.identifier = fn(b).toLowerCase();
  }
  function s() {
    const m = this.stack[this.stack.length - 1], b = this.resume(), w = this.stack[this.stack.length - 1];
    if (l("inReference", !0), w.type === "link") {
      const z = m.children;
      w.children = z;
    } else
      w.alt = b;
  }
  function o() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.url = m;
  }
  function cn() {
    const m = this.resume(), b = this.stack[this.stack.length - 1];
    b.title = m;
  }
  function xn() {
    l("inReference");
  }
  function hn() {
    l("referenceType", "collapsed");
  }
  function N(m) {
    const b = this.resume(), w = this.stack[this.stack.length - 1];
    w.label = b, w.identifier = fn(
      this.sliceSerialize(m)
    ).toLowerCase(), l("referenceType", "full");
  }
  function K(m) {
    l("characterReferenceType", m.type);
  }
  function ln(m) {
    const b = this.sliceSerialize(m), w = i("characterReferenceType");
    let z;
    w ? (z = ct(
      b,
      w === "characterReferenceMarkerNumeric" ? 10 : 16
    ), l("characterReferenceType")) : z = On(b);
    const I = this.stack.pop();
    I.value += z, I.position.end = on(m.end);
  }
  function pn(m) {
    E.call(this, m);
    const b = this.stack[this.stack.length - 1];
    b.url = this.sliceSerialize(m);
  }
  function mn(m) {
    E.call(this, m);
    const b = this.stack[this.stack.length - 1];
    b.url = "mailto:" + this.sliceSerialize(m);
  }
  function Fn() {
    return {
      type: "blockquote",
      children: []
    };
  }
  function Pn() {
    return {
      type: "code",
      lang: null,
      meta: null,
      value: ""
    };
  }
  function kt() {
    return {
      type: "inlineCode",
      value: ""
    };
  }
  function dt() {
    return {
      type: "definition",
      identifier: "",
      label: null,
      title: null,
      url: ""
    };
  }
  function bt() {
    return {
      type: "emphasis",
      children: []
    };
  }
  function _n() {
    return {
      type: "heading",
      depth: void 0,
      children: []
    };
  }
  function Mn() {
    return {
      type: "break"
    };
  }
  function Rn() {
    return {
      type: "html",
      value: ""
    };
  }
  function yt() {
    return {
      type: "image",
      title: null,
      url: "",
      alt: null
    };
  }
  function jn() {
    return {
      type: "link",
      title: null,
      url: "",
      children: []
    };
  }
  function qn(m) {
    return {
      type: "list",
      ordered: m.type === "listOrdered",
      start: null,
      // @ts-expect-error Patched.
      spread: m._spread,
      children: []
    };
  }
  function St(m) {
    return {
      type: "listItem",
      // @ts-expect-error Patched.
      spread: m._spread,
      checked: null,
      children: []
    };
  }
  function Ft() {
    return {
      type: "paragraph",
      children: []
    };
  }
  function Et() {
    return {
      type: "strong",
      children: []
    };
  }
  function wt() {
    return {
      type: "text",
      value: ""
    };
  }
  function Ct() {
    return {
      type: "thematicBreak"
    };
  }
}
function on(n) {
  return {
    line: n.line,
    column: n.column,
    offset: n.offset
  };
}
function mt(n, r) {
  let t = -1;
  for (; ++t < r.length; ) {
    const e = r[t];
    Array.isArray(e) ? mt(n, e) : Ar(n, e);
  }
}
function Ar(n, r) {
  let t;
  for (t in r)
    if (ht.call(r, t)) {
      if (t === "canContainEols") {
        const e = r[t];
        e && n[t].push(...e);
      } else if (t === "transforms") {
        const e = r[t];
        e && n[t].push(...e);
      } else if (t === "enter" || t === "exit") {
        const e = r[t];
        e && Object.assign(n[t], e);
      }
    }
}
function vn(n, r) {
  throw n ? new Error(
    "Cannot close `" + n.type + "` (" + yn({
      start: n.start,
      end: n.end
    }) + "): a different token (`" + r.type + "`, " + yn({
      start: r.start,
      end: r.end
    }) + ") is open"
  ) : new Error(
    "Cannot close document, a token (`" + r.type + "`, " + yn({
      start: r.start,
      end: r.end
    }) + ") is still open"
  );
}
function zr(n) {
  const r = n.replace(/\n{2,}/g, `
`);
  return At(r);
}
function Ir(n) {
  const r = zr(n), { children: t } = pt(r), e = [[]];
  let u = 0;
  function l(i, a = "normal") {
    i.type === "text" ? i.value.split(`
`).forEach((p, h) => {
      h !== 0 && (u++, e.push([])), p.split(" ").forEach((x) => {
        x && e[u].push({ content: x, type: a });
      });
    }) : (i.type === "strong" || i.type === "emphasis") && i.children.forEach((c) => {
      l(c, i.type);
    });
  }
  return t.forEach((i) => {
    i.type === "paragraph" && i.children.forEach((a) => {
      l(a);
    });
  }), e;
}
function Tr(n) {
  const { children: r } = pt(n);
  function t(e) {
    return e.type === "text" ? e.value.replace(/\n/g, "<br/>") : e.type === "strong" ? `<strong>${e.children.map(t).join("")}</strong>` : e.type === "emphasis" ? `<em>${e.children.map(t).join("")}</em>` : e.type === "paragraph" ? `<p>${e.children.map(t).join("")}</p>` : `Unsupported markdown: ${e.type}`;
  }
  return r.map(t).join("");
}
function Br(n) {
  return Intl.Segmenter ? [...new Intl.Segmenter().segment(n)].map((r) => r.segment) : [...n];
}
function Lr(n, r) {
  const t = Br(r.content);
  return ft(n, [], t, r.type);
}
function ft(n, r, t, e) {
  if (t.length === 0)
    return [
      { content: r.join(""), type: e },
      { content: "", type: e }
    ];
  const [u, ...l] = t, i = [...r, u];
  return n([{ content: i.join(""), type: e }]) ? ft(n, i, l, e) : (r.length === 0 && u && (r.push(u), t.shift()), [
    { content: r.join(""), type: e },
    { content: t.join(""), type: e }
  ]);
}
function Or(n, r) {
  if (n.some(({ content: t }) => t.includes(`
`)))
    throw new Error("splitLineToFitWidth does not support newlines in the line");
  return Bn(n, r);
}
function Bn(n, r, t = [], e = []) {
  if (n.length === 0)
    return e.length > 0 && t.push(e), t.length > 0 ? t : [];
  let u = "";
  n[0].content === " " && (u = " ", n.shift());
  const l = n.shift() ?? { content: " ", type: "normal" }, i = [...e];
  if (u !== "" && i.push({ content: u, type: "normal" }), i.push(l), r(i))
    return Bn(n, r, t, i);
  if (e.length > 0)
    t.push(e), n.unshift(l);
  else if (l.content) {
    const [a, c] = Lr(r, l);
    t.push([a]), c.content && n.unshift(c);
  }
  return Bn(n, r, t);
}
function Dr(n, r) {
  r && n.attr("style", r);
}
function Pr(n, r, t, e, u = !1) {
  const l = n.append("foreignObject"), i = l.append("xhtml:div"), a = r.label, c = r.isNode ? "nodeLabel" : "edgeLabel";
  i.html(
    `
    <span class="${c} ${e}" ` + (r.labelStyle ? 'style="' + r.labelStyle + '"' : "") + ">" + a + "</span>"
  ), Dr(i, r.labelStyle), i.style("display", "table-cell"), i.style("white-space", "nowrap"), i.style("max-width", t + "px"), i.attr("xmlns", "http://www.w3.org/1999/xhtml"), u && i.attr("class", "labelBkg");
  let p = i.node().getBoundingClientRect();
  return p.width === t && (i.style("display", "table"), i.style("white-space", "break-spaces"), i.style("width", t + "px"), p = i.node().getBoundingClientRect()), l.style("width", p.width), l.style("height", p.height), l.node();
}
function xt(n, r, t) {
  return n.append("tspan").attr("class", "text-outer-tspan").attr("x", 0).attr("y", r * t - 0.1 + "em").attr("dy", t + "em");
}
function _r(n, r, t) {
  const e = n.append("text"), u = xt(e, 1, r);
  gt(u, t);
  const l = u.node().getComputedTextLength();
  return e.remove(), l;
}
function Mr(n, r, t, e = !1) {
  const l = r.append("g"), i = l.insert("rect").attr("class", "background"), a = l.append("text").attr("y", "-10.1");
  let c = 0;
  for (const p of t) {
    const h = (g) => _r(l, 1.1, g) <= n, x = h(p) ? [p] : Or(p, h);
    for (const g of x) {
      const f = xt(a, c, 1.1);
      gt(f, g), c++;
    }
  }
  if (e) {
    const p = a.node().getBBox(), h = 2;
    return i.attr("x", -h).attr("y", -h).attr("width", p.width + 2 * h).attr("height", p.height + 2 * h), l.node();
  } else
    return a.node();
}
function gt(n, r) {
  n.text(""), r.forEach((t, e) => {
    const u = n.append("tspan").attr("font-style", t.type === "emphasis" ? "italic" : "normal").attr("class", "text-inner-tspan").attr("font-weight", t.type === "strong" ? "bold" : "normal");
    e === 0 ? u.text(t.content) : u.text(" " + t.content);
  });
}
const jr = (n, r = "", {
  style: t = "",
  isTitle: e = !1,
  classes: u = "",
  useHtmlLabels: l = !0,
  isNode: i = !0,
  width: a = 200,
  addSvgBackground: c = !1
} = {}) => {
  if (zt.info("createText", r, t, e, u, l, i, c), l) {
    const p = Tr(r), h = {
      isNode: i,
      label: It(p).replace(
        /fa[blrs]?:fa-[\w-]+/g,
        (g) => `<i class='${g.replace(":", " ")}'></i>`
      ),
      labelStyle: t.replace("fill:", "color:")
    };
    return Pr(n, h, a, u, c);
  } else {
    const p = Ir(r);
    return Mr(a, n, p, c);
  }
};
export {
  jr as c
};
