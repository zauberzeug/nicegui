import { l as u, p as H, c as w, aR as Q, j as _, d as J, z as D, F as nt } from "./mermaid-5f2d2ec5.js";
import { c as at } from "./createText-56dbee71.js";
import { l as lt } from "./line-9d49a987.js";
const ct = (a, t, r, n) => {
  t.forEach((e) => {
    bt[e](a, r, n);
  });
}, ht = (a, t, r) => {
  u.trace("Making markers for ", r), a.append("defs").append("marker").attr("id", r + "_" + t + "-extensionStart").attr("class", "marker extension " + t).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 1,7 L18,13 V 1 Z"), a.append("defs").append("marker").attr("id", r + "_" + t + "-extensionEnd").attr("class", "marker extension " + t).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 1,1 V 13 L18,7 Z");
}, ot = (a, t, r) => {
  a.append("defs").append("marker").attr("id", r + "_" + t + "-compositionStart").attr("class", "marker composition " + t).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), a.append("defs").append("marker").attr("id", r + "_" + t + "-compositionEnd").attr("class", "marker composition " + t).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
}, ft = (a, t, r) => {
  a.append("defs").append("marker").attr("id", r + "_" + t + "-aggregationStart").attr("class", "marker aggregation " + t).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z"), a.append("defs").append("marker").attr("id", r + "_" + t + "-aggregationEnd").attr("class", "marker aggregation " + t).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
}, pt = (a, t, r) => {
  a.append("defs").append("marker").attr("id", r + "_" + t + "-dependencyStart").attr("class", "marker dependency " + t).attr("refX", 6).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 5,7 L9,13 L1,7 L9,1 Z"), a.append("defs").append("marker").attr("id", r + "_" + t + "-dependencyEnd").attr("class", "marker dependency " + t).attr("refX", 13).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L14,7 L9,1 Z");
}, dt = (a, t, r) => {
  a.append("defs").append("marker").attr("id", r + "_" + t + "-lollipopStart").attr("class", "marker lollipop " + t).attr("refX", 13).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("circle").attr("stroke", "black").attr("fill", "transparent").attr("cx", 7).attr("cy", 7).attr("r", 6), a.append("defs").append("marker").attr("id", r + "_" + t + "-lollipopEnd").attr("class", "marker lollipop " + t).attr("refX", 1).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("circle").attr("stroke", "black").attr("fill", "transparent").attr("cx", 7).attr("cy", 7).attr("r", 6);
}, yt = (a, t, r) => {
  a.append("marker").attr("id", r + "_" + t + "-pointEnd").attr("class", "marker " + t).attr("viewBox", "0 0 10 10").attr("refX", 6).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 12).attr("markerHeight", 12).attr("orient", "auto").append("path").attr("d", "M 0 0 L 10 5 L 0 10 z").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0"), a.append("marker").attr("id", r + "_" + t + "-pointStart").attr("class", "marker " + t).attr("viewBox", "0 0 10 10").attr("refX", 4.5).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 12).attr("markerHeight", 12).attr("orient", "auto").append("path").attr("d", "M 0 5 L 10 10 L 10 0 z").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
}, ut = (a, t, r) => {
  a.append("marker").attr("id", r + "_" + t + "-circleEnd").attr("class", "marker " + t).attr("viewBox", "0 0 10 10").attr("refX", 11).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("circle").attr("cx", "5").attr("cy", "5").attr("r", "5").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0"), a.append("marker").attr("id", r + "_" + t + "-circleStart").attr("class", "marker " + t).attr("viewBox", "0 0 10 10").attr("refX", -1).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("circle").attr("cx", "5").attr("cy", "5").attr("r", "5").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
}, xt = (a, t, r) => {
  a.append("marker").attr("id", r + "_" + t + "-crossEnd").attr("class", "marker cross " + t).attr("viewBox", "0 0 11 11").attr("refX", 12).attr("refY", 5.2).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("path").attr("d", "M 1,1 l 9,9 M 10,1 l -9,9").attr("class", "arrowMarkerPath").style("stroke-width", 2).style("stroke-dasharray", "1,0"), a.append("marker").attr("id", r + "_" + t + "-crossStart").attr("class", "marker cross " + t).attr("viewBox", "0 0 11 11").attr("refX", -1).attr("refY", 5.2).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("path").attr("d", "M 1,1 l 9,9 M 10,1 l -9,9").attr("class", "arrowMarkerPath").style("stroke-width", 2).style("stroke-dasharray", "1,0");
}, gt = (a, t, r) => {
  a.append("defs").append("marker").attr("id", r + "_" + t + "-barbEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 14).attr("markerUnits", "strokeWidth").attr("orient", "auto").append("path").attr("d", "M 19,7 L9,13 L14,7 L9,1 Z");
}, bt = {
  extension: ht,
  composition: ot,
  aggregation: ft,
  dependency: pt,
  lollipop: dt,
  point: yt,
  circle: ut,
  cross: xt,
  barb: gt
}, rr = ct;
function wt(a, t) {
  t && a.attr("style", t);
}
function mt(a) {
  const t = _(document.createElementNS("http://www.w3.org/2000/svg", "foreignObject")), r = t.append("xhtml:div"), n = a.label, e = a.isNode ? "nodeLabel" : "edgeLabel";
  return r.html(
    '<span class="' + e + '" ' + (a.labelStyle ? 'style="' + a.labelStyle + '"' : "") + ">" + n + "</span>"
  ), wt(r, a.labelStyle), r.style("display", "inline-block"), r.style("white-space", "nowrap"), r.attr("xmlns", "http://www.w3.org/1999/xhtml"), t.node();
}
const kt = (a, t, r, n) => {
  let e = a || "";
  if (typeof e == "object" && (e = e[0]), H(w().flowchart.htmlLabels)) {
    e = e.replace(/\\n|\n/g, "<br />"), u.info("vertexText" + e);
    const i = {
      isNode: n,
      label: Q(e).replace(
        /fa[blrs]?:fa-[\w-]+/g,
        (l) => `<i class='${l.replace(":", " ")}'></i>`
      ),
      labelStyle: t.replace("fill:", "color:")
    };
    return mt(i);
  } else {
    const i = document.createElementNS("http://www.w3.org/2000/svg", "text");
    i.setAttribute("style", t.replace("color:", "fill:"));
    let s = [];
    typeof e == "string" ? s = e.split(/\\n|\n|<br\s*\/?>/gi) : Array.isArray(e) ? s = e : s = [];
    for (const l of s) {
      const c = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
      c.setAttributeNS("http://www.w3.org/XML/1998/namespace", "xml:space", "preserve"), c.setAttribute("dy", "1em"), c.setAttribute("x", "0"), r ? c.setAttribute("class", "title-row") : c.setAttribute("class", "row"), c.textContent = l.trim(), i.appendChild(c);
    }
    return i;
  }
}, I = kt, B = async (a, t, r, n) => {
  let e;
  const i = t.useHtmlLabels || H(w().flowchart.htmlLabels);
  r ? e = r : e = "node default";
  const s = a.insert("g").attr("class", e).attr("id", t.domId || t.id), l = s.insert("g").attr("class", "label").attr("style", t.labelStyle);
  let c;
  t.labelText === void 0 ? c = "" : c = typeof t.labelText == "string" ? t.labelText : t.labelText[0];
  const o = l.node();
  let h;
  t.labelType === "markdown" ? h = at(l, J(Q(c), w()), {
    useHtmlLabels: i,
    width: t.width || w().flowchart.wrappingWidth,
    classes: "markdown-node-label"
  }) : h = o.appendChild(
    I(
      J(Q(c), w()),
      t.labelStyle,
      !1,
      n
    )
  );
  let f = h.getBBox();
  const d = t.padding / 2;
  if (H(w().flowchart.htmlLabels)) {
    const p = h.children[0], b = _(h), k = p.getElementsByTagName("img");
    if (k) {
      const g = c.replace(/<img[^>]*>/g, "").trim() === "";
      await Promise.all(
        [...k].map(
          (y) => new Promise((x) => {
            function M() {
              if (y.style.display = "flex", y.style.flexDirection = "column", g) {
                const C = w().fontSize ? w().fontSize : window.getComputedStyle(document.body).fontSize, X = 5;
                y.style.width = parseInt(C, 10) * X + "px";
              } else
                y.style.width = "100%";
              x(y);
            }
            setTimeout(() => {
              y.complete && M();
            }), y.addEventListener("error", M), y.addEventListener("load", M);
          })
        )
      );
    }
    f = p.getBoundingClientRect(), b.attr("width", f.width), b.attr("height", f.height);
  }
  return i ? l.attr("transform", "translate(" + -f.width / 2 + ", " + -f.height / 2 + ")") : l.attr("transform", "translate(0, " + -f.height / 2 + ")"), t.centerLabel && l.attr("transform", "translate(" + -f.width / 2 + ", " + -f.height / 2 + ")"), l.insert("rect", ":first-child"), { shapeSvg: s, bbox: f, halfPadding: d, label: l };
}, S = (a, t) => {
  const r = t.node().getBBox();
  a.width = r.width, a.height = r.height;
};
function $(a, t, r, n) {
  return a.insert("polygon", ":first-child").attr(
    "points",
    n.map(function(e) {
      return e.x + "," + e.y;
    }).join(" ")
  ).attr("class", "label-container").attr("transform", "translate(" + -t / 2 + "," + r / 2 + ")");
}
function Lt(a, t) {
  return a.intersect(t);
}
function et(a, t, r, n) {
  var e = a.x, i = a.y, s = e - n.x, l = i - n.y, c = Math.sqrt(t * t * l * l + r * r * s * s), o = Math.abs(t * r * s / c);
  n.x < e && (o = -o);
  var h = Math.abs(t * r * l / c);
  return n.y < i && (h = -h), { x: e + o, y: i + h };
}
function vt(a, t, r) {
  return et(a, t, t, r);
}
function St(a, t, r, n) {
  var e, i, s, l, c, o, h, f, d, p, b, k, g, y, x;
  if (e = t.y - a.y, s = a.x - t.x, c = t.x * a.y - a.x * t.y, d = e * r.x + s * r.y + c, p = e * n.x + s * n.y + c, !(d !== 0 && p !== 0 && q(d, p)) && (i = n.y - r.y, l = r.x - n.x, o = n.x * r.y - r.x * n.y, h = i * a.x + l * a.y + o, f = i * t.x + l * t.y + o, !(h !== 0 && f !== 0 && q(h, f)) && (b = e * l - i * s, b !== 0)))
    return k = Math.abs(b / 2), g = s * o - l * c, y = g < 0 ? (g - k) / b : (g + k) / b, g = i * c - e * o, x = g < 0 ? (g - k) / b : (g + k) / b, { x: y, y: x };
}
function q(a, t) {
  return a * t > 0;
}
function Et(a, t, r) {
  var n = a.x, e = a.y, i = [], s = Number.POSITIVE_INFINITY, l = Number.POSITIVE_INFINITY;
  typeof t.forEach == "function" ? t.forEach(function(b) {
    s = Math.min(s, b.x), l = Math.min(l, b.y);
  }) : (s = Math.min(s, t.x), l = Math.min(l, t.y));
  for (var c = n - a.width / 2 - s, o = e - a.height / 2 - l, h = 0; h < t.length; h++) {
    var f = t[h], d = t[h < t.length - 1 ? h + 1 : 0], p = St(
      a,
      r,
      { x: c + f.x, y: o + f.y },
      { x: c + d.x, y: o + d.y }
    );
    p && i.push(p);
  }
  return i.length ? (i.length > 1 && i.sort(function(b, k) {
    var g = b.x - r.x, y = b.y - r.y, x = Math.sqrt(g * g + y * y), M = k.x - r.x, C = k.y - r.y, X = Math.sqrt(M * M + C * C);
    return x < X ? -1 : x === X ? 0 : 1;
  }), i[0]) : a;
}
const Mt = (a, t) => {
  var r = a.x, n = a.y, e = t.x - r, i = t.y - n, s = a.width / 2, l = a.height / 2, c, o;
  return Math.abs(i) * s > Math.abs(e) * l ? (i < 0 && (l = -l), c = i === 0 ? 0 : l * e / i, o = l) : (e < 0 && (s = -s), c = s, o = e === 0 ? 0 : s * i / e), { x: r + c, y: n + o };
}, _t = Mt, m = {
  node: Lt,
  circle: vt,
  ellipse: et,
  polygon: Et,
  rect: _t
}, Bt = async (a, t) => {
  t.useHtmlLabels || w().flowchart.htmlLabels || (t.centerLabel = !0);
  const { shapeSvg: n, bbox: e, halfPadding: i } = await B(
    a,
    t,
    "node " + t.classes,
    !0
  );
  u.info("Classes = ", t.classes);
  const s = n.insert("rect", ":first-child");
  return s.attr("rx", t.rx).attr("ry", t.ry).attr("x", -e.width / 2 - i).attr("y", -e.height / 2 - i).attr("width", e.width + t.padding).attr("height", e.height + t.padding), S(t, s), t.intersect = function(l) {
    return m.rect(t, l);
  }, n;
}, Ct = Bt, K = (a) => a ? " " + a : "", R = (a, t) => `${t || "node default"}${K(a.classes)} ${K(
  a.class
)}`, G = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.width + t.padding, i = n.height + t.padding, s = e + i, l = [
    { x: s / 2, y: 0 },
    { x: s, y: -s / 2 },
    { x: s / 2, y: -s },
    { x: 0, y: -s / 2 }
  ];
  u.info("Question main (Circle)");
  const c = $(r, s, s, l);
  return c.attr("style", t.style), S(t, c), t.intersect = function(o) {
    return u.warn("Intersect called"), m.polygon(t, l, o);
  }, r;
}, Tt = (a, t) => {
  const r = a.insert("g").attr("class", "node default").attr("id", t.domId || t.id), n = 28, e = [
    { x: 0, y: n / 2 },
    { x: n / 2, y: 0 },
    { x: 0, y: -n / 2 },
    { x: -n / 2, y: 0 }
  ];
  return r.insert("polygon", ":first-child").attr(
    "points",
    e.map(function(s) {
      return s.x + "," + s.y;
    }).join(" ")
  ).attr("class", "state-start").attr("r", 7).attr("width", 28).attr("height", 28), t.width = 28, t.height = 28, t.intersect = function(s) {
    return m.circle(t, 14, s);
  }, r;
}, Rt = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = 4, i = n.height + t.padding, s = i / e, l = n.width + 2 * s + t.padding, c = [
    { x: s, y: 0 },
    { x: l - s, y: 0 },
    { x: l, y: -i / 2 },
    { x: l - s, y: -i },
    { x: s, y: -i },
    { x: 0, y: -i / 2 }
  ], o = $(r, l, i, c);
  return o.attr("style", t.style), S(t, o), t.intersect = function(h) {
    return m.polygon(t, c, h);
  }, r;
}, It = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.width + t.padding, i = n.height + t.padding, s = [
    { x: -i / 2, y: 0 },
    { x: e, y: 0 },
    { x: e, y: -i },
    { x: -i / 2, y: -i },
    { x: 0, y: -i / 2 }
  ];
  return $(r, e, i, s).attr("style", t.style), t.width = e + i, t.height = i, t.intersect = function(c) {
    return m.polygon(t, s, c);
  }, r;
}, Ht = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(a, t, R(t), !0), e = n.width + t.padding, i = n.height + t.padding, s = [
    { x: -2 * i / 6, y: 0 },
    { x: e - i / 6, y: 0 },
    { x: e + 2 * i / 6, y: -i },
    { x: i / 6, y: -i }
  ], l = $(r, e, i, s);
  return l.attr("style", t.style), S(t, l), t.intersect = function(c) {
    return m.polygon(t, s, c);
  }, r;
}, Nt = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.width + t.padding, i = n.height + t.padding, s = [
    { x: 2 * i / 6, y: 0 },
    { x: e + i / 6, y: 0 },
    { x: e - 2 * i / 6, y: -i },
    { x: -i / 6, y: -i }
  ], l = $(r, e, i, s);
  return l.attr("style", t.style), S(t, l), t.intersect = function(c) {
    return m.polygon(t, s, c);
  }, r;
}, $t = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.width + t.padding, i = n.height + t.padding, s = [
    { x: -2 * i / 6, y: 0 },
    { x: e + 2 * i / 6, y: 0 },
    { x: e - i / 6, y: -i },
    { x: i / 6, y: -i }
  ], l = $(r, e, i, s);
  return l.attr("style", t.style), S(t, l), t.intersect = function(c) {
    return m.polygon(t, s, c);
  }, r;
}, Ot = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.width + t.padding, i = n.height + t.padding, s = [
    { x: i / 6, y: 0 },
    { x: e - i / 6, y: 0 },
    { x: e + 2 * i / 6, y: -i },
    { x: -2 * i / 6, y: -i }
  ], l = $(r, e, i, s);
  return l.attr("style", t.style), S(t, l), t.intersect = function(c) {
    return m.polygon(t, s, c);
  }, r;
}, Xt = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.width + t.padding, i = n.height + t.padding, s = [
    { x: 0, y: 0 },
    { x: e + i / 2, y: 0 },
    { x: e, y: -i / 2 },
    { x: e + i / 2, y: -i },
    { x: 0, y: -i }
  ], l = $(r, e, i, s);
  return l.attr("style", t.style), S(t, l), t.intersect = function(c) {
    return m.polygon(t, s, c);
  }, r;
}, Yt = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.width + t.padding, i = e / 2, s = i / (2.5 + e / 50), l = n.height + s + t.padding, c = "M 0," + s + " a " + i + "," + s + " 0,0,0 " + e + " 0 a " + i + "," + s + " 0,0,0 " + -e + " 0 l 0," + l + " a " + i + "," + s + " 0,0,0 " + e + " 0 l 0," + -l, o = r.attr("label-offset-y", s).insert("path", ":first-child").attr("style", t.style).attr("d", c).attr("transform", "translate(" + -e / 2 + "," + -(l / 2 + s) + ")");
  return S(t, o), t.intersect = function(h) {
    const f = m.rect(t, h), d = f.x - t.x;
    if (i != 0 && (Math.abs(d) < t.width / 2 || Math.abs(d) == t.width / 2 && Math.abs(f.y - t.y) > t.height / 2 - s)) {
      let p = s * s * (1 - d * d / (i * i));
      p != 0 && (p = Math.sqrt(p)), p = s - p, h.y - t.y > 0 && (p = -p), f.y += p;
    }
    return f;
  }, r;
}, Wt = async (a, t) => {
  const { shapeSvg: r, bbox: n, halfPadding: e } = await B(
    a,
    t,
    "node " + t.classes + " " + t.class,
    !0
  ), i = r.insert("rect", ":first-child"), s = n.width + t.padding, l = n.height + t.padding;
  if (i.attr("class", "basic label-container").attr("style", t.style).attr("rx", t.rx).attr("ry", t.ry).attr("x", -n.width / 2 - e).attr("y", -n.height / 2 - e).attr("width", s).attr("height", l), t.props) {
    const c = new Set(Object.keys(t.props));
    t.props.borders && (st(i, t.props.borders, s, l), c.delete("borders")), c.forEach((o) => {
      u.warn(`Unknown node property ${o}`);
    });
  }
  return S(t, i), t.intersect = function(c) {
    return m.rect(t, c);
  }, r;
}, jt = async (a, t) => {
  const { shapeSvg: r } = await B(a, t, "label", !0);
  u.trace("Classes = ", t.class);
  const n = r.insert("rect", ":first-child"), e = 0, i = 0;
  if (n.attr("width", e).attr("height", i), r.attr("class", "label edgeLabel"), t.props) {
    const s = new Set(Object.keys(t.props));
    t.props.borders && (st(n, t.props.borders, e, i), s.delete("borders")), s.forEach((l) => {
      u.warn(`Unknown node property ${l}`);
    });
  }
  return S(t, n), t.intersect = function(s) {
    return m.rect(t, s);
  }, r;
};
function st(a, t, r, n) {
  const e = [], i = (l) => {
    e.push(l, 0);
  }, s = (l) => {
    e.push(0, l);
  };
  t.includes("t") ? (u.debug("add top border"), i(r)) : s(r), t.includes("r") ? (u.debug("add right border"), i(n)) : s(n), t.includes("b") ? (u.debug("add bottom border"), i(r)) : s(r), t.includes("l") ? (u.debug("add left border"), i(n)) : s(n), a.attr("stroke-dasharray", e.join(" "));
}
const Dt = (a, t) => {
  let r;
  t.classes ? r = "node " + t.classes : r = "node default";
  const n = a.insert("g").attr("class", r).attr("id", t.domId || t.id), e = n.insert("rect", ":first-child"), i = n.insert("line"), s = n.insert("g").attr("class", "label"), l = t.labelText.flat ? t.labelText.flat() : t.labelText;
  let c = "";
  typeof l == "object" ? c = l[0] : c = l, u.info("Label text abc79", c, l, typeof l == "object");
  const o = s.node().appendChild(I(c, t.labelStyle, !0, !0));
  let h = { width: 0, height: 0 };
  if (H(w().flowchart.htmlLabels)) {
    const k = o.children[0], g = _(o);
    h = k.getBoundingClientRect(), g.attr("width", h.width), g.attr("height", h.height);
  }
  u.info("Text 2", l);
  const f = l.slice(1, l.length);
  let d = o.getBBox();
  const p = s.node().appendChild(
    I(f.join ? f.join("<br/>") : f, t.labelStyle, !0, !0)
  );
  if (H(w().flowchart.htmlLabels)) {
    const k = p.children[0], g = _(p);
    h = k.getBoundingClientRect(), g.attr("width", h.width), g.attr("height", h.height);
  }
  const b = t.padding / 2;
  return _(p).attr(
    "transform",
    "translate( " + // (titleBox.width - bbox.width) / 2 +
    (h.width > d.width ? 0 : (d.width - h.width) / 2) + ", " + (d.height + b + 5) + ")"
  ), _(o).attr(
    "transform",
    "translate( " + // (titleBox.width - bbox.width) / 2 +
    (h.width < d.width ? 0 : -(d.width - h.width) / 2) + ", 0)"
  ), h = s.node().getBBox(), s.attr(
    "transform",
    "translate(" + -h.width / 2 + ", " + (-h.height / 2 - b + 3) + ")"
  ), e.attr("class", "outer title-state").attr("x", -h.width / 2 - b).attr("y", -h.height / 2 - b).attr("width", h.width + t.padding).attr("height", h.height + t.padding), i.attr("class", "divider").attr("x1", -h.width / 2 - b).attr("x2", h.width / 2 + b).attr("y1", -h.height / 2 - b + d.height + b).attr("y2", -h.height / 2 - b + d.height + b), S(t, e), t.intersect = function(k) {
    return m.rect(t, k);
  }, n;
}, At = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.height + t.padding, i = n.width + e / 4 + t.padding, s = r.insert("rect", ":first-child").attr("style", t.style).attr("rx", e / 2).attr("ry", e / 2).attr("x", -i / 2).attr("y", -e / 2).attr("width", i).attr("height", e);
  return S(t, s), t.intersect = function(l) {
    return m.rect(t, l);
  }, r;
}, Ut = async (a, t) => {
  const { shapeSvg: r, bbox: n, halfPadding: e } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), i = r.insert("circle", ":first-child");
  return i.attr("style", t.style).attr("rx", t.rx).attr("ry", t.ry).attr("r", n.width / 2 + e).attr("width", n.width + t.padding).attr("height", n.height + t.padding), u.info("Circle main"), S(t, i), t.intersect = function(s) {
    return u.info("Circle intersect", t, n.width / 2 + e, s), m.circle(t, n.width / 2 + e, s);
  }, r;
}, zt = async (a, t) => {
  const { shapeSvg: r, bbox: n, halfPadding: e } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), i = 5, s = r.insert("g", ":first-child"), l = s.insert("circle"), c = s.insert("circle");
  return s.attr("class", t.class), l.attr("style", t.style).attr("rx", t.rx).attr("ry", t.ry).attr("r", n.width / 2 + e + i).attr("width", n.width + t.padding + i * 2).attr("height", n.height + t.padding + i * 2), c.attr("style", t.style).attr("rx", t.rx).attr("ry", t.ry).attr("r", n.width / 2 + e).attr("width", n.width + t.padding).attr("height", n.height + t.padding), u.info("DoubleCircle main"), S(t, l), t.intersect = function(o) {
    return u.info("DoubleCircle intersect", t, n.width / 2 + e + i, o), m.circle(t, n.width / 2 + e + i, o);
  }, r;
}, Zt = async (a, t) => {
  const { shapeSvg: r, bbox: n } = await B(
    a,
    t,
    R(t, void 0),
    !0
  ), e = n.width + t.padding, i = n.height + t.padding, s = [
    { x: 0, y: 0 },
    { x: e, y: 0 },
    { x: e, y: -i },
    { x: 0, y: -i },
    { x: 0, y: 0 },
    { x: -8, y: 0 },
    { x: e + 8, y: 0 },
    { x: e + 8, y: -i },
    { x: -8, y: -i },
    { x: -8, y: 0 }
  ], l = $(r, e, i, s);
  return l.attr("style", t.style), S(t, l), t.intersect = function(c) {
    return m.polygon(t, s, c);
  }, r;
}, Ft = (a, t) => {
  const r = a.insert("g").attr("class", "node default").attr("id", t.domId || t.id), n = r.insert("circle", ":first-child");
  return n.attr("class", "state-start").attr("r", 7).attr("width", 14).attr("height", 14), S(t, n), t.intersect = function(e) {
    return m.circle(t, 7, e);
  }, r;
}, P = (a, t, r) => {
  const n = a.insert("g").attr("class", "node default").attr("id", t.domId || t.id);
  let e = 70, i = 10;
  r === "LR" && (e = 10, i = 70);
  const s = n.append("rect").attr("x", -1 * e / 2).attr("y", -1 * i / 2).attr("width", e).attr("height", i).attr("class", "fork-join");
  return S(t, s), t.height = t.height + t.padding / 2, t.width = t.width + t.padding / 2, t.intersect = function(l) {
    return m.rect(t, l);
  }, n;
}, Qt = (a, t) => {
  const r = a.insert("g").attr("class", "node default").attr("id", t.domId || t.id), n = r.insert("circle", ":first-child"), e = r.insert("circle", ":first-child");
  return e.attr("class", "state-start").attr("r", 7).attr("width", 14).attr("height", 14), n.attr("class", "state-end").attr("r", 5).attr("width", 10).attr("height", 10), S(t, e), t.intersect = function(i) {
    return m.circle(t, 7, i);
  }, r;
}, Vt = (a, t) => {
  const r = t.padding / 2, n = 4, e = 8;
  let i;
  t.classes ? i = "node " + t.classes : i = "node default";
  const s = a.insert("g").attr("class", i).attr("id", t.domId || t.id), l = s.insert("rect", ":first-child"), c = s.insert("line"), o = s.insert("line");
  let h = 0, f = n;
  const d = s.insert("g").attr("class", "label");
  let p = 0;
  const b = t.classData.annotations && t.classData.annotations[0], k = t.classData.annotations[0] ? "«" + t.classData.annotations[0] + "»" : "", g = d.node().appendChild(I(k, t.labelStyle, !0, !0));
  let y = g.getBBox();
  if (H(w().flowchart.htmlLabels)) {
    const L = g.children[0], v = _(g);
    y = L.getBoundingClientRect(), v.attr("width", y.width), v.attr("height", y.height);
  }
  t.classData.annotations[0] && (f += y.height + n, h += y.width);
  let x = t.classData.label;
  t.classData.type !== void 0 && t.classData.type !== "" && (w().flowchart.htmlLabels ? x += "&lt;" + t.classData.type + "&gt;" : x += "<" + t.classData.type + ">");
  const M = d.node().appendChild(I(x, t.labelStyle, !0, !0));
  _(M).attr("class", "classTitle");
  let C = M.getBBox();
  if (H(w().flowchart.htmlLabels)) {
    const L = M.children[0], v = _(M);
    C = L.getBoundingClientRect(), v.attr("width", C.width), v.attr("height", C.height);
  }
  f += C.height + n, C.width > h && (h = C.width);
  const X = [];
  t.classData.members.forEach((L) => {
    const v = L.getDisplayDetails();
    let Y = v.displayText;
    w().flowchart.htmlLabels && (Y = Y.replace(/</g, "&lt;").replace(/>/g, "&gt;"));
    const N = d.node().appendChild(
      I(
        Y,
        v.cssStyle ? v.cssStyle : t.labelStyle,
        !0,
        !0
      )
    );
    let T = N.getBBox();
    if (H(w().flowchart.htmlLabels)) {
      const F = N.children[0], j = _(N);
      T = F.getBoundingClientRect(), j.attr("width", T.width), j.attr("height", T.height);
    }
    T.width > h && (h = T.width), f += T.height + n, X.push(N);
  }), f += e;
  const V = [];
  if (t.classData.methods.forEach((L) => {
    const v = L.getDisplayDetails();
    let Y = v.displayText;
    w().flowchart.htmlLabels && (Y = Y.replace(/</g, "&lt;").replace(/>/g, "&gt;"));
    const N = d.node().appendChild(
      I(
        Y,
        v.cssStyle ? v.cssStyle : t.labelStyle,
        !0,
        !0
      )
    );
    let T = N.getBBox();
    if (H(w().flowchart.htmlLabels)) {
      const F = N.children[0], j = _(N);
      T = F.getBoundingClientRect(), j.attr("width", T.width), j.attr("height", T.height);
    }
    T.width > h && (h = T.width), f += T.height + n, V.push(N);
  }), f += e, b) {
    let L = (h - y.width) / 2;
    _(g).attr(
      "transform",
      "translate( " + (-1 * h / 2 + L) + ", " + -1 * f / 2 + ")"
    ), p = y.height + n;
  }
  let it = (h - C.width) / 2;
  return _(M).attr(
    "transform",
    "translate( " + (-1 * h / 2 + it) + ", " + (-1 * f / 2 + p) + ")"
  ), p += C.height + n, c.attr("class", "divider").attr("x1", -h / 2 - r).attr("x2", h / 2 + r).attr("y1", -f / 2 - r + e + p).attr("y2", -f / 2 - r + e + p), p += e, X.forEach((L) => {
    _(L).attr(
      "transform",
      "translate( " + -h / 2 + ", " + (-1 * f / 2 + p + e / 2) + ")"
    );
    const v = L == null ? void 0 : L.getBBox();
    p += ((v == null ? void 0 : v.height) ?? 0) + n;
  }), p += e, o.attr("class", "divider").attr("x1", -h / 2 - r).attr("x2", h / 2 + r).attr("y1", -f / 2 - r + e + p).attr("y2", -f / 2 - r + e + p), p += e, V.forEach((L) => {
    _(L).attr(
      "transform",
      "translate( " + -h / 2 + ", " + (-1 * f / 2 + p) + ")"
    );
    const v = L == null ? void 0 : L.getBBox();
    p += ((v == null ? void 0 : v.height) ?? 0) + n;
  }), l.attr("class", "outer title-state").attr("x", -h / 2 - r).attr("y", -(f / 2) - r).attr("width", h + t.padding).attr("height", f + t.padding), S(t, l), t.intersect = function(L) {
    return m.rect(t, L);
  }, s;
}, tt = {
  rhombus: G,
  question: G,
  rect: Wt,
  labelRect: jt,
  rectWithTitle: Dt,
  choice: Tt,
  circle: Ut,
  doublecircle: zt,
  stadium: At,
  hexagon: Rt,
  rect_left_inv_arrow: It,
  lean_right: Ht,
  lean_left: Nt,
  trapezoid: $t,
  inv_trapezoid: Ot,
  rect_right_inv_arrow: Xt,
  cylinder: Yt,
  start: Ft,
  end: Qt,
  note: Ct,
  subroutine: Zt,
  fork: P,
  join: P,
  class_box: Vt
};
let W = {};
const ar = async (a, t, r) => {
  let n, e;
  if (t.link) {
    let i;
    w().securityLevel === "sandbox" ? i = "_top" : t.linkTarget && (i = t.linkTarget || "_blank"), n = a.insert("svg:a").attr("xlink:href", t.link).attr("target", i), e = await tt[t.shape](n, t, r);
  } else
    e = await tt[t.shape](a, t, r), n = e;
  return t.tooltip && e.attr("title", t.tooltip), t.class && e.attr("class", "node default " + t.class), W[t.id] = n, t.haveCallback && W[t.id].attr("class", W[t.id].attr("class") + " clickable"), n;
}, er = (a, t) => {
  W[t.id] = a;
}, sr = () => {
  W = {};
}, ir = (a) => {
  const t = W[a.id];
  u.trace(
    "Transforming node",
    a.diff,
    a,
    "translate(" + (a.x - a.width / 2 - 5) + ", " + a.width / 2 + ")"
  );
  const r = 8, n = a.diff || 0;
  return a.clusterNode ? t.attr(
    "transform",
    "translate(" + (a.x + n - a.width / 2) + ", " + (a.y - a.height / 2 - r) + ")"
  ) : t.attr("transform", "translate(" + a.x + ", " + a.y + ")"), n;
}, O = {
  aggregation: 18,
  extension: 18,
  composition: 18,
  dependency: 6,
  lollipop: 13.5,
  arrow_point: 5.3
};
function A(a, t) {
  a = z(a), t = z(t);
  const [r, n] = [a.x, a.y], [e, i] = [t.x, t.y], s = e - r, l = i - n;
  return { angle: Math.atan(l / s), deltaX: s, deltaY: l };
}
const z = (a) => Array.isArray(a) ? { x: a[0], y: a[1] } : a, Jt = (a) => ({
  x: function(t, r, n) {
    let e = 0;
    if (r === 0 && Object.hasOwn(O, a.arrowTypeStart)) {
      const { angle: i, deltaX: s } = A(n[0], n[1]);
      e = O[a.arrowTypeStart] * Math.cos(i) * (s >= 0 ? 1 : -1);
    } else if (r === n.length - 1 && Object.hasOwn(O, a.arrowTypeEnd)) {
      const { angle: i, deltaX: s } = A(
        n[n.length - 1],
        n[n.length - 2]
      );
      e = O[a.arrowTypeEnd] * Math.cos(i) * (s >= 0 ? 1 : -1);
    }
    return z(t).x + e;
  },
  y: function(t, r, n) {
    let e = 0;
    if (r === 0 && Object.hasOwn(O, a.arrowTypeStart)) {
      const { angle: i, deltaY: s } = A(n[0], n[1]);
      e = O[a.arrowTypeStart] * Math.abs(Math.sin(i)) * (s >= 0 ? 1 : -1);
    } else if (r === n.length - 1 && Object.hasOwn(O, a.arrowTypeEnd)) {
      const { angle: i, deltaY: s } = A(
        n[n.length - 1],
        n[n.length - 2]
      );
      e = O[a.arrowTypeEnd] * Math.abs(Math.sin(i)) * (s >= 0 ? 1 : -1);
    }
    return z(t).y + e;
  }
});
let Z = {}, E = {};
const nr = () => {
  Z = {}, E = {};
}, lr = (a, t) => {
  const r = H(w().flowchart.htmlLabels), n = t.labelType === "markdown" ? at(a, t.label, {
    style: t.labelStyle,
    useHtmlLabels: r,
    addSvgBackground: !0
  }) : I(t.label, t.labelStyle);
  u.info("abc82", t, t.labelType);
  const e = a.insert("g").attr("class", "edgeLabel"), i = e.insert("g").attr("class", "label");
  i.node().appendChild(n);
  let s = n.getBBox();
  if (r) {
    const c = n.children[0], o = _(n);
    s = c.getBoundingClientRect(), o.attr("width", s.width), o.attr("height", s.height);
  }
  i.attr("transform", "translate(" + -s.width / 2 + ", " + -s.height / 2 + ")"), Z[t.id] = e, t.width = s.width, t.height = s.height;
  let l;
  if (t.startLabelLeft) {
    const c = I(t.startLabelLeft, t.labelStyle), o = a.insert("g").attr("class", "edgeTerminals"), h = o.insert("g").attr("class", "inner");
    l = h.node().appendChild(c);
    const f = c.getBBox();
    h.attr("transform", "translate(" + -f.width / 2 + ", " + -f.height / 2 + ")"), E[t.id] || (E[t.id] = {}), E[t.id].startLeft = o, U(l, t.startLabelLeft);
  }
  if (t.startLabelRight) {
    const c = I(t.startLabelRight, t.labelStyle), o = a.insert("g").attr("class", "edgeTerminals"), h = o.insert("g").attr("class", "inner");
    l = o.node().appendChild(c), h.node().appendChild(c);
    const f = c.getBBox();
    h.attr("transform", "translate(" + -f.width / 2 + ", " + -f.height / 2 + ")"), E[t.id] || (E[t.id] = {}), E[t.id].startRight = o, U(l, t.startLabelRight);
  }
  if (t.endLabelLeft) {
    const c = I(t.endLabelLeft, t.labelStyle), o = a.insert("g").attr("class", "edgeTerminals"), h = o.insert("g").attr("class", "inner");
    l = h.node().appendChild(c);
    const f = c.getBBox();
    h.attr("transform", "translate(" + -f.width / 2 + ", " + -f.height / 2 + ")"), o.node().appendChild(c), E[t.id] || (E[t.id] = {}), E[t.id].endLeft = o, U(l, t.endLabelLeft);
  }
  if (t.endLabelRight) {
    const c = I(t.endLabelRight, t.labelStyle), o = a.insert("g").attr("class", "edgeTerminals"), h = o.insert("g").attr("class", "inner");
    l = h.node().appendChild(c);
    const f = c.getBBox();
    h.attr("transform", "translate(" + -f.width / 2 + ", " + -f.height / 2 + ")"), o.node().appendChild(c), E[t.id] || (E[t.id] = {}), E[t.id].endRight = o, U(l, t.endLabelRight);
  }
  return n;
};
function U(a, t) {
  w().flowchart.htmlLabels && a && (a.style.width = t.length * 9 + "px", a.style.height = "12px");
}
const cr = (a, t) => {
  u.info("Moving label abc78 ", a.id, a.label, Z[a.id]);
  let r = t.updatedPath ? t.updatedPath : t.originalPath;
  if (a.label) {
    const n = Z[a.id];
    let e = a.x, i = a.y;
    if (r) {
      const s = D.calcLabelPosition(r);
      u.info(
        "Moving label " + a.label + " from (",
        e,
        ",",
        i,
        ") to (",
        s.x,
        ",",
        s.y,
        ") abc78"
      ), t.updatedPath && (e = s.x, i = s.y);
    }
    n.attr("transform", "translate(" + e + ", " + i + ")");
  }
  if (a.startLabelLeft) {
    const n = E[a.id].startLeft;
    let e = a.x, i = a.y;
    if (r) {
      const s = D.calcTerminalLabelPosition(a.arrowTypeStart ? 10 : 0, "start_left", r);
      e = s.x, i = s.y;
    }
    n.attr("transform", "translate(" + e + ", " + i + ")");
  }
  if (a.startLabelRight) {
    const n = E[a.id].startRight;
    let e = a.x, i = a.y;
    if (r) {
      const s = D.calcTerminalLabelPosition(
        a.arrowTypeStart ? 10 : 0,
        "start_right",
        r
      );
      e = s.x, i = s.y;
    }
    n.attr("transform", "translate(" + e + ", " + i + ")");
  }
  if (a.endLabelLeft) {
    const n = E[a.id].endLeft;
    let e = a.x, i = a.y;
    if (r) {
      const s = D.calcTerminalLabelPosition(a.arrowTypeEnd ? 10 : 0, "end_left", r);
      e = s.x, i = s.y;
    }
    n.attr("transform", "translate(" + e + ", " + i + ")");
  }
  if (a.endLabelRight) {
    const n = E[a.id].endRight;
    let e = a.x, i = a.y;
    if (r) {
      const s = D.calcTerminalLabelPosition(a.arrowTypeEnd ? 10 : 0, "end_right", r);
      e = s.x, i = s.y;
    }
    n.attr("transform", "translate(" + e + ", " + i + ")");
  }
}, qt = (a, t) => {
  const r = a.x, n = a.y, e = Math.abs(t.x - r), i = Math.abs(t.y - n), s = a.width / 2, l = a.height / 2;
  return e >= s || i >= l;
}, Kt = (a, t, r) => {
  u.warn(`intersection calc abc89:
  outsidePoint: ${JSON.stringify(t)}
  insidePoint : ${JSON.stringify(r)}
  node        : x:${a.x} y:${a.y} w:${a.width} h:${a.height}`);
  const n = a.x, e = a.y, i = Math.abs(n - r.x), s = a.width / 2;
  let l = r.x < t.x ? s - i : s + i;
  const c = a.height / 2, o = Math.abs(t.y - r.y), h = Math.abs(t.x - r.x);
  if (Math.abs(e - t.y) * s > Math.abs(n - t.x) * c) {
    let f = r.y < t.y ? t.y - c - e : e - c - t.y;
    l = h * f / o;
    const d = {
      x: r.x < t.x ? r.x + l : r.x - h + l,
      y: r.y < t.y ? r.y + o - f : r.y - o + f
    };
    return l === 0 && (d.x = t.x, d.y = t.y), h === 0 && (d.x = t.x), o === 0 && (d.y = t.y), u.warn(`abc89 topp/bott calc, Q ${o}, q ${f}, R ${h}, r ${l}`, d), d;
  } else {
    r.x < t.x ? l = t.x - s - n : l = n - s - t.x;
    let f = o * l / h, d = r.x < t.x ? r.x + h - l : r.x - h + l, p = r.y < t.y ? r.y + f : r.y - f;
    return u.warn(`sides calc abc89, Q ${o}, q ${f}, R ${h}, r ${l}`, { _x: d, _y: p }), l === 0 && (d = t.x, p = t.y), h === 0 && (d = t.x), o === 0 && (p = t.y), { x: d, y: p };
  }
}, rt = (a, t) => {
  u.warn("abc88 cutPathAtIntersect", a, t);
  let r = [], n = a[0], e = !1;
  return a.forEach((i) => {
    if (u.info("abc88 checking point", i, t), !qt(t, i) && !e) {
      const s = Kt(t, n, i);
      u.warn("abc88 inside", i, n, s), u.warn("abc88 intersection", s);
      let l = !1;
      r.forEach((c) => {
        l = l || c.x === s.x && c.y === s.y;
      }), r.some((c) => c.x === s.x && c.y === s.y) ? u.warn("abc88 no intersect", s, r) : r.push(s), e = !0;
    } else
      u.warn("abc88 outside", i, n), n = i, e || r.push(i);
  }), u.warn("abc88 returning points", r), r;
}, hr = function(a, t, r, n, e, i, s) {
  let l = r.points, c = !1;
  const o = i.node(t.v);
  var h = i.node(t.w);
  u.info("abc88 InsertEdge: ", r), h.intersect && o.intersect && (l = l.slice(1, r.points.length - 1), l.unshift(o.intersect(l[0])), u.info(
    "Last point",
    l[l.length - 1],
    h,
    h.intersect(l[l.length - 1])
  ), l.push(h.intersect(l[l.length - 1]))), r.toCluster && (u.info("to cluster abc88", n[r.toCluster]), l = rt(r.points, n[r.toCluster].node), c = !0), r.fromCluster && (u.info("from cluster abc88", n[r.fromCluster]), l = rt(l.reverse(), n[r.fromCluster].node).reverse(), c = !0);
  const f = l.filter((C) => !Number.isNaN(C.y));
  let d = nt;
  r.curve && (e === "graph" || e === "flowchart") && (d = r.curve);
  const { x: p, y: b } = Jt(r), k = lt().x(p).y(b).curve(d);
  let g;
  switch (r.thickness) {
    case "normal":
      g = "edge-thickness-normal";
      break;
    case "thick":
      g = "edge-thickness-thick";
      break;
    case "invisible":
      g = "edge-thickness-thick";
      break;
    default:
      g = "";
  }
  switch (r.pattern) {
    case "solid":
      g += " edge-pattern-solid";
      break;
    case "dotted":
      g += " edge-pattern-dotted";
      break;
    case "dashed":
      g += " edge-pattern-dashed";
      break;
  }
  const y = a.append("path").attr("d", k(f)).attr("id", r.id).attr("class", " " + g + (r.classes ? " " + r.classes : "")).attr("style", r.style);
  let x = "";
  switch ((w().flowchart.arrowMarkerAbsolute || w().state.arrowMarkerAbsolute) && (x = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search, x = x.replace(/\(/g, "\\("), x = x.replace(/\)/g, "\\)")), u.info("arrowTypeStart", r.arrowTypeStart), u.info("arrowTypeEnd", r.arrowTypeEnd), r.arrowTypeStart) {
    case "arrow_cross":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-crossStart)"
      );
      break;
    case "arrow_point":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-pointStart)"
      );
      break;
    case "arrow_barb":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-barbStart)"
      );
      break;
    case "arrow_circle":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-circleStart)"
      );
      break;
    case "aggregation":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-aggregationStart)"
      );
      break;
    case "extension":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-extensionStart)"
      );
      break;
    case "composition":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-compositionStart)"
      );
      break;
    case "dependency":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-dependencyStart)"
      );
      break;
    case "lollipop":
      y.attr(
        "marker-start",
        "url(" + x + "#" + s + "_" + e + "-lollipopStart)"
      );
      break;
  }
  switch (r.arrowTypeEnd) {
    case "arrow_cross":
      y.attr("marker-end", "url(" + x + "#" + s + "_" + e + "-crossEnd)");
      break;
    case "arrow_point":
      y.attr("marker-end", "url(" + x + "#" + s + "_" + e + "-pointEnd)");
      break;
    case "arrow_barb":
      y.attr("marker-end", "url(" + x + "#" + s + "_" + e + "-barbEnd)");
      break;
    case "arrow_circle":
      y.attr("marker-end", "url(" + x + "#" + s + "_" + e + "-circleEnd)");
      break;
    case "aggregation":
      y.attr(
        "marker-end",
        "url(" + x + "#" + s + "_" + e + "-aggregationEnd)"
      );
      break;
    case "extension":
      y.attr(
        "marker-end",
        "url(" + x + "#" + s + "_" + e + "-extensionEnd)"
      );
      break;
    case "composition":
      y.attr(
        "marker-end",
        "url(" + x + "#" + s + "_" + e + "-compositionEnd)"
      );
      break;
    case "dependency":
      y.attr(
        "marker-end",
        "url(" + x + "#" + s + "_" + e + "-dependencyEnd)"
      );
      break;
    case "lollipop":
      y.attr(
        "marker-end",
        "url(" + x + "#" + s + "_" + e + "-lollipopEnd)"
      );
      break;
  }
  let M = {};
  return c && (M.updatedPath = l), M.originalPath = r.points, M;
};
export {
  rr as a,
  sr as b,
  I as c,
  nr as d,
  ar as e,
  lr as f,
  hr as g,
  cr as h,
  _t as i,
  Jt as j,
  B as l,
  ir as p,
  er as s,
  S as u
};
