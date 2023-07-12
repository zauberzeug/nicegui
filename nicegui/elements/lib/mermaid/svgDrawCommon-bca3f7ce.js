import { e as a } from "./mermaid-be6aa4a6.js";
const l = function(s, t) {
  const r = s.append("rect");
  if (r.attr("x", t.x), r.attr("y", t.y), r.attr("fill", t.fill), r.attr("stroke", t.stroke), r.attr("width", t.width), r.attr("height", t.height), r.attr("rx", t.rx), r.attr("ry", t.ry), t.attrs !== "undefined" && t.attrs !== null)
    for (let n in t.attrs)
      r.attr(n, t.attrs[n]);
  return t.class !== "undefined" && r.attr("class", t.class), r;
}, c = function(s, t) {
  l(s, {
    x: t.startx,
    y: t.starty,
    width: t.stopx - t.startx,
    height: t.stopy - t.starty,
    fill: t.fill,
    stroke: t.stroke,
    class: "rect"
  }).lower();
}, d = function(s, t) {
  const r = t.text.replace(/<br\s*\/?>/gi, " "), n = s.append("text");
  n.attr("x", t.x), n.attr("y", t.y), n.attr("class", "legend"), n.style("text-anchor", t.anchor), t.class !== void 0 && n.attr("class", t.class);
  const e = n.append("tspan");
  return e.attr("x", t.x + t.textMargin * 2), e.text(r), n;
}, f = function(s, t, r, n) {
  const e = s.append("image");
  e.attr("x", t), e.attr("y", r);
  var i = a(n);
  e.attr("xlink:href", i);
}, x = function(s, t, r, n) {
  const e = s.append("use");
  e.attr("x", t), e.attr("y", r);
  const i = a(n);
  e.attr("xlink:href", "#" + i);
}, h = function() {
  return {
    x: 0,
    y: 0,
    width: 100,
    height: 100,
    fill: "#EDF2AE",
    stroke: "#666",
    anchor: "start",
    rx: 0,
    ry: 0
  };
}, g = function() {
  return {
    x: 0,
    y: 0,
    width: 100,
    height: 100,
    fill: void 0,
    anchor: void 0,
    "text-anchor": "start",
    style: "#666",
    textMargin: 0,
    rx: 0,
    ry: 0,
    tspan: !0,
    valign: void 0
  };
};
export {
  c as a,
  x as b,
  f as c,
  l as d,
  g as e,
  d as f,
  h as g
};
