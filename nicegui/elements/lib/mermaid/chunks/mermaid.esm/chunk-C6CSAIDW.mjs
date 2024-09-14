import {
  getLineFunctionsWithOffset,
  getSubGraphTitleMargins
} from "./chunk-KW7S66XI.mjs";
import {
  createText
} from "./chunk-YP6PVJQ3.mjs";
import {
  decodeEntities,
  utils_default
} from "./chunk-I7ZFS43C.mjs";
import {
  basis_default,
  common_default,
  evaluate,
  getConfig2 as getConfig,
  hasKatex,
  line_default,
  log,
  renderKatex,
  sanitizeText,
  select_default
} from "./chunk-DD37ZF33.mjs";
import {
  __name
} from "./chunk-DLQEHMXD.mjs";

// ../../node_modules/.pnpm/roughjs@4.6.6/node_modules/roughjs/bundled/rough.esm.js
function t(t2, e2, s2) {
  if (t2 && t2.length) {
    const [n2, o2] = e2, a2 = Math.PI / 180 * s2, h2 = Math.cos(a2), r2 = Math.sin(a2);
    for (const e3 of t2) {
      const [t3, s3] = e3;
      e3[0] = (t3 - n2) * h2 - (s3 - o2) * r2 + n2, e3[1] = (t3 - n2) * r2 + (s3 - o2) * h2 + o2;
    }
  }
}
__name(t, "t");
function e(t2, e2) {
  return t2[0] === e2[0] && t2[1] === e2[1];
}
__name(e, "e");
function s(s2, n2, o2, a2 = 1) {
  const h2 = o2, r2 = Math.max(n2, 0.1), i2 = s2[0] && s2[0][0] && "number" == typeof s2[0][0] ? [s2] : s2, c2 = [0, 0];
  if (h2) for (const e2 of i2) t(e2, c2, h2);
  const l2 = function(t2, s3, n3) {
    const o3 = [];
    for (const s4 of t2) {
      const t3 = [...s4];
      e(t3[0], t3[t3.length - 1]) || t3.push([t3[0][0], t3[0][1]]), t3.length > 2 && o3.push(t3);
    }
    const a3 = [];
    s3 = Math.max(s3, 0.1);
    const h3 = [];
    for (const t3 of o3) for (let e2 = 0; e2 < t3.length - 1; e2++) {
      const s4 = t3[e2], n4 = t3[e2 + 1];
      if (s4[1] !== n4[1]) {
        const t4 = Math.min(s4[1], n4[1]);
        h3.push({ ymin: t4, ymax: Math.max(s4[1], n4[1]), x: t4 === s4[1] ? s4[0] : n4[0], islope: (n4[0] - s4[0]) / (n4[1] - s4[1]) });
      }
    }
    if (h3.sort((t3, e2) => t3.ymin < e2.ymin ? -1 : t3.ymin > e2.ymin ? 1 : t3.x < e2.x ? -1 : t3.x > e2.x ? 1 : t3.ymax === e2.ymax ? 0 : (t3.ymax - e2.ymax) / Math.abs(t3.ymax - e2.ymax)), !h3.length) return a3;
    let r3 = [], i3 = h3[0].ymin, c3 = 0;
    for (; r3.length || h3.length; ) {
      if (h3.length) {
        let t3 = -1;
        for (let e2 = 0; e2 < h3.length && !(h3[e2].ymin > i3); e2++) t3 = e2;
        h3.splice(0, t3 + 1).forEach((t4) => {
          r3.push({ s: i3, edge: t4 });
        });
      }
      if (r3 = r3.filter((t3) => !(t3.edge.ymax <= i3)), r3.sort((t3, e2) => t3.edge.x === e2.edge.x ? 0 : (t3.edge.x - e2.edge.x) / Math.abs(t3.edge.x - e2.edge.x)), (1 !== n3 || c3 % s3 == 0) && r3.length > 1) for (let t3 = 0; t3 < r3.length; t3 += 2) {
        const e2 = t3 + 1;
        if (e2 >= r3.length) break;
        const s4 = r3[t3].edge, n4 = r3[e2].edge;
        a3.push([[Math.round(s4.x), i3], [Math.round(n4.x), i3]]);
      }
      i3 += n3, r3.forEach((t3) => {
        t3.edge.x = t3.edge.x + n3 * t3.edge.islope;
      }), c3++;
    }
    return a3;
  }(i2, r2, a2);
  if (h2) {
    for (const e2 of i2) t(e2, c2, -h2);
    !function(e2, s3, n3) {
      const o3 = [];
      e2.forEach((t2) => o3.push(...t2)), t(o3, s3, n3);
    }(l2, c2, -h2);
  }
  return l2;
}
__name(s, "s");
function n(t2, e2) {
  var n2;
  const o2 = e2.hachureAngle + 90;
  let a2 = e2.hachureGap;
  a2 < 0 && (a2 = 4 * e2.strokeWidth), a2 = Math.round(Math.max(a2, 0.1));
  let h2 = 1;
  return e2.roughness >= 1 && ((null === (n2 = e2.randomizer) || void 0 === n2 ? void 0 : n2.next()) || Math.random()) > 0.7 && (h2 = a2), s(t2, a2, o2, h2 || 1);
}
__name(n, "n");
var o = class {
  static {
    __name(this, "o");
  }
  constructor(t2) {
    this.helper = t2;
  }
  fillPolygons(t2, e2) {
    return this._fillPolygons(t2, e2);
  }
  _fillPolygons(t2, e2) {
    const s2 = n(t2, e2);
    return { type: "fillSketch", ops: this.renderLines(s2, e2) };
  }
  renderLines(t2, e2) {
    const s2 = [];
    for (const n2 of t2) s2.push(...this.helper.doubleLineOps(n2[0][0], n2[0][1], n2[1][0], n2[1][1], e2));
    return s2;
  }
};
function a(t2) {
  const e2 = t2[0], s2 = t2[1];
  return Math.sqrt(Math.pow(e2[0] - s2[0], 2) + Math.pow(e2[1] - s2[1], 2));
}
__name(a, "a");
var h = class extends o {
  static {
    __name(this, "h");
  }
  fillPolygons(t2, e2) {
    let s2 = e2.hachureGap;
    s2 < 0 && (s2 = 4 * e2.strokeWidth), s2 = Math.max(s2, 0.1);
    const o2 = n(t2, Object.assign({}, e2, { hachureGap: s2 })), h2 = Math.PI / 180 * e2.hachureAngle, r2 = [], i2 = 0.5 * s2 * Math.cos(h2), c2 = 0.5 * s2 * Math.sin(h2);
    for (const [t3, e3] of o2) a([t3, e3]) && r2.push([[t3[0] - i2, t3[1] + c2], [...e3]], [[t3[0] + i2, t3[1] - c2], [...e3]]);
    return { type: "fillSketch", ops: this.renderLines(r2, e2) };
  }
};
var r = class extends o {
  static {
    __name(this, "r");
  }
  fillPolygons(t2, e2) {
    const s2 = this._fillPolygons(t2, e2), n2 = Object.assign({}, e2, { hachureAngle: e2.hachureAngle + 90 }), o2 = this._fillPolygons(t2, n2);
    return s2.ops = s2.ops.concat(o2.ops), s2;
  }
};
var i = class {
  static {
    __name(this, "i");
  }
  constructor(t2) {
    this.helper = t2;
  }
  fillPolygons(t2, e2) {
    const s2 = n(t2, e2 = Object.assign({}, e2, { hachureAngle: 0 }));
    return this.dotsOnLines(s2, e2);
  }
  dotsOnLines(t2, e2) {
    const s2 = [];
    let n2 = e2.hachureGap;
    n2 < 0 && (n2 = 4 * e2.strokeWidth), n2 = Math.max(n2, 0.1);
    let o2 = e2.fillWeight;
    o2 < 0 && (o2 = e2.strokeWidth / 2);
    const h2 = n2 / 4;
    for (const r2 of t2) {
      const t3 = a(r2), i2 = t3 / n2, c2 = Math.ceil(i2) - 1, l2 = t3 - c2 * n2, u2 = (r2[0][0] + r2[1][0]) / 2 - n2 / 4, p2 = Math.min(r2[0][1], r2[1][1]);
      for (let t4 = 0; t4 < c2; t4++) {
        const a2 = p2 + l2 + t4 * n2, r3 = u2 - h2 + 2 * Math.random() * h2, i3 = a2 - h2 + 2 * Math.random() * h2, c3 = this.helper.ellipse(r3, i3, o2, o2, e2);
        s2.push(...c3.ops);
      }
    }
    return { type: "fillSketch", ops: s2 };
  }
};
var c = class {
  static {
    __name(this, "c");
  }
  constructor(t2) {
    this.helper = t2;
  }
  fillPolygons(t2, e2) {
    const s2 = n(t2, e2);
    return { type: "fillSketch", ops: this.dashedLine(s2, e2) };
  }
  dashedLine(t2, e2) {
    const s2 = e2.dashOffset < 0 ? e2.hachureGap < 0 ? 4 * e2.strokeWidth : e2.hachureGap : e2.dashOffset, n2 = e2.dashGap < 0 ? e2.hachureGap < 0 ? 4 * e2.strokeWidth : e2.hachureGap : e2.dashGap, o2 = [];
    return t2.forEach((t3) => {
      const h2 = a(t3), r2 = Math.floor(h2 / (s2 + n2)), i2 = (h2 + n2 - r2 * (s2 + n2)) / 2;
      let c2 = t3[0], l2 = t3[1];
      c2[0] > l2[0] && (c2 = t3[1], l2 = t3[0]);
      const u2 = Math.atan((l2[1] - c2[1]) / (l2[0] - c2[0]));
      for (let t4 = 0; t4 < r2; t4++) {
        const a2 = t4 * (s2 + n2), h3 = a2 + s2, r3 = [c2[0] + a2 * Math.cos(u2) + i2 * Math.cos(u2), c2[1] + a2 * Math.sin(u2) + i2 * Math.sin(u2)], l3 = [c2[0] + h3 * Math.cos(u2) + i2 * Math.cos(u2), c2[1] + h3 * Math.sin(u2) + i2 * Math.sin(u2)];
        o2.push(...this.helper.doubleLineOps(r3[0], r3[1], l3[0], l3[1], e2));
      }
    }), o2;
  }
};
var l = class {
  static {
    __name(this, "l");
  }
  constructor(t2) {
    this.helper = t2;
  }
  fillPolygons(t2, e2) {
    const s2 = e2.hachureGap < 0 ? 4 * e2.strokeWidth : e2.hachureGap, o2 = e2.zigzagOffset < 0 ? s2 : e2.zigzagOffset, a2 = n(t2, e2 = Object.assign({}, e2, { hachureGap: s2 + o2 }));
    return { type: "fillSketch", ops: this.zigzagLines(a2, o2, e2) };
  }
  zigzagLines(t2, e2, s2) {
    const n2 = [];
    return t2.forEach((t3) => {
      const o2 = a(t3), h2 = Math.round(o2 / (2 * e2));
      let r2 = t3[0], i2 = t3[1];
      r2[0] > i2[0] && (r2 = t3[1], i2 = t3[0]);
      const c2 = Math.atan((i2[1] - r2[1]) / (i2[0] - r2[0]));
      for (let t4 = 0; t4 < h2; t4++) {
        const o3 = 2 * t4 * e2, a2 = 2 * (t4 + 1) * e2, h3 = Math.sqrt(2 * Math.pow(e2, 2)), i3 = [r2[0] + o3 * Math.cos(c2), r2[1] + o3 * Math.sin(c2)], l2 = [r2[0] + a2 * Math.cos(c2), r2[1] + a2 * Math.sin(c2)], u2 = [i3[0] + h3 * Math.cos(c2 + Math.PI / 4), i3[1] + h3 * Math.sin(c2 + Math.PI / 4)];
        n2.push(...this.helper.doubleLineOps(i3[0], i3[1], u2[0], u2[1], s2), ...this.helper.doubleLineOps(u2[0], u2[1], l2[0], l2[1], s2));
      }
    }), n2;
  }
};
var u = {};
var p = class {
  static {
    __name(this, "p");
  }
  constructor(t2) {
    this.seed = t2;
  }
  next() {
    return this.seed ? (2 ** 31 - 1 & (this.seed = Math.imul(48271, this.seed))) / 2 ** 31 : Math.random();
  }
};
var f = 0;
var d = 1;
var g = 2;
var M = { A: 7, a: 7, C: 6, c: 6, H: 1, h: 1, L: 2, l: 2, M: 2, m: 2, Q: 4, q: 4, S: 4, s: 4, T: 2, t: 2, V: 1, v: 1, Z: 0, z: 0 };
function k(t2, e2) {
  return t2.type === e2;
}
__name(k, "k");
function b(t2) {
  const e2 = [], s2 = function(t3) {
    const e3 = new Array();
    for (; "" !== t3; ) if (t3.match(/^([ \t\r\n,]+)/)) t3 = t3.substr(RegExp.$1.length);
    else if (t3.match(/^([aAcChHlLmMqQsStTvVzZ])/)) e3[e3.length] = { type: f, text: RegExp.$1 }, t3 = t3.substr(RegExp.$1.length);
    else {
      if (!t3.match(/^(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)/)) return [];
      e3[e3.length] = { type: d, text: `${parseFloat(RegExp.$1)}` }, t3 = t3.substr(RegExp.$1.length);
    }
    return e3[e3.length] = { type: g, text: "" }, e3;
  }(t2);
  let n2 = "BOD", o2 = 0, a2 = s2[o2];
  for (; !k(a2, g); ) {
    let h2 = 0;
    const r2 = [];
    if ("BOD" === n2) {
      if ("M" !== a2.text && "m" !== a2.text) return b("M0,0" + t2);
      o2++, h2 = M[a2.text], n2 = a2.text;
    } else k(a2, d) ? h2 = M[n2] : (o2++, h2 = M[a2.text], n2 = a2.text);
    if (!(o2 + h2 < s2.length)) throw new Error("Path data ended short");
    for (let t3 = o2; t3 < o2 + h2; t3++) {
      const e3 = s2[t3];
      if (!k(e3, d)) throw new Error("Param not a number: " + n2 + "," + e3.text);
      r2[r2.length] = +e3.text;
    }
    if ("number" != typeof M[n2]) throw new Error("Bad segment: " + n2);
    {
      const t3 = { key: n2, data: r2 };
      e2.push(t3), o2 += h2, a2 = s2[o2], "M" === n2 && (n2 = "L"), "m" === n2 && (n2 = "l");
    }
  }
  return e2;
}
__name(b, "b");
function y(t2) {
  let e2 = 0, s2 = 0, n2 = 0, o2 = 0;
  const a2 = [];
  for (const { key: h2, data: r2 } of t2) switch (h2) {
    case "M":
      a2.push({ key: "M", data: [...r2] }), [e2, s2] = r2, [n2, o2] = r2;
      break;
    case "m":
      e2 += r2[0], s2 += r2[1], a2.push({ key: "M", data: [e2, s2] }), n2 = e2, o2 = s2;
      break;
    case "L":
      a2.push({ key: "L", data: [...r2] }), [e2, s2] = r2;
      break;
    case "l":
      e2 += r2[0], s2 += r2[1], a2.push({ key: "L", data: [e2, s2] });
      break;
    case "C":
      a2.push({ key: "C", data: [...r2] }), e2 = r2[4], s2 = r2[5];
      break;
    case "c": {
      const t3 = r2.map((t4, n3) => n3 % 2 ? t4 + s2 : t4 + e2);
      a2.push({ key: "C", data: t3 }), e2 = t3[4], s2 = t3[5];
      break;
    }
    case "Q":
      a2.push({ key: "Q", data: [...r2] }), e2 = r2[2], s2 = r2[3];
      break;
    case "q": {
      const t3 = r2.map((t4, n3) => n3 % 2 ? t4 + s2 : t4 + e2);
      a2.push({ key: "Q", data: t3 }), e2 = t3[2], s2 = t3[3];
      break;
    }
    case "A":
      a2.push({ key: "A", data: [...r2] }), e2 = r2[5], s2 = r2[6];
      break;
    case "a":
      e2 += r2[5], s2 += r2[6], a2.push({ key: "A", data: [r2[0], r2[1], r2[2], r2[3], r2[4], e2, s2] });
      break;
    case "H":
      a2.push({ key: "H", data: [...r2] }), e2 = r2[0];
      break;
    case "h":
      e2 += r2[0], a2.push({ key: "H", data: [e2] });
      break;
    case "V":
      a2.push({ key: "V", data: [...r2] }), s2 = r2[0];
      break;
    case "v":
      s2 += r2[0], a2.push({ key: "V", data: [s2] });
      break;
    case "S":
      a2.push({ key: "S", data: [...r2] }), e2 = r2[2], s2 = r2[3];
      break;
    case "s": {
      const t3 = r2.map((t4, n3) => n3 % 2 ? t4 + s2 : t4 + e2);
      a2.push({ key: "S", data: t3 }), e2 = t3[2], s2 = t3[3];
      break;
    }
    case "T":
      a2.push({ key: "T", data: [...r2] }), e2 = r2[0], s2 = r2[1];
      break;
    case "t":
      e2 += r2[0], s2 += r2[1], a2.push({ key: "T", data: [e2, s2] });
      break;
    case "Z":
    case "z":
      a2.push({ key: "Z", data: [] }), e2 = n2, s2 = o2;
  }
  return a2;
}
__name(y, "y");
function m(t2) {
  const e2 = [];
  let s2 = "", n2 = 0, o2 = 0, a2 = 0, h2 = 0, r2 = 0, i2 = 0;
  for (const { key: c2, data: l2 } of t2) {
    switch (c2) {
      case "M":
        e2.push({ key: "M", data: [...l2] }), [n2, o2] = l2, [a2, h2] = l2;
        break;
      case "C":
        e2.push({ key: "C", data: [...l2] }), n2 = l2[4], o2 = l2[5], r2 = l2[2], i2 = l2[3];
        break;
      case "L":
        e2.push({ key: "L", data: [...l2] }), [n2, o2] = l2;
        break;
      case "H":
        n2 = l2[0], e2.push({ key: "L", data: [n2, o2] });
        break;
      case "V":
        o2 = l2[0], e2.push({ key: "L", data: [n2, o2] });
        break;
      case "S": {
        let t3 = 0, a3 = 0;
        "C" === s2 || "S" === s2 ? (t3 = n2 + (n2 - r2), a3 = o2 + (o2 - i2)) : (t3 = n2, a3 = o2), e2.push({ key: "C", data: [t3, a3, ...l2] }), r2 = l2[0], i2 = l2[1], n2 = l2[2], o2 = l2[3];
        break;
      }
      case "T": {
        const [t3, a3] = l2;
        let h3 = 0, c3 = 0;
        "Q" === s2 || "T" === s2 ? (h3 = n2 + (n2 - r2), c3 = o2 + (o2 - i2)) : (h3 = n2, c3 = o2);
        const u2 = n2 + 2 * (h3 - n2) / 3, p2 = o2 + 2 * (c3 - o2) / 3, f2 = t3 + 2 * (h3 - t3) / 3, d2 = a3 + 2 * (c3 - a3) / 3;
        e2.push({ key: "C", data: [u2, p2, f2, d2, t3, a3] }), r2 = h3, i2 = c3, n2 = t3, o2 = a3;
        break;
      }
      case "Q": {
        const [t3, s3, a3, h3] = l2, c3 = n2 + 2 * (t3 - n2) / 3, u2 = o2 + 2 * (s3 - o2) / 3, p2 = a3 + 2 * (t3 - a3) / 3, f2 = h3 + 2 * (s3 - h3) / 3;
        e2.push({ key: "C", data: [c3, u2, p2, f2, a3, h3] }), r2 = t3, i2 = s3, n2 = a3, o2 = h3;
        break;
      }
      case "A": {
        const t3 = Math.abs(l2[0]), s3 = Math.abs(l2[1]), a3 = l2[2], h3 = l2[3], r3 = l2[4], i3 = l2[5], c3 = l2[6];
        if (0 === t3 || 0 === s3) e2.push({ key: "C", data: [n2, o2, i3, c3, i3, c3] }), n2 = i3, o2 = c3;
        else if (n2 !== i3 || o2 !== c3) {
          x(n2, o2, i3, c3, t3, s3, a3, h3, r3).forEach(function(t4) {
            e2.push({ key: "C", data: t4 });
          }), n2 = i3, o2 = c3;
        }
        break;
      }
      case "Z":
        e2.push({ key: "Z", data: [] }), n2 = a2, o2 = h2;
    }
    s2 = c2;
  }
  return e2;
}
__name(m, "m");
function w(t2, e2, s2) {
  return [t2 * Math.cos(s2) - e2 * Math.sin(s2), t2 * Math.sin(s2) + e2 * Math.cos(s2)];
}
__name(w, "w");
function x(t2, e2, s2, n2, o2, a2, h2, r2, i2, c2) {
  const l2 = (u2 = h2, Math.PI * u2 / 180);
  var u2;
  let p2 = [], f2 = 0, d2 = 0, g2 = 0, M2 = 0;
  if (c2) [f2, d2, g2, M2] = c2;
  else {
    [t2, e2] = w(t2, e2, -l2), [s2, n2] = w(s2, n2, -l2);
    const h3 = (t2 - s2) / 2, c3 = (e2 - n2) / 2;
    let u3 = h3 * h3 / (o2 * o2) + c3 * c3 / (a2 * a2);
    u3 > 1 && (u3 = Math.sqrt(u3), o2 *= u3, a2 *= u3);
    const p3 = o2 * o2, k3 = a2 * a2, b3 = p3 * k3 - p3 * c3 * c3 - k3 * h3 * h3, y3 = p3 * c3 * c3 + k3 * h3 * h3, m3 = (r2 === i2 ? -1 : 1) * Math.sqrt(Math.abs(b3 / y3));
    g2 = m3 * o2 * c3 / a2 + (t2 + s2) / 2, M2 = m3 * -a2 * h3 / o2 + (e2 + n2) / 2, f2 = Math.asin(parseFloat(((e2 - M2) / a2).toFixed(9))), d2 = Math.asin(parseFloat(((n2 - M2) / a2).toFixed(9))), t2 < g2 && (f2 = Math.PI - f2), s2 < g2 && (d2 = Math.PI - d2), f2 < 0 && (f2 = 2 * Math.PI + f2), d2 < 0 && (d2 = 2 * Math.PI + d2), i2 && f2 > d2 && (f2 -= 2 * Math.PI), !i2 && d2 > f2 && (d2 -= 2 * Math.PI);
  }
  let k2 = d2 - f2;
  if (Math.abs(k2) > 120 * Math.PI / 180) {
    const t3 = d2, e3 = s2, r3 = n2;
    d2 = i2 && d2 > f2 ? f2 + 120 * Math.PI / 180 * 1 : f2 + 120 * Math.PI / 180 * -1, p2 = x(s2 = g2 + o2 * Math.cos(d2), n2 = M2 + a2 * Math.sin(d2), e3, r3, o2, a2, h2, 0, i2, [d2, t3, g2, M2]);
  }
  k2 = d2 - f2;
  const b2 = Math.cos(f2), y2 = Math.sin(f2), m2 = Math.cos(d2), P2 = Math.sin(d2), v2 = Math.tan(k2 / 4), S2 = 4 / 3 * o2 * v2, O2 = 4 / 3 * a2 * v2, L2 = [t2, e2], T2 = [t2 + S2 * y2, e2 - O2 * b2], D2 = [s2 + S2 * P2, n2 - O2 * m2], A2 = [s2, n2];
  if (T2[0] = 2 * L2[0] - T2[0], T2[1] = 2 * L2[1] - T2[1], c2) return [T2, D2, A2].concat(p2);
  {
    p2 = [T2, D2, A2].concat(p2);
    const t3 = [];
    for (let e3 = 0; e3 < p2.length; e3 += 3) {
      const s3 = w(p2[e3][0], p2[e3][1], l2), n3 = w(p2[e3 + 1][0], p2[e3 + 1][1], l2), o3 = w(p2[e3 + 2][0], p2[e3 + 2][1], l2);
      t3.push([s3[0], s3[1], n3[0], n3[1], o3[0], o3[1]]);
    }
    return t3;
  }
}
__name(x, "x");
var P = { randOffset: /* @__PURE__ */ __name(function(t2, e2) {
  return G(t2, e2);
}, "randOffset"), randOffsetWithRange: /* @__PURE__ */ __name(function(t2, e2, s2) {
  return E(t2, e2, s2);
}, "randOffsetWithRange"), ellipse: /* @__PURE__ */ __name(function(t2, e2, s2, n2, o2) {
  const a2 = T(s2, n2, o2);
  return D(t2, e2, o2, a2).opset;
}, "ellipse"), doubleLineOps: /* @__PURE__ */ __name(function(t2, e2, s2, n2, o2) {
  return $(t2, e2, s2, n2, o2, true);
}, "doubleLineOps") };
function v(t2, e2, s2, n2, o2) {
  return { type: "path", ops: $(t2, e2, s2, n2, o2) };
}
__name(v, "v");
function S(t2, e2, s2) {
  const n2 = (t2 || []).length;
  if (n2 > 2) {
    const o2 = [];
    for (let e3 = 0; e3 < n2 - 1; e3++) o2.push(...$(t2[e3][0], t2[e3][1], t2[e3 + 1][0], t2[e3 + 1][1], s2));
    return e2 && o2.push(...$(t2[n2 - 1][0], t2[n2 - 1][1], t2[0][0], t2[0][1], s2)), { type: "path", ops: o2 };
  }
  return 2 === n2 ? v(t2[0][0], t2[0][1], t2[1][0], t2[1][1], s2) : { type: "path", ops: [] };
}
__name(S, "S");
function O(t2, e2, s2, n2, o2) {
  return function(t3, e3) {
    return S(t3, true, e3);
  }([[t2, e2], [t2 + s2, e2], [t2 + s2, e2 + n2], [t2, e2 + n2]], o2);
}
__name(O, "O");
function L(t2, e2) {
  if (t2.length) {
    const s2 = "number" == typeof t2[0][0] ? [t2] : t2, n2 = j(s2[0], 1 * (1 + 0.2 * e2.roughness), e2), o2 = e2.disableMultiStroke ? [] : j(s2[0], 1.5 * (1 + 0.22 * e2.roughness), z(e2));
    for (let t3 = 1; t3 < s2.length; t3++) {
      const a2 = s2[t3];
      if (a2.length) {
        const t4 = j(a2, 1 * (1 + 0.2 * e2.roughness), e2), s3 = e2.disableMultiStroke ? [] : j(a2, 1.5 * (1 + 0.22 * e2.roughness), z(e2));
        for (const e3 of t4) "move" !== e3.op && n2.push(e3);
        for (const t5 of s3) "move" !== t5.op && o2.push(t5);
      }
    }
    return { type: "path", ops: n2.concat(o2) };
  }
  return { type: "path", ops: [] };
}
__name(L, "L");
function T(t2, e2, s2) {
  const n2 = Math.sqrt(2 * Math.PI * Math.sqrt((Math.pow(t2 / 2, 2) + Math.pow(e2 / 2, 2)) / 2)), o2 = Math.ceil(Math.max(s2.curveStepCount, s2.curveStepCount / Math.sqrt(200) * n2)), a2 = 2 * Math.PI / o2;
  let h2 = Math.abs(t2 / 2), r2 = Math.abs(e2 / 2);
  const i2 = 1 - s2.curveFitting;
  return h2 += G(h2 * i2, s2), r2 += G(r2 * i2, s2), { increment: a2, rx: h2, ry: r2 };
}
__name(T, "T");
function D(t2, e2, s2, n2) {
  const [o2, a2] = F(n2.increment, t2, e2, n2.rx, n2.ry, 1, n2.increment * E(0.1, E(0.4, 1, s2), s2), s2);
  let h2 = q(o2, null, s2);
  if (!s2.disableMultiStroke && 0 !== s2.roughness) {
    const [o3] = F(n2.increment, t2, e2, n2.rx, n2.ry, 1.5, 0, s2), a3 = q(o3, null, s2);
    h2 = h2.concat(a3);
  }
  return { estimatedPoints: a2, opset: { type: "path", ops: h2 } };
}
__name(D, "D");
function A(t2, e2, s2, n2, o2, a2, h2, r2, i2) {
  const c2 = t2, l2 = e2;
  let u2 = Math.abs(s2 / 2), p2 = Math.abs(n2 / 2);
  u2 += G(0.01 * u2, i2), p2 += G(0.01 * p2, i2);
  let f2 = o2, d2 = a2;
  for (; f2 < 0; ) f2 += 2 * Math.PI, d2 += 2 * Math.PI;
  d2 - f2 > 2 * Math.PI && (f2 = 0, d2 = 2 * Math.PI);
  const g2 = 2 * Math.PI / i2.curveStepCount, M2 = Math.min(g2 / 2, (d2 - f2) / 2), k2 = V(M2, c2, l2, u2, p2, f2, d2, 1, i2);
  if (!i2.disableMultiStroke) {
    const t3 = V(M2, c2, l2, u2, p2, f2, d2, 1.5, i2);
    k2.push(...t3);
  }
  return h2 && (r2 ? k2.push(...$(c2, l2, c2 + u2 * Math.cos(f2), l2 + p2 * Math.sin(f2), i2), ...$(c2, l2, c2 + u2 * Math.cos(d2), l2 + p2 * Math.sin(d2), i2)) : k2.push({ op: "lineTo", data: [c2, l2] }, { op: "lineTo", data: [c2 + u2 * Math.cos(f2), l2 + p2 * Math.sin(f2)] })), { type: "path", ops: k2 };
}
__name(A, "A");
function _(t2, e2) {
  const s2 = m(y(b(t2))), n2 = [];
  let o2 = [0, 0], a2 = [0, 0];
  for (const { key: t3, data: h2 } of s2) switch (t3) {
    case "M":
      a2 = [h2[0], h2[1]], o2 = [h2[0], h2[1]];
      break;
    case "L":
      n2.push(...$(a2[0], a2[1], h2[0], h2[1], e2)), a2 = [h2[0], h2[1]];
      break;
    case "C": {
      const [t4, s3, o3, r2, i2, c2] = h2;
      n2.push(...Z(t4, s3, o3, r2, i2, c2, a2, e2)), a2 = [i2, c2];
      break;
    }
    case "Z":
      n2.push(...$(a2[0], a2[1], o2[0], o2[1], e2)), a2 = [o2[0], o2[1]];
  }
  return { type: "path", ops: n2 };
}
__name(_, "_");
function I(t2, e2) {
  const s2 = [];
  for (const n2 of t2) if (n2.length) {
    const t3 = e2.maxRandomnessOffset || 0, o2 = n2.length;
    if (o2 > 2) {
      s2.push({ op: "move", data: [n2[0][0] + G(t3, e2), n2[0][1] + G(t3, e2)] });
      for (let a2 = 1; a2 < o2; a2++) s2.push({ op: "lineTo", data: [n2[a2][0] + G(t3, e2), n2[a2][1] + G(t3, e2)] });
    }
  }
  return { type: "fillPath", ops: s2 };
}
__name(I, "I");
function C(t2, e2) {
  return function(t3, e3) {
    let s2 = t3.fillStyle || "hachure";
    if (!u[s2]) switch (s2) {
      case "zigzag":
        u[s2] || (u[s2] = new h(e3));
        break;
      case "cross-hatch":
        u[s2] || (u[s2] = new r(e3));
        break;
      case "dots":
        u[s2] || (u[s2] = new i(e3));
        break;
      case "dashed":
        u[s2] || (u[s2] = new c(e3));
        break;
      case "zigzag-line":
        u[s2] || (u[s2] = new l(e3));
        break;
      default:
        s2 = "hachure", u[s2] || (u[s2] = new o(e3));
    }
    return u[s2];
  }(e2, P).fillPolygons(t2, e2);
}
__name(C, "C");
function z(t2) {
  const e2 = Object.assign({}, t2);
  return e2.randomizer = void 0, t2.seed && (e2.seed = t2.seed + 1), e2;
}
__name(z, "z");
function W(t2) {
  return t2.randomizer || (t2.randomizer = new p(t2.seed || 0)), t2.randomizer.next();
}
__name(W, "W");
function E(t2, e2, s2, n2 = 1) {
  return s2.roughness * n2 * (W(s2) * (e2 - t2) + t2);
}
__name(E, "E");
function G(t2, e2, s2 = 1) {
  return E(-t2, t2, e2, s2);
}
__name(G, "G");
function $(t2, e2, s2, n2, o2, a2 = false) {
  const h2 = a2 ? o2.disableMultiStrokeFill : o2.disableMultiStroke, r2 = R(t2, e2, s2, n2, o2, true, false);
  if (h2) return r2;
  const i2 = R(t2, e2, s2, n2, o2, true, true);
  return r2.concat(i2);
}
__name($, "$");
function R(t2, e2, s2, n2, o2, a2, h2) {
  const r2 = Math.pow(t2 - s2, 2) + Math.pow(e2 - n2, 2), i2 = Math.sqrt(r2);
  let c2 = 1;
  c2 = i2 < 200 ? 1 : i2 > 500 ? 0.4 : -16668e-7 * i2 + 1.233334;
  let l2 = o2.maxRandomnessOffset || 0;
  l2 * l2 * 100 > r2 && (l2 = i2 / 10);
  const u2 = l2 / 2, p2 = 0.2 + 0.2 * W(o2);
  let f2 = o2.bowing * o2.maxRandomnessOffset * (n2 - e2) / 200, d2 = o2.bowing * o2.maxRandomnessOffset * (t2 - s2) / 200;
  f2 = G(f2, o2, c2), d2 = G(d2, o2, c2);
  const g2 = [], M2 = /* @__PURE__ */ __name(() => G(u2, o2, c2), "M"), k2 = /* @__PURE__ */ __name(() => G(l2, o2, c2), "k"), b2 = o2.preserveVertices;
  return a2 && (h2 ? g2.push({ op: "move", data: [t2 + (b2 ? 0 : M2()), e2 + (b2 ? 0 : M2())] }) : g2.push({ op: "move", data: [t2 + (b2 ? 0 : G(l2, o2, c2)), e2 + (b2 ? 0 : G(l2, o2, c2))] })), h2 ? g2.push({ op: "bcurveTo", data: [f2 + t2 + (s2 - t2) * p2 + M2(), d2 + e2 + (n2 - e2) * p2 + M2(), f2 + t2 + 2 * (s2 - t2) * p2 + M2(), d2 + e2 + 2 * (n2 - e2) * p2 + M2(), s2 + (b2 ? 0 : M2()), n2 + (b2 ? 0 : M2())] }) : g2.push({ op: "bcurveTo", data: [f2 + t2 + (s2 - t2) * p2 + k2(), d2 + e2 + (n2 - e2) * p2 + k2(), f2 + t2 + 2 * (s2 - t2) * p2 + k2(), d2 + e2 + 2 * (n2 - e2) * p2 + k2(), s2 + (b2 ? 0 : k2()), n2 + (b2 ? 0 : k2())] }), g2;
}
__name(R, "R");
function j(t2, e2, s2) {
  if (!t2.length) return [];
  const n2 = [];
  n2.push([t2[0][0] + G(e2, s2), t2[0][1] + G(e2, s2)]), n2.push([t2[0][0] + G(e2, s2), t2[0][1] + G(e2, s2)]);
  for (let o2 = 1; o2 < t2.length; o2++) n2.push([t2[o2][0] + G(e2, s2), t2[o2][1] + G(e2, s2)]), o2 === t2.length - 1 && n2.push([t2[o2][0] + G(e2, s2), t2[o2][1] + G(e2, s2)]);
  return q(n2, null, s2);
}
__name(j, "j");
function q(t2, e2, s2) {
  const n2 = t2.length, o2 = [];
  if (n2 > 3) {
    const a2 = [], h2 = 1 - s2.curveTightness;
    o2.push({ op: "move", data: [t2[1][0], t2[1][1]] });
    for (let e3 = 1; e3 + 2 < n2; e3++) {
      const s3 = t2[e3];
      a2[0] = [s3[0], s3[1]], a2[1] = [s3[0] + (h2 * t2[e3 + 1][0] - h2 * t2[e3 - 1][0]) / 6, s3[1] + (h2 * t2[e3 + 1][1] - h2 * t2[e3 - 1][1]) / 6], a2[2] = [t2[e3 + 1][0] + (h2 * t2[e3][0] - h2 * t2[e3 + 2][0]) / 6, t2[e3 + 1][1] + (h2 * t2[e3][1] - h2 * t2[e3 + 2][1]) / 6], a2[3] = [t2[e3 + 1][0], t2[e3 + 1][1]], o2.push({ op: "bcurveTo", data: [a2[1][0], a2[1][1], a2[2][0], a2[2][1], a2[3][0], a2[3][1]] });
    }
    if (e2 && 2 === e2.length) {
      const t3 = s2.maxRandomnessOffset;
      o2.push({ op: "lineTo", data: [e2[0] + G(t3, s2), e2[1] + G(t3, s2)] });
    }
  } else 3 === n2 ? (o2.push({ op: "move", data: [t2[1][0], t2[1][1]] }), o2.push({ op: "bcurveTo", data: [t2[1][0], t2[1][1], t2[2][0], t2[2][1], t2[2][0], t2[2][1]] })) : 2 === n2 && o2.push(...R(t2[0][0], t2[0][1], t2[1][0], t2[1][1], s2, true, true));
  return o2;
}
__name(q, "q");
function F(t2, e2, s2, n2, o2, a2, h2, r2) {
  const i2 = [], c2 = [];
  if (0 === r2.roughness) {
    t2 /= 4, c2.push([e2 + n2 * Math.cos(-t2), s2 + o2 * Math.sin(-t2)]);
    for (let a3 = 0; a3 <= 2 * Math.PI; a3 += t2) {
      const t3 = [e2 + n2 * Math.cos(a3), s2 + o2 * Math.sin(a3)];
      i2.push(t3), c2.push(t3);
    }
    c2.push([e2 + n2 * Math.cos(0), s2 + o2 * Math.sin(0)]), c2.push([e2 + n2 * Math.cos(t2), s2 + o2 * Math.sin(t2)]);
  } else {
    const l2 = G(0.5, r2) - Math.PI / 2;
    c2.push([G(a2, r2) + e2 + 0.9 * n2 * Math.cos(l2 - t2), G(a2, r2) + s2 + 0.9 * o2 * Math.sin(l2 - t2)]);
    const u2 = 2 * Math.PI + l2 - 0.01;
    for (let h3 = l2; h3 < u2; h3 += t2) {
      const t3 = [G(a2, r2) + e2 + n2 * Math.cos(h3), G(a2, r2) + s2 + o2 * Math.sin(h3)];
      i2.push(t3), c2.push(t3);
    }
    c2.push([G(a2, r2) + e2 + n2 * Math.cos(l2 + 2 * Math.PI + 0.5 * h2), G(a2, r2) + s2 + o2 * Math.sin(l2 + 2 * Math.PI + 0.5 * h2)]), c2.push([G(a2, r2) + e2 + 0.98 * n2 * Math.cos(l2 + h2), G(a2, r2) + s2 + 0.98 * o2 * Math.sin(l2 + h2)]), c2.push([G(a2, r2) + e2 + 0.9 * n2 * Math.cos(l2 + 0.5 * h2), G(a2, r2) + s2 + 0.9 * o2 * Math.sin(l2 + 0.5 * h2)]);
  }
  return [c2, i2];
}
__name(F, "F");
function V(t2, e2, s2, n2, o2, a2, h2, r2, i2) {
  const c2 = a2 + G(0.1, i2), l2 = [];
  l2.push([G(r2, i2) + e2 + 0.9 * n2 * Math.cos(c2 - t2), G(r2, i2) + s2 + 0.9 * o2 * Math.sin(c2 - t2)]);
  for (let a3 = c2; a3 <= h2; a3 += t2) l2.push([G(r2, i2) + e2 + n2 * Math.cos(a3), G(r2, i2) + s2 + o2 * Math.sin(a3)]);
  return l2.push([e2 + n2 * Math.cos(h2), s2 + o2 * Math.sin(h2)]), l2.push([e2 + n2 * Math.cos(h2), s2 + o2 * Math.sin(h2)]), q(l2, null, i2);
}
__name(V, "V");
function Z(t2, e2, s2, n2, o2, a2, h2, r2) {
  const i2 = [], c2 = [r2.maxRandomnessOffset || 1, (r2.maxRandomnessOffset || 1) + 0.3];
  let l2 = [0, 0];
  const u2 = r2.disableMultiStroke ? 1 : 2, p2 = r2.preserveVertices;
  for (let f2 = 0; f2 < u2; f2++) 0 === f2 ? i2.push({ op: "move", data: [h2[0], h2[1]] }) : i2.push({ op: "move", data: [h2[0] + (p2 ? 0 : G(c2[0], r2)), h2[1] + (p2 ? 0 : G(c2[0], r2))] }), l2 = p2 ? [o2, a2] : [o2 + G(c2[f2], r2), a2 + G(c2[f2], r2)], i2.push({ op: "bcurveTo", data: [t2 + G(c2[f2], r2), e2 + G(c2[f2], r2), s2 + G(c2[f2], r2), n2 + G(c2[f2], r2), l2[0], l2[1]] });
  return i2;
}
__name(Z, "Z");
function Q(t2) {
  return [...t2];
}
__name(Q, "Q");
function H(t2, e2 = 0) {
  const s2 = t2.length;
  if (s2 < 3) throw new Error("A curve must have at least three points.");
  const n2 = [];
  if (3 === s2) n2.push(Q(t2[0]), Q(t2[1]), Q(t2[2]), Q(t2[2]));
  else {
    const s3 = [];
    s3.push(t2[0], t2[0]);
    for (let e3 = 1; e3 < t2.length; e3++) s3.push(t2[e3]), e3 === t2.length - 1 && s3.push(t2[e3]);
    const o2 = [], a2 = 1 - e2;
    n2.push(Q(s3[0]));
    for (let t3 = 1; t3 + 2 < s3.length; t3++) {
      const e3 = s3[t3];
      o2[0] = [e3[0], e3[1]], o2[1] = [e3[0] + (a2 * s3[t3 + 1][0] - a2 * s3[t3 - 1][0]) / 6, e3[1] + (a2 * s3[t3 + 1][1] - a2 * s3[t3 - 1][1]) / 6], o2[2] = [s3[t3 + 1][0] + (a2 * s3[t3][0] - a2 * s3[t3 + 2][0]) / 6, s3[t3 + 1][1] + (a2 * s3[t3][1] - a2 * s3[t3 + 2][1]) / 6], o2[3] = [s3[t3 + 1][0], s3[t3 + 1][1]], n2.push(o2[1], o2[2], o2[3]);
    }
  }
  return n2;
}
__name(H, "H");
function N(t2, e2) {
  return Math.pow(t2[0] - e2[0], 2) + Math.pow(t2[1] - e2[1], 2);
}
__name(N, "N");
function B(t2, e2, s2) {
  const n2 = N(e2, s2);
  if (0 === n2) return N(t2, e2);
  let o2 = ((t2[0] - e2[0]) * (s2[0] - e2[0]) + (t2[1] - e2[1]) * (s2[1] - e2[1])) / n2;
  return o2 = Math.max(0, Math.min(1, o2)), N(t2, J(e2, s2, o2));
}
__name(B, "B");
function J(t2, e2, s2) {
  return [t2[0] + (e2[0] - t2[0]) * s2, t2[1] + (e2[1] - t2[1]) * s2];
}
__name(J, "J");
function K(t2, e2, s2, n2) {
  const o2 = n2 || [];
  if (function(t3, e3) {
    const s3 = t3[e3 + 0], n3 = t3[e3 + 1], o3 = t3[e3 + 2], a3 = t3[e3 + 3];
    let h3 = 3 * n3[0] - 2 * s3[0] - a3[0];
    h3 *= h3;
    let r2 = 3 * n3[1] - 2 * s3[1] - a3[1];
    r2 *= r2;
    let i2 = 3 * o3[0] - 2 * a3[0] - s3[0];
    i2 *= i2;
    let c2 = 3 * o3[1] - 2 * a3[1] - s3[1];
    return c2 *= c2, h3 < i2 && (h3 = i2), r2 < c2 && (r2 = c2), h3 + r2;
  }(t2, e2) < s2) {
    const s3 = t2[e2 + 0];
    if (o2.length) {
      (a2 = o2[o2.length - 1], h2 = s3, Math.sqrt(N(a2, h2))) > 1 && o2.push(s3);
    } else o2.push(s3);
    o2.push(t2[e2 + 3]);
  } else {
    const n3 = 0.5, a3 = t2[e2 + 0], h3 = t2[e2 + 1], r2 = t2[e2 + 2], i2 = t2[e2 + 3], c2 = J(a3, h3, n3), l2 = J(h3, r2, n3), u2 = J(r2, i2, n3), p2 = J(c2, l2, n3), f2 = J(l2, u2, n3), d2 = J(p2, f2, n3);
    K([a3, c2, p2, d2], 0, s2, o2), K([d2, f2, u2, i2], 0, s2, o2);
  }
  var a2, h2;
  return o2;
}
__name(K, "K");
function U(t2, e2) {
  return X(t2, 0, t2.length, e2);
}
__name(U, "U");
function X(t2, e2, s2, n2, o2) {
  const a2 = o2 || [], h2 = t2[e2], r2 = t2[s2 - 1];
  let i2 = 0, c2 = 1;
  for (let n3 = e2 + 1; n3 < s2 - 1; ++n3) {
    const e3 = B(t2[n3], h2, r2);
    e3 > i2 && (i2 = e3, c2 = n3);
  }
  return Math.sqrt(i2) > n2 ? (X(t2, e2, c2 + 1, n2, a2), X(t2, c2, s2, n2, a2)) : (a2.length || a2.push(h2), a2.push(r2)), a2;
}
__name(X, "X");
function Y(t2, e2 = 0.15, s2) {
  const n2 = [], o2 = (t2.length - 1) / 3;
  for (let s3 = 0; s3 < o2; s3++) {
    K(t2, 3 * s3, e2, n2);
  }
  return s2 && s2 > 0 ? X(n2, 0, n2.length, s2) : n2;
}
__name(Y, "Y");
var tt = "none";
var et = class {
  static {
    __name(this, "et");
  }
  constructor(t2) {
    this.defaultOptions = { maxRandomnessOffset: 2, roughness: 1, bowing: 1, stroke: "#000", strokeWidth: 1, curveTightness: 0, curveFitting: 0.95, curveStepCount: 9, fillStyle: "hachure", fillWeight: -1, hachureAngle: -41, hachureGap: -1, dashOffset: -1, dashGap: -1, zigzagOffset: -1, seed: 0, disableMultiStroke: false, disableMultiStrokeFill: false, preserveVertices: false, fillShapeRoughnessGain: 0.8 }, this.config = t2 || {}, this.config.options && (this.defaultOptions = this._o(this.config.options));
  }
  static newSeed() {
    return Math.floor(Math.random() * 2 ** 31);
  }
  _o(t2) {
    return t2 ? Object.assign({}, this.defaultOptions, t2) : this.defaultOptions;
  }
  _d(t2, e2, s2) {
    return { shape: t2, sets: e2 || [], options: s2 || this.defaultOptions };
  }
  line(t2, e2, s2, n2, o2) {
    const a2 = this._o(o2);
    return this._d("line", [v(t2, e2, s2, n2, a2)], a2);
  }
  rectangle(t2, e2, s2, n2, o2) {
    const a2 = this._o(o2), h2 = [], r2 = O(t2, e2, s2, n2, a2);
    if (a2.fill) {
      const o3 = [[t2, e2], [t2 + s2, e2], [t2 + s2, e2 + n2], [t2, e2 + n2]];
      "solid" === a2.fillStyle ? h2.push(I([o3], a2)) : h2.push(C([o3], a2));
    }
    return a2.stroke !== tt && h2.push(r2), this._d("rectangle", h2, a2);
  }
  ellipse(t2, e2, s2, n2, o2) {
    const a2 = this._o(o2), h2 = [], r2 = T(s2, n2, a2), i2 = D(t2, e2, a2, r2);
    if (a2.fill) if ("solid" === a2.fillStyle) {
      const s3 = D(t2, e2, a2, r2).opset;
      s3.type = "fillPath", h2.push(s3);
    } else h2.push(C([i2.estimatedPoints], a2));
    return a2.stroke !== tt && h2.push(i2.opset), this._d("ellipse", h2, a2);
  }
  circle(t2, e2, s2, n2) {
    const o2 = this.ellipse(t2, e2, s2, s2, n2);
    return o2.shape = "circle", o2;
  }
  linearPath(t2, e2) {
    const s2 = this._o(e2);
    return this._d("linearPath", [S(t2, false, s2)], s2);
  }
  arc(t2, e2, s2, n2, o2, a2, h2 = false, r2) {
    const i2 = this._o(r2), c2 = [], l2 = A(t2, e2, s2, n2, o2, a2, h2, true, i2);
    if (h2 && i2.fill) if ("solid" === i2.fillStyle) {
      const h3 = Object.assign({}, i2);
      h3.disableMultiStroke = true;
      const r3 = A(t2, e2, s2, n2, o2, a2, true, false, h3);
      r3.type = "fillPath", c2.push(r3);
    } else c2.push(function(t3, e3, s3, n3, o3, a3, h3) {
      const r3 = t3, i3 = e3;
      let c3 = Math.abs(s3 / 2), l3 = Math.abs(n3 / 2);
      c3 += G(0.01 * c3, h3), l3 += G(0.01 * l3, h3);
      let u2 = o3, p2 = a3;
      for (; u2 < 0; ) u2 += 2 * Math.PI, p2 += 2 * Math.PI;
      p2 - u2 > 2 * Math.PI && (u2 = 0, p2 = 2 * Math.PI);
      const f2 = (p2 - u2) / h3.curveStepCount, d2 = [];
      for (let t4 = u2; t4 <= p2; t4 += f2) d2.push([r3 + c3 * Math.cos(t4), i3 + l3 * Math.sin(t4)]);
      return d2.push([r3 + c3 * Math.cos(p2), i3 + l3 * Math.sin(p2)]), d2.push([r3, i3]), C([d2], h3);
    }(t2, e2, s2, n2, o2, a2, i2));
    return i2.stroke !== tt && c2.push(l2), this._d("arc", c2, i2);
  }
  curve(t2, e2) {
    const s2 = this._o(e2), n2 = [], o2 = L(t2, s2);
    if (s2.fill && s2.fill !== tt) if ("solid" === s2.fillStyle) {
      const e3 = L(t2, Object.assign(Object.assign({}, s2), { disableMultiStroke: true, roughness: s2.roughness ? s2.roughness + s2.fillShapeRoughnessGain : 0 }));
      n2.push({ type: "fillPath", ops: this._mergedShape(e3.ops) });
    } else {
      const e3 = [], o3 = t2;
      if (o3.length) {
        const t3 = "number" == typeof o3[0][0] ? [o3] : o3;
        for (const n3 of t3) n3.length < 3 ? e3.push(...n3) : 3 === n3.length ? e3.push(...Y(H([n3[0], n3[0], n3[1], n3[2]]), 10, (1 + s2.roughness) / 2)) : e3.push(...Y(H(n3), 10, (1 + s2.roughness) / 2));
      }
      e3.length && n2.push(C([e3], s2));
    }
    return s2.stroke !== tt && n2.push(o2), this._d("curve", n2, s2);
  }
  polygon(t2, e2) {
    const s2 = this._o(e2), n2 = [], o2 = S(t2, true, s2);
    return s2.fill && ("solid" === s2.fillStyle ? n2.push(I([t2], s2)) : n2.push(C([t2], s2))), s2.stroke !== tt && n2.push(o2), this._d("polygon", n2, s2);
  }
  path(t2, e2) {
    const s2 = this._o(e2), n2 = [];
    if (!t2) return this._d("path", n2, s2);
    t2 = (t2 || "").replace(/\n/g, " ").replace(/(-\s)/g, "-").replace("/(ss)/g", " ");
    const o2 = s2.fill && "transparent" !== s2.fill && s2.fill !== tt, a2 = s2.stroke !== tt, h2 = !!(s2.simplification && s2.simplification < 1), r2 = function(t3, e3, s3) {
      const n3 = m(y(b(t3))), o3 = [];
      let a3 = [], h3 = [0, 0], r3 = [];
      const i3 = /* @__PURE__ */ __name(() => {
        r3.length >= 4 && a3.push(...Y(r3, e3)), r3 = [];
      }, "i"), c2 = /* @__PURE__ */ __name(() => {
        i3(), a3.length && (o3.push(a3), a3 = []);
      }, "c");
      for (const { key: t4, data: e4 } of n3) switch (t4) {
        case "M":
          c2(), h3 = [e4[0], e4[1]], a3.push(h3);
          break;
        case "L":
          i3(), a3.push([e4[0], e4[1]]);
          break;
        case "C":
          if (!r3.length) {
            const t5 = a3.length ? a3[a3.length - 1] : h3;
            r3.push([t5[0], t5[1]]);
          }
          r3.push([e4[0], e4[1]]), r3.push([e4[2], e4[3]]), r3.push([e4[4], e4[5]]);
          break;
        case "Z":
          i3(), a3.push([h3[0], h3[1]]);
      }
      if (c2(), !s3) return o3;
      const l2 = [];
      for (const t4 of o3) {
        const e4 = U(t4, s3);
        e4.length && l2.push(e4);
      }
      return l2;
    }(t2, 1, h2 ? 4 - 4 * (s2.simplification || 1) : (1 + s2.roughness) / 2), i2 = _(t2, s2);
    if (o2) if ("solid" === s2.fillStyle) if (1 === r2.length) {
      const e3 = _(t2, Object.assign(Object.assign({}, s2), { disableMultiStroke: true, roughness: s2.roughness ? s2.roughness + s2.fillShapeRoughnessGain : 0 }));
      n2.push({ type: "fillPath", ops: this._mergedShape(e3.ops) });
    } else n2.push(I(r2, s2));
    else n2.push(C(r2, s2));
    return a2 && (h2 ? r2.forEach((t3) => {
      n2.push(S(t3, false, s2));
    }) : n2.push(i2)), this._d("path", n2, s2);
  }
  opsToPath(t2, e2) {
    let s2 = "";
    for (const n2 of t2.ops) {
      const t3 = "number" == typeof e2 && e2 >= 0 ? n2.data.map((t4) => +t4.toFixed(e2)) : n2.data;
      switch (n2.op) {
        case "move":
          s2 += `M${t3[0]} ${t3[1]} `;
          break;
        case "bcurveTo":
          s2 += `C${t3[0]} ${t3[1]}, ${t3[2]} ${t3[3]}, ${t3[4]} ${t3[5]} `;
          break;
        case "lineTo":
          s2 += `L${t3[0]} ${t3[1]} `;
      }
    }
    return s2.trim();
  }
  toPaths(t2) {
    const e2 = t2.sets || [], s2 = t2.options || this.defaultOptions, n2 = [];
    for (const t3 of e2) {
      let e3 = null;
      switch (t3.type) {
        case "path":
          e3 = { d: this.opsToPath(t3), stroke: s2.stroke, strokeWidth: s2.strokeWidth, fill: tt };
          break;
        case "fillPath":
          e3 = { d: this.opsToPath(t3), stroke: tt, strokeWidth: 0, fill: s2.fill || tt };
          break;
        case "fillSketch":
          e3 = this.fillSketch(t3, s2);
      }
      e3 && n2.push(e3);
    }
    return n2;
  }
  fillSketch(t2, e2) {
    let s2 = e2.fillWeight;
    return s2 < 0 && (s2 = e2.strokeWidth / 2), { d: this.opsToPath(t2), stroke: e2.fill || tt, strokeWidth: s2, fill: tt };
  }
  _mergedShape(t2) {
    return t2.filter((t3, e2) => 0 === e2 || "move" !== t3.op);
  }
};
var st = class {
  static {
    __name(this, "st");
  }
  constructor(t2, e2) {
    this.canvas = t2, this.ctx = this.canvas.getContext("2d"), this.gen = new et(e2);
  }
  draw(t2) {
    const e2 = t2.sets || [], s2 = t2.options || this.getDefaultOptions(), n2 = this.ctx, o2 = t2.options.fixedDecimalPlaceDigits;
    for (const a2 of e2) switch (a2.type) {
      case "path":
        n2.save(), n2.strokeStyle = "none" === s2.stroke ? "transparent" : s2.stroke, n2.lineWidth = s2.strokeWidth, s2.strokeLineDash && n2.setLineDash(s2.strokeLineDash), s2.strokeLineDashOffset && (n2.lineDashOffset = s2.strokeLineDashOffset), this._drawToContext(n2, a2, o2), n2.restore();
        break;
      case "fillPath": {
        n2.save(), n2.fillStyle = s2.fill || "";
        const e3 = "curve" === t2.shape || "polygon" === t2.shape || "path" === t2.shape ? "evenodd" : "nonzero";
        this._drawToContext(n2, a2, o2, e3), n2.restore();
        break;
      }
      case "fillSketch":
        this.fillSketch(n2, a2, s2);
    }
  }
  fillSketch(t2, e2, s2) {
    let n2 = s2.fillWeight;
    n2 < 0 && (n2 = s2.strokeWidth / 2), t2.save(), s2.fillLineDash && t2.setLineDash(s2.fillLineDash), s2.fillLineDashOffset && (t2.lineDashOffset = s2.fillLineDashOffset), t2.strokeStyle = s2.fill || "", t2.lineWidth = n2, this._drawToContext(t2, e2, s2.fixedDecimalPlaceDigits), t2.restore();
  }
  _drawToContext(t2, e2, s2, n2 = "nonzero") {
    t2.beginPath();
    for (const n3 of e2.ops) {
      const e3 = "number" == typeof s2 && s2 >= 0 ? n3.data.map((t3) => +t3.toFixed(s2)) : n3.data;
      switch (n3.op) {
        case "move":
          t2.moveTo(e3[0], e3[1]);
          break;
        case "bcurveTo":
          t2.bezierCurveTo(e3[0], e3[1], e3[2], e3[3], e3[4], e3[5]);
          break;
        case "lineTo":
          t2.lineTo(e3[0], e3[1]);
      }
    }
    "fillPath" === e2.type ? t2.fill(n2) : t2.stroke();
  }
  get generator() {
    return this.gen;
  }
  getDefaultOptions() {
    return this.gen.defaultOptions;
  }
  line(t2, e2, s2, n2, o2) {
    const a2 = this.gen.line(t2, e2, s2, n2, o2);
    return this.draw(a2), a2;
  }
  rectangle(t2, e2, s2, n2, o2) {
    const a2 = this.gen.rectangle(t2, e2, s2, n2, o2);
    return this.draw(a2), a2;
  }
  ellipse(t2, e2, s2, n2, o2) {
    const a2 = this.gen.ellipse(t2, e2, s2, n2, o2);
    return this.draw(a2), a2;
  }
  circle(t2, e2, s2, n2) {
    const o2 = this.gen.circle(t2, e2, s2, n2);
    return this.draw(o2), o2;
  }
  linearPath(t2, e2) {
    const s2 = this.gen.linearPath(t2, e2);
    return this.draw(s2), s2;
  }
  polygon(t2, e2) {
    const s2 = this.gen.polygon(t2, e2);
    return this.draw(s2), s2;
  }
  arc(t2, e2, s2, n2, o2, a2, h2 = false, r2) {
    const i2 = this.gen.arc(t2, e2, s2, n2, o2, a2, h2, r2);
    return this.draw(i2), i2;
  }
  curve(t2, e2) {
    const s2 = this.gen.curve(t2, e2);
    return this.draw(s2), s2;
  }
  path(t2, e2) {
    const s2 = this.gen.path(t2, e2);
    return this.draw(s2), s2;
  }
};
var nt = "http://www.w3.org/2000/svg";
var ot = class {
  static {
    __name(this, "ot");
  }
  constructor(t2, e2) {
    this.svg = t2, this.gen = new et(e2);
  }
  draw(t2) {
    const e2 = t2.sets || [], s2 = t2.options || this.getDefaultOptions(), n2 = this.svg.ownerDocument || window.document, o2 = n2.createElementNS(nt, "g"), a2 = t2.options.fixedDecimalPlaceDigits;
    for (const h2 of e2) {
      let e3 = null;
      switch (h2.type) {
        case "path":
          e3 = n2.createElementNS(nt, "path"), e3.setAttribute("d", this.opsToPath(h2, a2)), e3.setAttribute("stroke", s2.stroke), e3.setAttribute("stroke-width", s2.strokeWidth + ""), e3.setAttribute("fill", "none"), s2.strokeLineDash && e3.setAttribute("stroke-dasharray", s2.strokeLineDash.join(" ").trim()), s2.strokeLineDashOffset && e3.setAttribute("stroke-dashoffset", `${s2.strokeLineDashOffset}`);
          break;
        case "fillPath":
          e3 = n2.createElementNS(nt, "path"), e3.setAttribute("d", this.opsToPath(h2, a2)), e3.setAttribute("stroke", "none"), e3.setAttribute("stroke-width", "0"), e3.setAttribute("fill", s2.fill || ""), "curve" !== t2.shape && "polygon" !== t2.shape || e3.setAttribute("fill-rule", "evenodd");
          break;
        case "fillSketch":
          e3 = this.fillSketch(n2, h2, s2);
      }
      e3 && o2.appendChild(e3);
    }
    return o2;
  }
  fillSketch(t2, e2, s2) {
    let n2 = s2.fillWeight;
    n2 < 0 && (n2 = s2.strokeWidth / 2);
    const o2 = t2.createElementNS(nt, "path");
    return o2.setAttribute("d", this.opsToPath(e2, s2.fixedDecimalPlaceDigits)), o2.setAttribute("stroke", s2.fill || ""), o2.setAttribute("stroke-width", n2 + ""), o2.setAttribute("fill", "none"), s2.fillLineDash && o2.setAttribute("stroke-dasharray", s2.fillLineDash.join(" ").trim()), s2.fillLineDashOffset && o2.setAttribute("stroke-dashoffset", `${s2.fillLineDashOffset}`), o2;
  }
  get generator() {
    return this.gen;
  }
  getDefaultOptions() {
    return this.gen.defaultOptions;
  }
  opsToPath(t2, e2) {
    return this.gen.opsToPath(t2, e2);
  }
  line(t2, e2, s2, n2, o2) {
    const a2 = this.gen.line(t2, e2, s2, n2, o2);
    return this.draw(a2);
  }
  rectangle(t2, e2, s2, n2, o2) {
    const a2 = this.gen.rectangle(t2, e2, s2, n2, o2);
    return this.draw(a2);
  }
  ellipse(t2, e2, s2, n2, o2) {
    const a2 = this.gen.ellipse(t2, e2, s2, n2, o2);
    return this.draw(a2);
  }
  circle(t2, e2, s2, n2) {
    const o2 = this.gen.circle(t2, e2, s2, n2);
    return this.draw(o2);
  }
  linearPath(t2, e2) {
    const s2 = this.gen.linearPath(t2, e2);
    return this.draw(s2);
  }
  polygon(t2, e2) {
    const s2 = this.gen.polygon(t2, e2);
    return this.draw(s2);
  }
  arc(t2, e2, s2, n2, o2, a2, h2 = false, r2) {
    const i2 = this.gen.arc(t2, e2, s2, n2, o2, a2, h2, r2);
    return this.draw(i2);
  }
  curve(t2, e2) {
    const s2 = this.gen.curve(t2, e2);
    return this.draw(s2);
  }
  path(t2, e2) {
    const s2 = this.gen.path(t2, e2);
    return this.draw(s2);
  }
};
var at = { canvas: /* @__PURE__ */ __name((t2, e2) => new st(t2, e2), "canvas"), svg: /* @__PURE__ */ __name((t2, e2) => new ot(t2, e2), "svg"), generator: /* @__PURE__ */ __name((t2) => new et(t2), "generator"), newSeed: /* @__PURE__ */ __name(() => et.newSeed(), "newSeed") };

