import { p as R, d as N, s as B } from "./styles-ca8ceaa2.js";
import { l as c, c as r, j as k, x as G, t as _, r as E, o as C, p as z, f as A } from "./mermaid-be6aa4a6.js";
import { G as P } from "./layout-b178bd1a.js";
import { r as $ } from "./index-745c9ffe.js";
import "./edges-1ceb0db9.js";
import "./createText-7fe61f7a.js";
import "./svgDraw-51404f3b.js";
import "./line-d1abfd73.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
const S = (o) => A.sanitizeText(o, r());
let v = {
  dividerMargin: 10,
  padding: 5,
  textHeight: 10,
  curve: void 0
};
const q = function(o, t, p, n) {
  const e = Object.keys(o);
  c.info("keys:", e), c.info(o), e.forEach(function(s) {
    var y, d;
    const l = o[s], i = {
      shape: "rect",
      id: l.id,
      domId: l.domId,
      labelText: S(l.id),
      labelStyle: "",
      style: "fill: none; stroke: black",
      // TODO V10: Flowchart ? Keeping flowchart for backwards compatibility. Remove in next major release
      padding: ((y = r().flowchart) == null ? void 0 : y.padding) ?? ((d = r().class) == null ? void 0 : d.padding)
    };
    t.setNode(l.id, i), I(l.classes, t, p, n, l.id), c.info("setNode", i);
  });
}, I = function(o, t, p, n, e) {
  const s = Object.keys(o);
  c.info("keys:", s), c.info(o), s.filter((l) => o[l].parent == e).forEach(function(l) {
    var u, m;
    const a = o[l], i = a.cssClasses.join(" "), y = { labelStyle: "", style: "" }, d = a.label ?? a.id, f = 0, h = "class_box", b = {
      labelStyle: y.labelStyle,
      shape: h,
      labelText: S(d),
      classData: a,
      rx: f,
      ry: f,
      class: i,
      style: y.style,
      id: a.id,
      domId: a.domId,
      tooltip: n.db.getTooltip(a.id, e) || "",
      haveCallback: a.haveCallback,
      link: a.link,
      width: a.type === "group" ? 500 : void 0,
      type: a.type,
      // TODO V10: Flowchart ? Keeping flowchart for backwards compatibility. Remove in next major release
      padding: ((u = r().flowchart) == null ? void 0 : u.padding) ?? ((m = r().class) == null ? void 0 : m.padding)
    };
    t.setNode(a.id, b), e && t.setParent(a.id, e), c.info("setNode", b);
  });
}, F = function(o, t, p, n) {
  c.info(o), o.forEach(function(e, s) {
    var m, g;
    const l = e, a = "", i = { labelStyle: "", style: "" }, y = l.text, d = 0, f = "note", h = {
      labelStyle: i.labelStyle,
      shape: f,
      labelText: S(y),
      noteData: l,
      rx: d,
      ry: d,
      class: a,
      style: i.style,
      id: l.id,
      domId: l.id,
      tooltip: "",
      type: "note",
      // TODO V10: Flowchart ? Keeping flowchart for backwards compatibility. Remove in next major release
      padding: ((m = r().flowchart) == null ? void 0 : m.padding) ?? ((g = r().class) == null ? void 0 : g.padding)
    };
    if (t.setNode(l.id, h), c.info("setNode", h), !l.class || !(l.class in n))
      return;
    const b = p + s, u = {
      id: `edgeNote${b}`,
      //Set relationship style and line type
      classes: "relation",
      pattern: "dotted",
      // Set link type for rendering
      arrowhead: "none",
      //Set edge extra labels
      startLabelRight: "",
      endLabelLeft: "",
      //Set relation arrow types
      arrowTypeStart: "none",
      arrowTypeEnd: "none",
      style: "fill:none",
      labelStyle: "",
      curve: E(v.curve, C)
    };
    t.setEdge(l.id, l.class, u, b);
  });
}, H = function(o, t) {
  const p = r().flowchart;
  let n = 0;
  o.forEach(function(e) {
    var l;
    n++;
    const s = {
      //Set relationship style and line type
      classes: "relation",
      pattern: e.relation.lineType == 1 ? "dashed" : "solid",
      id: "id" + n,
      // Set link type for rendering
      arrowhead: e.type === "arrow_open" ? "none" : "normal",
      //Set edge extra labels
      startLabelRight: e.relationTitle1 === "none" ? "" : e.relationTitle1,
      endLabelLeft: e.relationTitle2 === "none" ? "" : e.relationTitle2,
      //Set relation arrow types
      arrowTypeStart: D(e.relation.type1),
      arrowTypeEnd: D(e.relation.type2),
      style: "fill:none",
      labelStyle: "",
      curve: E(p == null ? void 0 : p.curve, C)
    };
    if (c.info(s, e), e.style !== void 0) {
      const a = z(e.style);
      s.style = a.style, s.labelStyle = a.labelStyle;
    }
    e.text = e.title, e.text === void 0 ? e.style !== void 0 && (s.arrowheadStyle = "fill: #333") : (s.arrowheadStyle = "fill: #333", s.labelpos = "c", ((l = r().flowchart) == null ? void 0 : l.htmlLabels) ?? r().htmlLabels ? (s.labelType = "html", s.label = '<span class="edgeLabel">' + e.text + "</span>") : (s.labelType = "text", s.label = e.text.replace(A.lineBreakRegex, `
`), e.style === void 0 && (s.style = s.style || "stroke: #333; stroke-width: 1.5px;fill:none"), s.labelStyle = s.labelStyle.replace("color:", "fill:"))), t.setEdge(e.id1, e.id2, s, n);
  });
}, V = function(o) {
  v = {
    ...v,
    ...o
  };
}, W = async function(o, t, p, n) {
  c.info("Drawing class - ", t);
  const e = r().flowchart ?? r().class, s = r().securityLevel;
  c.info("config:", e);
  const l = (e == null ? void 0 : e.nodeSpacing) ?? 50, a = (e == null ? void 0 : e.rankSpacing) ?? 50, i = new P({
    multigraph: !0,
    compound: !0
  }).setGraph({
    rankdir: n.db.getDirection(),
    nodesep: l,
    ranksep: a,
    marginx: 8,
    marginy: 8
  }).setDefaultEdgeLabel(function() {
    return {};
  }), y = n.db.getNamespaces(), d = n.db.getClasses(), f = n.db.getRelations(), h = n.db.getNotes();
  c.info(f), q(y, i, t, n), I(d, i, t, n), H(f, i), F(h, i, f.length + 1, d);
  let b;
  s === "sandbox" && (b = k("#i" + t));
  const u = s === "sandbox" ? k(b.nodes()[0].contentDocument.body) : k("body"), m = u.select(`[id="${t}"]`), g = u.select("#" + t + " g");
  if (await $(
    g,
    i,
    ["aggregation", "extension", "composition", "dependency", "lollipop"],
    "classDiagram",
    t
  ), G.insertTitle(m, "classTitleText", (e == null ? void 0 : e.titleTopMargin) ?? 5, n.db.getDiagramTitle()), _(i, m, e == null ? void 0 : e.diagramPadding, e == null ? void 0 : e.useMaxWidth), !(e != null && e.htmlLabels)) {
    const T = s === "sandbox" ? b.nodes()[0].contentDocument : document, M = T.querySelectorAll('[id="' + t + '"] .edgeLabel .label');
    for (const w of M) {
      const L = w.getBBox(), x = T.createElementNS("http://www.w3.org/2000/svg", "rect");
      x.setAttribute("rx", 0), x.setAttribute("ry", 0), x.setAttribute("width", L.width), x.setAttribute("height", L.height), w.insertBefore(x, w.firstChild);
    }
  }
};
function D(o) {
  let t;
  switch (o) {
    case 0:
      t = "aggregation";
      break;
    case 1:
      t = "extension";
      break;
    case 2:
      t = "composition";
      break;
    case 3:
      t = "dependency";
      break;
    case 4:
      t = "lollipop";
      break;
    default:
      t = "none";
  }
  return t;
}
const J = {
  setConf: V,
  draw: W
}, se = {
  parser: R,
  db: N,
  renderer: J,
  styles: B,
  init: (o) => {
    o.class || (o.class = {}), o.class.arrowMarkerAbsolute = o.arrowMarkerAbsolute, N.clear();
  }
};
export {
  se as diagram
};
