import { l as b, v as w } from "./config-e567ef17.js";
import { E as C, u as E } from "./utils-aa888deb.js";
import { l as k } from "./isPlainObject-a5cb4071.js";
let M = 0;
const O = function(i, e, t, r, n) {
  const a = function(o) {
    switch (o) {
      case n.db.relationType.AGGREGATION:
        return "aggregation";
      case n.db.relationType.EXTENSION:
        return "extension";
      case n.db.relationType.COMPOSITION:
        return "composition";
      case n.db.relationType.DEPENDENCY:
        return "dependency";
      case n.db.relationType.LOLLIPOP:
        return "lollipop";
    }
  };
  e.points = e.points.filter((o) => !Number.isNaN(o.y));
  const l = e.points, d = k().x(function(o) {
    return o.x;
  }).y(function(o) {
    return o.y;
  }).curve(C), s = i.append("path").attr("d", d(l)).attr("id", "edge" + M).attr("class", "relation");
  let g = "";
  r.arrowMarkerAbsolute && (g = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search, g = g.replace(/\(/g, "\\("), g = g.replace(/\)/g, "\\)")), t.relation.lineType == 1 && s.attr("class", "relation dashed-line"), t.relation.lineType == 10 && s.attr("class", "relation dotted-line"), t.relation.type1 !== "none" && s.attr(
    "marker-start",
    "url(" + g + "#" + a(t.relation.type1) + "Start)"
  ), t.relation.type2 !== "none" && s.attr(
    "marker-end",
    "url(" + g + "#" + a(t.relation.type2) + "End)"
  );
  let f, c;
  const p = e.points.length;
  let B = E.calcLabelPosition(e.points);
  f = B.x, c = B.y;
  let x, v, N, m;
  if (p % 2 !== 0 && p > 1) {
    let o = E.calcCardinalityPosition(
      t.relation.type1 !== "none",
      e.points,
      e.points[0]
    ), u = E.calcCardinalityPosition(
      t.relation.type2 !== "none",
      e.points,
      e.points[p - 1]
    );
    b.debug("cardinality_1_point " + JSON.stringify(o)), b.debug("cardinality_2_point " + JSON.stringify(u)), x = o.x, v = o.y, N = u.x, m = u.y;
  }
  if (t.title !== void 0) {
    const o = i.append("g").attr("class", "classLabel"), u = o.append("text").attr("class", "label").attr("x", f).attr("y", c).attr("fill", "red").attr("text-anchor", "middle").text(t.title);
    window.label = u;
    const h = u.node().getBBox();
    o.insert("rect", ":first-child").attr("class", "box").attr("x", h.x - r.padding / 2).attr("y", h.y - r.padding / 2).attr("width", h.width + r.padding).attr("height", h.height + r.padding);
  }
  b.info("Rendering relation " + JSON.stringify(t)), t.relationTitle1 !== void 0 && t.relationTitle1 !== "none" && i.append("g").attr("class", "cardinality").append("text").attr("class", "type1").attr("x", x).attr("y", v).attr("fill", "black").attr("font-size", "6").text(t.relationTitle1), t.relationTitle2 !== void 0 && t.relationTitle2 !== "none" && i.append("g").attr("class", "cardinality").append("text").attr("class", "type2").attr("x", N).attr("y", m).attr("fill", "black").attr("font-size", "6").text(t.relationTitle2), M++;
}, P = function(i, e, t, r) {
  b.debug("Rendering class ", e, t);
  const n = e.id, a = {
    id: n,
    label: e.id,
    width: 0,
    height: 0
  }, l = i.append("g").attr("id", r.db.lookUpDomId(n)).attr("class", "classGroup");
  let d;
  e.link ? d = l.append("svg:a").attr("xlink:href", e.link).attr("target", e.linkTarget).append("text").attr("y", t.textHeight + t.padding).attr("x", 0) : d = l.append("text").attr("y", t.textHeight + t.padding).attr("x", 0);
  let s = !0;
  e.annotations.forEach(function(y) {
    const H = d.append("tspan").text("«" + y + "»");
    s || H.attr("dy", t.textHeight), s = !1;
  });
  let g = e.id;
  e.type !== void 0 && e.type !== "" && (g += "<" + e.type + ">");
  const f = d.append("tspan").text(g).attr("class", "title");
  s || f.attr("dy", t.textHeight);
  const c = d.node().getBBox().height, p = l.append("line").attr("x1", 0).attr("y1", t.padding + c + t.dividerMargin / 2).attr("y2", t.padding + c + t.dividerMargin / 2), B = l.append("text").attr("x", t.padding).attr("y", c + t.dividerMargin + t.textHeight).attr("fill", "white").attr("class", "classText");
  s = !0, e.members.forEach(function(y) {
    _(B, y, s, t), s = !1;
  });
  const x = B.node().getBBox(), v = l.append("line").attr("x1", 0).attr("y1", t.padding + c + t.dividerMargin + x.height).attr("y2", t.padding + c + t.dividerMargin + x.height), N = l.append("text").attr("x", t.padding).attr("y", c + 2 * t.dividerMargin + x.height + t.textHeight).attr("fill", "white").attr("class", "classText");
  s = !0, e.methods.forEach(function(y) {
    _(N, y, s, t), s = !1;
  });
  const m = l.node().getBBox();
  var o = " ";
  e.cssClasses.length > 0 && (o = o + e.cssClasses.join(" "));
  const h = l.insert("rect", ":first-child").attr("x", 0).attr("y", 0).attr("width", m.width + 2 * t.padding).attr("height", m.height + t.padding + 0.5 * t.dividerMargin).attr("class", o).node().getBBox().width;
  return d.node().childNodes.forEach(function(y) {
    y.setAttribute("x", (h - y.getBBox().width) / 2);
  }), e.tooltip && d.insert("title").text(e.tooltip), p.attr("x2", h), v.attr("x2", h), a.width = h, a.height = m.height + t.padding + 0.5 * t.dividerMargin, a;
}, I = function(i, e, t, r) {
  b.debug("Rendering note ", e, t);
  const n = e.id, a = {
    id: n,
    text: e.text,
    width: 0,
    height: 0
  }, l = i.append("g").attr("id", n).attr("class", "classGroup");
  let d = l.append("text").attr("y", t.textHeight + t.padding).attr("x", 0);
  const s = JSON.parse(`"${e.text}"`).split(`
`);
  s.forEach(function(p) {
    b.debug(`Adding line: ${p}`), d.append("tspan").text(p).attr("class", "title").attr("dy", t.textHeight);
  });
  const g = l.node().getBBox(), c = l.insert("rect", ":first-child").attr("x", 0).attr("y", 0).attr("width", g.width + 2 * t.padding).attr(
    "height",
    g.height + s.length * t.textHeight + t.padding + 0.5 * t.dividerMargin
  ).node().getBBox().width;
  return d.node().childNodes.forEach(function(p) {
    p.setAttribute("x", (c - p.getBBox().width) / 2);
  }), a.width = c, a.height = g.height + s.length * t.textHeight + t.padding + 0.5 * t.dividerMargin, a;
}, T = function(i) {
  const e = /^([#+~-])?(\w+)(~\w+~|\[])?\s+(\w+) *([$*])?$/, t = /^([#+|~-])?(\w+) *\( *(.*)\) *([$*])? *(\w*[[\]|~]*\s*\w*~?)$/;
  let r = i.match(e), n = i.match(t);
  return r && !n ? L(r) : n ? R(n) : $(i);
}, L = function(i) {
  let e = "", t = "";
  try {
    let r = i[1] ? i[1].trim() : "", n = i[2] ? i[2].trim() : "", a = i[3] ? w(i[3].trim()) : "", l = i[4] ? i[4].trim() : "", d = i[5] ? i[5].trim() : "";
    t = r + n + a + " " + l, e = S(d);
  } catch {
    t = i;
  }
  return {
    displayText: t,
    cssStyle: e
  };
}, R = function(i) {
  let e = "", t = "";
  try {
    let r = i[1] ? i[1].trim() : "", n = i[2] ? i[2].trim() : "", a = i[3] ? w(i[3].trim()) : "", l = i[4] ? i[4].trim() : "", d = i[5] ? " : " + w(i[5]).trim() : "";
    t = r + n + "(" + a + ")" + d, e = S(l);
  } catch {
    t = i;
  }
  return {
    displayText: t,
    cssStyle: e
  };
}, $ = function(i) {
  let e = "", t = "", r = "", n = i.indexOf("("), a = i.indexOf(")");
  if (n > 1 && a > n && a <= i.length) {
    let l = "", d = "", s = i.substring(0, 1);
    s.match(/\w/) ? d = i.substring(0, n).trim() : (s.match(/[#+~-]/) && (l = s), d = i.substring(1, n).trim());
    const g = i.substring(n + 1, a);
    i.substring(a + 1, 1), t = S(i.substring(a + 1, a + 2)), e = l + d + "(" + w(g.trim()) + ")", a < i.length && (r = i.substring(a + 2).trim(), r !== "" && (r = " : " + w(r), e += r));
  } else
    e = w(i);
  return {
    displayText: e,
    cssStyle: t
  };
}, _ = function(i, e, t, r) {
  let n = T(e);
  const a = i.append("tspan").attr("x", r.padding).text(n.displayText);
  n.cssStyle !== "" && a.attr("style", n.cssStyle), t || a.attr("dy", r.textHeight);
}, S = function(i) {
  switch (i) {
    case "*":
      return "font-style:italic;";
    case "$":
      return "text-decoration:underline;";
    default:
      return "";
  }
}, F = {
  drawClass: P,
  drawEdge: O,
  drawNote: I,
  parseMember: T
};
export {
  T as p,
  F as s
};
//# sourceMappingURL=svgDraw-c034b55e.js.map
