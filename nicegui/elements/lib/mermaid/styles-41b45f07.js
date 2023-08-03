import { i as V, G as q } from "./layout-b178bd1a.js";
import { _ as M, C as R, v as F, p as N, l as u, q as U, c as C, f as I, r as $, o as E, j as _, x as H, t as W, y as X } from "./mermaid-be6aa4a6.js";
import { f as J } from "./flowDb-5c3f1e8c.js";
import { r as K } from "./index-745c9ffe.js";
import { s as Q } from "./selectAll-b44befab.js";
const Y = (e, l) => M.lang.round(R.parse(e)[l]), Z = Y;
function pe(e, l) {
  return !!e.children(l).length;
}
function be(e) {
  return L(e.v) + ":" + L(e.w) + ":" + L(e.name);
}
var j = /:/g;
function L(e) {
  return e ? String(e).replace(j, "\\:") : "";
}
function O(e, l) {
  l && e.attr("style", l);
}
function ue(e, l, c) {
  l && e.attr("class", l).attr("class", c + " " + e.attr("class"));
}
function we(e, l) {
  var c = l.graph();
  if (V(c)) {
    var a = c.transition;
    if (F(a))
      return a(e);
  }
  return e;
}
function ee(e, l) {
  var c = e.append("foreignObject").attr("width", "100000"), a = c.append("xhtml:div");
  a.attr("xmlns", "http://www.w3.org/1999/xhtml");
  var i = l.label;
  switch (typeof i) {
    case "function":
      a.insert(i);
      break;
    case "object":
      a.insert(function() {
        return i;
      });
      break;
    default:
      a.html(i);
  }
  O(a, l.labelStyle), a.style("display", "inline-block"), a.style("white-space", "nowrap");
  var d = a.node().getBoundingClientRect();
  return c.attr("width", d.width).attr("height", d.height), c;
}
const G = {}, te = function(e) {
  const l = Object.keys(e);
  for (const c of l)
    G[c] = e[c];
}, z = function(e, l, c, a, i, d) {
  const w = a.select(`[id="${c}"]`);
  Object.keys(e).forEach(function(f) {
    const r = e[f];
    let g = "default";
    r.classes.length > 0 && (g = r.classes.join(" ")), g = g + " flowchart-label";
    const h = N(r.styles);
    let t = r.text !== void 0 ? r.text : r.id, s;
    if (u.info("vertex", r, r.labelType), r.labelType === "markdown")
      u.info("vertex", r, r.labelType);
    else if (U(C().flowchart.htmlLabels)) {
      const m = {
        label: t.replace(
          /fa[blrs]?:fa-[\w-]+/g,
          (k) => `<i class='${k.replace(":", " ")}'></i>`
        )
      };
      s = ee(w, m).node(), s.parentNode.removeChild(s);
    } else {
      const m = i.createElementNS("http://www.w3.org/2000/svg", "text");
      m.setAttribute("style", h.labelStyle.replace("color:", "fill:"));
      const k = t.split(I.lineBreakRegex);
      for (const T of k) {
        const S = i.createElementNS("http://www.w3.org/2000/svg", "tspan");
        S.setAttributeNS("http://www.w3.org/XML/1998/namespace", "xml:space", "preserve"), S.setAttribute("dy", "1em"), S.setAttribute("x", "1"), S.textContent = T, m.appendChild(S);
      }
      s = m;
    }
    let p = 0, n = "";
    switch (r.type) {
      case "round":
        p = 5, n = "rect";
        break;
      case "square":
        n = "rect";
        break;
      case "diamond":
        n = "question";
        break;
      case "hexagon":
        n = "hexagon";
        break;
      case "odd":
        n = "rect_left_inv_arrow";
        break;
      case "lean_right":
        n = "lean_right";
        break;
      case "lean_left":
        n = "lean_left";
        break;
      case "trapezoid":
        n = "trapezoid";
        break;
      case "inv_trapezoid":
        n = "inv_trapezoid";
        break;
      case "odd_right":
        n = "rect_left_inv_arrow";
        break;
      case "circle":
        n = "circle";
        break;
      case "ellipse":
        n = "ellipse";
        break;
      case "stadium":
        n = "stadium";
        break;
      case "subroutine":
        n = "subroutine";
        break;
      case "cylinder":
        n = "cylinder";
        break;
      case "group":
        n = "rect";
        break;
      case "doublecircle":
        n = "doublecircle";
        break;
      default:
        n = "rect";
    }
    l.setNode(r.id, {
      labelStyle: h.labelStyle,
      shape: n,
      labelText: t,
      labelType: r.labelType,
      rx: p,
      ry: p,
      class: g,
      style: h.style,
      id: r.id,
      link: r.link,
      linkTarget: r.linkTarget,
      tooltip: d.db.getTooltip(r.id) || "",
      domId: d.db.lookUpDomId(r.id),
      haveCallback: r.haveCallback,
      width: r.type === "group" ? 500 : void 0,
      dir: r.dir,
      type: r.type,
      props: r.props,
      padding: C().flowchart.padding
    }), u.info("setNode", {
      labelStyle: h.labelStyle,
      labelType: r.labelType,
      shape: n,
      labelText: t,
      rx: p,
      ry: p,
      class: g,
      style: h.style,
      id: r.id,
      domId: d.db.lookUpDomId(r.id),
      width: r.type === "group" ? 500 : void 0,
      type: r.type,
      dir: r.dir,
      props: r.props,
      padding: C().flowchart.padding
    });
  });
}, P = function(e, l, c) {
  u.info("abc78 edges = ", e);
  let a = 0, i = {}, d, w;
  if (e.defaultStyle !== void 0) {
    const o = N(e.defaultStyle);
    d = o.style, w = o.labelStyle;
  }
  e.forEach(function(o) {
    a++;
    const f = "L-" + o.start + "-" + o.end;
    i[f] === void 0 ? (i[f] = 0, u.info("abc78 new entry", f, i[f])) : (i[f]++, u.info("abc78 new entry", f, i[f]));
    let r = f + "-" + i[f];
    u.info("abc78 new link id to be used is", f, r, i[f]);
    const g = "LS-" + o.start, h = "LE-" + o.end, t = { style: "", labelStyle: "" };
    switch (t.minlen = o.length || 1, o.type === "arrow_open" ? t.arrowhead = "none" : t.arrowhead = "normal", t.arrowTypeStart = "arrow_open", t.arrowTypeEnd = "arrow_open", o.type) {
      case "double_arrow_cross":
        t.arrowTypeStart = "arrow_cross";
      case "arrow_cross":
        t.arrowTypeEnd = "arrow_cross";
        break;
      case "double_arrow_point":
        t.arrowTypeStart = "arrow_point";
      case "arrow_point":
        t.arrowTypeEnd = "arrow_point";
        break;
      case "double_arrow_circle":
        t.arrowTypeStart = "arrow_circle";
      case "arrow_circle":
        t.arrowTypeEnd = "arrow_circle";
        break;
    }
    let s = "", p = "";
    switch (o.stroke) {
      case "normal":
        s = "fill:none;", d !== void 0 && (s = d), w !== void 0 && (p = w), t.thickness = "normal", t.pattern = "solid";
        break;
      case "dotted":
        t.thickness = "normal", t.pattern = "dotted", t.style = "fill:none;stroke-width:2px;stroke-dasharray:3;";
        break;
      case "thick":
        t.thickness = "thick", t.pattern = "solid", t.style = "stroke-width: 3.5px;fill:none;";
        break;
      case "invisible":
        t.thickness = "invisible", t.pattern = "solid", t.style = "stroke-width: 0;fill:none;";
        break;
    }
    if (o.style !== void 0) {
      const n = N(o.style);
      s = n.style, p = n.labelStyle;
    }
    t.style = t.style += s, t.labelStyle = t.labelStyle += p, o.interpolate !== void 0 ? t.curve = $(o.interpolate, E) : e.defaultInterpolate !== void 0 ? t.curve = $(e.defaultInterpolate, E) : t.curve = $(G.curve, E), o.text === void 0 ? o.style !== void 0 && (t.arrowheadStyle = "fill: #333") : (t.arrowheadStyle = "fill: #333", t.labelpos = "c"), t.labelType = o.labelType, t.label = o.text.replace(I.lineBreakRegex, `
`), o.style === void 0 && (t.style = t.style || "stroke: #333; stroke-width: 1.5px;fill:none;"), t.labelStyle = t.labelStyle.replace("color:", "fill:"), t.id = r, t.classes = "flowchart-link " + g + " " + h, l.setEdge(o.start, o.end, t, a);
  });
}, re = function(e, l) {
  u.info("Extracting classes"), l.db.clear();
  try {
    return l.parse(e), l.db.getClasses();
  } catch {
    return;
  }
}, le = async function(e, l, c, a) {
  u.info("Drawing flowchart"), a.db.clear(), J.setGen("gen-2"), a.parser.parse(e);
  let i = a.db.getDirection();
  i === void 0 && (i = "TD");
  const { securityLevel: d, flowchart: w } = C(), o = w.nodeSpacing || 50, f = w.rankSpacing || 50;
  let r;
  d === "sandbox" && (r = _("#i" + l));
  const g = d === "sandbox" ? _(r.nodes()[0].contentDocument.body) : _("body"), h = d === "sandbox" ? r.nodes()[0].contentDocument : document, t = new q({
    multigraph: !0,
    compound: !0
  }).setGraph({
    rankdir: i,
    nodesep: o,
    ranksep: f,
    marginx: 0,
    marginy: 0
  }).setDefaultEdgeLabel(function() {
    return {};
  });
  let s;
  const p = a.db.getSubGraphs();
  u.info("Subgraphs - ", p);
  for (let b = p.length - 1; b >= 0; b--)
    s = p[b], u.info("Subgraph - ", s), a.db.addVertex(
      s.id,
      { text: s.title, type: s.labelType },
      "group",
      void 0,
      s.classes,
      s.dir
    );
  const n = a.db.getVertices(), m = a.db.getEdges();
  u.info("Edges", m);
  let k = 0;
  for (k = p.length - 1; k >= 0; k--) {
    s = p[k], Q("cluster").append("text");
    for (let b = 0; b < s.nodes.length; b++)
      u.info("Setting up subgraphs", s.nodes[b], s.id), t.setParent(s.nodes[b], s.id);
  }
  z(n, t, l, g, h, a), P(m, t);
  const T = g.select(`[id="${l}"]`), S = g.select("#" + l + " g");
  if (await K(S, t, ["point", "circle", "cross"], "flowchart", l), H.insertTitle(T, "flowchartTitleText", w.titleTopMargin, a.db.getDiagramTitle()), W(t, T, w.diagramPadding, w.useMaxWidth), a.db.indexNodes("subGraph" + k), !w.htmlLabels) {
    const b = h.querySelectorAll('[id="' + l + '"] .edgeLabel .label');
    for (const x of b) {
      const v = x.getBBox(), y = h.createElementNS("http://www.w3.org/2000/svg", "rect");
      y.setAttribute("rx", 0), y.setAttribute("ry", 0), y.setAttribute("width", v.width), y.setAttribute("height", v.height), x.insertBefore(y, x.firstChild);
    }
  }
  Object.keys(n).forEach(function(b) {
    const x = n[b];
    if (x.link) {
      const v = _("#" + l + ' [id="' + b + '"]');
      if (v) {
        const y = h.createElementNS("http://www.w3.org/2000/svg", "a");
        y.setAttributeNS("http://www.w3.org/2000/svg", "class", x.classes.join(" ")), y.setAttributeNS("http://www.w3.org/2000/svg", "href", x.link), y.setAttributeNS("http://www.w3.org/2000/svg", "rel", "noopener"), d === "sandbox" ? y.setAttributeNS("http://www.w3.org/2000/svg", "target", "_top") : x.linkTarget && y.setAttributeNS("http://www.w3.org/2000/svg", "target", x.linkTarget);
        const A = v.insert(function() {
          return y;
        }, ":first-child"), B = v.select(".label-container");
        B && A.append(function() {
          return B.node();
        });
        const D = v.select(".label");
        D && A.append(function() {
          return D.node();
        });
      }
    }
  });
}, he = {
  setConf: te,
  addVertices: z,
  addEdges: P,
  getClasses: re,
  draw: le
}, ae = (e, l) => {
  const c = Z, a = c(e, "r"), i = c(e, "g"), d = c(e, "b");
  return X(a, i, d, l);
}, ne = (e) => `.label {
    font-family: ${e.fontFamily};
    color: ${e.nodeTextColor || e.textColor};
  }
  .cluster-label text {
    fill: ${e.titleColor};
  }
  .cluster-label span,p {
    color: ${e.titleColor};
  }

  .label text,span,p {
    fill: ${e.nodeTextColor || e.textColor};
    color: ${e.nodeTextColor || e.textColor};
  }

  .node rect,
  .node circle,
  .node ellipse,
  .node polygon,
  .node path {
    fill: ${e.mainBkg};
    stroke: ${e.nodeBorder};
    stroke-width: 1px;
  }
  .flowchart-label text {
    text-anchor: middle;
  }
  // .flowchart-label .text-outer-tspan {
  //   text-anchor: middle;
  // }
  // .flowchart-label .text-inner-tspan {
  //   text-anchor: start;
  // }

  .node .label {
    text-align: center;
  }
  .node.clickable {
    cursor: pointer;
  }

  .arrowheadPath {
    fill: ${e.arrowheadColor};
  }

  .edgePath .path {
    stroke: ${e.lineColor};
    stroke-width: 2.0px;
  }

  .flowchart-link {
    stroke: ${e.lineColor};
    fill: none;
  }

  .edgeLabel {
    background-color: ${e.edgeLabelBackground};
    rect {
      opacity: 0.5;
      background-color: ${e.edgeLabelBackground};
      fill: ${e.edgeLabelBackground};
    }
    text-align: center;
  }

  /* For html labels only */
  .labelBkg {
    background-color: ${ae(e.edgeLabelBackground, 0.5)};
    // background-color: 
  }

  .cluster rect {
    fill: ${e.clusterBkg};
    stroke: ${e.clusterBorder};
    stroke-width: 1px;
  }

  .cluster text {
    fill: ${e.titleColor};
  }

  .cluster span,p {
    color: ${e.titleColor};
  }
  /* .cluster div {
    color: ${e.titleColor};
  } */

  div.mermaidTooltip {
    position: absolute;
    text-align: center;
    max-width: 200px;
    padding: 2px;
    font-family: ${e.fontFamily};
    font-size: 12px;
    background: ${e.tertiaryColor};
    border: 1px solid ${e.border2};
    border-radius: 2px;
    pointer-events: none;
    z-index: 100;
  }

  .flowchartTitleText {
    text-anchor: middle;
    font-size: 18px;
    fill: ${e.textColor};
  }
`, ye = ne;
export {
  O as a,
  ee as b,
  we as c,
  ue as d,
  be as e,
  he as f,
  ye as g,
  pe as i
};
