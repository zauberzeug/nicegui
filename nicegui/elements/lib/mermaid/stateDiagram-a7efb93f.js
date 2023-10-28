import { d as N, p as C, s as R } from "./styles-554c1edb.js";
import { c as t, F as U, z as F, f as T, l as b, j as H, k as O } from "./mermaid-5f2d2ec5.js";
import { G as X, l as J } from "./layout-1caf14c9.js";
import { l as Y } from "./line-9d49a987.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
const L = {}, $ = (e, i) => {
  L[e] = i;
}, v = (e) => L[e], P = () => Object.keys(L), I = () => P().length, _ = {
  get: v,
  set: $,
  keys: P,
  size: I
}, j = (e) => e.append("circle").attr("class", "start-state").attr("r", t().state.sizeUnit).attr("cx", t().state.padding + t().state.sizeUnit).attr("cy", t().state.padding + t().state.sizeUnit), q = (e) => e.append("line").style("stroke", "grey").style("stroke-dasharray", "3").attr("x1", t().state.textHeight).attr("class", "divider").attr("x2", t().state.textHeight * 2).attr("y1", 0).attr("y2", 0), Z = (e, i) => {
  const o = e.append("text").attr("x", 2 * t().state.padding).attr("y", t().state.textHeight + 2 * t().state.padding).attr("font-size", t().state.fontSize).attr("class", "state-title").text(i.id), d = o.node().getBBox();
  return e.insert("rect", ":first-child").attr("x", t().state.padding).attr("y", t().state.padding).attr("width", d.width + 2 * t().state.padding).attr("height", d.height + 2 * t().state.padding).attr("rx", t().state.radius), o;
}, K = (e, i) => {
  const o = function(l, m, w) {
    const k = l.append("tspan").attr("x", 2 * t().state.padding).text(m);
    w || k.attr("dy", t().state.textHeight);
  }, s = e.append("text").attr("x", 2 * t().state.padding).attr("y", t().state.textHeight + 1.3 * t().state.padding).attr("font-size", t().state.fontSize).attr("class", "state-title").text(i.descriptions[0]).node().getBBox(), g = s.height, p = e.append("text").attr("x", t().state.padding).attr(
    "y",
    g + t().state.padding * 0.4 + t().state.dividerMargin + t().state.textHeight
  ).attr("class", "state-description");
  let a = !0, r = !0;
  i.descriptions.forEach(function(l) {
    a || (o(p, l, r), r = !1), a = !1;
  });
  const y = e.append("line").attr("x1", t().state.padding).attr("y1", t().state.padding + g + t().state.dividerMargin / 2).attr("y2", t().state.padding + g + t().state.dividerMargin / 2).attr("class", "descr-divider"), x = p.node().getBBox(), c = Math.max(x.width, s.width);
  return y.attr("x2", c + 3 * t().state.padding), e.insert("rect", ":first-child").attr("x", t().state.padding).attr("y", t().state.padding).attr("width", c + 2 * t().state.padding).attr("height", x.height + g + 2 * t().state.padding).attr("rx", t().state.radius), e;
}, Q = (e, i, o) => {
  const d = t().state.padding, s = 2 * t().state.padding, g = e.node().getBBox(), p = g.width, a = g.x, r = e.append("text").attr("x", 0).attr("y", t().state.titleShift).attr("font-size", t().state.fontSize).attr("class", "state-title").text(i.id), x = r.node().getBBox().width + s;
  let c = Math.max(x, p);
  c === p && (c = c + s);
  let l;
  const m = e.node().getBBox();
  i.doc, l = a - d, x > p && (l = (p - c) / 2 + d), Math.abs(a - m.x) < d && x > p && (l = a - (x - p) / 2);
  const w = 1 - t().state.textHeight;
  return e.insert("rect", ":first-child").attr("x", l).attr("y", w).attr("class", o ? "alt-composit" : "composit").attr("width", c).attr(
    "height",
    m.height + t().state.textHeight + t().state.titleShift + 1
  ).attr("rx", "0"), r.attr("x", l + d), x <= p && r.attr("x", a + (c - s) / 2 - x / 2 + d), e.insert("rect", ":first-child").attr("x", l).attr(
    "y",
    t().state.titleShift - t().state.textHeight - t().state.padding
  ).attr("width", c).attr("height", t().state.textHeight * 3).attr("rx", t().state.radius), e.insert("rect", ":first-child").attr("x", l).attr(
    "y",
    t().state.titleShift - t().state.textHeight - t().state.padding
  ).attr("width", c).attr("height", m.height + 3 + 2 * t().state.textHeight).attr("rx", t().state.radius), e;
}, V = (e) => (e.append("circle").attr("class", "end-state-outer").attr("r", t().state.sizeUnit + t().state.miniPadding).attr(
  "cx",
  t().state.padding + t().state.sizeUnit + t().state.miniPadding
).attr(
  "cy",
  t().state.padding + t().state.sizeUnit + t().state.miniPadding
), e.append("circle").attr("class", "end-state-inner").attr("r", t().state.sizeUnit).attr("cx", t().state.padding + t().state.sizeUnit + 2).attr("cy", t().state.padding + t().state.sizeUnit + 2)), D = (e, i) => {
  let o = t().state.forkWidth, d = t().state.forkHeight;
  if (i.parentId) {
    let s = o;
    o = d, d = s;
  }
  return e.append("rect").style("stroke", "black").style("fill", "black").attr("width", o).attr("height", d).attr("x", t().state.padding).attr("y", t().state.padding);
}, tt = (e, i, o, d) => {
  let s = 0;
  const g = d.append("text");
  g.style("text-anchor", "start"), g.attr("class", "noteText");
  let p = e.replace(/\r\n/g, "<br/>");
  p = p.replace(/\n/g, "<br/>");
  const a = p.split(T.lineBreakRegex);
  let r = 1.25 * t().state.noteMargin;
  for (const y of a) {
    const x = y.trim();
    if (x.length > 0) {
      const c = g.append("tspan");
      if (c.text(x), r === 0) {
        const l = c.node().getBBox();
        r += l.height;
      }
      s += r, c.attr("x", i + t().state.noteMargin), c.attr("y", o + s + 1.25 * t().state.noteMargin);
    }
  }
  return { textWidth: g.node().getBBox().width, textHeight: s };
}, et = (e, i) => {
  i.attr("class", "state-note");
  const o = i.append("rect").attr("x", 0).attr("y", t().state.padding), d = i.append("g"), { textWidth: s, textHeight: g } = tt(e, 0, 0, d);
  return o.attr("height", g + 2 * t().state.noteMargin), o.attr("width", s + t().state.noteMargin * 2), o;
}, G = function(e, i) {
  const o = i.id, d = {
    id: o,
    label: i.id,
    width: 0,
    height: 0
  }, s = e.append("g").attr("id", o).attr("class", "stateGroup");
  i.type === "start" && j(s), i.type === "end" && V(s), (i.type === "fork" || i.type === "join") && D(s, i), i.type === "note" && et(i.note.text, s), i.type === "divider" && q(s), i.type === "default" && i.descriptions.length === 0 && Z(s, i), i.type === "default" && i.descriptions.length > 0 && K(s, i);
  const g = s.node().getBBox();
  return d.width = g.width + 2 * t().state.padding, d.height = g.height + 2 * t().state.padding, _.set(o, d), d;
};
let A = 0;
const at = function(e, i, o) {
  const d = function(r) {
    switch (r) {
      case N.relationType.AGGREGATION:
        return "aggregation";
      case N.relationType.EXTENSION:
        return "extension";
      case N.relationType.COMPOSITION:
        return "composition";
      case N.relationType.DEPENDENCY:
        return "dependency";
    }
  };
  i.points = i.points.filter((r) => !Number.isNaN(r.y));
  const s = i.points, g = Y().x(function(r) {
    return r.x;
  }).y(function(r) {
    return r.y;
  }).curve(U), p = e.append("path").attr("d", g(s)).attr("id", "edge" + A).attr("class", "transition");
  let a = "";
  if (t().state.arrowMarkerAbsolute && (a = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search, a = a.replace(/\(/g, "\\("), a = a.replace(/\)/g, "\\)")), p.attr(
    "marker-end",
    "url(" + a + "#" + d(N.relationType.DEPENDENCY) + "End)"
  ), o.title !== void 0) {
    const r = e.append("g").attr("class", "stateLabel"), { x: y, y: x } = F.calcLabelPosition(i.points), c = T.getRows(o.title);
    let l = 0;
    const m = [];
    let w = 0, k = 0;
    for (let u = 0; u <= c.length; u++) {
      const h = r.append("text").attr("text-anchor", "middle").text(c[u]).attr("x", y).attr("y", x + l), f = h.node().getBBox();
      w = Math.max(w, f.width), k = Math.min(k, f.x), b.info(f.x, y, x + l), l === 0 && (l = h.node().getBBox().height, b.info("Title height", l, x)), m.push(h);
    }
    let E = l * c.length;
    if (c.length > 1) {
      const u = (c.length - 1) * l * 0.5;
      m.forEach((h, f) => h.attr("y", x + f * l - u)), E = l * c.length;
    }
    const n = r.node().getBBox();
    r.insert("rect", ":first-child").attr("class", "box").attr("x", y - w / 2 - t().state.padding / 2).attr("y", x - E / 2 - t().state.padding / 2 - 3.5).attr("width", w + t().state.padding).attr("height", E + t().state.padding), b.info(n);
  }
  A++;
};
let B;
const z = {}, it = function() {
}, nt = function(e) {
  e.append("defs").append("marker").attr("id", "dependencyEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 19,7 L9,13 L14,7 L9,1 Z");
}, st = function(e, i, o, d) {
  B = t().state;
  const s = t().securityLevel;
  let g;
  s === "sandbox" && (g = H("#i" + i));
  const p = s === "sandbox" ? H(g.nodes()[0].contentDocument.body) : H("body"), a = s === "sandbox" ? g.nodes()[0].contentDocument : document;
  b.debug("Rendering diagram " + e);
  const r = p.select(`[id='${i}']`);
  nt(r);
  const y = d.db.getRootDoc();
  W(y, r, void 0, !1, p, a, d);
  const x = B.padding, c = r.node().getBBox(), l = c.width + x * 2, m = c.height + x * 2, w = l * 1.75;
  O(r, m, w, B.useMaxWidth), r.attr(
    "viewBox",
    `${c.x - B.padding}  ${c.y - B.padding} ` + l + " " + m
  );
}, rt = (e) => e ? e.length * B.fontSizeFactor : 1, W = (e, i, o, d, s, g, p) => {
  const a = new X({
    compound: !0,
    multigraph: !0
  });
  let r, y = !0;
  for (r = 0; r < e.length; r++)
    if (e[r].stmt === "relation") {
      y = !1;
      break;
    }
  o ? a.setGraph({
    rankdir: "LR",
    multigraph: !0,
    compound: !0,
    // acyclicer: 'greedy',
    ranker: "tight-tree",
    ranksep: y ? 1 : B.edgeLengthFactor,
    nodeSep: y ? 1 : 50,
    isMultiGraph: !0
    // ranksep: 5,
    // nodesep: 1
  }) : a.setGraph({
    rankdir: "TB",
    multigraph: !0,
    compound: !0,
    // isCompound: true,
    // acyclicer: 'greedy',
    // ranker: 'longest-path'
    ranksep: y ? 1 : B.edgeLengthFactor,
    nodeSep: y ? 1 : 50,
    ranker: "tight-tree",
    // ranker: 'network-simplex'
    isMultiGraph: !0
  }), a.setDefaultEdgeLabel(function() {
    return {};
  }), p.db.extract(e);
  const x = p.db.getStates(), c = p.db.getRelations(), l = Object.keys(x);
  for (const n of l) {
    const u = x[n];
    o && (u.parentId = o);
    let h;
    if (u.doc) {
      let f = i.append("g").attr("id", u.id).attr("class", "stateGroup");
      h = W(u.doc, f, u.id, !d, s, g, p);
      {
        f = Q(f, u, d);
        let S = f.node().getBBox();
        h.width = S.width, h.height = S.height + B.padding / 2, z[u.id] = { y: B.compositTitleSize };
      }
    } else
      h = G(i, u);
    if (u.note) {
      const f = {
        descriptions: [],
        id: u.id + "-note",
        note: u.note,
        type: "note"
      }, S = G(i, f);
      u.note.position === "left of" ? (a.setNode(h.id + "-note", S), a.setNode(h.id, h)) : (a.setNode(h.id, h), a.setNode(h.id + "-note", S)), a.setParent(h.id, h.id + "-group"), a.setParent(h.id + "-note", h.id + "-group");
    } else
      a.setNode(h.id, h);
  }
  b.debug("Count=", a.nodeCount(), a);
  let m = 0;
  c.forEach(function(n) {
    m++, b.debug("Setting edge", n), a.setEdge(
      n.id1,
      n.id2,
      {
        relation: n,
        width: rt(n.title),
        height: B.labelHeight * T.getRows(n.title).length,
        labelpos: "c"
      },
      "id" + m
    );
  }), J(a), b.debug("Graph after layout", a.nodes());
  const w = i.node();
  a.nodes().forEach(function(n) {
    n !== void 0 && a.node(n) !== void 0 ? (b.warn("Node " + n + ": " + JSON.stringify(a.node(n))), s.select("#" + w.id + " #" + n).attr(
      "transform",
      "translate(" + (a.node(n).x - a.node(n).width / 2) + "," + (a.node(n).y + (z[n] ? z[n].y : 0) - a.node(n).height / 2) + " )"
    ), s.select("#" + w.id + " #" + n).attr("data-x-shift", a.node(n).x - a.node(n).width / 2), g.querySelectorAll("#" + w.id + " #" + n + " .divider").forEach((h) => {
      const f = h.parentElement;
      let S = 0, M = 0;
      f && (f.parentElement && (S = f.parentElement.getBBox().width), M = parseInt(f.getAttribute("data-x-shift"), 10), Number.isNaN(M) && (M = 0)), h.setAttribute("x1", 0 - M + 8), h.setAttribute("x2", S - M - 8);
    })) : b.debug("No Node " + n + ": " + JSON.stringify(a.node(n)));
  });
  let k = w.getBBox();
  a.edges().forEach(function(n) {
    n !== void 0 && a.edge(n) !== void 0 && (b.debug("Edge " + n.v + " -> " + n.w + ": " + JSON.stringify(a.edge(n))), at(i, a.edge(n), a.edge(n).relation));
  }), k = w.getBBox();
  const E = {
    id: o || "root",
    label: o || "root",
    width: 0,
    height: 0
  };
  return E.width = k.width + 2 * B.padding, E.height = k.height + 2 * B.padding, b.debug("Doc rendered", E, a), E;
}, ot = {
  setConf: it,
  draw: st
}, xt = {
  parser: C,
  db: N,
  renderer: ot,
  styles: R,
  init: (e) => {
    e.state || (e.state = {}), e.state.arrowMarkerAbsolute = e.arrowMarkerAbsolute, N.clear();
  }
};
export {
  xt as diagram
};
