import { G as V } from "./layout-d6d8be39.js";
import { k as P, g as C, e as D, l as y, f as T } from "./config-e567ef17.js";
import { b as q, f as F } from "./add-html-label-6e56ed67.js";
import { y as N, z as $, x as E, u as M } from "./utils-aa888deb.js";
import { r as R } from "./index-e6caf2ad.js";
import { s as U } from "./setupGraphViewbox-a4603a92.js";
import { s as H } from "./selectAll-8155f162.js";
const G = {}, W = function(t) {
  const n = Object.keys(t);
  for (const m of n)
    G[m] = t[m];
}, I = function(t, n, m, s, d, p) {
  const b = s.select(`[id="${m}"]`);
  Object.keys(t).forEach(function(i) {
    const r = t[i];
    let h = "default";
    r.classes.length > 0 && (h = r.classes.join(" "));
    const u = N(r.styles);
    let e = r.text !== void 0 ? r.text : r.id, o;
    if (P(C().flowchart.htmlLabels)) {
      const x = {
        label: e.replace(
          /fa[blrs]?:fa-[\w-]+/g,
          (k) => `<i class='${k.replace(":", " ")}'></i>`
        )
      };
      o = q(b, x).node(), o.parentNode.removeChild(o);
    } else {
      const x = d.createElementNS("http://www.w3.org/2000/svg", "text");
      x.setAttribute("style", u.labelStyle.replace("color:", "fill:"));
      const k = e.split(D.lineBreakRegex);
      for (const _ of k) {
        const S = d.createElementNS("http://www.w3.org/2000/svg", "tspan");
        S.setAttributeNS("http://www.w3.org/XML/1998/namespace", "xml:space", "preserve"), S.setAttribute("dy", "1em"), S.setAttribute("x", "1"), S.textContent = _, x.appendChild(S);
      }
      o = x;
    }
    let c = 0, l = "";
    switch (r.type) {
      case "round":
        c = 5, l = "rect";
        break;
      case "square":
        l = "rect";
        break;
      case "diamond":
        l = "question";
        break;
      case "hexagon":
        l = "hexagon";
        break;
      case "odd":
        l = "rect_left_inv_arrow";
        break;
      case "lean_right":
        l = "lean_right";
        break;
      case "lean_left":
        l = "lean_left";
        break;
      case "trapezoid":
        l = "trapezoid";
        break;
      case "inv_trapezoid":
        l = "inv_trapezoid";
        break;
      case "odd_right":
        l = "rect_left_inv_arrow";
        break;
      case "circle":
        l = "circle";
        break;
      case "ellipse":
        l = "ellipse";
        break;
      case "stadium":
        l = "stadium";
        break;
      case "subroutine":
        l = "subroutine";
        break;
      case "cylinder":
        l = "cylinder";
        break;
      case "group":
        l = "rect";
        break;
      case "doublecircle":
        l = "doublecircle";
        break;
      default:
        l = "rect";
    }
    n.setNode(r.id, {
      labelStyle: u.labelStyle,
      shape: l,
      labelText: e,
      rx: c,
      ry: c,
      class: h,
      style: u.style,
      id: r.id,
      link: r.link,
      linkTarget: r.linkTarget,
      tooltip: p.db.getTooltip(r.id) || "",
      domId: p.db.lookUpDomId(r.id),
      haveCallback: r.haveCallback,
      width: r.type === "group" ? 500 : void 0,
      dir: r.dir,
      type: r.type,
      props: r.props,
      padding: C().flowchart.padding
    }), y.info("setNode", {
      labelStyle: u.labelStyle,
      shape: l,
      labelText: e,
      rx: c,
      ry: c,
      class: h,
      style: u.style,
      id: r.id,
      domId: p.db.lookUpDomId(r.id),
      width: r.type === "group" ? 500 : void 0,
      type: r.type,
      dir: r.dir,
      props: r.props,
      padding: C().flowchart.padding
    });
  });
}, z = function(t, n, m) {
  y.info("abc78 edges = ", t);
  let s = 0, d = {}, p, b;
  if (t.defaultStyle !== void 0) {
    const a = N(t.defaultStyle);
    p = a.style, b = a.labelStyle;
  }
  t.forEach(function(a) {
    s++;
    var i = "L-" + a.start + "-" + a.end;
    d[i] === void 0 ? (d[i] = 0, y.info("abc78 new entry", i, d[i])) : (d[i]++, y.info("abc78 new entry", i, d[i]));
    let r = i + "-" + d[i];
    y.info("abc78 new link id to be used is", i, r, d[i]);
    var h = "LS-" + a.start, u = "LE-" + a.end;
    const e = { style: "", labelStyle: "" };
    switch (e.minlen = a.length || 1, a.type === "arrow_open" ? e.arrowhead = "none" : e.arrowhead = "normal", e.arrowTypeStart = "arrow_open", e.arrowTypeEnd = "arrow_open", a.type) {
      case "double_arrow_cross":
        e.arrowTypeStart = "arrow_cross";
      case "arrow_cross":
        e.arrowTypeEnd = "arrow_cross";
        break;
      case "double_arrow_point":
        e.arrowTypeStart = "arrow_point";
      case "arrow_point":
        e.arrowTypeEnd = "arrow_point";
        break;
      case "double_arrow_circle":
        e.arrowTypeStart = "arrow_circle";
      case "arrow_circle":
        e.arrowTypeEnd = "arrow_circle";
        break;
    }
    let o = "", c = "";
    switch (a.stroke) {
      case "normal":
        o = "fill:none;", p !== void 0 && (o = p), b !== void 0 && (c = b), e.thickness = "normal", e.pattern = "solid";
        break;
      case "dotted":
        e.thickness = "normal", e.pattern = "dotted", e.style = "fill:none;stroke-width:2px;stroke-dasharray:3;";
        break;
      case "thick":
        e.thickness = "thick", e.pattern = "solid", e.style = "stroke-width: 3.5px;fill:none;";
        break;
      case "invisible":
        e.thickness = "invisible", e.pattern = "solid", e.style = "stroke-width: 0;fill:none;";
        break;
    }
    if (a.style !== void 0) {
      const l = N(a.style);
      o = l.style, c = l.labelStyle;
    }
    e.style = e.style += o, e.labelStyle = e.labelStyle += c, a.interpolate !== void 0 ? e.curve = $(a.interpolate, E) : t.defaultInterpolate !== void 0 ? e.curve = $(t.defaultInterpolate, E) : e.curve = $(G.curve, E), a.text === void 0 ? a.style !== void 0 && (e.arrowheadStyle = "fill: #333") : (e.arrowheadStyle = "fill: #333", e.labelpos = "c"), e.labelType = "text", e.label = a.text.replace(D.lineBreakRegex, `
`), a.style === void 0 && (e.style = e.style || "stroke: #333; stroke-width: 1.5px;fill:none;"), e.labelStyle = e.labelStyle.replace("color:", "fill:"), e.id = r, e.classes = "flowchart-link " + h + " " + u, n.setEdge(a.start, a.end, e, s);
  });
}, X = function(t, n) {
  y.info("Extracting classes"), n.db.clear();
  try {
    return n.parse(t), n.db.getClasses();
  } catch {
    return;
  }
}, J = function(t, n, m, s) {
  y.info("Drawing flowchart"), s.db.clear(), F.setGen("gen-2"), s.parser.parse(t);
  let d = s.db.getDirection();
  d === void 0 && (d = "TD");
  const { securityLevel: p, flowchart: b } = C(), a = b.nodeSpacing || 50, i = b.rankSpacing || 50;
  let r;
  p === "sandbox" && (r = T("#i" + n));
  const h = p === "sandbox" ? T(r.nodes()[0].contentDocument.body) : T("body"), u = p === "sandbox" ? r.nodes()[0].contentDocument : document, e = new V({
    multigraph: !0,
    compound: !0
  }).setGraph({
    rankdir: d,
    nodesep: a,
    ranksep: i,
    marginx: 0,
    marginy: 0
  }).setDefaultEdgeLabel(function() {
    return {};
  });
  let o;
  const c = s.db.getSubGraphs();
  y.info("Subgraphs - ", c);
  for (let f = c.length - 1; f >= 0; f--)
    o = c[f], y.info("Subgraph - ", o), s.db.addVertex(o.id, o.title, "group", void 0, o.classes, o.dir);
  const l = s.db.getVertices(), x = s.db.getEdges();
  y.info("Edges", x);
  let k = 0;
  for (k = c.length - 1; k >= 0; k--) {
    o = c[k], H("cluster").append("text");
    for (let f = 0; f < o.nodes.length; f++)
      y.info("Setting up subgraphs", o.nodes[f], o.id), e.setParent(o.nodes[f], o.id);
  }
  I(l, e, n, h, u, s), z(x, e);
  const _ = h.select(`[id="${n}"]`), S = h.select("#" + n + " g");
  if (R(S, e, ["point", "circle", "cross"], "flowchart", n), M.insertTitle(_, "flowchartTitleText", b.titleTopMargin, s.db.getDiagramTitle()), U(e, _, b.diagramPadding, b.useMaxWidth), s.db.indexNodes("subGraph" + k), !b.htmlLabels) {
    const f = u.querySelectorAll('[id="' + n + '"] .edgeLabel .label');
    for (const g of f) {
      const v = g.getBBox(), w = u.createElementNS("http://www.w3.org/2000/svg", "rect");
      w.setAttribute("rx", 0), w.setAttribute("ry", 0), w.setAttribute("width", v.width), w.setAttribute("height", v.height), g.insertBefore(w, g.firstChild);
    }
  }
  Object.keys(l).forEach(function(f) {
    const g = l[f];
    if (g.link) {
      const v = T("#" + n + ' [id="' + f + '"]');
      if (v) {
        const w = u.createElementNS("http://www.w3.org/2000/svg", "a");
        w.setAttributeNS("http://www.w3.org/2000/svg", "class", g.classes.join(" ")), w.setAttributeNS("http://www.w3.org/2000/svg", "href", g.link), w.setAttributeNS("http://www.w3.org/2000/svg", "rel", "noopener"), p === "sandbox" ? w.setAttributeNS("http://www.w3.org/2000/svg", "target", "_top") : g.linkTarget && w.setAttributeNS("http://www.w3.org/2000/svg", "target", g.linkTarget);
        const L = v.insert(function() {
          return w;
        }, ":first-child"), A = v.select(".label-container");
        A && L.append(function() {
          return A.node();
        });
        const B = v.select(".label");
        B && L.append(function() {
          return B.node();
        });
      }
    }
  });
}, le = {
  setConf: W,
  addVertices: I,
  addEdges: z,
  getClasses: X,
  draw: J
}, K = (t) => `.label {
    font-family: ${t.fontFamily};
    color: ${t.nodeTextColor || t.textColor};
  }
  .cluster-label text {
    fill: ${t.titleColor};
  }
  .cluster-label span {
    color: ${t.titleColor};
  }

  .label text,span {
    fill: ${t.nodeTextColor || t.textColor};
    color: ${t.nodeTextColor || t.textColor};
  }

  .node rect,
  .node circle,
  .node ellipse,
  .node polygon,
  .node path {
    fill: ${t.mainBkg};
    stroke: ${t.nodeBorder};
    stroke-width: 1px;
  }

  .node .label {
    text-align: center;
  }
  .node.clickable {
    cursor: pointer;
  }

  .arrowheadPath {
    fill: ${t.arrowheadColor};
  }

  .edgePath .path {
    stroke: ${t.lineColor};
    stroke-width: 2.0px;
  }

  .flowchart-link {
    stroke: ${t.lineColor};
    fill: none;
  }

  .edgeLabel {
    background-color: ${t.edgeLabelBackground};
    rect {
      opacity: 0.5;
      background-color: ${t.edgeLabelBackground};
      fill: ${t.edgeLabelBackground};
    }
    text-align: center;
  }

  .cluster rect {
    fill: ${t.clusterBkg};
    stroke: ${t.clusterBorder};
    stroke-width: 1px;
  }

  .cluster text {
    fill: ${t.titleColor};
  }

  .cluster span {
    color: ${t.titleColor};
  }
  /* .cluster div {
    color: ${t.titleColor};
  } */

  div.mermaidTooltip {
    position: absolute;
    text-align: center;
    max-width: 200px;
    padding: 2px;
    font-family: ${t.fontFamily};
    font-size: 12px;
    background: ${t.tertiaryColor};
    border: 1px solid ${t.border2};
    border-radius: 2px;
    pointer-events: none;
    z-index: 100;
  }

  .flowchartTitleText {
    text-anchor: middle;
    font-size: 18px;
    fill: ${t.textColor};
  }
`, ae = K;
export {
  ae as a,
  le as f
};
//# sourceMappingURL=styles-0beab977.js.map
