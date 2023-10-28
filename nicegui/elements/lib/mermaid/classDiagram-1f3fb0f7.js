import { p as G, d as S, s as A } from "./styles-47086cb2.js";
import { F as W, z as B, l as u, G as I, c as H, j as M, k as O } from "./mermaid-5f2d2ec5.js";
import { G as P, l as X } from "./layout-1caf14c9.js";
import { l as Y } from "./line-9d49a987.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
let _ = 0;
const $ = function(i, a, t, o, p) {
  const g = function(e) {
    switch (e) {
      case p.db.relationType.AGGREGATION:
        return "aggregation";
      case p.db.relationType.EXTENSION:
        return "extension";
      case p.db.relationType.COMPOSITION:
        return "composition";
      case p.db.relationType.DEPENDENCY:
        return "dependency";
      case p.db.relationType.LOLLIPOP:
        return "lollipop";
    }
  };
  a.points = a.points.filter((e) => !Number.isNaN(e.y));
  const s = a.points, c = Y().x(function(e) {
    return e.x;
  }).y(function(e) {
    return e.y;
  }).curve(W), n = i.append("path").attr("d", c(s)).attr("id", "edge" + _).attr("class", "relation");
  let r = "";
  o.arrowMarkerAbsolute && (r = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search, r = r.replace(/\(/g, "\\("), r = r.replace(/\)/g, "\\)")), t.relation.lineType == 1 && n.attr("class", "relation dashed-line"), t.relation.lineType == 10 && n.attr("class", "relation dotted-line"), t.relation.type1 !== "none" && n.attr(
    "marker-start",
    "url(" + r + "#" + g(t.relation.type1) + "Start)"
  ), t.relation.type2 !== "none" && n.attr(
    "marker-end",
    "url(" + r + "#" + g(t.relation.type2) + "End)"
  );
  let f, h;
  const x = a.points.length;
  let k = B.calcLabelPosition(a.points);
  f = k.x, h = k.y;
  let y, m, w, b;
  if (x % 2 !== 0 && x > 1) {
    let e = B.calcCardinalityPosition(
      t.relation.type1 !== "none",
      a.points,
      a.points[0]
    ), d = B.calcCardinalityPosition(
      t.relation.type2 !== "none",
      a.points,
      a.points[x - 1]
    );
    u.debug("cardinality_1_point " + JSON.stringify(e)), u.debug("cardinality_2_point " + JSON.stringify(d)), y = e.x, m = e.y, w = d.x, b = d.y;
  }
  if (t.title !== void 0) {
    const e = i.append("g").attr("class", "classLabel"), d = e.append("text").attr("class", "label").attr("x", f).attr("y", h).attr("fill", "red").attr("text-anchor", "middle").text(t.title);
    window.label = d;
    const l = d.node().getBBox();
    e.insert("rect", ":first-child").attr("class", "box").attr("x", l.x - o.padding / 2).attr("y", l.y - o.padding / 2).attr("width", l.width + o.padding).attr("height", l.height + o.padding);
  }
  u.info("Rendering relation " + JSON.stringify(t)), t.relationTitle1 !== void 0 && t.relationTitle1 !== "none" && i.append("g").attr("class", "cardinality").append("text").attr("class", "type1").attr("x", y).attr("y", m).attr("fill", "black").attr("font-size", "6").text(t.relationTitle1), t.relationTitle2 !== void 0 && t.relationTitle2 !== "none" && i.append("g").attr("class", "cardinality").append("text").attr("class", "type2").attr("x", w).attr("y", b).attr("fill", "black").attr("font-size", "6").text(t.relationTitle2), _++;
}, J = function(i, a, t, o) {
  u.debug("Rendering class ", a, t);
  const p = a.id, g = {
    id: p,
    label: a.id,
    width: 0,
    height: 0
  }, s = i.append("g").attr("id", o.db.lookUpDomId(p)).attr("class", "classGroup");
  let c;
  a.link ? c = s.append("svg:a").attr("xlink:href", a.link).attr("target", a.linkTarget).append("text").attr("y", t.textHeight + t.padding).attr("x", 0) : c = s.append("text").attr("y", t.textHeight + t.padding).attr("x", 0);
  let n = !0;
  a.annotations.forEach(function(d) {
    const l = c.append("tspan").text("«" + d + "»");
    n || l.attr("dy", t.textHeight), n = !1;
  });
  let r = C(a);
  const f = c.append("tspan").text(r).attr("class", "title");
  n || f.attr("dy", t.textHeight);
  const h = c.node().getBBox().height;
  let x, k, y;
  if (a.members.length > 0) {
    x = s.append("line").attr("x1", 0).attr("y1", t.padding + h + t.dividerMargin / 2).attr("y2", t.padding + h + t.dividerMargin / 2);
    const d = s.append("text").attr("x", t.padding).attr("y", h + t.dividerMargin + t.textHeight).attr("fill", "white").attr("class", "classText");
    n = !0, a.members.forEach(function(l) {
      v(d, l, n, t), n = !1;
    }), k = d.node().getBBox();
  }
  if (a.methods.length > 0) {
    y = s.append("line").attr("x1", 0).attr("y1", t.padding + h + t.dividerMargin + k.height).attr("y2", t.padding + h + t.dividerMargin + k.height);
    const d = s.append("text").attr("x", t.padding).attr("y", h + 2 * t.dividerMargin + k.height + t.textHeight).attr("fill", "white").attr("class", "classText");
    n = !0, a.methods.forEach(function(l) {
      v(d, l, n, t), n = !1;
    });
  }
  const m = s.node().getBBox();
  var w = " ";
  a.cssClasses.length > 0 && (w = w + a.cssClasses.join(" "));
  const e = s.insert("rect", ":first-child").attr("x", 0).attr("y", 0).attr("width", m.width + 2 * t.padding).attr("height", m.height + t.padding + 0.5 * t.dividerMargin).attr("class", w).node().getBBox().width;
  return c.node().childNodes.forEach(function(d) {
    d.setAttribute("x", (e - d.getBBox().width) / 2);
  }), a.tooltip && c.insert("title").text(a.tooltip), x && x.attr("x2", e), y && y.attr("x2", e), g.width = e, g.height = m.height + t.padding + 0.5 * t.dividerMargin, g;
}, C = function(i) {
  let a = i.id;
  return i.type && (a += "<" + I(i.type) + ">"), a;
}, Z = function(i, a, t, o) {
  u.debug("Rendering note ", a, t);
  const p = a.id, g = {
    id: p,
    text: a.text,
    width: 0,
    height: 0
  }, s = i.append("g").attr("id", p).attr("class", "classGroup");
  let c = s.append("text").attr("y", t.textHeight + t.padding).attr("x", 0);
  const n = JSON.parse(`"${a.text}"`).split(`
`);
  n.forEach(function(x) {
    u.debug(`Adding line: ${x}`), c.append("tspan").text(x).attr("class", "title").attr("dy", t.textHeight);
  });
  const r = s.node().getBBox(), h = s.insert("rect", ":first-child").attr("x", 0).attr("y", 0).attr("width", r.width + 2 * t.padding).attr(
    "height",
    r.height + n.length * t.textHeight + t.padding + 0.5 * t.dividerMargin
  ).node().getBBox().width;
  return c.node().childNodes.forEach(function(x) {
    x.setAttribute("x", (h - x.getBBox().width) / 2);
  }), g.width = h, g.height = r.height + n.length * t.textHeight + t.padding + 0.5 * t.dividerMargin, g;
}, v = function(i, a, t, o) {
  const { displayText: p, cssStyle: g } = a.getDisplayDetails(), s = i.append("tspan").attr("x", o.padding).text(p);
  g !== "" && s.attr("style", a.cssStyle), t || s.attr("dy", o.textHeight);
}, N = {
  getClassTitleString: C,
  drawClass: J,
  drawEdge: $,
  drawNote: Z
};
let T = {};
const E = 20, L = function(i) {
  const a = Object.entries(T).find((t) => t[1].label === i);
  if (a)
    return a[0];
}, R = function(i) {
  i.append("defs").append("marker").attr("id", "extensionStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 1,7 L18,13 V 1 Z"), i.append("defs").append("marker").attr("id", "extensionEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 1,1 V 13 L18,7 Z"), i.append("defs").append("marker").attr("id", "compositionStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), i.append("defs").append("marker").attr("id", "compositionEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), i.append("defs").append("marker").attr("id", "aggregationStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), i.append("defs").append("marker").attr("id", "aggregationEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), i.append("defs").append("marker").attr("id", "dependencyStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 5,7 L9,13 L1,7 L9,1 Z"), i.append("defs").append("marker").attr("id", "dependencyEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L14,7 L9,1 Z");
}, F = function(i, a, t, o) {
  const p = H().class;
  T = {}, u.info("Rendering diagram " + i);
  const g = H().securityLevel;
  let s;
  g === "sandbox" && (s = M("#i" + a));
  const c = g === "sandbox" ? M(s.nodes()[0].contentDocument.body) : M("body"), n = c.select(`[id='${a}']`);
  R(n);
  const r = new P({
    multigraph: !0
  });
  r.setGraph({
    isMultiGraph: !0
  }), r.setDefaultEdgeLabel(function() {
    return {};
  });
  const f = o.db.getClasses(), h = Object.keys(f);
  for (const e of h) {
    const d = f[e], l = N.drawClass(n, d, p, o);
    T[l.id] = l, r.setNode(l.id, l), u.info("Org height: " + l.height);
  }
  o.db.getRelations().forEach(function(e) {
    u.info(
      "tjoho" + L(e.id1) + L(e.id2) + JSON.stringify(e)
    ), r.setEdge(
      L(e.id1),
      L(e.id2),
      {
        relation: e
      },
      e.title || "DEFAULT"
    );
  }), o.db.getNotes().forEach(function(e) {
    u.debug(`Adding note: ${JSON.stringify(e)}`);
    const d = N.drawNote(n, e, p, o);
    T[d.id] = d, r.setNode(d.id, d), e.class && e.class in f && r.setEdge(
      e.id,
      L(e.class),
      {
        relation: {
          id1: e.id,
          id2: e.class,
          relation: {
            type1: "none",
            type2: "none",
            lineType: 10
          }
        }
      },
      "DEFAULT"
    );
  }), X(r), r.nodes().forEach(function(e) {
    e !== void 0 && r.node(e) !== void 0 && (u.debug("Node " + e + ": " + JSON.stringify(r.node(e))), c.select("#" + (o.db.lookUpDomId(e) || e)).attr(
      "transform",
      "translate(" + (r.node(e).x - r.node(e).width / 2) + "," + (r.node(e).y - r.node(e).height / 2) + " )"
    ));
  }), r.edges().forEach(function(e) {
    e !== void 0 && r.edge(e) !== void 0 && (u.debug("Edge " + e.v + " -> " + e.w + ": " + JSON.stringify(r.edge(e))), N.drawEdge(n, r.edge(e), r.edge(e).relation, p, o));
  });
  const y = n.node().getBBox(), m = y.width + E * 2, w = y.height + E * 2;
  O(n, w, m, p.useMaxWidth);
  const b = `${y.x - E} ${y.y - E} ${m} ${w}`;
  u.debug(`viewBox ${b}`), n.attr("viewBox", b);
}, z = {
  draw: F
}, D = {
  parser: G,
  db: S,
  renderer: z,
  styles: A,
  init: (i) => {
    i.class || (i.class = {}), i.class.arrowMarkerAbsolute = i.arrowMarkerAbsolute, S.clear();
  }
};
export {
  D as diagram
};
