import { p as W, d as M, s as H } from "./styles-55d85316.js";
import { g as S, l as d, f as u } from "./config-e567ef17.js";
import { G as X, l as Y } from "./layout-d6d8be39.js";
import { s as l } from "./svgDraw-c034b55e.js";
import { c as Z } from "./setupGraphViewbox-a4603a92.js";
import "./utils-aa888deb.js";
import "./commonDb-4dc3d465.js";
import "./mermaidAPI-04b5c286.js";
import "./errorRenderer-a3c4bedb.js";
import "./isPlainObject-a5cb4071.js";
import "./array-2ff2c7a6.js";
import "./constant-2fe7eae5.js";
let h = {};
const g = 20, p = function(e) {
  const s = Object.entries(h).find((k) => k[1].label === e);
  if (s)
    return s[0];
}, D = function(e) {
  e.append("defs").append("marker").attr("id", "extensionStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 1,7 L18,13 V 1 Z"), e.append("defs").append("marker").attr("id", "extensionEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 1,1 V 13 L18,7 Z"), e.append("defs").append("marker").attr("id", "compositionStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), e.append("defs").append("marker").attr("id", "compositionEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), e.append("defs").append("marker").attr("id", "aggregationStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), e.append("defs").append("marker").attr("id", "aggregationEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), e.append("defs").append("marker").attr("id", "dependencyStart").attr("class", "extension").attr("refX", 0).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 5,7 L9,13 L1,7 L9,1 Z"), e.append("defs").append("marker").attr("id", "dependencyEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L14,7 L9,1 Z");
}, $ = function(e, s, k, a) {
  const f = S().class;
  h = {}, d.info("Rendering diagram " + e);
  const L = S().securityLevel;
  let y;
  L === "sandbox" && (y = u("#i" + s));
  const x = L === "sandbox" ? u(y.nodes()[0].contentDocument.body) : u("body"), n = x.select(`[id='${s}']`);
  D(n);
  const r = new X({
    multigraph: !0
  });
  r.setGraph({
    isMultiGraph: !0
  }), r.setDefaultEdgeLabel(function() {
    return {};
  });
  const m = a.db.getClasses(), N = Object.keys(m);
  for (const t of N) {
    const o = m[t], i = l.drawClass(n, o, f, a);
    h[i.id] = i, r.setNode(i.id, i), d.info("Org height: " + i.height);
  }
  a.db.getRelations().forEach(function(t) {
    d.info(
      "tjoho" + p(t.id1) + p(t.id2) + JSON.stringify(t)
    ), r.setEdge(
      p(t.id1),
      p(t.id2),
      {
        relation: t
      },
      t.title || "DEFAULT"
    );
  }), a.db.getNotes().forEach(function(t) {
    d.debug(`Adding note: ${JSON.stringify(t)}`);
    const o = l.drawNote(n, t, f, a);
    h[o.id] = o, r.setNode(o.id, o), t.class && t.class in m && r.setEdge(
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
  }), Y(r), r.nodes().forEach(function(t) {
    t !== void 0 && r.node(t) !== void 0 && (d.debug("Node " + t + ": " + JSON.stringify(r.node(t))), x.select("#" + (a.db.lookUpDomId(t) || t)).attr(
      "transform",
      "translate(" + (r.node(t).x - r.node(t).width / 2) + "," + (r.node(t).y - r.node(t).height / 2) + " )"
    ));
  }), r.edges().forEach(function(t) {
    t !== void 0 && r.edge(t) !== void 0 && (d.debug("Edge " + t.v + " -> " + t.w + ": " + JSON.stringify(r.edge(t))), l.drawEdge(n, r.edge(t), r.edge(t).relation, f, a));
  });
  const c = n.node().getBBox(), E = c.width + g * 2, b = c.height + g * 2;
  Z(n, b, E, f.useMaxWidth);
  const w = `${c.x - g} ${c.y - g} ${E} ${b}`;
  d.debug(`viewBox ${w}`), n.attr("viewBox", w);
}, B = {
  draw: $
}, q = {
  parser: W,
  db: M,
  renderer: B,
  styles: H,
  init: (e) => {
    e.class || (e.class = {}), e.class.arrowMarkerAbsolute = e.arrowMarkerAbsolute, M.clear();
  }
};
export {
  q as diagram
};
//# sourceMappingURL=classDiagram-17eafd8a.js.map
