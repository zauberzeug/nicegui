import { p as M, d as k, s as R } from "./styles-55d85316.js";
import { l as p, g as r, f as v, e as C } from "./config-e567ef17.js";
import { G as B } from "./layout-d6d8be39.js";
import { r as G } from "./index-e6caf2ad.js";
import { u as I, z as D, x as E, y as _ } from "./utils-aa888deb.js";
import { s as z } from "./setupGraphViewbox-a4603a92.js";
import "./mermaidAPI-04b5c286.js";
import "./errorRenderer-a3c4bedb.js";
import "./commonDb-4dc3d465.js";
import "./isPlainObject-a5cb4071.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
import "./edges-0979260b.js";
import "./svgDraw-c034b55e.js";
const A = (l) => C.sanitizeText(l, r());
let S = {
  dividerMargin: 10,
  padding: 5,
  textHeight: 10,
  curve: void 0
};
const $ = function(l, o, b, a) {
  const e = Object.keys(l);
  p.info("keys:", e), p.info(l), e.forEach(function(s) {
    var y, m;
    const t = l[s];
    let i = "";
    t.cssClasses.length > 0 && (i = i + " " + t.cssClasses.join(" "));
    const n = { labelStyle: "", style: "" }, f = t.label ?? t.id, c = 0, u = "class_box", d = {
      labelStyle: n.labelStyle,
      shape: u,
      labelText: A(f),
      classData: t,
      rx: c,
      ry: c,
      class: i,
      style: n.style,
      id: t.id,
      domId: t.domId,
      tooltip: a.db.getTooltip(t.id) || "",
      haveCallback: t.haveCallback,
      link: t.link,
      width: t.type === "group" ? 500 : void 0,
      type: t.type,
      // TODO V10: Flowchart ? Keeping flowchart for backwards compatibility. Remove in next major release
      padding: ((y = r().flowchart) == null ? void 0 : y.padding) ?? ((m = r().class) == null ? void 0 : m.padding)
    };
    o.setNode(t.id, d), p.info("setNode", d);
  });
}, q = function(l, o, b, a) {
  p.info(l), l.forEach(function(e, s) {
    var x, h;
    const t = e, i = "", n = { labelStyle: "", style: "" }, f = t.text, c = 0, u = "note", d = {
      labelStyle: n.labelStyle,
      shape: u,
      labelText: A(f),
      noteData: t,
      rx: c,
      ry: c,
      class: i,
      style: n.style,
      id: t.id,
      domId: t.id,
      tooltip: "",
      type: "note",
      // TODO V10: Flowchart ? Keeping flowchart for backwards compatibility. Remove in next major release
      padding: ((x = r().flowchart) == null ? void 0 : x.padding) ?? ((h = r().class) == null ? void 0 : h.padding)
    };
    if (o.setNode(t.id, d), p.info("setNode", d), !t.class || !(t.class in a))
      return;
    const y = b + s, m = {
      id: `edgeNote${y}`,
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
      curve: D(S.curve, E)
    };
    o.setEdge(t.id, t.class, m, y);
  });
}, F = function(l, o) {
  const b = r().flowchart;
  let a = 0;
  l.forEach(function(e) {
    var t;
    a++;
    const s = {
      //Set relationship style and line type
      classes: "relation",
      pattern: e.relation.lineType == 1 ? "dashed" : "solid",
      id: "id" + a,
      // Set link type for rendering
      arrowhead: e.type === "arrow_open" ? "none" : "normal",
      //Set edge extra labels
      startLabelRight: e.relationTitle1 === "none" ? "" : e.relationTitle1,
      endLabelLeft: e.relationTitle2 === "none" ? "" : e.relationTitle2,
      //Set relation arrow types
      arrowTypeStart: L(e.relation.type1),
      arrowTypeEnd: L(e.relation.type2),
      style: "fill:none",
      labelStyle: "",
      curve: D(b == null ? void 0 : b.curve, E)
    };
    if (p.info(s, e), e.style !== void 0) {
      const i = _(e.style);
      s.style = i.style, s.labelStyle = i.labelStyle;
    }
    e.text = e.title, e.text === void 0 ? e.style !== void 0 && (s.arrowheadStyle = "fill: #333") : (s.arrowheadStyle = "fill: #333", s.labelpos = "c", ((t = r().flowchart) == null ? void 0 : t.htmlLabels) ?? r().htmlLabels ? (s.labelType = "html", s.label = '<span class="edgeLabel">' + e.text + "</span>") : (s.labelType = "text", s.label = e.text.replace(C.lineBreakRegex, `
`), e.style === void 0 && (s.style = s.style || "stroke: #333; stroke-width: 1.5px;fill:none"), s.labelStyle = s.labelStyle.replace("color:", "fill:"))), o.setEdge(e.id1, e.id2, s, a);
  });
}, H = function(l) {
  S = {
    ...S,
    ...l
  };
}, P = function(l, o, b, a) {
  p.info("Drawing class - ", o);
  const e = r().flowchart ?? r().class, s = r().securityLevel;
  p.info("config:", e);
  const t = (e == null ? void 0 : e.nodeSpacing) ?? 50, i = (e == null ? void 0 : e.rankSpacing) ?? 50, n = new B({
    multigraph: !0,
    compound: !0
  }).setGraph({
    rankdir: a.db.getDirection(),
    nodesep: t,
    ranksep: i,
    marginx: 8,
    marginy: 8
  }).setDefaultEdgeLabel(function() {
    return {};
  }), f = a.db.getClasses(), c = a.db.getRelations(), u = a.db.getNotes();
  p.info(c), $(f, n, o, a), F(c, n), q(u, n, c.length + 1, f);
  let d;
  s === "sandbox" && (d = v("#i" + o));
  const y = s === "sandbox" ? (
    // @ts-ignore Ignore type error for now
    v(d.nodes()[0].contentDocument.body)
  ) : v("body"), m = y.select(`[id="${o}"]`), x = y.select("#" + o + " g");
  if (G(
    x,
    n,
    ["aggregation", "extension", "composition", "dependency", "lollipop"],
    "classDiagram",
    o
  ), I.insertTitle(m, "classTitleText", (e == null ? void 0 : e.titleTopMargin) ?? 5, a.db.getDiagramTitle()), z(n, m, e == null ? void 0 : e.diagramPadding, e == null ? void 0 : e.useMaxWidth), !(e != null && e.htmlLabels)) {
    const h = s === "sandbox" ? d.nodes()[0].contentDocument : document, N = h.querySelectorAll('[id="' + o + '"] .edgeLabel .label');
    for (const w of N) {
      const T = w.getBBox(), g = h.createElementNS("http://www.w3.org/2000/svg", "rect");
      g.setAttribute("rx", 0), g.setAttribute("ry", 0), g.setAttribute("width", T.width), g.setAttribute("height", T.height), w.insertBefore(g, w.firstChild);
    }
  }
};
function L(l) {
  let o;
  switch (l) {
    case 0:
      o = "aggregation";
      break;
    case 1:
      o = "extension";
      break;
    case 2:
      o = "composition";
      break;
    case 3:
      o = "dependency";
      break;
    case 4:
      o = "lollipop";
      break;
    default:
      o = "none";
  }
  return o;
}
const V = {
  setConf: H,
  draw: P
}, le = {
  parser: M,
  db: k,
  renderer: V,
  styles: R,
  init: (l) => {
    l.class || (l.class = {}), l.class.arrowMarkerAbsolute = l.arrowMarkerAbsolute, k.clear();
  }
};
export {
  le as diagram
};
//# sourceMappingURL=classDiagram-v2-146d8a48.js.map