// src/rendering-util/rendering-elements/intersect/intersect-rect.js
var intersectRect = /* @__PURE__ */ __name((node, point2) => {
  var x2 = node.x;
  var y2 = node.y;
  var dx = point2.x - x2;
  var dy = point2.y - y2;
  var w2 = node.width / 2;
  var h2 = node.height / 2;
  var sx, sy;
  if (Math.abs(dy) * w2 > Math.abs(dx) * h2) {
    if (dy < 0) {
      h2 = -h2;
    }
    sx = dy === 0 ? 0 : h2 * dx / dy;
    sy = h2;
  } else {
    if (dx < 0) {
      w2 = -w2;
    }
    sx = w2;
    sy = dx === 0 ? 0 : w2 * dy / dx;
  }
  return { x: x2 + sx, y: y2 + sy };
}, "intersectRect");
var intersect_rect_default = intersectRect;

// src/rendering-util/rendering-elements/createLabel.js
function applyStyle(dom, styleFn) {
  if (styleFn) {
    dom.attr("style", styleFn);
  }
}
__name(applyStyle, "applyStyle");
async function addHtmlLabel(node) {
  const fo = select_default(document.createElementNS("http://www.w3.org/2000/svg", "foreignObject"));
  const div = fo.append("xhtml:div");
  let label = node.label;
  if (node.label && hasKatex(node.label)) {
    label = await renderKatex(node.label.replace(common_default.lineBreakRegex, "\n"), getConfig());
  }
  const labelClass = node.isNode ? "nodeLabel" : "edgeLabel";
  div.html(
    '<span class="' + labelClass + '" ' + (node.labelStyle ? 'style="' + node.labelStyle + '"' : "") + // codeql [js/html-constructed-from-input] : false positive
    ">" + label + "</span>"
  );
  applyStyle(div, node.labelStyle);
  div.style("display", "inline-block");
  div.style("padding-right", "1px");
  div.style("white-space", "nowrap");
  div.attr("xmlns", "http://www.w3.org/1999/xhtml");
  return fo.node();
}
__name(addHtmlLabel, "addHtmlLabel");
var createLabel = /* @__PURE__ */ __name(async (_vertexText, style, isTitle, isNode) => {
  let vertexText = _vertexText || "";
  if (typeof vertexText === "object") {
    vertexText = vertexText[0];
  }
  if (evaluate(getConfig().flowchart.htmlLabels)) {
    vertexText = vertexText.replace(/\\n|\n/g, "<br />");
    log.info("vertexText" + vertexText);
    const node = {
      isNode,
      label: decodeEntities(vertexText).replace(
        /fa[blrs]?:fa-[\w-]+/g,
        (s2) => `<i class='${s2.replace(":", " ")}'></i>`
      ),
      labelStyle: style ? style.replace("fill:", "color:") : style
    };
    let vertexNode = await addHtmlLabel(node);
    return vertexNode;
  } else {
    const svgLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    svgLabel.setAttribute("style", style.replace("color:", "fill:"));
    let rows = [];
    if (typeof vertexText === "string") {
      rows = vertexText.split(/\\n|\n|<br\s*\/?>/gi);
    } else if (Array.isArray(vertexText)) {
      rows = vertexText;
    } else {
      rows = [];
    }
    for (const row of rows) {
      const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
      tspan.setAttributeNS("http://www.w3.org/XML/1998/namespace", "xml:space", "preserve");
      tspan.setAttribute("dy", "1em");
      tspan.setAttribute("x", "0");
      if (isTitle) {
        tspan.setAttribute("class", "title-row");
      } else {
        tspan.setAttribute("class", "row");
      }
      tspan.textContent = row.trim();
      svgLabel.appendChild(tspan);
    }
    return svgLabel;
  }
}, "createLabel");
var createLabel_default = createLabel;

