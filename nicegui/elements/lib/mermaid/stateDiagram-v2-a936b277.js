import { D as Q, a as U, b as X, S as Z, c as j, e as I, p as tt, d as v, s as et } from "./styles-d2effb1a.js";
import { G as ot } from "./layout-d6d8be39.js";
import { l as a, g, f as x, e as G } from "./config-e567ef17.js";
import { r as st } from "./index-e6caf2ad.js";
import { c as nt } from "./setupGraphViewbox-a4603a92.js";
import { u as ct } from "./utils-aa888deb.js";
import "./mermaidAPI-04b5c286.js";
import "./errorRenderer-a3c4bedb.js";
import "./commonDb-4dc3d465.js";
import "./isPlainObject-a5cb4071.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
import "./edges-0979260b.js";
import "./svgDraw-c034b55e.js";
const h = "rect", C = "rectWithTitle", it = "start", rt = "end", lt = "divider", at = "roundedWithTitle", dt = "note", Et = "noteGroup", p = "statediagram", St = "state", Tt = `${p}-${St}`, V = "transition", pt = "note", _t = "note-edge", ft = `${V} ${_t}`, ut = `${p}-${pt}`, Dt = "cluster", At = `${p}-${Dt}`, bt = "cluster-alt", ht = `${p}-${bt}`, m = "parent", Y = "note", yt = "state", N = "----", gt = `${N}${Y}`, H = `${N}${m}`, W = "fill:none", z = "fill: #333", q = "c", K = "text", F = "normal";
let y = {}, E = 0;
const Rt = function(t) {
  const n = Object.keys(t);
  for (const o of n)
    t[o];
}, xt = function(t, n) {
  a.trace("Extracting classes"), n.db.clear();
  try {
    return n.parser.parse(t), n.db.extract(n.db.getRootDocV2()), n.db.getClasses();
  } catch (o) {
    return o;
  }
};
function Ct(t) {
  return t == null ? "" : t.classes ? t.classes.join(" ") : "";
}
function $(t = "", n = 0, o = "", c = N) {
  const i = o !== null && o.length > 0 ? `${c}${o}` : "";
  return `${yt}-${t}${i}-${n}`;
}
const D = (t, n, o, c, i, r) => {
  const e = o.id, _ = Ct(c[e]);
  if (e !== "root") {
    let T = h;
    o.start === !0 && (T = it), o.start === !1 && (T = rt), o.type !== U && (T = o.type), y[e] || (y[e] = {
      id: e,
      shape: T,
      description: G.sanitizeText(e, g()),
      classes: `${_} ${Tt}`
    });
    const s = y[e];
    o.description && (Array.isArray(s.description) ? (s.shape = C, s.description.push(o.description)) : s.description.length > 0 ? (s.shape = C, s.description === e ? s.description = [o.description] : s.description = [s.description, o.description]) : (s.shape = h, s.description = o.description), s.description = G.sanitizeTextOrArray(s.description, g())), s.description.length === 1 && s.shape === C && (s.shape = h), !s.type && o.doc && (a.info("Setting cluster for ", e, w(o)), s.type = "group", s.dir = w(o), s.shape = o.type === X ? lt : at, s.classes = s.classes + " " + At + " " + (r ? ht : ""));
    const f = {
      labelStyle: "",
      shape: s.shape,
      labelText: s.description,
      // typeof newNode.description === 'object'
      //   ? newNode.description[0]
      //   : newNode.description,
      classes: s.classes,
      style: "",
      //styles.style,
      id: e,
      dir: s.dir,
      domId: $(e, E),
      type: s.type,
      padding: 15
      //getConfig().flowchart.padding
    };
    if (o.note) {
      const d = {
        labelStyle: "",
        shape: dt,
        labelText: o.note.text,
        classes: ut,
        style: "",
        // styles.style,
        id: e + gt + "-" + E,
        domId: $(e, E, Y),
        type: s.type,
        padding: 15
        //getConfig().flowchart.padding
      }, A = {
        labelStyle: "",
        shape: Et,
        labelText: o.note.text,
        classes: s.classes,
        style: "",
        // styles.style,
        id: e + H,
        domId: $(e, E, m),
        type: "group",
        padding: 0
        //getConfig().flowchart.padding
      };
      E++;
      const l = e + H;
      t.setNode(l, A), t.setNode(d.id, d), t.setNode(e, f), t.setParent(e, l), t.setParent(d.id, l);
      let b = e, S = d.id;
      o.note.position === "left of" && (b = d.id, S = e), t.setEdge(b, S, {
        arrowhead: "none",
        arrowType: "",
        style: W,
        labelStyle: "",
        classes: ft,
        arrowheadStyle: z,
        labelpos: q,
        labelType: K,
        thickness: F
      });
    } else
      t.setNode(e, f);
  }
  n && n.id !== "root" && (a.trace("Setting node ", e, " to be child of its parent ", n.id), t.setParent(e, n.id)), o.doc && (a.trace("Adding nodes children "), $t(t, o, o.doc, c, i, !r));
}, $t = (t, n, o, c, i, r) => {
  a.trace("items", o), o.forEach((e) => {
    switch (e.stmt) {
      case j:
        D(t, n, e, c, i, r);
        break;
      case U:
        D(t, n, e, c, i, r);
        break;
      case Z:
        {
          D(t, n, e.state1, c, i, r), D(t, n, e.state2, c, i, r);
          const _ = {
            id: "edge" + E,
            arrowhead: "normal",
            arrowTypeEnd: "arrow_barb",
            style: W,
            labelStyle: "",
            label: G.sanitizeText(e.description, g()),
            arrowheadStyle: z,
            labelpos: q,
            labelType: K,
            thickness: F,
            classes: V
          };
          t.setEdge(e.state1.id, e.state2.id, _, E), E++;
        }
        break;
    }
  });
}, w = (t, n = I) => {
  let o = n;
  if (t.doc)
    for (let c = 0; c < t.doc.length; c++) {
      const i = t.doc[c];
      i.stmt === "dir" && (o = i.value);
    }
  return o;
}, Gt = function(t, n, o, c) {
  a.info("Drawing state diagram (v2)", n), y = {};
  let i = c.db.getDirection();
  i === void 0 && (i = Q);
  const { securityLevel: r, state: e } = g(), _ = e.nodeSpacing || 50, T = e.rankSpacing || 50;
  a.info(c.db.getRootDocV2()), c.db.extract(c.db.getRootDocV2()), a.info(c.db.getRootDocV2());
  const s = c.db.getStates(), f = new ot({
    multigraph: !0,
    compound: !0
  }).setGraph({
    rankdir: w(c.db.getRootDocV2()),
    nodesep: _,
    ranksep: T,
    marginx: 8,
    marginy: 8
  }).setDefaultEdgeLabel(function() {
    return {};
  });
  D(f, void 0, c.db.getRootDocV2(), s, c.db, !0);
  let d;
  r === "sandbox" && (d = x("#i" + n));
  const A = r === "sandbox" ? x(d.nodes()[0].contentDocument.body) : x("body"), l = A.select(`[id="${n}"]`), b = A.select("#" + n + " g");
  st(b, f, ["barb"], p, n);
  const S = 8;
  ct.insertTitle(l, "statediagramTitleText", e.titleTopMargin, c.db.getDiagramTitle());
  const L = l.node().getBBox(), P = L.width + S * 2, O = L.height + S * 2;
  l.attr("class", p);
  const k = l.node().getBBox();
  nt(l, O, P, e.useMaxWidth);
  const M = `${k.x - S} ${k.y - S} ${P} ${O}`;
  a.debug(`viewBox ${M}`), l.attr("viewBox", M);
  const J = document.querySelectorAll('[id="' + n + '"] .edgeLabel .label');
  for (const R of J) {
    const B = R.getBBox(), u = document.createElementNS("http://www.w3.org/2000/svg", h);
    u.setAttribute("rx", 0), u.setAttribute("ry", 0), u.setAttribute("width", B.width), u.setAttribute("height", B.height), R.insertBefore(u, R.firstChild);
  }
}, wt = {
  setConf: Rt,
  getClasses: xt,
  draw: Gt
}, zt = {
  parser: tt,
  db: v,
  renderer: wt,
  styles: et,
  init: (t) => {
    t.state || (t.state = {}), t.state.arrowMarkerAbsolute = t.arrowMarkerAbsolute, v.clear();
  }
};
export {
  zt as diagram
};
//# sourceMappingURL=stateDiagram-v2-a936b277.js.map
