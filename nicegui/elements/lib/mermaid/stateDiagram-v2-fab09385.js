import { D as H, a as Q, S as X, b as Z, c as j, p as F, d as M, s as I } from "./styles-be2d7003.js";
import { G as tt } from "./layout-b178bd1a.js";
import { l, c as g, j as $, x as et, k as st, f as w } from "./mermaid-be6aa4a6.js";
import { r as ot } from "./index-745c9ffe.js";
import "./edges-1ceb0db9.js";
import "./createText-7fe61f7a.js";
import "./svgDraw-51404f3b.js";
import "./line-d1abfd73.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
const h = "rect", C = "rectWithTitle", nt = "start", ct = "end", it = "divider", rt = "roundedWithTitle", lt = "note", at = "noteGroup", u = "statediagram", dt = "state", Et = `${u}-${dt}`, U = "transition", St = "note", Tt = "note-edge", pt = `${U} ${Tt}`, ut = `${u}-${St}`, _t = "cluster", ft = `${u}-${_t}`, Dt = "cluster-alt", bt = `${u}-${Dt}`, V = "parent", Y = "note", At = "state", N = "----", ht = `${N}${Y}`, v = `${N}${V}`, W = "fill:none", z = "fill: #333", m = "c", q = "text", K = "normal";
let y = {}, E = 0;
const yt = function(t) {
  const n = Object.keys(t);
  for (const e of n)
    t[e];
}, gt = function(t, n) {
  l.trace("Extracting classes"), n.db.clear();
  try {
    return n.parser.parse(t), n.db.extract(n.db.getRootDocV2()), n.db.getClasses();
  } catch (e) {
    return e;
  }
};
function xt(t) {
  return t == null ? "" : t.classes ? t.classes.join(" ") : "";
}
function R(t = "", n = 0, e = "", c = N) {
  const i = e !== null && e.length > 0 ? `${c}${e}` : "";
  return `${At}-${t}${i}-${n}`;
}
const A = (t, n, e, c, i, r) => {
  const s = e.id, _ = xt(c[s]);
  if (s !== "root") {
    let T = h;
    e.start === !0 && (T = nt), e.start === !1 && (T = ct), e.type !== H && (T = e.type), y[s] || (y[s] = {
      id: s,
      shape: T,
      description: w.sanitizeText(s, g()),
      classes: `${_} ${Et}`
    });
    const o = y[s];
    e.description && (Array.isArray(o.description) ? (o.shape = C, o.description.push(e.description)) : o.description.length > 0 ? (o.shape = C, o.description === s ? o.description = [e.description] : o.description = [o.description, e.description]) : (o.shape = h, o.description = e.description), o.description = w.sanitizeTextOrArray(o.description, g())), o.description.length === 1 && o.shape === C && (o.shape = h), !o.type && e.doc && (l.info("Setting cluster for ", s, G(e)), o.type = "group", o.dir = G(e), o.shape = e.type === Q ? it : rt, o.classes = o.classes + " " + ft + " " + (r ? bt : ""));
    const p = {
      labelStyle: "",
      shape: o.shape,
      labelText: o.description,
      // typeof newNode.description === 'object'
      //   ? newNode.description[0]
      //   : newNode.description,
      classes: o.classes,
      style: "",
      //styles.style,
      id: s,
      dir: o.dir,
      domId: R(s, E),
      type: o.type,
      padding: 15
      //getConfig().flowchart.padding
    };
    if (p.centerLabel = !0, e.note) {
      const a = {
        labelStyle: "",
        shape: lt,
        labelText: e.note.text,
        classes: ut,
        // useHtmlLabels: false,
        style: "",
        // styles.style,
        id: s + ht + "-" + E,
        domId: R(s, E, Y),
        type: o.type,
        padding: 15
        //getConfig().flowchart.padding
      }, d = {
        labelStyle: "",
        shape: at,
        labelText: e.note.text,
        classes: o.classes,
        style: "",
        // styles.style,
        id: s + v,
        domId: R(s, E, V),
        type: "group",
        padding: 0
        //getConfig().flowchart.padding
      };
      E++;
      const f = s + v;
      t.setNode(f, d), t.setNode(a.id, a), t.setNode(s, p), t.setParent(s, f), t.setParent(a.id, f);
      let S = s, D = a.id;
      e.note.position === "left of" && (S = a.id, D = s), t.setEdge(S, D, {
        arrowhead: "none",
        arrowType: "",
        style: W,
        labelStyle: "",
        classes: pt,
        arrowheadStyle: z,
        labelpos: m,
        labelType: q,
        thickness: K
      });
    } else
      t.setNode(s, p);
  }
  n && n.id !== "root" && (l.trace("Setting node ", s, " to be child of its parent ", n.id), t.setParent(s, n.id)), e.doc && (l.trace("Adding nodes children "), $t(t, e, e.doc, c, i, !r));
}, $t = (t, n, e, c, i, r) => {
  l.trace("items", e), e.forEach((s) => {
    switch (s.stmt) {
      case Z:
        A(t, n, s, c, i, r);
        break;
      case H:
        A(t, n, s, c, i, r);
        break;
      case X:
        {
          A(t, n, s.state1, c, i, r), A(t, n, s.state2, c, i, r);
          const _ = {
            id: "edge" + E,
            arrowhead: "normal",
            arrowTypeEnd: "arrow_barb",
            style: W,
            labelStyle: "",
            label: w.sanitizeText(s.description, g()),
            arrowheadStyle: z,
            labelpos: m,
            labelType: q,
            thickness: K,
            classes: U
          };
          t.setEdge(s.state1.id, s.state2.id, _, E), E++;
        }
        break;
    }
  });
}, G = (t, n = j) => {
  let e = n;
  if (t.doc)
    for (let c = 0; c < t.doc.length; c++) {
      const i = t.doc[c];
      i.stmt === "dir" && (e = i.value);
    }
  return e;
}, Ct = async function(t, n, e, c) {
  l.info("Drawing state diagram (v2)", n), y = {}, c.db.getDirection();
  const { securityLevel: i, state: r } = g(), s = r.nodeSpacing || 50, _ = r.rankSpacing || 50;
  l.info(c.db.getRootDocV2()), c.db.extract(c.db.getRootDocV2()), l.info(c.db.getRootDocV2());
  const T = c.db.getStates(), o = new tt({
    multigraph: !0,
    compound: !0
  }).setGraph({
    rankdir: G(c.db.getRootDocV2()),
    nodesep: s,
    ranksep: _,
    marginx: 8,
    marginy: 8
  }).setDefaultEdgeLabel(function() {
    return {};
  });
  A(o, void 0, c.db.getRootDocV2(), T, c.db, !0);
  let p;
  i === "sandbox" && (p = $("#i" + n));
  const a = i === "sandbox" ? $(p.nodes()[0].contentDocument.body) : $("body"), d = a.select(`[id="${n}"]`), f = a.select("#" + n + " g");
  await ot(f, o, ["barb"], u, n);
  const S = 8;
  et.insertTitle(d, "statediagramTitleText", r.titleTopMargin, c.db.getDiagramTitle());
  const D = d.node().getBBox(), L = D.width + S * 2, P = D.height + S * 2;
  d.attr("class", u);
  const k = d.node().getBBox();
  st(d, P, L, r.useMaxWidth);
  const O = `${k.x - S} ${k.y - S} ${L} ${P}`;
  l.debug(`viewBox ${O}`), d.attr("viewBox", O);
  const J = document.querySelectorAll('[id="' + n + '"] .edgeLabel .label');
  for (const x of J) {
    const B = x.getBBox(), b = document.createElementNS("http://www.w3.org/2000/svg", h);
    b.setAttribute("rx", 0), b.setAttribute("ry", 0), b.setAttribute("width", B.width), b.setAttribute("height", B.height), x.insertBefore(b, x.firstChild);
  }
}, Rt = {
  setConf: yt,
  getClasses: gt,
  draw: Ct
}, Ht = {
  parser: F,
  db: M,
  renderer: Rt,
  styles: I,
  init: (t) => {
    t.state || (t.state = {}), t.state.arrowMarkerAbsolute = t.arrowMarkerAbsolute, M.clear();
  }
};
export {
  Ht as diagram
};