// src/rendering-util/rendering-elements/shapes/roundedRectPath.ts
var createRoundedRectPathD = /* @__PURE__ */ __name((x2, y2, totalWidth, totalHeight, radius) => [
  "M",
  x2 + radius,
  y2,
  // Move to the first point
  "H",
  x2 + totalWidth - radius,
  // Draw horizontal line to the beginning of the right corner
  "A",
  radius,
  radius,
  0,
  0,
  1,
  x2 + totalWidth,
  y2 + radius,
  // Draw arc to the right top corner
  "V",
  y2 + totalHeight - radius,
  // Draw vertical line down to the beginning of the right bottom corner
  "A",
  radius,
  radius,
  0,
  0,
  1,
  x2 + totalWidth - radius,
  y2 + totalHeight,
  // Draw arc to the right bottom corner
  "H",
  x2 + radius,
  // Draw horizontal line to the beginning of the left bottom corner
  "A",
  radius,
  radius,
  0,
  0,
  1,
  x2,
  y2 + totalHeight - radius,
  // Draw arc to the left bottom corner
  "V",
  y2 + radius,
  // Draw vertical line up to the beginning of the left top corner
  "A",
  radius,
  radius,
  0,
  0,
  1,
  x2 + radius,
  y2,
  // Draw arc to the left top corner
  "Z"
  // Close the path
].join(" "), "createRoundedRectPathD");

