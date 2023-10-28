import { D as H, a as J, S as Q, b as X, c as Z, p as F, d as M, s as I } from "./styles-554c1edb.js";
import { G as tt } from "./layout-1caf14c9.js";
import { l as E, c as g, j as $, z as et, k as ot, f as w } from "./mermaid-5f2d2ec5.js";
import { r as st } from "./index-08d47d0a.js";
import "./edges-345e4ceb.js";
import "./createText-56dbee71.js";
import "./line-9d49a987.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
const h = "rect", C = "rectWithTitle", nt = "start", ct = "end", it = "divider", rt = "roundedWithTitle", lt = "note", at = "noteGroup", _ = "statediagram", dt = "state", Et = `${_}-${dt}`, U = "transition", St = "note", Tt = "note-edge", pt = `${U} ${Tt}`, _t = `${_}-${St}`, ut = "cluster", ft = `${_}-${ut}`, Dt = "cluster-alt", bt = `${_}-${Dt}`, V = "parent", Y = "note", At = "state", N = "----", ht = `${N}${Y}`, v = `${N}${V}`, z = "fill:none", W = "fill: #333", m = "c", j = "text", q = "normal";
let y = {}, d = 0;
const yt = function(t) {
  const n = Object.keys(t);
  for (const e of n)
    t[e];
}, gt = function(t, n) {
  return n.db.extract(n.db.getRootDocV2()), n.db.getClasses();
};
function xt(t) {
  return t == null ? "" : t.classes ? t.classes.join(" ") : "";
}
function R(t = "", n = 0, e = "", c = N) {
  const i = e !== null && e.length > 0 ? `${c}${e}` : "";
  return `${At}-${t}${i}-${n}`;
}
const A = (t, n, e, c, i, r) => {
  const o = e.id, u = xt(c[o]);
  if (o !== "root") {
    let T = h;
    e.start === !0 && (T = nt), e.start === !1 && (T = ct), e.type !== H && (T = e.type), y[o] || (y[o] = {
      id: o,
      shape: T,
      description: w.sanitizeText(o, g()),
      classes: `${u} ${Et}`
    });
    const s = y[o];
    e.description && (Array.isArray(s.description) ? (s.shape = C, s.description.push(e.description)) : s.description.length > 0 ? (s.shape = C, s.description === o ? s.description = [e.description] : s.description = [s.description, e.description]) : (s.shape = h, s.description = e.description), s.description = w.sanitizeTextOrArray(s.description, g())), s.description.length === 1 && s.shape === C && (s.shape = h), !s.type && e.doc && (E.info("Setting cluster for ", o, G(e)), s.type = "group", s.dir = G(e), s.shape = e.type === J ? it : rt, s.classes = s.classes + " " + ft + " " + (r ? bt : ""));
    const p = {
      labelStyle: "",
      shape: s.shape,
      labelText: s.description,
      // typeof newNode.description === 'object'
      //   ? newNode.description[0]
      //   : newNode.description,
      classes: s.classes,
      style: "",
      //styles.style,
      id: o,
      dir: s.dir,
      domId: R(o, d),
      type: s.type,
      padding: 15
      //getConfig().flowchart.padding
    };
    if (p.centerLabel = !0, e.note) {
      const l = {
        labelStyle: "",
        shape: lt,
        labelText: e.note.text,
        classes: _t,
        // useHtmlLabels: false,
        style: "",
        // styles.style,
        id: o + ht + "-" + d,
        domId: R(o, d, Y),
        type: s.type,
        padding: 15
        //getConfig().flowchart.padding
      }, a = {
        labelStyle: "",
        shape: at,
        labelText: e.note.text,
        classes: s.classes,
        style: "",
        // styles.style,
        id: o + v,
        domId: R(o, d, V),
        type: "group",
        padding: 0
        //getConfig().flowchart.padding
      };
      d++;
      const f = o + v;
      t.setNode(f, a), t.setNode(l.id, l), t.setNode(o, p), t.setParent(o, f), t.setParent(l.id, f);
      let S = o, D = l.id;
      e.note.position === "left of" && (S = l.id, D = o), t.setEdge(S, D, {
        arrowhead: "none",
        arrowType: "",
        style: z,
        labelStyle: "",
        classes: pt,
        arrowheadStyle: W,
        labelpos: m,
        labelType: j,
        thickness: q
      });
    } else
      t.setNode(o, p);
  }
  n && n.id !== "root" && (E.trace("Setting node ", o, " to be child of its parent ", n.id), t.setParent(o, n.id)), e.doc && (E.trace("Adding nodes children "), $t(t, e, e.doc, c, i, !r));
}, $t = (t, n, e, c, i, r) => {
  E.trace("items", e), e.forEach((o) => {
    switch (o.stmt) {
      case X:
        A(t, n, o, c, i, r);
        break;
      case H:
        A(t, n, o, c, i, r);
        break;
      case Q:
        {
          A(t, n, o.state1, c, i, r), A(t, n, o.state2, c, i, r);
          const u = {
            id: "edge" + d,
            arrowhead: "normal",
            arrowTypeEnd: "arrow_barb",
            style: z,
            labelStyle: "",
            label: w.sanitizeText(o.description, g()),
            arrowheadStyle: W,
            labelpos: m,
            labelType: j,
            thickness: q,
            classes: U
          };
          t.setEdge(o.state1.id, o.state2.id, u, d), d++;
        }
        break;
    }
  });
}, G = (t, n = Z) => {
  let e = n;
  if (t.doc)
    for (let c = 0; c < t.doc.length; c++) {
      const i = t.doc[c];
      i.stmt === "dir" && (e = i.value);
    }
  return e;
}, Ct = async function(t, n, e, c) {
  E.info("Drawing state diagram (v2)", n), y = {}, c.db.getDirection();
  const { securityLevel: i, state: r } = g(), o = r.nodeSpacing || 50, u = r.rankSpacing || 50;
  E.info(c.db.getRootDocV2()), c.db.extract(c.db.getRootDocV2()), E.info(c.db.getRootDocV2());
  const T = c.db.getStates(), s = new tt({
    multigraph: !0,
    compound: !0
  }).setGraph({
    rankdir: G(c.db.getRootDocV2()),
    nodesep: o,
    ranksep: u,
    marginx: 8,
    marginy: 8
  }).setDefaultEdgeLabel(function() {
    return {};
  });
  A(s, void 0, c.db.getRootDocV2(), T, c.db, !0);
  let p;
  i === "sandbox" && (p = $("#i" + n));
  const l = i === "sandbox" ? $(p.nodes()[0].contentDocument.body) : $("body"), a = l.select(`[id="${n}"]`), f = l.select("#" + n + " g");
  await st(f, s, ["barb"], _, n);
  const S = 8;
  et.insertTitle(a, "statediagramTitleText", r.titleTopMargin, c.db.getDiagramTitle());
  const D = a.node().getBBox(), L = D.width + S * 2, P = D.height + S * 2;
  a.attr("class", _);
  const O = a.node().getBBox();
  ot(a, P, L, r.useMaxWidth);
  const k = `${O.x - S} ${O.y - S} ${L} ${P}`;
  E.debug(`viewBox ${k}`), a.attr("viewBox", k);
  const K = document.querySelectorAll('[id="' + n + '"] .edgeLabel .label');
  for (const x of K) {
    const B = x.getBBox(), b = document.createElementNS("http://www.w3.org/2000/svg", h);
    b.setAttribute("rx", 0), b.setAttribute("ry", 0), b.setAttribute("width", B.width), b.setAttribute("height", B.height), x.insertBefore(b, x.firstChild);
  }
}, Rt = {
  setConf: yt,
  getClasses: gt,
  draw: Ct
}, vt = {
  parser: F,
  db: M,
  renderer: Rt,
  styles: I,
  init: (t) => {
    t.state || (t.state = {}), t.state.arrowMarkerAbsolute = t.arrowMarkerAbsolute, M.clear();
  }
};
export {
  vt as diagram
};
