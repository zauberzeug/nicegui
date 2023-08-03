import { p as W, d as M, s as H } from "./styles-ca8ceaa2.js";
import { c as S, l as d, j as m, k as X } from "./mermaid-be6aa4a6.js";
import { G as Y, l as Z } from "./layout-b178bd1a.js";
import { s as l } from "./svgDraw-51404f3b.js";
import "./line-d1abfd73.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
let h = {};
const g = 20, p = function(r) {
  const o = Object.entries(h).find((k) => k[1].label === r);
  if (o)
    return o[0];
}, D = function(r) {
  r.append("defs").append("marker").attr("id", "extensionStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 1,7 L18,13 V 1 Z"), r.append("defs").append("marker").attr("id", "extensionEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 1,1 V 13 L18,7 Z"), r.append("defs").append("marker").attr("id", "compositionStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), r.append("defs").append("marker").attr("id", "compositionEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), r.append("defs").append("marker").attr("id", "aggregationStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), r.append("defs").append("marker").attr("id", "aggregationEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), r.append("defs").append("marker").attr("id", "dependencyStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 5,7 L9,13 L1,7 L9,1 Z"), r.append("defs").append("marker").attr("id", "dependencyEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L14,7 L9,1 Z");
}, $ = function(r, o, k, a) {
  const c = S().class;
  h = {}, d.info("Rendering diagram " + r);
  const L = S().securityLevel;
  let y;
  L === "sandbox" && (y = m("#i" + o));
  const x = L === "sandbox" ? m(y.nodes()[0].contentDocument.body) : m("body"), n = x.select(`[id='${o}']`);
  D(n);
  const e = new Y({
    multigraph: !0
  });
  e.setGraph({
    isMultiGraph: !0
  }), e.setDefaultEdgeLabel(function() {
    return {};
  });
  const u = a.db.getClasses(), N = Object.keys(u);
  for (const t of N) {
    const s = u[t], i = l.drawClass(n, s, c, a);
    h[i.id] = i, e.setNode(i.id, i), d.info("Org height: " + i.height);
  }
  a.db.getRelations().forEach(function(t) {
    d.info(
      "tjoho" + p(t.id1) + p(t.id2) + JSON.stringify(t)
    ), e.setEdge(
      p(t.id1),
      p(t.id2),
      {
        relation: t
      },
      t.title || "DEFAULT"
    );
  }), a.db.getNotes().forEach(function(t) {
    d.debug(`Adding note: ${JSON.stringify(t)}`);
    const s = l.drawNote(n, t, c, a);
    h[s.id] = s, e.setNode(s.id, s), t.class && t.class in u && e.setEdge(
      t.id,
      p(t.class),
      {
        relation: {
          id1: t.id,
          id2: t.class,
          relation: {
            type1: "none",
            type2: "none",
            lineType: 10
          }
        }
      },
      "DEFAULT"
    );
  }), Z(e), e.nodes().forEach(function(t) {
    t !== void 0 && e.node(t) !== void 0 && (d.debug("Node " + t + ": " + JSON.stringify(e.node(t))), x.select("#" + (a.db.lookUpDomId(t) || t)).attr(
      "transform",
      "translate(" + (e.node(t).x - e.node(t).width / 2) + "," + (e.node(t).y - e.node(t).height / 2) + " )"
    ));
  }), e.edges().forEach(function(t) {
    t !== void 0 && e.edge(t) !== void 0 && (d.debug("Edge " + t.v + " -> " + t.w + ": " + JSON.stringify(e.edge(t))), l.drawEdge(n, e.edge(t), e.edge(t).relation, c, a));
  });
  const f = n.node().getBBox(), E = f.width + g * 2, b = f.height + g * 2;
  X(n, b, E, c.useMaxWidth);
  const w = `${f.x - g} ${f.y - g} ${E} ${b}`;
  d.debug(`viewBox ${w}`), n.attr("viewBox", w);
}, B = {
  draw: $
}, V = {
  parser: W,
  db: M,
  renderer: B,
  styles: H,
  init: (r) => {
    r.class || (r.class = {}), r.class.arrowMarkerAbsolute = r.arrowMarkerAbsolute, M.clear();
  }
};
export {
  V as diagram
};