// src/rendering-util/rendering-elements/shapes/handDrawnShapeStyles.ts
var solidStateFill = /* @__PURE__ */ __name((color) => {
  const { handDrawnSeed } = getConfig();
  return {
    fill: color,
    hachureAngle: 120,
    // angle of hachure,
    hachureGap: 4,
    fillWeight: 2,
    roughness: 0.7,
    stroke: color,
    seed: handDrawnSeed
  };
}, "solidStateFill");
var compileStyles = /* @__PURE__ */ __name((node) => {
  const stylesMap = styles2Map([...node.cssCompiledStyles || [], ...node.cssStyles || []]);
  return { stylesMap, stylesArray: [...stylesMap] };
}, "compileStyles");
var styles2Map = /* @__PURE__ */ __name((styles) => {
  const styleMap = /* @__PURE__ */ new Map();
  styles.forEach((style) => {
    const [key, value] = style.split(":");
    styleMap.set(key.trim(), value?.trim());
  });
  return styleMap;
}, "styles2Map");
var styles2String = /* @__PURE__ */ __name((node) => {
  const { stylesArray } = compileStyles(node);
  const labelStyles = [];
  const nodeStyles = [];
  const borderStyles = [];
  const backgroundStyles = [];
  stylesArray.forEach((style) => {
    const key = style[0];
    if (key === "color" || key === "font-size" || key === "font-family" || key === "font-weight" || key === "font-style" || key === "text-decoration" || key === "text-align" || key === "text-transform" || key === "line-height" || key === "letter-spacing" || key === "word-spacing" || key === "text-shadow" || key === "text-overflow" || key === "white-space" || key === "word-wrap" || key === "word-break" || key === "overflow-wrap" || key === "hyphens") {
      labelStyles.push(style.join(":") + " !important");
    } else {
      nodeStyles.push(style.join(":") + " !important");
      if (key.includes("stroke")) {
        borderStyles.push(style.join(":") + " !important");
      }
      if (key === "fill") {
        backgroundStyles.push(style.join(":") + " !important");
      }
    }
  });
  return {
    labelStyles: labelStyles.join(";"),
    nodeStyles: nodeStyles.join(";"),
    stylesArray,
    borderStyles,
    backgroundStyles
  };
}, "styles2String");
var userNodeOverrides = /* @__PURE__ */ __name((node, options) => {
  const { themeVariables, handDrawnSeed } = getConfig();
  const { nodeBorder, mainBkg } = themeVariables;
  const { stylesMap } = compileStyles(node);
  const result = Object.assign(
    {
      roughness: 0.7,
      fill: stylesMap.get("fill") || mainBkg,
      fillStyle: "hachure",
      // solid fill
      fillWeight: 4,
      stroke: stylesMap.get("stroke") || nodeBorder,
      seed: handDrawnSeed,
      strokeWidth: 1.3
    },
    options
  );
  return result;
}, "userNodeOverrides");

