import { d as N, p as C, s as U } from "./styles-d2effb1a.js";
import { g as t, e as L, l as b, f as H } from "./config-e567ef17.js";
import { G as P, l as F } from "./layout-d6d8be39.js";
import { E as O, u as X } from "./utils-aa888deb.js";
import { l as J } from "./isPlainObject-a5cb4071.js";
import { c as Y } from "./setupGraphViewbox-a4603a92.js";
import "./mermaidAPI-04b5c286.js";
import "./errorRenderer-a3c4bedb.js";
import "./commonDb-4dc3d465.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
const T = {}, $ = (e, i) => {
  T[e] = i;
}, v = (e) => T[e], R = () => Object.keys(T), I = () => R().length, _ = {
  get: v,
  set: $,
  keys: R,
  size: I
}, q = (e) => e.append("circle").attr("class", "start-state").attr("r", t().state.sizeUnit).attr("cx", t().state.padding + t().state.sizeUnit).attr("cy", t().state.padding + t().state.sizeUnit), Z = (e) => e.append("line").style("stroke", "grey").style("stroke-dasharray", "3").attr("x1", t().state.textHeight).attr("class", "divider").attr("x2", t().state.textHeight * 2).attr("y1", 0).attr("y2", 0), j = (e, i) => {
  const o = e.append("text").attr("x", 2 * t().state.padding).attr("y", t().state.textHeight + 2 * t().state.padding).attr("font-size", t().state.fontSize).attr("class", "state-title").text(i.id), d = o.node().getBBox();
  return e.insert("rect", ":first-child").attr("x", t().state.padding).attr("y", t().state.padding).attr("width", d.width + 2 * t().state.padding).attr("height", d.height + 2 * t().state.padding).attr("rx", t().state.radius), o;
}, D = (e, i) => {
  const o = function(c, m, f) {
    const S = c.append("tspan").attr("x", 2 * t().state.padding).text(m);
    f || S.attr("dy", t().state.textHeight);
  }, s = e.append("text").attr("x", 2 * t().state.padding).attr("y", t().state.textHeight + 1.3 * t().state.padding).attr("font-size", t().state.fontSize).attr("class", "state-title").text(i.descriptions[0]).node().getBBox(), g = s.height, p = e.append("text").attr("x", t().state.padding).attr(
    "y",
    g + t().state.padding * 0.4 + t().state.dividerMargin + t().state.textHeight
  ).attr("class", "state-description");
  let a = !0, r = !0;
  i.descriptions.forEach(function(c) {
    a || (o(p, c, r), r = !1), a = !1;
  });
  const w = e.append("line").attr("x1", t().state.padding).attr("y1", t().state.padding + g + t().state.dividerMargin / 2).attr("y2", t().state.padding + g + t().state.dividerMargin / 2).attr("class", "descr-divider"), x = p.node().getBBox(), l = Math.max(x.width, s.width);
  return w.attr("x2", l + 3 * t().state.padding), e.insert("rect", ":first-child").attr("x", t().state.padding).attr("y", t().state.padding).attr("width", l + 2 * t().state.padding).attr("height", x.height + g + 2 * t().state.padding).attr("rx", t().state.radius), e;
}, K = (e, i, o) => {
  const d = t().state.padding, s = 2 * t().state.padding, g = e.node().getBBox(), p = g.width, a = g.x, r = e.append("text").attr("x", 0).attr("y", t().state.titleShift).attr("font-size", t().state.fontSize).attr("class", "state-title").text(i.id), x = r.node().getBBox().width + s;
  let l = Math.max(x, p);
  l === p && (l = l + s);
  let c;
  const m = e.node().getBBox();
  i.doc, c = a - d, x > p && (c = (p - l) / 2 + d), Math.abs(a - m.x) < d && x > p && (c = a - (x - p) / 2);
  const f = 1 - t().state.textHeight;
  return e.insert("rect", ":first-child").attr("x", c).attr("y", f).attr("class", o ? "alt-composit" : "composit").attr("width", l).attr(
    "height",
    m.height + t().state.textHeight + t().state.titleShift + 1
  ).attr("rx", "0"), r.attr("x", c + d), x <= p && r.attr("x", a + (l - s) / 2 - x / 2 + d), e.insert("rect", ":first-child").attr("x", c).attr(
    "y",
    t().state.titleShift - t().state.textHeight - t().state.padding
  ).attr("width", l).attr("height", t().state.textHeight * 3).attr("rx", t().state.radius), e.insert("rect", ":first-child").attr("x", c).attr(
    "y",
    t().state.titleShift - t().state.textHeight - t().state.padding
  ).attr("width", l).attr("height", m.height + 3 + 2 * t().state.textHeight).attr("rx", t().state.radius), e;
}, Q = (e) => (e.append("circle").attr("class", "end-state-outer").attr("r", t().state.sizeUnit + t().state.miniPadding).attr(
  "cx",
  t().state.padding + t().state.sizeUnit + t().state.miniPadding
).attr(
  "cy",
  t().state.padding + t().state.sizeUnit + t().state.miniPadding
), e.append("circle").attr("class", "end-state-inner").attr("r", t().state.sizeUnit).attr("cx", t().state.padding + t().state.sizeUnit + 2).attr("cy", t().state.padding + t().state.sizeUnit + 2)), V = (e, i) => {
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
  const a = p.split(L.lineBreakRegex);
  let r = 1.25 * t().state.noteMargin;
  for (const w of a) {
    const x = w.trim();
    if (x.length > 0) {
      const l = g.append("tspan");
      if (l.text(x), r === 0) {
        const c = l.node().getBBox();
        r += c.height;
      }
      s += r, l.attr("x", i + t().state.noteMargin), l.attr("y", o + s + 1.25 * t().state.noteMargin);
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
  i.type === "start" && q(s), i.type === "end" && Q(s), (i.type === "fork" || i.type === "join") && V(s, i), i.type === "note" && et(i.note.text, s), i.type === "divider" && Z(s), i.type === "default" && i.descriptions.length === 0 && j(s, i), i.type === "default" && i.descriptions.length > 0 && D(s, i);
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
  const s = i.points, g = J().x(function(r) {
    return r.x;
  }).y(function(r) {
    return r.y;
  }).curve(O), p = e.append("path").attr("d", g(s)).attr("id", "edge" + A).attr("class", "transition");
  let a = "";
  if (t().state.arrowMarkerAbsolute && (a = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search, a = a.replace(/\(/g, "\\("), a = a.replace(/\)/g, "\\)")), p.attr(
    "marker-end",
    "url(" + a + "#" + d(N.relationType.DEPENDENCY) + "End)"
  ), o.title !== void 0) {
    const r = e.append("g").attr("class", "stateLabel"), { x: w, y: x } = X.calcLabelPosition(i.points), l = L.getRows(o.title);
    let c = 0;
    const m = [];
    let f = 0, S = 0;
    for (let u = 0; u <= l.length; u++) {
      const h = r.append("text").attr("text-anchor", "middle").text(l[u]).attr("x", w).attr("y", x + c), y = h.node().getBBox();
      f = Math.max(f, y.width), S = Math.min(S, y.x), b.info(y.x, w, x + c), c === 0 && (c = h.node().getBBox().height, b.info("Title height", c, x)), m.push(h);
    }
    let k = c * l.length;
    if (l.length > 1) {
      const u = (l.length - 1) * c * 0.5;
      m.forEach((h, y) => h.attr("y", x + y * c - u)), k = c * l.length;
    }
    const n = r.node().getBBox();
    r.insert("rect", ":first-child").attr("class", "box").attr("x", w - f / 2 - t().state.padding / 2).attr("y", x - k / 2 - t().state.padding / 2 - 3.5).attr("width", f + t().state.padding).attr("height", k + t().state.padding), b.info(n);
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
  nt(r), new P({
    multigraph: !0,
    compound: !0,
    // acyclicer: 'greedy',
    rankdir: "RL"
    // ranksep: '20'
  }).setDefaultEdgeLabel(function() {
    return {};
  });
  const x = d.db.getRootDoc();
  W(x, r, void 0, !1, p, a, d);
  const l = B.padding, c = r.node().getBBox(), m = c.width + l * 2, f = c.height + l * 2, S = m * 1.75;
  Y(r, f, S, B.useMaxWidth), r.attr(
    "viewBox",
    `${c.x - B.padding}  ${c.y - B.padding} ` + m + " " + f
  );
}, rt = (e) => e ? e.length * B.fontSizeFactor : 1, W = (e, i, o, d, s, g, p) => {
  const a = new P({
    compound: !0,
    multigraph: !0
  });
  let r, w = !0;
  for (r = 0; r < e.length; r++)
    if (e[r].stmt === "relation") {
      w = !1;
      break;
    }
  o ? a.setGraph({
    rankdir: "LR",
    multigraph: !0,
    compound: !0,
    // acyclicer: 'greedy',
    ranker: "tight-tree",
    ranksep: w ? 1 : B.edgeLengthFactor,
    nodeSep: w ? 1 : 50,
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
    ranksep: w ? 1 : B.edgeLengthFactor,
    nodeSep: w ? 1 : 50,
    ranker: "tight-tree",
    // ranker: 'network-simplex'
    isMultiGraph: !0
  }), a.setDefaultEdgeLabel(function() {
    return {};
  }), p.db.extract(e);
  const x = p.db.getStates(), l = p.db.getRelations(), c = Object.keys(x);
  for (const n of c) {
    const u = x[n];
    o && (u.parentId = o);
    let h;
    if (u.doc) {
      let y = i.append("g").attr("id", u.id).attr("class", "stateGroup");
      h = W(u.doc, y, u.id, !d, s, g, p);
      {
        y = K(y, u, d);
        let E = y.node().getBBox();
        h.width = E.width, h.height = E.height + B.padding / 2, z[u.id] = { y: B.compositTitleSize };
      }
    } else
      h = G(i, u);
    if (u.note) {
      const y = {
        descriptions: [],
        id: u.id + "-note",
        note: u.note,
        type: "note"
      }, E = G(i, y);
      u.note.position === "left of" ? (a.setNode(h.id + "-note", E), a.setNode(h.id, h)) : (a.setNode(h.id, h), a.setNode(h.id + "-note", E)), a.setParent(h.id, h.id + "-group"), a.setParent(h.id + "-note", h.id + "-group");
    } else
      a.setNode(h.id, h);
  }
  b.debug("Count=", a.nodeCount(), a);
  let m = 0;
  l.forEach(function(n) {
    m++, b.debug("Setting edge", n), a.setEdge(
      n.id1,
      n.id2,
      {
        relation: n,
        width: rt(n.title),
        height: B.labelHeight * L.getRows(n.title).length,
        labelpos: "c"
      },
      "id" + m
    );
  }), F(a), b.debug("Graph after layout", a.nodes());
  const f = i.node();
  a.nodes().forEach(function(n) {
    n !== void 0 && a.node(n) !== void 0 ? (b.warn("Node " + n + ": " + JSON.stringify(a.node(n))), s.select("#" + f.id + " #" + n).attr(
      "transform",
      "translate(" + (a.node(n).x - a.node(n).width / 2) + "," + (a.node(n).y + (z[n] ? z[n].y : 0) - a.node(n).height / 2) + " )"
    ), s.select("#" + f.id + " #" + n).attr("data-x-shift", a.node(n).x - a.node(n).width / 2), g.querySelectorAll("#" + f.id + " #" + n + " .divider").forEach((h) => {
      const y = h.parentElement;
      let E = 0, M = 0;
      y && (y.parentElement && (E = y.parentElement.getBBox().width), M = parseInt(y.getAttribute("data-x-shift"), 10), Number.isNaN(M) && (M = 0)), h.setAttribute("x1", 0 - M + 8), h.setAttribute("x2", E - M - 8);
    })) : b.debug("No Node " + n + ": " + JSON.stringify(a.node(n)));
  });
  let S = f.getBBox();
  a.edges().forEach(function(n) {
    n !== void 0 && a.edge(n) !== void 0 && (b.debug("Edge " + n.v + " -> " + n.w + ": " + JSON.stringify(a.edge(n))), at(i, a.edge(n), a.edge(n).relation));
  }), S = f.getBBox();
  const k = {
    id: o || "root",
    label: o || "root",
    width: 0,
    height: 0
  };
  return k.width = S.width + 2 * B.padding, k.height = S.height + 2 * B.padding, b.debug("Doc rendered", k, a), k;
}, ot = {
  setConf: it,
  draw: st
}, mt = {
  parser: C,
  db: N,
  renderer: ot,
  styles: U,
  init: (e) => {
    e.state || (e.state = {}), e.state.arrowMarkerAbsolute = e.arrowMarkerAbsolute, N.clear();
  }
};
export {
  mt as diagram
};
//# sourceMappingURL=stateDiagram-4e5e77ae.js.map