// src/rendering-util/rendering-elements/clusters.js
var rect = /* @__PURE__ */ __name(async (parent, node) => {
  log.info("Creating subgraph rect for ", node.id, node);
  const siteConfig = getConfig();
  const { themeVariables, handDrawnSeed } = siteConfig;
  const { clusterBkg, clusterBorder } = themeVariables;
  const { labelStyles, nodeStyles, borderStyles, backgroundStyles } = styles2String(node);
  const shapeSvg = parent.insert("g").attr("class", "cluster " + node.cssClasses).attr("id", node.id).attr("data-look", node.look);
  const useHtmlLabels = evaluate(siteConfig.flowchart.htmlLabels);
  const labelEl = shapeSvg.insert("g").attr("class", "cluster-label ");
  const text = await createText(labelEl, node.label, {
    style: node.labelStyle,
    useHtmlLabels,
    isNode: true
  });
  let bbox = text.getBBox();
  if (evaluate(siteConfig.flowchart.htmlLabels)) {
    const div = text.children[0];
    const dv = select_default(text);
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  const width = node.width <= bbox.width + node.padding ? bbox.width + node.padding : node.width;
  if (node.width <= bbox.width + node.padding) {
    node.diff = (width - node.width) / 2 - node.padding;
  } else {
    node.diff = -node.padding;
  }
  const height = node.height;
  const x2 = node.x - width / 2;
  const y2 = node.y - height / 2;
  log.trace("Data ", node, JSON.stringify(node));
  let rect2;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {
      roughness: 0.7,
      fill: clusterBkg,
      // fill: 'red',
      stroke: clusterBorder,
      fillWeight: 3,
      seed: handDrawnSeed
    });
    const roughNode = rc.path(createRoundedRectPathD(x2, y2, width, height, 0), options);
    rect2 = shapeSvg.insert(() => {
      log.debug("Rough node insert CXC", roughNode);
      return roughNode;
    }, ":first-child");
    rect2.select("path:nth-child(2)").attr("style", borderStyles.join(";"));
    rect2.select("path").attr("style", backgroundStyles.join(";").replace("fill", "stroke"));
  } else {
    rect2 = shapeSvg.insert("rect", ":first-child");
    rect2.attr("style", nodeStyles).attr("rx", node.rx).attr("ry", node.ry).attr("x", x2).attr("y", y2).attr("width", width).attr("height", height);
  }
  const { subGraphTitleTopMargin } = getSubGraphTitleMargins(siteConfig);
  labelEl.attr(
    "transform",
    // This puts the label on top of the box instead of inside it
    `translate(${node.x - bbox.width / 2}, ${node.y - node.height / 2 + subGraphTitleTopMargin})`
  );
  if (labelStyles) {
    const span = labelEl.select("span");
    if (span) {
      span.attr("style", labelStyles);
    }
  }
  const rectBox = rect2.node().getBBox();
  node.offsetX = 0;
  node.width = rectBox.width;
  node.height = rectBox.height;
  node.offsetY = bbox.height - node.padding / 2;
  node.intersect = function(point2) {
    return intersect_rect_default(node, point2);
  };
  return { cluster: shapeSvg, labelBBox: bbox };
}, "rect");
var noteGroup = /* @__PURE__ */ __name((parent, node) => {
  const shapeSvg = parent.insert("g").attr("class", "note-cluster").attr("id", node.id);
  const rect2 = shapeSvg.insert("rect", ":first-child");
  const padding = 0 * node.padding;
  const halfPadding = padding / 2;
  rect2.attr("rx", node.rx).attr("ry", node.ry).attr("x", node.x - node.width / 2 - halfPadding).attr("y", node.y - node.height / 2 - halfPadding).attr("width", node.width + padding).attr("height", node.height + padding).attr("fill", "none");
  const rectBox = rect2.node().getBBox();
  node.width = rectBox.width;
  node.height = rectBox.height;
  node.intersect = function(point2) {
    return intersect_rect_default(node, point2);
  };
  return { cluster: shapeSvg, labelBBox: { width: 0, height: 0 } };
}, "noteGroup");
var roundedWithTitle = /* @__PURE__ */ __name(async (parent, node) => {
  const siteConfig = getConfig();
  const { themeVariables, handDrawnSeed } = siteConfig;
  const { altBackground, compositeBackground, compositeTitleBackground, nodeBorder } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", node.cssClasses).attr("id", node.id).attr("data-id", node.id).attr("data-look", node.look);
  const outerRectG = shapeSvg.insert("g", ":first-child");
  const label = shapeSvg.insert("g").attr("class", "cluster-label");
  let innerRect = shapeSvg.append("rect");
  const text = label.node().appendChild(await createLabel_default(node.label, node.labelStyle, void 0, true));
  let bbox = text.getBBox();
  if (evaluate(siteConfig.flowchart.htmlLabels)) {
    const div = text.children[0];
    const dv = select_default(text);
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  const padding = 0 * node.padding;
  const halfPadding = padding / 2;
  const width = (node.width <= bbox.width + node.padding ? bbox.width + node.padding : node.width) + padding;
  if (node.width <= bbox.width + node.padding) {
    node.diff = (width - node.width) / 2 - node.padding;
  } else {
    node.diff = -node.padding;
  }
  const height = node.height + padding;
  const innerHeight = node.height + padding - bbox.height - 6;
  const x2 = node.x - width / 2;
  const y2 = node.y - height / 2;
  node.width = width;
  const innerY = node.y - node.height / 2 - halfPadding + bbox.height + 2;
  let rect2;
  if (node.look === "handDrawn") {
    const isAlt = node.cssClasses.includes("statediagram-cluster-alt");
    const rc = at.svg(shapeSvg);
    const roughOuterNode = node.rx || node.ry ? rc.path(createRoundedRectPathD(x2, y2, width, height, 10), {
      roughness: 0.7,
      fill: compositeTitleBackground,
      fillStyle: "solid",
      stroke: nodeBorder,
      seed: handDrawnSeed
    }) : rc.rectangle(x2, y2, width, height, { seed: handDrawnSeed });
    rect2 = shapeSvg.insert(() => roughOuterNode, ":first-child");
    const roughInnerNode = rc.rectangle(x2, innerY, width, innerHeight, {
      fill: isAlt ? altBackground : compositeBackground,
      fillStyle: isAlt ? "hachure" : "solid",
      stroke: nodeBorder,
      seed: handDrawnSeed
    });
    rect2 = shapeSvg.insert(() => roughOuterNode, ":first-child");
    innerRect = shapeSvg.insert(() => roughInnerNode);
  } else {
    rect2 = outerRectG.insert("rect", ":first-child");
    const outerRectClass = "outer";
    rect2.attr("class", outerRectClass).attr("x", x2).attr("y", y2).attr("width", width).attr("height", height).attr("data-look", node.look);
    innerRect.attr("class", "inner").attr("x", x2).attr("y", innerY).attr("width", width).attr("height", innerHeight);
  }
  label.attr(
    "transform",
    `translate(${node.x - bbox.width / 2}, ${y2 + 1 - (evaluate(siteConfig.flowchart.htmlLabels) ? 0 : 3)})`
  );
  const rectBox = rect2.node().getBBox();
  node.height = rectBox.height;
  node.offsetX = 0;
  node.offsetY = bbox.height - node.padding / 2;
  node.labelBBox = bbox;
  node.intersect = function(point2) {
    return intersect_rect_default(node, point2);
  };
  return { cluster: shapeSvg, labelBBox: bbox };
}, "roundedWithTitle");
var divider = /* @__PURE__ */ __name((parent, node) => {
  const siteConfig = getConfig();
  const { themeVariables, handDrawnSeed } = siteConfig;
  const { nodeBorder } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", node.cssClasses).attr("id", node.id).attr("data-look", node.look);
  const outerRectG = shapeSvg.insert("g", ":first-child");
  const padding = 0 * node.padding;
  const width = node.width + padding;
  node.diff = -node.padding;
  const height = node.height + padding;
  const x2 = node.x - width / 2;
  const y2 = node.y - height / 2;
  node.width = width;
  let rect2;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const roughOuterNode = rc.rectangle(x2, y2, width, height, {
      fill: "lightgrey",
      roughness: 0.5,
      strokeLineDash: [5],
      stroke: nodeBorder,
      seed: handDrawnSeed
    });
    rect2 = shapeSvg.insert(() => roughOuterNode, ":first-child");
  } else {
    rect2 = outerRectG.insert("rect", ":first-child");
    const outerRectClass = "divider";
    rect2.attr("class", outerRectClass).attr("x", x2).attr("y", y2).attr("width", width).attr("height", height).attr("data-look", node.look);
  }
  const rectBox = rect2.node().getBBox();
  node.height = rectBox.height;
  node.offsetX = 0;
  node.offsetY = 0;
  node.intersect = function(point2) {
    return intersect_rect_default(node, point2);
  };
  return { cluster: shapeSvg, labelBBox: {} };
}, "divider");
var squareRect = rect;
var shapes = {
  rect,
  squareRect,
  roundedWithTitle,
  noteGroup,
  divider
};
var clusterElems = /* @__PURE__ */ new Map();
var insertCluster = /* @__PURE__ */ __name(async (elem, node) => {
  const shape = node.shape || "rect";
  const cluster = await shapes[shape](elem, node);
  clusterElems.set(node.id, cluster);
  return cluster;
}, "insertCluster");
var clear = /* @__PURE__ */ __name(() => {
  clusterElems = /* @__PURE__ */ new Map();
}, "clear");

// src/rendering-util/rendering-elements/edgeMarker.ts
var addEdgeMarkers = /* @__PURE__ */ __name((svgPath, edge, url, id, diagramType) => {
  if (edge.arrowTypeStart) {
    addEdgeMarker(svgPath, "start", edge.arrowTypeStart, url, id, diagramType);
  }
  if (edge.arrowTypeEnd) {
    addEdgeMarker(svgPath, "end", edge.arrowTypeEnd, url, id, diagramType);
  }
}, "addEdgeMarkers");
var arrowTypesMap = {
  arrow_cross: "cross",
  arrow_point: "point",
  arrow_barb: "barb",
  arrow_circle: "circle",
  aggregation: "aggregation",
  extension: "extension",
  composition: "composition",
  dependency: "dependency",
  lollipop: "lollipop"
};
var addEdgeMarker = /* @__PURE__ */ __name((svgPath, position, arrowType, url, id, diagramType) => {
  const endMarkerType = arrowTypesMap[arrowType];
  if (!endMarkerType) {
    log.warn(`Unknown arrow type: ${arrowType}`);
    return;
  }
  const suffix = position === "start" ? "Start" : "End";
  svgPath.attr(`marker-${position}`, `url(${url}#${id}_${diagramType}-${endMarkerType}${suffix})`);
}, "addEdgeMarker");

// src/rendering-util/rendering-elements/edges.js
var edgeLabels = /* @__PURE__ */ new Map();
var terminalLabels = /* @__PURE__ */ new Map();
var clear2 = /* @__PURE__ */ __name(() => {
  edgeLabels.clear();
  terminalLabels.clear();
}, "clear");
var getLabelStyles = /* @__PURE__ */ __name((styleArray) => {
  let styles = styleArray ? styleArray.reduce((acc, style) => acc + ";" + style, "") : "";
  return styles;
}, "getLabelStyles");
var insertEdgeLabel = /* @__PURE__ */ __name(async (elem, edge) => {
  let useHtmlLabels = evaluate(getConfig().flowchart.htmlLabels);
  const labelElement = await createText(elem, edge.label, {
    style: getLabelStyles(edge.labelStyle),
    useHtmlLabels,
    addSvgBackground: true,
    isNode: false
  });
  log.info("abc82", edge, edge.labelType);
  const edgeLabel = elem.insert("g").attr("class", "edgeLabel");
  const label = edgeLabel.insert("g").attr("class", "label");
  label.node().appendChild(labelElement);
  let bbox = labelElement.getBBox();
  if (useHtmlLabels) {
    const div = labelElement.children[0];
    const dv = select_default(labelElement);
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  label.attr("transform", "translate(" + -bbox.width / 2 + ", " + -bbox.height / 2 + ")");
  edgeLabels.set(edge.id, edgeLabel);
  edge.width = bbox.width;
  edge.height = bbox.height;
  let fo;
  if (edge.startLabelLeft) {
    const startLabelElement = await createLabel_default(
      edge.startLabelLeft,
      getLabelStyles(edge.labelStyle)
    );
    const startEdgeLabelLeft = elem.insert("g").attr("class", "edgeTerminals");
    const inner = startEdgeLabelLeft.insert("g").attr("class", "inner");
    fo = inner.node().appendChild(startLabelElement);
    const slBox = startLabelElement.getBBox();
    inner.attr("transform", "translate(" + -slBox.width / 2 + ", " + -slBox.height / 2 + ")");
    if (!terminalLabels.get(edge.id)) {
      terminalLabels.set(edge.id, {});
    }
    terminalLabels.get(edge.id).startLeft = startEdgeLabelLeft;
    setTerminalWidth(fo, edge.startLabelLeft);
  }
  if (edge.startLabelRight) {
    const startLabelElement = await createLabel_default(
      edge.startLabelRight,
      getLabelStyles(edge.labelStyle)
    );
    const startEdgeLabelRight = elem.insert("g").attr("class", "edgeTerminals");
    const inner = startEdgeLabelRight.insert("g").attr("class", "inner");
    fo = startEdgeLabelRight.node().appendChild(startLabelElement);
    inner.node().appendChild(startLabelElement);
    const slBox = startLabelElement.getBBox();
    inner.attr("transform", "translate(" + -slBox.width / 2 + ", " + -slBox.height / 2 + ")");
    if (!terminalLabels.get(edge.id)) {
      terminalLabels.set(edge.id, {});
    }
    terminalLabels.get(edge.id).startRight = startEdgeLabelRight;
    setTerminalWidth(fo, edge.startLabelRight);
  }
  if (edge.endLabelLeft) {
    const endLabelElement = await createLabel_default(edge.endLabelLeft, getLabelStyles(edge.labelStyle));
    const endEdgeLabelLeft = elem.insert("g").attr("class", "edgeTerminals");
    const inner = endEdgeLabelLeft.insert("g").attr("class", "inner");
    fo = inner.node().appendChild(endLabelElement);
    const slBox = endLabelElement.getBBox();
    inner.attr("transform", "translate(" + -slBox.width / 2 + ", " + -slBox.height / 2 + ")");
    endEdgeLabelLeft.node().appendChild(endLabelElement);
    if (!terminalLabels.get(edge.id)) {
      terminalLabels.set(edge.id, {});
    }
    terminalLabels.get(edge.id).endLeft = endEdgeLabelLeft;
    setTerminalWidth(fo, edge.endLabelLeft);
  }
  if (edge.endLabelRight) {
    const endLabelElement = await createLabel_default(edge.endLabelRight, getLabelStyles(edge.labelStyle));
    const endEdgeLabelRight = elem.insert("g").attr("class", "edgeTerminals");
    const inner = endEdgeLabelRight.insert("g").attr("class", "inner");
    fo = inner.node().appendChild(endLabelElement);
    const slBox = endLabelElement.getBBox();
    inner.attr("transform", "translate(" + -slBox.width / 2 + ", " + -slBox.height / 2 + ")");
    endEdgeLabelRight.node().appendChild(endLabelElement);
    if (!terminalLabels.get(edge.id)) {
      terminalLabels.set(edge.id, {});
    }
    terminalLabels.get(edge.id).endRight = endEdgeLabelRight;
    setTerminalWidth(fo, edge.endLabelRight);
  }
  return labelElement;
}, "insertEdgeLabel");
function setTerminalWidth(fo, value) {
  if (getConfig().flowchart.htmlLabels && fo) {
    fo.style.width = value.length * 9 + "px";
    fo.style.height = "12px";
  }
}
__name(setTerminalWidth, "setTerminalWidth");
var positionEdgeLabel = /* @__PURE__ */ __name((edge, paths) => {
  log.debug("Moving label abc88 ", edge.id, edge.label, edgeLabels.get(edge.id), paths);
  let path = paths.updatedPath ? paths.updatedPath : paths.originalPath;
  const siteConfig = getConfig();
  const { subGraphTitleTotalMargin } = getSubGraphTitleMargins(siteConfig);
  if (edge.label) {
    const el = edgeLabels.get(edge.id);
    let x2 = edge.x;
    let y2 = edge.y;
    if (path) {
      const pos = utils_default.calcLabelPosition(path);
      log.debug(
        "Moving label " + edge.label + " from (",
        x2,
        ",",
        y2,
        ") to (",
        pos.x,
        ",",
        pos.y,
        ") abc88"
      );
      if (paths.updatedPath) {
        x2 = pos.x;
        y2 = pos.y;
      }
    }
    el.attr("transform", `translate(${x2}, ${y2 + subGraphTitleTotalMargin / 2})`);
  }
  if (edge.startLabelLeft) {
    const el = terminalLabels.get(edge.id).startLeft;
    let x2 = edge.x;
    let y2 = edge.y;
    if (path) {
      const pos = utils_default.calcTerminalLabelPosition(edge.arrowTypeStart ? 10 : 0, "start_left", path);
      x2 = pos.x;
      y2 = pos.y;
    }
    el.attr("transform", `translate(${x2}, ${y2})`);
  }
  if (edge.startLabelRight) {
    const el = terminalLabels.get(edge.id).startRight;
    let x2 = edge.x;
    let y2 = edge.y;
    if (path) {
      const pos = utils_default.calcTerminalLabelPosition(
        edge.arrowTypeStart ? 10 : 0,
        "start_right",
        path
      );
      x2 = pos.x;
      y2 = pos.y;
    }
    el.attr("transform", `translate(${x2}, ${y2})`);
  }
  if (edge.endLabelLeft) {
    const el = terminalLabels.get(edge.id).endLeft;
    let x2 = edge.x;
    let y2 = edge.y;
    if (path) {
      const pos = utils_default.calcTerminalLabelPosition(edge.arrowTypeEnd ? 10 : 0, "end_left", path);
      x2 = pos.x;
      y2 = pos.y;
    }
    el.attr("transform", `translate(${x2}, ${y2})`);
  }
  if (edge.endLabelRight) {
    const el = terminalLabels.get(edge.id).endRight;
    let x2 = edge.x;
    let y2 = edge.y;
    if (path) {
      const pos = utils_default.calcTerminalLabelPosition(edge.arrowTypeEnd ? 10 : 0, "end_right", path);
      x2 = pos.x;
      y2 = pos.y;
    }
    el.attr("transform", `translate(${x2}, ${y2})`);
  }
}, "positionEdgeLabel");
var outsideNode = /* @__PURE__ */ __name((node, point2) => {
  const x2 = node.x;
  const y2 = node.y;
  const dx = Math.abs(point2.x - x2);
  const dy = Math.abs(point2.y - y2);
  const w2 = node.width / 2;
  const h2 = node.height / 2;
  return dx >= w2 || dy >= h2;
}, "outsideNode");
var intersection = /* @__PURE__ */ __name((node, outsidePoint, insidePoint) => {
  log.debug(`intersection calc abc89:
  outsidePoint: ${JSON.stringify(outsidePoint)}
  insidePoint : ${JSON.stringify(insidePoint)}
  node        : x:${node.x} y:${node.y} w:${node.width} h:${node.height}`);
  const x2 = node.x;
  const y2 = node.y;
  const dx = Math.abs(x2 - insidePoint.x);
  const w2 = node.width / 2;
  let r2 = insidePoint.x < outsidePoint.x ? w2 - dx : w2 + dx;
  const h2 = node.height / 2;
  const Q2 = Math.abs(outsidePoint.y - insidePoint.y);
  const R2 = Math.abs(outsidePoint.x - insidePoint.x);
  if (Math.abs(y2 - outsidePoint.y) * w2 > Math.abs(x2 - outsidePoint.x) * h2) {
    let q2 = insidePoint.y < outsidePoint.y ? outsidePoint.y - h2 - y2 : y2 - h2 - outsidePoint.y;
    r2 = R2 * q2 / Q2;
    const res = {
      x: insidePoint.x < outsidePoint.x ? insidePoint.x + r2 : insidePoint.x - R2 + r2,
      y: insidePoint.y < outsidePoint.y ? insidePoint.y + Q2 - q2 : insidePoint.y - Q2 + q2
    };
    if (r2 === 0) {
      res.x = outsidePoint.x;
      res.y = outsidePoint.y;
    }
    if (R2 === 0) {
      res.x = outsidePoint.x;
    }
    if (Q2 === 0) {
      res.y = outsidePoint.y;
    }
    log.debug(`abc89 top/bottom calc, Q ${Q2}, q ${q2}, R ${R2}, r ${r2}`, res);
    return res;
  } else {
    if (insidePoint.x < outsidePoint.x) {
      r2 = outsidePoint.x - w2 - x2;
    } else {
      r2 = x2 - w2 - outsidePoint.x;
    }
    let q2 = Q2 * r2 / R2;
    let _x = insidePoint.x < outsidePoint.x ? insidePoint.x + R2 - r2 : insidePoint.x - R2 + r2;
    let _y = insidePoint.y < outsidePoint.y ? insidePoint.y + q2 : insidePoint.y - q2;
    log.debug(`sides calc abc89, Q ${Q2}, q ${q2}, R ${R2}, r ${r2}`, { _x, _y });
    if (r2 === 0) {
      _x = outsidePoint.x;
      _y = outsidePoint.y;
    }
    if (R2 === 0) {
      _x = outsidePoint.x;
    }
    if (Q2 === 0) {
      _y = outsidePoint.y;
    }
    return { x: _x, y: _y };
  }
}, "intersection");
var cutPathAtIntersect = /* @__PURE__ */ __name((_points, boundaryNode) => {
  log.warn("abc88 cutPathAtIntersect", _points, boundaryNode);
  let points = [];
  let lastPointOutside = _points[0];
  let isInside = false;
  _points.forEach((point2) => {
    log.info("abc88 checking point", point2, boundaryNode);
    if (!outsideNode(boundaryNode, point2) && !isInside) {
      const inter = intersection(boundaryNode, lastPointOutside, point2);
      log.debug("abc88 inside", point2, lastPointOutside, inter);
      log.debug("abc88 intersection", inter, boundaryNode);
      let pointPresent = false;
      points.forEach((p2) => {
        pointPresent = pointPresent || p2.x === inter.x && p2.y === inter.y;
      });
      if (!points.some((e2) => e2.x === inter.x && e2.y === inter.y)) {
        points.push(inter);
      } else {
        log.warn("abc88 no intersect", inter, points);
      }
      isInside = true;
    } else {
      log.warn("abc88 outside", point2, lastPointOutside);
      lastPointOutside = point2;
      if (!isInside) {
        points.push(point2);
      }
    }
  });
  log.debug("returning points", points);
  return points;
}, "cutPathAtIntersect");
function extractCornerPoints(points) {
  const cornerPoints = [];
  const cornerPointPositions = [];
  for (let i2 = 1; i2 < points.length - 1; i2++) {
    const prev = points[i2 - 1];
    const curr = points[i2];
    const next = points[i2 + 1];
    if (prev.x === curr.x && curr.y === next.y && Math.abs(curr.x - next.x) > 5 && Math.abs(curr.y - prev.y) > 5) {
      cornerPoints.push(curr);
      cornerPointPositions.push(i2);
    } else if (prev.y === curr.y && curr.x === next.x && Math.abs(curr.x - prev.x) > 5 && Math.abs(curr.y - next.y) > 5) {
      cornerPoints.push(curr);
      cornerPointPositions.push(i2);
    }
  }
  return { cornerPoints, cornerPointPositions };
}
__name(extractCornerPoints, "extractCornerPoints");
var findAdjacentPoint = /* @__PURE__ */ __name(function(pointA, pointB, distance) {
  const xDiff = pointB.x - pointA.x;
  const yDiff = pointB.y - pointA.y;
  const length = Math.sqrt(xDiff * xDiff + yDiff * yDiff);
  const ratio = distance / length;
  return { x: pointB.x - ratio * xDiff, y: pointB.y - ratio * yDiff };
}, "findAdjacentPoint");
var fixCorners = /* @__PURE__ */ __name(function(lineData) {
  const { cornerPointPositions } = extractCornerPoints(lineData);
  const newLineData = [];
  for (let i2 = 0; i2 < lineData.length; i2++) {
    if (cornerPointPositions.includes(i2)) {
      const prevPoint = lineData[i2 - 1];
      const nextPoint = lineData[i2 + 1];
      const cornerPoint = lineData[i2];
      const newPrevPoint = findAdjacentPoint(prevPoint, cornerPoint, 5);
      const newNextPoint = findAdjacentPoint(nextPoint, cornerPoint, 5);
      const xDiff = newNextPoint.x - newPrevPoint.x;
      const yDiff = newNextPoint.y - newPrevPoint.y;
      newLineData.push(newPrevPoint);
      const a2 = Math.sqrt(2) * 2;
      let newCornerPoint = { x: cornerPoint.x, y: cornerPoint.y };
      if (Math.abs(nextPoint.x - prevPoint.x) > 10 && Math.abs(nextPoint.y - prevPoint.y) >= 10) {
        log.debug(
          "Corner point fixing",
          Math.abs(nextPoint.x - prevPoint.x),
          Math.abs(nextPoint.y - prevPoint.y)
        );
        const r2 = 5;
        if (cornerPoint.x === newPrevPoint.x) {
          newCornerPoint = {
            x: xDiff < 0 ? newPrevPoint.x - r2 + a2 : newPrevPoint.x + r2 - a2,
            y: yDiff < 0 ? newPrevPoint.y - a2 : newPrevPoint.y + a2
          };
        } else {
          newCornerPoint = {
            x: xDiff < 0 ? newPrevPoint.x - a2 : newPrevPoint.x + a2,
            y: yDiff < 0 ? newPrevPoint.y - r2 + a2 : newPrevPoint.y + r2 - a2
          };
        }
      } else {
        log.debug(
          "Corner point skipping fixing",
          Math.abs(nextPoint.x - prevPoint.x),
          Math.abs(nextPoint.y - prevPoint.y)
        );
      }
      newLineData.push(newCornerPoint, newNextPoint);
    } else {
      newLineData.push(lineData[i2]);
    }
  }
  return newLineData;
}, "fixCorners");
var insertEdge = /* @__PURE__ */ __name(function(elem, edge, clusterDb, diagramType, startNode, endNode, id) {
  const { handDrawnSeed } = getConfig();
  let points = edge.points;
  let pointsHasChanged = false;
  const tail = startNode;
  var head = endNode;
  if (head.intersect && tail.intersect) {
    points = points.slice(1, edge.points.length - 1);
    points.unshift(tail.intersect(points[0]));
    log.debug(
      "Last point APA12",
      edge.start,
      "-->",
      edge.end,
      points[points.length - 1],
      head,
      head.intersect(points[points.length - 1])
    );
    points.push(head.intersect(points[points.length - 1]));
  }
  if (edge.toCluster) {
    log.info("to cluster abc88", clusterDb.get(edge.toCluster));
    points = cutPathAtIntersect(edge.points, clusterDb.get(edge.toCluster).node);
    pointsHasChanged = true;
  }
  if (edge.fromCluster) {
    log.debug(
      "from cluster abc88",
      clusterDb.get(edge.fromCluster),
      JSON.stringify(points, null, 2)
    );
    points = cutPathAtIntersect(points.reverse(), clusterDb.get(edge.fromCluster).node).reverse();
    pointsHasChanged = true;
  }
  let lineData = points.filter((p2) => !Number.isNaN(p2.y));
  lineData = fixCorners(lineData);
  let lastPoint = lineData[lineData.length - 1];
  if (lineData.length > 1) {
    lastPoint = lineData[lineData.length - 1];
    const secondLastPoint = lineData[lineData.length - 2];
    const diffX = (lastPoint.x - secondLastPoint.x) / 2;
    const diffY = (lastPoint.y - secondLastPoint.y) / 2;
    const midPoint = { x: secondLastPoint.x + diffX, y: secondLastPoint.y + diffY };
    lineData.splice(-1, 0, midPoint);
  }
  let curve = basis_default;
  if (edge.curve) {
    curve = edge.curve;
  }
  const { x: x2, y: y2 } = getLineFunctionsWithOffset(edge);
  const lineFunction = line_default().x(x2).y(y2).curve(curve);
  let strokeClasses;
  switch (edge.thickness) {
    case "normal":
      strokeClasses = "edge-thickness-normal";
      break;
    case "thick":
      strokeClasses = "edge-thickness-thick";
      break;
    case "invisible":
      strokeClasses = "edge-thickness-invisible";
      break;
    default:
      strokeClasses = "edge-thickness-normal";
  }
  switch (edge.pattern) {
    case "solid":
      strokeClasses += " edge-pattern-solid";
      break;
    case "dotted":
      strokeClasses += " edge-pattern-dotted";
      break;
    case "dashed":
      strokeClasses += " edge-pattern-dashed";
      break;
    default:
      strokeClasses += " edge-pattern-solid";
  }
  let svgPath;
  let linePath = lineFunction(lineData);
  const edgeStyles = Array.isArray(edge.style) ? edge.style : [edge.style];
  if (edge.look === "handDrawn") {
    const rc = at.svg(elem);
    Object.assign([], lineData);
    const svgPathNode = rc.path(linePath, {
      roughness: 0.3,
      seed: handDrawnSeed
    });
    strokeClasses += " transition";
    svgPath = select_default(svgPathNode).select("path").attr("id", edge.id).attr("class", " " + strokeClasses + (edge.classes ? " " + edge.classes : "")).attr("style", edgeStyles ? edgeStyles.reduce((acc, style) => acc + ";" + style, "") : "");
    let d2 = svgPath.attr("d");
    svgPath.attr("d", d2);
    elem.node().appendChild(svgPath.node());
  } else {
    svgPath = elem.append("path").attr("d", linePath).attr("id", edge.id).attr("class", " " + strokeClasses + (edge.classes ? " " + edge.classes : "")).attr("style", edgeStyles ? edgeStyles.reduce((acc, style) => acc + ";" + style, "") : "");
  }
  let url = "";
  if (getConfig().flowchart.arrowMarkerAbsolute || getConfig().state.arrowMarkerAbsolute) {
    url = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search;
    url = url.replace(/\(/g, "\\(").replace(/\)/g, "\\)");
  }
  log.info("arrowTypeStart", edge.arrowTypeStart);
  log.info("arrowTypeEnd", edge.arrowTypeEnd);
  addEdgeMarkers(svgPath, edge, url, id, diagramType);
  let paths = {};
  if (pointsHasChanged) {
    paths.updatedPath = points;
  }
  paths.originalPath = edge.points;
  return paths;
}, "insertEdge");

// src/rendering-util/rendering-elements/markers.js
var insertMarkers = /* @__PURE__ */ __name((elem, markerArray, type, id) => {
  markerArray.forEach((markerName) => {
    markers[markerName](elem, type, id);
  });
}, "insertMarkers");
var extension = /* @__PURE__ */ __name((elem, type, id) => {
  log.trace("Making markers for ", id);
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-extensionStart").attr("class", "marker extension " + type).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 1,7 L18,13 V 1 Z");
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-extensionEnd").attr("class", "marker extension " + type).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 1,1 V 13 L18,7 Z");
}, "extension");
var composition = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-compositionStart").attr("class", "marker composition " + type).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-compositionEnd").attr("class", "marker composition " + type).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
}, "composition");
var aggregation = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-aggregationStart").attr("class", "marker aggregation " + type).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-aggregationEnd").attr("class", "marker aggregation " + type).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
}, "aggregation");
var dependency = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-dependencyStart").attr("class", "marker dependency " + type).attr("refX", 6).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 5,7 L9,13 L1,7 L9,1 Z");
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-dependencyEnd").attr("class", "marker dependency " + type).attr("refX", 13).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L14,7 L9,1 Z");
}, "dependency");
var lollipop = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-lollipopStart").attr("class", "marker lollipop " + type).attr("refX", 13).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("circle").attr("stroke", "black").attr("fill", "transparent").attr("cx", 7).attr("cy", 7).attr("r", 6);
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-lollipopEnd").attr("class", "marker lollipop " + type).attr("refX", 1).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("circle").attr("stroke", "black").attr("fill", "transparent").attr("cx", 7).attr("cy", 7).attr("r", 6);
}, "lollipop");
var point = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("marker").attr("id", id + "_" + type + "-pointEnd").attr("class", "marker " + type).attr("viewBox", "0 0 10 10").attr("refX", 5).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 8).attr("markerHeight", 8).attr("orient", "auto").append("path").attr("d", "M 0 0 L 10 5 L 0 10 z").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
  elem.append("marker").attr("id", id + "_" + type + "-pointStart").attr("class", "marker " + type).attr("viewBox", "0 0 10 10").attr("refX", 4.5).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 8).attr("markerHeight", 8).attr("orient", "auto").append("path").attr("d", "M 0 5 L 10 10 L 10 0 z").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
}, "point");
var circle = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("marker").attr("id", id + "_" + type + "-circleEnd").attr("class", "marker " + type).attr("viewBox", "0 0 10 10").attr("refX", 11).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("circle").attr("cx", "5").attr("cy", "5").attr("r", "5").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
  elem.append("marker").attr("id", id + "_" + type + "-circleStart").attr("class", "marker " + type).attr("viewBox", "0 0 10 10").attr("refX", -1).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("circle").attr("cx", "5").attr("cy", "5").attr("r", "5").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
}, "circle");
var cross = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("marker").attr("id", id + "_" + type + "-crossEnd").attr("class", "marker cross " + type).attr("viewBox", "0 0 11 11").attr("refX", 12).attr("refY", 5.2).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("path").attr("d", "M 1,1 l 9,9 M 10,1 l -9,9").attr("class", "arrowMarkerPath").style("stroke-width", 2).style("stroke-dasharray", "1,0");
  elem.append("marker").attr("id", id + "_" + type + "-crossStart").attr("class", "marker cross " + type).attr("viewBox", "0 0 11 11").attr("refX", -1).attr("refY", 5.2).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("path").attr("d", "M 1,1 l 9,9 M 10,1 l -9,9").attr("class", "arrowMarkerPath").style("stroke-width", 2).style("stroke-dasharray", "1,0");
}, "cross");
var barb = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-barbEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 14).attr("markerUnits", "userSpaceOnUse").attr("orient", "auto").append("path").attr("d", "M 19,7 L9,13 L14,7 L9,1 Z");
}, "barb");
var markers = {
  extension,
  composition,
  aggregation,
  dependency,
  lollipop,
  point,
  circle,
  cross,
  barb
};
var markers_default = insertMarkers;

// src/rendering-util/rendering-elements/shapes/util.js
var labelHelper = /* @__PURE__ */ __name(async (parent, node, _classes) => {
  let cssClasses;
  const useHtmlLabels = node.useHtmlLabels || evaluate(getConfig().flowchart.htmlLabels);
  if (!_classes) {
    cssClasses = "node default";
  } else {
    cssClasses = _classes;
  }
  const shapeSvg = parent.insert("g").attr("class", cssClasses).attr("id", node.domId || node.id);
  const labelEl = shapeSvg.insert("g").attr("class", "label").attr("style", node.labelStyle);
  let label;
  if (node.label === void 0) {
    label = "";
  } else {
    label = typeof node.label === "string" ? node.label : node.label[0];
  }
  let text;
  text = await createText(labelEl, sanitizeText(decodeEntities(label), getConfig()), {
    useHtmlLabels,
    width: node.width || getConfig().flowchart.wrappingWidth,
    cssClasses: "markdown-node-label",
    style: node.labelStyle
  });
  let bbox = text.getBBox();
  const halfPadding = node.padding / 2;
  if (evaluate(getConfig().flowchart.htmlLabels)) {
    const div = text.children[0];
    const dv = select_default(text);
    const images = div.getElementsByTagName("img");
    if (images) {
      const noImgText = label.replace(/<img[^>]*>/g, "").trim() === "";
      await Promise.all(
        [...images].map(
          (img) => new Promise((res) => {
            function setupImage() {
              img.style.display = "flex";
              img.style.flexDirection = "column";
              if (noImgText) {
                const bodyFontSize = getConfig().fontSize ? getConfig().fontSize : window.getComputedStyle(document.body).fontSize;
                const enlargingFactor = 5;
                const width = parseInt(bodyFontSize, 10) * enlargingFactor + "px";
                img.style.minWidth = width;
                img.style.maxWidth = width;
              } else {
                img.style.width = "100%";
              }
              res(img);
            }
            __name(setupImage, "setupImage");
            setTimeout(() => {
              if (img.complete) {
                setupImage();
              }
            });
            img.addEventListener("error", setupImage);
            img.addEventListener("load", setupImage);
          })
        )
      );
    }
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  if (useHtmlLabels) {
    labelEl.attr("transform", "translate(" + -bbox.width / 2 + ", " + -bbox.height / 2 + ")");
  } else {
    labelEl.attr("transform", "translate(0, " + -bbox.height / 2 + ")");
  }
  if (node.centerLabel) {
    labelEl.attr("transform", "translate(" + -bbox.width / 2 + ", " + -bbox.height / 2 + ")");
  }
  labelEl.insert("rect", ":first-child");
  return { shapeSvg, bbox, halfPadding, label: labelEl };
}, "labelHelper");
var updateNodeBounds = /* @__PURE__ */ __name((node, element) => {
  const bbox = element.node().getBBox();
  node.width = bbox.width;
  node.height = bbox.height;
}, "updateNodeBounds");
var getNodeClasses = /* @__PURE__ */ __name((node, extra) => (node.look === "handDrawn" ? "rough-node" : "node") + " " + node.cssClasses + " " + (extra || ""), "getNodeClasses");

// src/rendering-util/rendering-elements/intersect/intersect-node.js
function intersectNode(node, point2) {
  return node.intersect(point2);
}
__name(intersectNode, "intersectNode");
var intersect_node_default = intersectNode;

// src/rendering-util/rendering-elements/intersect/intersect-ellipse.js
function intersectEllipse(node, rx, ry, point2) {
  var cx = node.x;
  var cy = node.y;
  var px = cx - point2.x;
  var py = cy - point2.y;
  var det = Math.sqrt(rx * rx * py * py + ry * ry * px * px);
  var dx = Math.abs(rx * ry * px / det);
  if (point2.x < cx) {
    dx = -dx;
  }
  var dy = Math.abs(rx * ry * py / det);
  if (point2.y < cy) {
    dy = -dy;
  }
  return { x: cx + dx, y: cy + dy };
}
__name(intersectEllipse, "intersectEllipse");
var intersect_ellipse_default = intersectEllipse;

// src/rendering-util/rendering-elements/intersect/intersect-circle.js
function intersectCircle(node, rx, point2) {
  return intersect_ellipse_default(node, rx, rx, point2);
}
__name(intersectCircle, "intersectCircle");
var intersect_circle_default = intersectCircle;

// src/rendering-util/rendering-elements/intersect/intersect-line.js
function intersectLine(p1, p2, q1, q2) {
  var a1, a2, b1, b2, c1, c2;
  var r1, r2, r3, r4;
  var denom, offset, num;
  var x2, y2;
  a1 = p2.y - p1.y;
  b1 = p1.x - p2.x;
  c1 = p2.x * p1.y - p1.x * p2.y;
  r3 = a1 * q1.x + b1 * q1.y + c1;
  r4 = a1 * q2.x + b1 * q2.y + c1;
  if (r3 !== 0 && r4 !== 0 && sameSign(r3, r4)) {
    return;
  }
  a2 = q2.y - q1.y;
  b2 = q1.x - q2.x;
  c2 = q2.x * q1.y - q1.x * q2.y;
  r1 = a2 * p1.x + b2 * p1.y + c2;
  r2 = a2 * p2.x + b2 * p2.y + c2;
  if (r1 !== 0 && r2 !== 0 && sameSign(r1, r2)) {
    return;
  }
  denom = a1 * b2 - a2 * b1;
  if (denom === 0) {
    return;
  }
  offset = Math.abs(denom / 2);
  num = b1 * c2 - b2 * c1;
  x2 = num < 0 ? (num - offset) / denom : (num + offset) / denom;
  num = a2 * c1 - a1 * c2;
  y2 = num < 0 ? (num - offset) / denom : (num + offset) / denom;
  return { x: x2, y: y2 };
}
__name(intersectLine, "intersectLine");
function sameSign(r1, r2) {
  return r1 * r2 > 0;
}
__name(sameSign, "sameSign");
var intersect_line_default = intersectLine;

// src/rendering-util/rendering-elements/intersect/intersect-polygon.js
function intersectPolygon(node, polyPoints, point2) {
  let x1 = node.x;
  let y1 = node.y;
  let intersections = [];
  let minX = Number.POSITIVE_INFINITY;
  let minY = Number.POSITIVE_INFINITY;
  if (typeof polyPoints.forEach === "function") {
    polyPoints.forEach(function(entry) {
      minX = Math.min(minX, entry.x);
      minY = Math.min(minY, entry.y);
    });
  } else {
    minX = Math.min(minX, polyPoints.x);
    minY = Math.min(minY, polyPoints.y);
  }
  let left = x1 - node.width / 2 - minX;
  let top = y1 - node.height / 2 - minY;
  for (let i2 = 0; i2 < polyPoints.length; i2++) {
    let p1 = polyPoints[i2];
    let p2 = polyPoints[i2 < polyPoints.length - 1 ? i2 + 1 : 0];
    let intersect = intersect_line_default(
      node,
      point2,
      { x: left + p1.x, y: top + p1.y },
      { x: left + p2.x, y: top + p2.y }
    );
    if (intersect) {
      intersections.push(intersect);
    }
  }
  if (!intersections.length) {
    return node;
  }
  if (intersections.length > 1) {
    intersections.sort(function(p2, q2) {
      let pdx = p2.x - point2.x;
      let pdy = p2.y - point2.y;
      let distp = Math.sqrt(pdx * pdx + pdy * pdy);
      let qdx = q2.x - point2.x;
      let qdy = q2.y - point2.y;
      let distq = Math.sqrt(qdx * qdx + qdy * qdy);
      return distp < distq ? -1 : distp === distq ? 0 : 1;
    });
  }
  return intersections[0];
}
__name(intersectPolygon, "intersectPolygon");
var intersect_polygon_default = intersectPolygon;

// src/rendering-util/rendering-elements/intersect/index.js
var intersect_default = {
  node: intersect_node_default,
  circle: intersect_circle_default,
  ellipse: intersect_ellipse_default,
  polygon: intersect_polygon_default,
  rect: intersect_rect_default
};

// src/rendering-util/rendering-elements/shapes/drawRect.ts
var drawRect = /* @__PURE__ */ __name(async (parent, node, options) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const totalWidth = Math.max(bbox.width + options.labelPaddingX * 2, node?.width || 0);
  const totalHeight = Math.max(bbox.height + options.labelPaddingY * 2, node?.height || 0);
  const x2 = -totalWidth / 2;
  const y2 = -totalHeight / 2;
  let rect2;
  let { rx, ry } = node;
  const { cssStyles } = node;
  if (options?.rx && options.ry) {
    rx = options.rx;
    ry = options.ry;
  }
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options2 = userNodeOverrides(node, {});
    const roughNode = rx || ry ? rc.path(createRoundedRectPathD(x2, y2, totalWidth, totalHeight, rx || 0), options2) : rc.rectangle(x2, y2, totalWidth, totalHeight, options2);
    rect2 = shapeSvg.insert(() => roughNode, ":first-child");
    rect2.attr("class", "basic label-container").attr("style", cssStyles);
  } else {
    rect2 = shapeSvg.insert("rect", ":first-child");
    rect2.attr("class", "basic label-container").attr("style", nodeStyles).attr("rx", rx).attr("data-id", "abc").attr("data-et", "node").attr("ry", ry).attr("x", x2).attr("y", y2).attr("width", totalWidth).attr("height", totalHeight);
  }
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "drawRect");

// src/rendering-util/rendering-elements/shapes/state.ts
var state = /* @__PURE__ */ __name(async (parent, node) => {
  const options = {
    rx: 5,
    ry: 5,
    classes: "flowchart-node"
  };
  return drawRect(parent, node, options);
}, "state");

// src/rendering-util/rendering-elements/shapes/roundedRect.ts
var roundedRect = /* @__PURE__ */ __name(async (parent, node) => {
  const options = {
    rx: 5,
    ry: 5,
    classes: "",
    labelPaddingX: (node?.padding || 0) * 1,
    labelPaddingY: (node?.padding || 0) * 1
  };
  return drawRect(parent, node, options);
}, "roundedRect");

// src/rendering-util/rendering-elements/shapes/squareRect.ts
var squareRect2 = /* @__PURE__ */ __name(async (parent, node) => {
  const options = {
    rx: 0,
    ry: 0,
    classes: "",
    labelPaddingX: (node?.padding || 0) * 2,
    labelPaddingY: (node?.padding || 0) * 1
  };
  return drawRect(parent, node, options);
}, "squareRect");

// src/rendering-util/rendering-elements/shapes/stateStart.ts
var stateStart = /* @__PURE__ */ __name((parent, node) => {
  const { themeVariables } = getConfig();
  const { lineColor } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", "node default").attr("id", node.domId || node.id);
  let circle3;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const roughNode = rc.circle(0, 0, 14, solidStateFill(lineColor));
    circle3 = shapeSvg.insert(() => roughNode);
  } else {
    circle3 = shapeSvg.insert("circle", ":first-child");
  }
  circle3.attr("class", "state-start").attr("r", 7).attr("width", 14).attr("height", 14);
  updateNodeBounds(node, circle3);
  node.intersect = function(point2) {
    return intersect_default.circle(node, 7, point2);
  };
  return shapeSvg;
}, "stateStart");

// src/rendering-util/rendering-elements/shapes/stateEnd.ts
var stateEnd = /* @__PURE__ */ __name((parent, node) => {
  const { themeVariables } = getConfig();
  const { lineColor } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", "node default").attr("id", node.domId || node.id);
  let circle3;
  let innerCircle;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const roughNode = rc.circle(0, 0, 14, { ...solidStateFill(lineColor), roughness: 0.5 });
    const roughInnerNode = rc.circle(0, 0, 5, { ...solidStateFill(lineColor), fillStyle: "solid" });
    circle3 = shapeSvg.insert(() => roughNode);
    innerCircle = shapeSvg.insert(() => roughInnerNode);
  } else {
    innerCircle = shapeSvg.insert("circle", ":first-child");
    circle3 = shapeSvg.insert("circle", ":first-child");
    circle3.attr("class", "state-start").attr("r", 7).attr("width", 14).attr("height", 14);
    innerCircle.attr("class", "state-end").attr("r", 5).attr("width", 10).attr("height", 10);
  }
  updateNodeBounds(node, circle3);
  node.intersect = function(point2) {
    return intersect_default.circle(node, 7, point2);
  };
  return shapeSvg;
}, "stateEnd");

// src/rendering-util/rendering-elements/shapes/forkJoin.ts
var forkJoin = /* @__PURE__ */ __name((parent, node, dir) => {
  const { themeVariables } = getConfig();
  const { lineColor } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", "node default").attr("id", node.domId || node.id);
  let width = 70;
  let height = 10;
  if (dir === "LR") {
    width = 10;
    height = 70;
  }
  const x2 = -1 * width / 2;
  const y2 = -1 * height / 2;
  let shape;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const roughNode = rc.rectangle(x2, y2, width, height, solidStateFill(lineColor));
    shape = shapeSvg.insert(() => roughNode);
  } else {
    shape = shapeSvg.append("rect").attr("x", x2).attr("y", y2).attr("width", width).attr("height", height).attr("class", "fork-join");
  }
  updateNodeBounds(node, shape);
  let nodeHeight = 0;
  let nodeWidth = 0;
  let nodePadding = 10;
  if (node.height) {
    nodeHeight = node.height;
  }
  if (node.width) {
    nodeWidth = node.width;
  }
  if (node.padding) {
    nodePadding = node.padding;
  }
  node.height = nodeHeight + nodePadding / 2;
  node.width = nodeWidth + nodePadding / 2;
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "forkJoin");

// src/rendering-util/rendering-elements/shapes/choice.ts
var choice = /* @__PURE__ */ __name((parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { themeVariables } = getConfig();
  const { lineColor } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", "node default").attr("id", node.domId || node.id);
  const s2 = 28;
  const points = [
    { x: 0, y: s2 / 2 },
    { x: s2 / 2, y: 0 },
    { x: 0, y: -s2 / 2 },
    { x: -s2 / 2, y: 0 }
  ];
  let choice2;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const pointArr = points.map(function(d2) {
      return [d2.x, d2.y];
    });
    const roughNode = rc.polygon(pointArr, solidStateFill(lineColor));
    choice2 = shapeSvg.insert(() => roughNode);
  } else {
    choice2 = shapeSvg.insert("polygon", ":first-child").attr(
      "points",
      points.map(function(d2) {
        return d2.x + "," + d2.y;
      }).join(" ")
    );
  }
  choice2.attr("class", "state-start").attr("r", 7).attr("width", 28).attr("height", 28).attr("style", nodeStyles);
  node.width = 28;
  node.height = 28;
  node.intersect = function(point2) {
    return intersect_default.circle(node, 14, point2);
  };
  return shapeSvg;
}, "choice");

// src/rendering-util/rendering-elements/shapes/note.ts
var note = /* @__PURE__ */ __name(async (parent, node) => {
  const { themeVariables, handDrawnSeed } = getConfig();
  const { noteBorderColor, noteBkgColor } = themeVariables;
  const useHtmlLabels = node.useHtmlLabels;
  if (!useHtmlLabels) {
    node.centerLabel = true;
  }
  const { shapeSvg, bbox } = await labelHelper(parent, node, "node " + node.cssClasses);
  log.info("Classes = ", node.cssClasses);
  const { cssStyles } = node;
  let rect2;
  const totalWidth = bbox.width + node.padding;
  const totalHeight = bbox.height + node.padding;
  const x2 = -totalWidth / 2;
  const y2 = -totalHeight / 2;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const roughNode = rc.rectangle(x2, y2, totalWidth, totalHeight, {
      roughness: 0.7,
      fill: noteBkgColor,
      fillWeight: 3,
      seed: handDrawnSeed,
      // fillStyle: 'solid', // solid fill'
      stroke: noteBorderColor
    });
    rect2 = shapeSvg.insert(() => roughNode, ":first-child");
    rect2.attr("class", "basic label-container").attr("style", cssStyles);
  } else {
    rect2 = shapeSvg.insert("rect", ":first-child");
    rect2.attr("rx", node.rx).attr("ry", node.ry).attr("x", x2).attr("y", y2).attr("width", totalWidth).attr("height", totalHeight);
  }
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "note");

// src/rendering-util/rendering-elements/shapes/stadium.ts
var stadium = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const h2 = bbox.height + node.padding;
  const w2 = bbox.width + h2 / 4 + node.padding;
  let rect2;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createRoundedRectPathD(-w2 / 2, -h2 / 2, w2, h2, h2 / 2);
    const roughNode = rc.path(pathData, options);
    rect2 = shapeSvg.insert(() => roughNode, ":first-child");
    rect2.attr("class", "basic label-container").attr("style", cssStyles);
  } else {
    rect2 = shapeSvg.insert("rect", ":first-child");
    rect2.attr("class", "basic label-container").attr("style", nodeStyles).attr("rx", h2 / 2).attr("ry", h2 / 2).attr("x", -w2 / 2).attr("y", -h2 / 2).attr("width", w2).attr("height", h2);
  }
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "stadium");

// src/rendering-util/rendering-elements/shapes/rectWithTitle.ts
var rectWithTitle = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  let classes;
  if (!node.cssClasses) {
    classes = "node default";
  } else {
    classes = "node " + node.cssClasses;
  }
  const shapeSvg = parent.insert("g").attr("class", classes).attr("id", node.domId || node.id);
  const g2 = shapeSvg.insert("g");
  const label = shapeSvg.insert("g").attr("class", "label").attr("style", nodeStyles);
  const description = node.description;
  const title = node.label;
  const text = label.node().appendChild(await createLabel_default(title, node.labelStyle, true, true));
  let bbox = { width: 0, height: 0 };
  if (evaluate(getConfig()?.flowchart?.htmlLabels)) {
    const div2 = text.children[0];
    const dv2 = select_default(text);
    bbox = div2.getBoundingClientRect();
    dv2.attr("width", bbox.width);
    dv2.attr("height", bbox.height);
  }
  log.info("Text 2", description);
  const textRows = description || [];
  const titleBox = text.getBBox();
  const descr = label.node().appendChild(
    await createLabel_default(
      textRows.join ? textRows.join("<br/>") : textRows,
      node.labelStyle,
      true,
      true
    )
  );
  const div = descr.children[0];
  const dv = select_default(descr);
  bbox = div.getBoundingClientRect();
  dv.attr("width", bbox.width);
  dv.attr("height", bbox.height);
  const halfPadding = (node.padding || 0) / 2;
  select_default(descr).attr(
    "transform",
    "translate( " + (bbox.width > titleBox.width ? 0 : (titleBox.width - bbox.width) / 2) + ", " + (titleBox.height + halfPadding + 5) + ")"
  );
  select_default(text).attr(
    "transform",
    "translate( " + (bbox.width < titleBox.width ? 0 : -(titleBox.width - bbox.width) / 2) + ", 0)"
  );
  bbox = label.node().getBBox();
  label.attr(
    "transform",
    "translate(" + -bbox.width / 2 + ", " + (-bbox.height / 2 - halfPadding + 3) + ")"
  );
  const totalWidth = bbox.width + (node.padding || 0);
  const totalHeight = bbox.height + (node.padding || 0);
  const x2 = -bbox.width / 2 - halfPadding;
  const y2 = -bbox.height / 2 - halfPadding;
  let rect2;
  let innerLine;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const roughNode = rc.path(
      createRoundedRectPathD(x2, y2, totalWidth, totalHeight, node.rx || 0),
      options
    );
    const roughLine = rc.line(
      -bbox.width / 2 - halfPadding,
      -bbox.height / 2 - halfPadding + titleBox.height + halfPadding,
      bbox.width / 2 + halfPadding,
      -bbox.height / 2 - halfPadding + titleBox.height + halfPadding,
      options
    );
    innerLine = shapeSvg.insert(() => {
      log.debug("Rough node insert CXC", roughNode);
      return roughLine;
    }, ":first-child");
    rect2 = shapeSvg.insert(() => {
      log.debug("Rough node insert CXC", roughNode);
      return roughNode;
    }, ":first-child");
  } else {
    rect2 = g2.insert("rect", ":first-child");
    innerLine = g2.insert("line");
    rect2.attr("class", "outer title-state").attr("style", nodeStyles).attr("x", -bbox.width / 2 - halfPadding).attr("y", -bbox.height / 2 - halfPadding).attr("width", bbox.width + (node.padding || 0)).attr("height", bbox.height + (node.padding || 0));
    innerLine.attr("class", "divider").attr("x1", -bbox.width / 2 - halfPadding).attr("x2", bbox.width / 2 + halfPadding).attr("y1", -bbox.height / 2 - halfPadding + titleBox.height + halfPadding).attr("y2", -bbox.height / 2 - halfPadding + titleBox.height + halfPadding);
  }
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "rectWithTitle");

// src/rendering-util/rendering-elements/shapes/insertPolygonShape.ts
function insertPolygonShape(parent, w2, h2, points) {
  return parent.insert("polygon", ":first-child").attr(
    "points",
    points.map(function(d2) {
      return d2.x + "," + d2.y;
    }).join(" ")
  ).attr("class", "label-container").attr("transform", "translate(" + -w2 / 2 + "," + h2 / 2 + ")");
}
__name(insertPolygonShape, "insertPolygonShape");

// src/rendering-util/rendering-elements/shapes/subroutine.ts
var subroutine = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const halfPadding = (node?.padding || 0) / 2;
  const w2 = bbox.width + node.padding;
  const h2 = bbox.height + node.padding;
  const x2 = -bbox.width / 2 - halfPadding;
  const y2 = -bbox.height / 2 - halfPadding;
  const points = [
    { x: 0, y: 0 },
    { x: w2, y: 0 },
    { x: w2, y: -h2 },
    { x: 0, y: -h2 },
    { x: 0, y: 0 },
    { x: -8, y: 0 },
    { x: w2 + 8, y: 0 },
    { x: w2 + 8, y: -h2 },
    { x: -8, y: -h2 },
    { x: -8, y: 0 }
  ];
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const roughNode = rc.rectangle(x2 - 8, y2, w2 + 16, h2, options);
    const l1 = rc.line(x2, y2, x2, y2 + h2, options);
    const l2 = rc.line(x2 + w2, y2, x2 + w2, y2 + h2, options);
    shapeSvg.insert(() => l1, ":first-child");
    shapeSvg.insert(() => l2, ":first-child");
    const rect2 = shapeSvg.insert(() => roughNode, ":first-child");
    const { cssStyles } = node;
    rect2.attr("class", "basic label-container").attr("style", cssStyles);
    updateNodeBounds(node, rect2);
  } else {
    const el = insertPolygonShape(shapeSvg, w2, h2, points);
    if (nodeStyles) {
      el.attr("style", nodeStyles);
    }
    updateNodeBounds(node, el);
  }
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "subroutine");

// src/rendering-util/rendering-elements/shapes/cylinder.ts
var createCylinderPathD = /* @__PURE__ */ __name((x2, y2, width, height, rx, ry) => {
  return [
    `M${x2},${y2 + ry}`,
    `a${rx},${ry} 0,0,0 ${width},0`,
    `a${rx},${ry} 0,0,0 ${-width},0`,
    `l0,${height}`,
    `a${rx},${ry} 0,0,0 ${width},0`,
    `l0,${-height}`
  ].join(" ");
}, "createCylinderPathD");
var createOuterCylinderPathD = /* @__PURE__ */ __name((x2, y2, width, height, rx, ry) => {
  return [
    `M${x2},${y2 + ry}`,
    `M${x2 + width},${y2 + ry}`,
    `a${rx},${ry} 0,0,0 ${-width},0`,
    `l0,${height}`,
    `a${rx},${ry} 0,0,0 ${width},0`,
    `l0,${-height}`
  ].join(" ");
}, "createOuterCylinderPathD");
var createInnerCylinderPathD = /* @__PURE__ */ __name((x2, y2, width, height, rx, ry) => {
  return [`M${x2 - width / 2},${-height / 2}`, `a${rx},${ry} 0,0,0 ${width},0`].join(" ");
}, "createInnerCylinderPathD");
var cylinder = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w2 = bbox.width + node.padding;
  const rx = w2 / 2;
  const ry = rx / (2.5 + w2 / 50);
  const h2 = bbox.height + ry + node.padding;
  let cylinder2;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const outerPathData = createOuterCylinderPathD(0, 0, w2, h2, rx, ry);
    const innerPathData = createInnerCylinderPathD(0, ry, w2, h2, rx, ry);
    const outerNode = rc.path(outerPathData, userNodeOverrides(node, {}));
    const innerLine = rc.path(innerPathData, userNodeOverrides(node, { fill: "none" }));
    cylinder2 = shapeSvg.insert(() => innerLine, ":first-child");
    cylinder2 = shapeSvg.insert(() => outerNode, ":first-child");
    cylinder2.attr("class", "basic label-container");
    if (cssStyles) {
      cylinder2.attr("style", cssStyles);
    }
  } else {
    const pathData = createCylinderPathD(0, 0, w2, h2, rx, ry);
    cylinder2 = shapeSvg.insert("path", ":first-child").attr("d", pathData).attr("class", "basic label-container").attr("style", cssStyles).attr("style", nodeStyles);
  }
  cylinder2.attr("label-offset-y", ry);
  cylinder2.attr("transform", `translate(${-w2 / 2}, ${-(h2 / 2 + ry)})`);
  updateNodeBounds(node, cylinder2);
  node.intersect = function(point2) {
    const pos = intersect_default.rect(node, point2);
    const x2 = pos.x - (node.x ?? 0);
    if (rx != 0 && (Math.abs(x2) < (node.width ?? 0) / 2 || Math.abs(x2) == (node.width ?? 0) / 2 && Math.abs(pos.y - (node.y ?? 0)) > (node.height ?? 0) / 2 - ry)) {
      let y2 = ry * ry * (1 - x2 * x2 / (rx * rx));
      if (y2 > 0) {
        y2 = Math.sqrt(y2);
      }
      y2 = ry - y2;
      if (point2.y - (node.y ?? 0) > 0) {
        y2 = -y2;
      }
      pos.y += y2;
    }
    return pos;
  };
  return shapeSvg;
}, "cylinder");

// src/rendering-util/rendering-elements/shapes/circle.ts
var circle2 = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox, halfPadding } = await labelHelper(parent, node, getNodeClasses(node));
  const radius = bbox.width / 2 + halfPadding;
  let circleElem;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const roughNode = rc.circle(0, 0, radius * 2, options);
    circleElem = shapeSvg.insert(() => roughNode, ":first-child");
    circleElem.attr("class", "basic label-container").attr("style", cssStyles);
  } else {
    circleElem = shapeSvg.insert("circle", ":first-child").attr("class", "basic label-container").attr("style", nodeStyles).attr("r", radius).attr("cx", 0).attr("cy", 0);
  }
  updateNodeBounds(node, circleElem);
  node.intersect = function(point2) {
    log.info("Circle intersect", node, radius, point2);
    return intersect_default.circle(node, radius, point2);
  };
  return shapeSvg;
}, "circle");

// src/rendering-util/rendering-elements/shapes/doubleCircle.ts
var doublecircle = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox, halfPadding } = await labelHelper(parent, node, getNodeClasses(node));
  const gap = 5;
  const outerRadius = bbox.width / 2 + halfPadding + gap;
  const innerRadius = bbox.width / 2 + halfPadding;
  let circleGroup;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const outerOptions = userNodeOverrides(node, { roughness: 0.2, strokeWidth: 2.5 });
    const innerOptions = userNodeOverrides(node, { roughness: 0.2, strokeWidth: 1.5 });
    const outerRoughNode = rc.circle(0, 0, outerRadius * 2, outerOptions);
    const innerRoughNode = rc.circle(0, 0, innerRadius * 2, innerOptions);
    circleGroup = shapeSvg.insert("g", ":first-child");
    circleGroup.attr("class", node.cssClasses).attr("style", cssStyles);
    circleGroup.node()?.appendChild(outerRoughNode);
    circleGroup.node()?.appendChild(innerRoughNode);
  } else {
    circleGroup = shapeSvg.insert("g", ":first-child");
    const outerCircle = circleGroup.insert("circle", ":first-child");
    const innerCircle = circleGroup.insert("circle");
    circleGroup.attr("class", "basic label-container").attr("style", nodeStyles);
    outerCircle.attr("class", "outer-circle").attr("style", nodeStyles).attr("r", outerRadius).attr("cx", 0).attr("cy", 0);
    innerCircle.attr("class", "inner-circle").attr("style", nodeStyles).attr("r", innerRadius).attr("cx", 0).attr("cy", 0);
  }
  updateNodeBounds(node, circleGroup);
  node.intersect = function(point2) {
    log.info("DoubleCircle intersect", node, outerRadius, point2);
    return intersect_default.circle(node, outerRadius, point2);
  };
  return shapeSvg;
}, "doublecircle");

// src/rendering-util/rendering-elements/shapes/rectLeftInvArrow.ts
var createPolygonPathD = /* @__PURE__ */ __name((x2, y2, width, height) => {
  return [
    `M${x2 - height / 2},${y2}`,
    `L${x2 + width},${y2}`,
    `L${x2 + width},${y2 - height}`,
    `L${x2 - height / 2},${y2 - height}`,
    `L${x2},${y2 - height / 2}`,
    "Z"
  ].join(" ");
}, "createPolygonPathD");
var rect_left_inv_arrow = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w2 = bbox.width + node.padding;
  const h2 = bbox.height + node.padding;
  const points = [
    { x: -h2 / 2, y: 0 },
    { x: w2, y: 0 },
    { x: w2, y: -h2 },
    { x: -h2 / 2, y: -h2 },
    { x: 0, y: -h2 / 2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createPolygonPathD(0, 0, w2, h2);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w2 / 2}, ${h2 / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w2, h2, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w2 + h2;
  node.height = h2;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "rect_left_inv_arrow");

// src/rendering-util/rendering-elements/shapes/question.ts
var createDecisionBoxPathD = /* @__PURE__ */ __name((x2, y2, size) => {
  return [
    `M${x2 + size / 2},${y2}`,
    `L${x2 + size},${y2 - size / 2}`,
    `L${x2 + size / 2},${y2 - size}`,
    `L${x2},${y2 - size / 2}`,
    "Z"
  ].join(" ");
}, "createDecisionBoxPathD");
var question = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w2 = bbox.width + node.padding;
  const h2 = bbox.height + node.padding;
  const s2 = w2 + h2;
  const points = [
    { x: s2 / 2, y: 0 },
    { x: s2, y: -s2 / 2 },
    { x: s2 / 2, y: -s2 },
    { x: 0, y: -s2 / 2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createDecisionBoxPathD(0, 0, s2);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-s2 / 2}, ${s2 / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, s2, s2, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    log.debug(
      "APA12 Intersect called SPLIT\npoint:",
      point2,
      "\nnode:\n",
      node,
      "\nres:",
      intersect_default.polygon(node, points, point2)
    );
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "question");

// src/rendering-util/rendering-elements/shapes/hexagon.ts
var createHexagonPathD = /* @__PURE__ */ __name((x2, y2, width, height, m2) => {
  return [
    `M${x2 + m2},${y2}`,
    `L${x2 + width - m2},${y2}`,
    `L${x2 + width},${y2 - height / 2}`,
    `L${x2 + width - m2},${y2 - height}`,
    `L${x2 + m2},${y2 - height}`,
    `L${x2},${y2 - height / 2}`,
    "Z"
  ].join(" ");
}, "createHexagonPathD");
var hexagon = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const f2 = 4;
  const h2 = bbox.height + node.padding;
  const m2 = h2 / f2;
  const w2 = bbox.width + 2 * m2 + node.padding;
  const points = [
    { x: m2, y: 0 },
    { x: w2 - m2, y: 0 },
    { x: w2, y: -h2 / 2 },
    { x: w2 - m2, y: -h2 },
    { x: m2, y: -h2 },
    { x: 0, y: -h2 / 2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createHexagonPathD(0, 0, w2, h2, m2);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w2 / 2}, ${h2 / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w2, h2, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w2;
  node.height = h2;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "hexagon");

// src/rendering-util/rendering-elements/shapes/leanRight.ts
var createLeanRightPathD = /* @__PURE__ */ __name((x2, y2, width, height) => {
  return [
    `M${x2 - 2 * height / 6},${y2}`,
    `L${x2 + width - height / 6},${y2}`,
    `L${x2 + width + 2 * height / 6},${y2 - height}`,
    `L${x2 + height / 6},${y2 - height}`,
    "Z"
  ].join(" ");
}, "createLeanRightPathD");
var lean_right = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w2 = bbox.width + node.padding;
  const h2 = bbox.height + node.padding;
  const points = [
    { x: -2 * h2 / 6, y: 0 },
    { x: w2 - h2 / 6, y: 0 },
    { x: w2 + 2 * h2 / 6, y: -h2 },
    { x: h2 / 6, y: -h2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createLeanRightPathD(0, 0, w2, h2);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w2 / 2}, ${h2 / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w2, h2, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w2;
  node.height = h2;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "lean_right");

// src/rendering-util/rendering-elements/shapes/leanLeft.ts
var createLeanLeftPathD = /* @__PURE__ */ __name((x2, y2, width, height) => {
  return [
    `M${x2 + 2 * height / 6},${y2}`,
    `L${x2 + width + height / 6},${y2}`,
    `L${x2 + width - 2 * height / 6},${y2 - height}`,
    `L${x2 - height / 6},${y2 - height}`,
    "Z"
  ].join(" ");
}, "createLeanLeftPathD");
var lean_left = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w2 = bbox.width + node.padding;
  const h2 = bbox.height + node.padding;
  const points = [
    { x: 2 * h2 / 6, y: 0 },
    { x: w2 + h2 / 6, y: 0 },
    { x: w2 - 2 * h2 / 6, y: -h2 },
    { x: -h2 / 6, y: -h2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createLeanLeftPathD(0, 0, w2, h2);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w2 / 2}, ${h2 / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w2, h2, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w2;
  node.height = h2;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "lean_left");

// src/rendering-util/rendering-elements/shapes/trapezoid.ts
var createTrapezoidPathD = /* @__PURE__ */ __name((x2, y2, width, height) => {
  return [
    `M${x2 - 2 * height / 6},${y2}`,
    `L${x2 + width + 2 * height / 6},${y2}`,
    `L${x2 + width - height / 6},${y2 - height}`,
    `L${x2 + height / 6},${y2 - height}`,
    "Z"
  ].join(" ");
}, "createTrapezoidPathD");
var trapezoid = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w2 = bbox.width + node.padding;
  const h2 = bbox.height + node.padding;
  const points = [
    { x: -2 * h2 / 6, y: 0 },
    { x: w2 + 2 * h2 / 6, y: 0 },
    { x: w2 - h2 / 6, y: -h2 },
    { x: h2 / 6, y: -h2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createTrapezoidPathD(0, 0, w2, h2);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w2 / 2}, ${h2 / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w2, h2, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w2;
  node.height = h2;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "trapezoid");

// src/rendering-util/rendering-elements/shapes/invertedTrapezoid.ts
var createInvertedTrapezoidPathD = /* @__PURE__ */ __name((x2, y2, width, height) => {
  return [
    `M${x2 + height / 6},${y2}`,
    `L${x2 + width - height / 6},${y2}`,
    `L${x2 + width + 2 * height / 6},${y2 - height}`,
    `L${x2 - 2 * height / 6},${y2 - height}`,
    "Z"
  ].join(" ");
}, "createInvertedTrapezoidPathD");
var inv_trapezoid = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w2 = bbox.width + node.padding;
  const h2 = bbox.height + node.padding;
  const points = [
    { x: h2 / 6, y: 0 },
    { x: w2 - h2 / 6, y: 0 },
    { x: w2 + 2 * h2 / 6, y: -h2 },
    { x: -2 * h2 / 6, y: -h2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = at.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createInvertedTrapezoidPathD(0, 0, w2, h2);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w2 / 2}, ${h2 / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w2, h2, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w2;
  node.height = h2;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "inv_trapezoid");

// src/rendering-util/rendering-elements/shapes/labelRect.ts
var labelRect = /* @__PURE__ */ __name(async (parent, node) => {
  const { shapeSvg } = await labelHelper(parent, node, "label");
  const rect2 = shapeSvg.insert("rect", ":first-child");
  const totalWidth = 0.1;
  const totalHeight = 0.1;
  rect2.attr("width", totalWidth).attr("height", totalHeight);
  shapeSvg.attr("class", "label edgeLabel");
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "labelRect");

// src/rendering-util/rendering-elements/nodes.js
var shapes2 = {
  state,
  stateStart,
  stateEnd,
  fork: forkJoin,
  join: forkJoin,
  choice,
  note,
  roundedRect,
  rectWithTitle,
  squareRect: squareRect2,
  stadium,
  subroutine,
  cylinder,
  circle: circle2,
  doublecircle,
  odd: rect_left_inv_arrow,
  diamond: question,
  hexagon,
  lean_right,
  lean_left,
  trapezoid,
  inv_trapezoid,
  labelRect
};
var nodeElems = /* @__PURE__ */ new Map();
var insertNode = /* @__PURE__ */ __name(async (elem, node, dir) => {
  let newEl;
  let el;
  if (node.shape === "rect") {
    if (node.rx && node.ry) {
      node.shape = "roundedRect";
    } else {
      node.shape = "squareRect";
    }
  }
  if (node.link) {
    let target;
    if (getConfig().securityLevel === "sandbox") {
      target = "_top";
    } else if (node.linkTarget) {
      target = node.linkTarget || "_blank";
    }
    newEl = elem.insert("svg:a").attr("xlink:href", node.link).attr("target", target);
    el = await shapes2[node.shape](newEl, node, dir);
  } else {
    el = await shapes2[node.shape](elem, node, dir);
    newEl = el;
  }
  if (node.tooltip) {
    el.attr("title", node.tooltip);
  }
  nodeElems.set(node.id, newEl);
  if (node.haveCallback) {
    nodeElems.get(node.id).attr("class", nodeElems.get(node.id).attr("class") + " clickable");
  }
  return newEl;
}, "insertNode");
var setNodeElem = /* @__PURE__ */ __name((elem, node) => {
  nodeElems.set(node.id, elem);
}, "setNodeElem");
var clear3 = /* @__PURE__ */ __name(() => {
  nodeElems.clear();
}, "clear");
var positionNode = /* @__PURE__ */ __name((node) => {
  const el = nodeElems.get(node.id);
  log.trace(
    "Transforming node",
    node.diff,
    node,
    "translate(" + (node.x - node.width / 2 - 5) + ", " + node.width / 2 + ")"
  );
  const padding = 8;
  const diff = node.diff || 0;
  if (node.clusterNode) {
    el.attr(
      "transform",
      "translate(" + (node.x + diff - node.width / 2) + ", " + (node.y - node.height / 2 - padding) + ")"
    );
  } else {
    el.attr("transform", "translate(" + node.x + ", " + node.y + ")");
  }
  return diff;
}, "positionNode");

export {
  insertCluster,
  clear,
  clear2,
  insertEdgeLabel,
  positionEdgeLabel,
  insertEdge,
  markers_default,
  labelHelper,
  updateNodeBounds,
  insertNode,
  setNodeElem,
  clear3,
  positionNode
};
