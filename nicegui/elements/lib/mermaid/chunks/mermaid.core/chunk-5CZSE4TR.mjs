import {
  getLineFunctionsWithOffset,
  getSubGraphTitleMargins
} from "./chunk-TINLTEC2.mjs";
import {
  createText
} from "./chunk-OERGPBFJ.mjs";
import {
  decodeEntities,
  utils_default
} from "./chunk-VKXSJROQ.mjs";
import {
  __name,
  common_default,
  evaluate,
  getConfig2 as getConfig,
  hasKatex,
  log,
  renderKatex,
  sanitizeText
} from "./chunk-O2AGWWWV.mjs";

// src/rendering-util/rendering-elements/clusters.js
import { select as select2 } from "d3";
import rough from "roughjs";

// src/rendering-util/rendering-elements/intersect/intersect-rect.js
var intersectRect = /* @__PURE__ */ __name((node, point2) => {
  var x = node.x;
  var y = node.y;
  var dx = point2.x - x;
  var dy = point2.y - y;
  var w = node.width / 2;
  var h = node.height / 2;
  var sx, sy;
  if (Math.abs(dy) * w > Math.abs(dx) * h) {
    if (dy < 0) {
      h = -h;
    }
    sx = dy === 0 ? 0 : h * dx / dy;
    sy = h;
  } else {
    if (dx < 0) {
      w = -w;
    }
    sx = w;
    sy = dx === 0 ? 0 : w * dy / dx;
  }
  return { x: x + sx, y: y + sy };
}, "intersectRect");
var intersect_rect_default = intersectRect;

// src/rendering-util/rendering-elements/createLabel.js
import { select } from "d3";
function applyStyle(dom, styleFn) {
  if (styleFn) {
    dom.attr("style", styleFn);
  }
}
__name(applyStyle, "applyStyle");
async function addHtmlLabel(node) {
  const fo = select(document.createElementNS("http://www.w3.org/2000/svg", "foreignObject"));
  const div = fo.append("xhtml:div");
  let label = node.label;
  if (node.label && hasKatex(node.label)) {
    label = await renderKatex(node.label.replace(common_default.lineBreakRegex, "\n"), getConfig());
  }
  const labelClass = node.isNode ? "nodeLabel" : "edgeLabel";
  div.html(
    '<span class="' + labelClass + '" ' + (node.labelStyle ? 'style="' + node.labelStyle + '"' : "") + // codeql [js/html-constructed-from-input] : false positive
    ">" + label + "</span>"
  );
  applyStyle(div, node.labelStyle);
  div.style("display", "inline-block");
  div.style("padding-right", "1px");
  div.style("white-space", "nowrap");
  div.attr("xmlns", "http://www.w3.org/1999/xhtml");
  return fo.node();
}
__name(addHtmlLabel, "addHtmlLabel");
var createLabel = /* @__PURE__ */ __name(async (_vertexText, style, isTitle, isNode) => {
  let vertexText = _vertexText || "";
  if (typeof vertexText === "object") {
    vertexText = vertexText[0];
  }
  if (evaluate(getConfig().flowchart.htmlLabels)) {
    vertexText = vertexText.replace(/\\n|\n/g, "<br />");
    log.info("vertexText" + vertexText);
    const node = {
      isNode,
      label: decodeEntities(vertexText).replace(
        /fa[blrs]?:fa-[\w-]+/g,
        (s) => `<i class='${s.replace(":", " ")}'></i>`
      ),
      labelStyle: style ? style.replace("fill:", "color:") : style
    };
    let vertexNode = await addHtmlLabel(node);
    return vertexNode;
  } else {
    const svgLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    svgLabel.setAttribute("style", style.replace("color:", "fill:"));
    let rows = [];
    if (typeof vertexText === "string") {
      rows = vertexText.split(/\\n|\n|<br\s*\/?>/gi);
    } else if (Array.isArray(vertexText)) {
      rows = vertexText;
    } else {
      rows = [];
    }
    for (const row of rows) {
      const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
      tspan.setAttributeNS("http://www.w3.org/XML/1998/namespace", "xml:space", "preserve");
      tspan.setAttribute("dy", "1em");
      tspan.setAttribute("x", "0");
      if (isTitle) {
        tspan.setAttribute("class", "title-row");
      } else {
        tspan.setAttribute("class", "row");
      }
      tspan.textContent = row.trim();
      svgLabel.appendChild(tspan);
    }
    return svgLabel;
  }
}, "createLabel");
var createLabel_default = createLabel;

// src/rendering-util/rendering-elements/shapes/roundedRectPath.ts
var createRoundedRectPathD = /* @__PURE__ */ __name((x, y, totalWidth, totalHeight, radius) => [
  "M",
  x + radius,
  y,
  // Move to the first point
  "H",
  x + totalWidth - radius,
  // Draw horizontal line to the beginning of the right corner
  "A",
  radius,
  radius,
  0,
  0,
  1,
  x + totalWidth,
  y + radius,
  // Draw arc to the right top corner
  "V",
  y + totalHeight - radius,
  // Draw vertical line down to the beginning of the right bottom corner
  "A",
  radius,
  radius,
  0,
  0,
  1,
  x + totalWidth - radius,
  y + totalHeight,
  // Draw arc to the right bottom corner
  "H",
  x + radius,
  // Draw horizontal line to the beginning of the left bottom corner
  "A",
  radius,
  radius,
  0,
  0,
  1,
  x,
  y + totalHeight - radius,
  // Draw arc to the left bottom corner
  "V",
  y + radius,
  // Draw vertical line up to the beginning of the left top corner
  "A",
  radius,
  radius,
  0,
  0,
  1,
  x + radius,
  y,
  // Draw arc to the left top corner
  "Z"
  // Close the path
].join(" "), "createRoundedRectPathD");

// src/rendering-util/rendering-elements/shapes/handDrawnShapeStyles.ts
var solidStateFill = /* @__PURE__ */ __name((color) => {
  const { handDrawnSeed } = getConfig();
  return {
    fill: color,
    hachureAngle: 120,
    // angle of hachure,
    hachureGap: 4,
    fillWeight: 2,
    roughness: 0.7,
    stroke: color,
    seed: handDrawnSeed
  };
}, "solidStateFill");
var compileStyles = /* @__PURE__ */ __name((node) => {
  const stylesMap = styles2Map([...node.cssCompiledStyles || [], ...node.cssStyles || []]);
  return { stylesMap, stylesArray: [...stylesMap] };
}, "compileStyles");
var styles2Map = /* @__PURE__ */ __name((styles) => {
  const styleMap = /* @__PURE__ */ new Map();
  styles.forEach((style) => {
    const [key, value] = style.split(":");
    styleMap.set(key.trim(), value?.trim());
  });
  return styleMap;
}, "styles2Map");
var styles2String = /* @__PURE__ */ __name((node) => {
  const { stylesArray } = compileStyles(node);
  const labelStyles = [];
  const nodeStyles = [];
  const borderStyles = [];
  const backgroundStyles = [];
  stylesArray.forEach((style) => {
    const key = style[0];
    if (key === "color" || key === "font-size" || key === "font-family" || key === "font-weight" || key === "font-style" || key === "text-decoration" || key === "text-align" || key === "text-transform" || key === "line-height" || key === "letter-spacing" || key === "word-spacing" || key === "text-shadow" || key === "text-overflow" || key === "white-space" || key === "word-wrap" || key === "word-break" || key === "overflow-wrap" || key === "hyphens") {
      labelStyles.push(style.join(":") + " !important");
    } else {
      nodeStyles.push(style.join(":") + " !important");
      if (key.includes("stroke")) {
        borderStyles.push(style.join(":") + " !important");
      }
      if (key === "fill") {
        backgroundStyles.push(style.join(":") + " !important");
      }
    }
  });
  return {
    labelStyles: labelStyles.join(";"),
    nodeStyles: nodeStyles.join(";"),
    stylesArray,
    borderStyles,
    backgroundStyles
  };
}, "styles2String");
var userNodeOverrides = /* @__PURE__ */ __name((node, options) => {
  const { themeVariables, handDrawnSeed } = getConfig();
  const { nodeBorder, mainBkg } = themeVariables;
  const { stylesMap } = compileStyles(node);
  const result = Object.assign(
    {
      roughness: 0.7,
      fill: stylesMap.get("fill") || mainBkg,
      fillStyle: "hachure",
      // solid fill
      fillWeight: 4,
      stroke: stylesMap.get("stroke") || nodeBorder,
      seed: handDrawnSeed,
      strokeWidth: 1.3
    },
    options
  );
  return result;
}, "userNodeOverrides");

// src/rendering-util/rendering-elements/clusters.js
var rect = /* @__PURE__ */ __name(async (parent, node) => {
  log.info("Creating subgraph rect for ", node.id, node);
  const siteConfig = getConfig();
  const { themeVariables, handDrawnSeed } = siteConfig;
  const { clusterBkg, clusterBorder } = themeVariables;
  const { labelStyles, nodeStyles, borderStyles, backgroundStyles } = styles2String(node);
  const shapeSvg = parent.insert("g").attr("class", "cluster " + node.cssClasses).attr("id", node.id).attr("data-look", node.look);
  const useHtmlLabels = evaluate(siteConfig.flowchart.htmlLabels);
  const labelEl = shapeSvg.insert("g").attr("class", "cluster-label ");
  const text = await createText(labelEl, node.label, {
    style: node.labelStyle,
    useHtmlLabels,
    isNode: true
  });
  let bbox = text.getBBox();
  if (evaluate(siteConfig.flowchart.htmlLabels)) {
    const div = text.children[0];
    const dv = select2(text);
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  const width = node.width <= bbox.width + node.padding ? bbox.width + node.padding : node.width;
  if (node.width <= bbox.width + node.padding) {
    node.diff = (width - node.width) / 2 - node.padding;
  } else {
    node.diff = -node.padding;
  }
  const height = node.height;
  const x = node.x - width / 2;
  const y = node.y - height / 2;
  log.trace("Data ", node, JSON.stringify(node));
  let rect2;
  if (node.look === "handDrawn") {
    const rc = rough.svg(shapeSvg);
    const options = userNodeOverrides(node, {
      roughness: 0.7,
      fill: clusterBkg,
      // fill: 'red',
      stroke: clusterBorder,
      fillWeight: 3,
      seed: handDrawnSeed
    });
    const roughNode = rc.path(createRoundedRectPathD(x, y, width, height, 0), options);
    rect2 = shapeSvg.insert(() => {
      log.debug("Rough node insert CXC", roughNode);
      return roughNode;
    }, ":first-child");
    rect2.select("path:nth-child(2)").attr("style", borderStyles.join(";"));
    rect2.select("path").attr("style", backgroundStyles.join(";").replace("fill", "stroke"));
  } else {
    rect2 = shapeSvg.insert("rect", ":first-child");
    rect2.attr("style", nodeStyles).attr("rx", node.rx).attr("ry", node.ry).attr("x", x).attr("y", y).attr("width", width).attr("height", height);
  }
  const { subGraphTitleTopMargin } = getSubGraphTitleMargins(siteConfig);
  labelEl.attr(
    "transform",
    // This puts the label on top of the box instead of inside it
    `translate(${node.x - bbox.width / 2}, ${node.y - node.height / 2 + subGraphTitleTopMargin})`
  );
  if (labelStyles) {
    const span = labelEl.select("span");
    if (span) {
      span.attr("style", labelStyles);
    }
  }
  const rectBox = rect2.node().getBBox();
  node.offsetX = 0;
  node.width = rectBox.width;
  node.height = rectBox.height;
  node.offsetY = bbox.height - node.padding / 2;
  node.intersect = function(point2) {
    return intersect_rect_default(node, point2);
  };
  return { cluster: shapeSvg, labelBBox: bbox };
}, "rect");
var noteGroup = /* @__PURE__ */ __name((parent, node) => {
  const shapeSvg = parent.insert("g").attr("class", "note-cluster").attr("id", node.id);
  const rect2 = shapeSvg.insert("rect", ":first-child");
  const padding = 0 * node.padding;
  const halfPadding = padding / 2;
  rect2.attr("rx", node.rx).attr("ry", node.ry).attr("x", node.x - node.width / 2 - halfPadding).attr("y", node.y - node.height / 2 - halfPadding).attr("width", node.width + padding).attr("height", node.height + padding).attr("fill", "none");
  const rectBox = rect2.node().getBBox();
  node.width = rectBox.width;
  node.height = rectBox.height;
  node.intersect = function(point2) {
    return intersect_rect_default(node, point2);
  };
  return { cluster: shapeSvg, labelBBox: { width: 0, height: 0 } };
}, "noteGroup");
var roundedWithTitle = /* @__PURE__ */ __name(async (parent, node) => {
  const siteConfig = getConfig();
  const { themeVariables, handDrawnSeed } = siteConfig;
  const { altBackground, compositeBackground, compositeTitleBackground, nodeBorder } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", node.cssClasses).attr("id", node.id).attr("data-id", node.id).attr("data-look", node.look);
  const outerRectG = shapeSvg.insert("g", ":first-child");
  const label = shapeSvg.insert("g").attr("class", "cluster-label");
  let innerRect = shapeSvg.append("rect");
  const text = label.node().appendChild(await createLabel_default(node.label, node.labelStyle, void 0, true));
  let bbox = text.getBBox();
  if (evaluate(siteConfig.flowchart.htmlLabels)) {
    const div = text.children[0];
    const dv = select2(text);
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  const padding = 0 * node.padding;
  const halfPadding = padding / 2;
  const width = (node.width <= bbox.width + node.padding ? bbox.width + node.padding : node.width) + padding;
  if (node.width <= bbox.width + node.padding) {
    node.diff = (width - node.width) / 2 - node.padding;
  } else {
    node.diff = -node.padding;
  }
  const height = node.height + padding;
  const innerHeight = node.height + padding - bbox.height - 6;
  const x = node.x - width / 2;
  const y = node.y - height / 2;
  node.width = width;
  const innerY = node.y - node.height / 2 - halfPadding + bbox.height + 2;
  let rect2;
  if (node.look === "handDrawn") {
    const isAlt = node.cssClasses.includes("statediagram-cluster-alt");
    const rc = rough.svg(shapeSvg);
    const roughOuterNode = node.rx || node.ry ? rc.path(createRoundedRectPathD(x, y, width, height, 10), {
      roughness: 0.7,
      fill: compositeTitleBackground,
      fillStyle: "solid",
      stroke: nodeBorder,
      seed: handDrawnSeed
    }) : rc.rectangle(x, y, width, height, { seed: handDrawnSeed });
    rect2 = shapeSvg.insert(() => roughOuterNode, ":first-child");
    const roughInnerNode = rc.rectangle(x, innerY, width, innerHeight, {
      fill: isAlt ? altBackground : compositeBackground,
      fillStyle: isAlt ? "hachure" : "solid",
      stroke: nodeBorder,
      seed: handDrawnSeed
    });
    rect2 = shapeSvg.insert(() => roughOuterNode, ":first-child");
    innerRect = shapeSvg.insert(() => roughInnerNode);
  } else {
    rect2 = outerRectG.insert("rect", ":first-child");
    const outerRectClass = "outer";
    rect2.attr("class", outerRectClass).attr("x", x).attr("y", y).attr("width", width).attr("height", height).attr("data-look", node.look);
    innerRect.attr("class", "inner").attr("x", x).attr("y", innerY).attr("width", width).attr("height", innerHeight);
  }
  label.attr(
    "transform",
    `translate(${node.x - bbox.width / 2}, ${y + 1 - (evaluate(siteConfig.flowchart.htmlLabels) ? 0 : 3)})`
  );
  const rectBox = rect2.node().getBBox();
  node.height = rectBox.height;
  node.offsetX = 0;
  node.offsetY = bbox.height - node.padding / 2;
  node.labelBBox = bbox;
  node.intersect = function(point2) {
    return intersect_rect_default(node, point2);
  };
  return { cluster: shapeSvg, labelBBox: bbox };
}, "roundedWithTitle");
var divider = /* @__PURE__ */ __name((parent, node) => {
  const siteConfig = getConfig();
  const { themeVariables, handDrawnSeed } = siteConfig;
  const { nodeBorder } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", node.cssClasses).attr("id", node.id).attr("data-look", node.look);
  const outerRectG = shapeSvg.insert("g", ":first-child");
  const padding = 0 * node.padding;
  const width = node.width + padding;
  node.diff = -node.padding;
  const height = node.height + padding;
  const x = node.x - width / 2;
  const y = node.y - height / 2;
  node.width = width;
  let rect2;
  if (node.look === "handDrawn") {
    const rc = rough.svg(shapeSvg);
    const roughOuterNode = rc.rectangle(x, y, width, height, {
      fill: "lightgrey",
      roughness: 0.5,
      strokeLineDash: [5],
      stroke: nodeBorder,
      seed: handDrawnSeed
    });
    rect2 = shapeSvg.insert(() => roughOuterNode, ":first-child");
  } else {
    rect2 = outerRectG.insert("rect", ":first-child");
    const outerRectClass = "divider";
    rect2.attr("class", outerRectClass).attr("x", x).attr("y", y).attr("width", width).attr("height", height).attr("data-look", node.look);
  }
  const rectBox = rect2.node().getBBox();
  node.height = rectBox.height;
  node.offsetX = 0;
  node.offsetY = 0;
  node.intersect = function(point2) {
    return intersect_rect_default(node, point2);
  };
  return { cluster: shapeSvg, labelBBox: {} };
}, "divider");
var squareRect = rect;
var shapes = {
  rect,
  squareRect,
  roundedWithTitle,
  noteGroup,
  divider
};
var clusterElems = /* @__PURE__ */ new Map();
var insertCluster = /* @__PURE__ */ __name(async (elem, node) => {
  const shape = node.shape || "rect";
  const cluster = await shapes[shape](elem, node);
  clusterElems.set(node.id, cluster);
  return cluster;
}, "insertCluster");
var clear = /* @__PURE__ */ __name(() => {
  clusterElems = /* @__PURE__ */ new Map();
}, "clear");

// src/rendering-util/rendering-elements/edges.js
import { curveBasis, line, select as select3 } from "d3";
import rough2 from "roughjs";

// src/rendering-util/rendering-elements/edgeMarker.ts
var addEdgeMarkers = /* @__PURE__ */ __name((svgPath, edge, url, id, diagramType) => {
  if (edge.arrowTypeStart) {
    addEdgeMarker(svgPath, "start", edge.arrowTypeStart, url, id, diagramType);
  }
  if (edge.arrowTypeEnd) {
    addEdgeMarker(svgPath, "end", edge.arrowTypeEnd, url, id, diagramType);
  }
}, "addEdgeMarkers");
var arrowTypesMap = {
  arrow_cross: "cross",
  arrow_point: "point",
  arrow_barb: "barb",
  arrow_circle: "circle",
  aggregation: "aggregation",
  extension: "extension",
  composition: "composition",
  dependency: "dependency",
  lollipop: "lollipop"
};
var addEdgeMarker = /* @__PURE__ */ __name((svgPath, position, arrowType, url, id, diagramType) => {
  const endMarkerType = arrowTypesMap[arrowType];
  if (!endMarkerType) {
    log.warn(`Unknown arrow type: ${arrowType}`);
    return;
  }
  const suffix = position === "start" ? "Start" : "End";
  svgPath.attr(`marker-${position}`, `url(${url}#${id}_${diagramType}-${endMarkerType}${suffix})`);
}, "addEdgeMarker");

// src/rendering-util/rendering-elements/edges.js
var edgeLabels = /* @__PURE__ */ new Map();
var terminalLabels = /* @__PURE__ */ new Map();
var clear2 = /* @__PURE__ */ __name(() => {
  edgeLabels.clear();
  terminalLabels.clear();
}, "clear");
var getLabelStyles = /* @__PURE__ */ __name((styleArray) => {
  let styles = styleArray ? styleArray.reduce((acc, style) => acc + ";" + style, "") : "";
  return styles;
}, "getLabelStyles");
var insertEdgeLabel = /* @__PURE__ */ __name(async (elem, edge) => {
  let useHtmlLabels = evaluate(getConfig().flowchart.htmlLabels);
  const labelElement = await createText(elem, edge.label, {
    style: getLabelStyles(edge.labelStyle),
    useHtmlLabels,
    addSvgBackground: true,
    isNode: false
  });
  log.info("abc82", edge, edge.labelType);
  const edgeLabel = elem.insert("g").attr("class", "edgeLabel");
  const label = edgeLabel.insert("g").attr("class", "label");
  label.node().appendChild(labelElement);
  let bbox = labelElement.getBBox();
  if (useHtmlLabels) {
    const div = labelElement.children[0];
    const dv = select3(labelElement);
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  label.attr("transform", "translate(" + -bbox.width / 2 + ", " + -bbox.height / 2 + ")");
  edgeLabels.set(edge.id, edgeLabel);
  edge.width = bbox.width;
  edge.height = bbox.height;
  let fo;
  if (edge.startLabelLeft) {
    const startLabelElement = await createLabel_default(
      edge.startLabelLeft,
      getLabelStyles(edge.labelStyle)
    );
    const startEdgeLabelLeft = elem.insert("g").attr("class", "edgeTerminals");
    const inner = startEdgeLabelLeft.insert("g").attr("class", "inner");
    fo = inner.node().appendChild(startLabelElement);
    const slBox = startLabelElement.getBBox();
    inner.attr("transform", "translate(" + -slBox.width / 2 + ", " + -slBox.height / 2 + ")");
    if (!terminalLabels.get(edge.id)) {
      terminalLabels.set(edge.id, {});
    }
    terminalLabels.get(edge.id).startLeft = startEdgeLabelLeft;
    setTerminalWidth(fo, edge.startLabelLeft);
  }
  if (edge.startLabelRight) {
    const startLabelElement = await createLabel_default(
      edge.startLabelRight,
      getLabelStyles(edge.labelStyle)
    );
    const startEdgeLabelRight = elem.insert("g").attr("class", "edgeTerminals");
    const inner = startEdgeLabelRight.insert("g").attr("class", "inner");
    fo = startEdgeLabelRight.node().appendChild(startLabelElement);
    inner.node().appendChild(startLabelElement);
    const slBox = startLabelElement.getBBox();
    inner.attr("transform", "translate(" + -slBox.width / 2 + ", " + -slBox.height / 2 + ")");
    if (!terminalLabels.get(edge.id)) {
      terminalLabels.set(edge.id, {});
    }
    terminalLabels.get(edge.id).startRight = startEdgeLabelRight;
    setTerminalWidth(fo, edge.startLabelRight);
  }
  if (edge.endLabelLeft) {
    const endLabelElement = await createLabel_default(edge.endLabelLeft, getLabelStyles(edge.labelStyle));
    const endEdgeLabelLeft = elem.insert("g").attr("class", "edgeTerminals");
    const inner = endEdgeLabelLeft.insert("g").attr("class", "inner");
    fo = inner.node().appendChild(endLabelElement);
    const slBox = endLabelElement.getBBox();
    inner.attr("transform", "translate(" + -slBox.width / 2 + ", " + -slBox.height / 2 + ")");
    endEdgeLabelLeft.node().appendChild(endLabelElement);
    if (!terminalLabels.get(edge.id)) {
      terminalLabels.set(edge.id, {});
    }
    terminalLabels.get(edge.id).endLeft = endEdgeLabelLeft;
    setTerminalWidth(fo, edge.endLabelLeft);
  }
  if (edge.endLabelRight) {
    const endLabelElement = await createLabel_default(edge.endLabelRight, getLabelStyles(edge.labelStyle));
    const endEdgeLabelRight = elem.insert("g").attr("class", "edgeTerminals");
    const inner = endEdgeLabelRight.insert("g").attr("class", "inner");
    fo = inner.node().appendChild(endLabelElement);
    const slBox = endLabelElement.getBBox();
    inner.attr("transform", "translate(" + -slBox.width / 2 + ", " + -slBox.height / 2 + ")");
    endEdgeLabelRight.node().appendChild(endLabelElement);
    if (!terminalLabels.get(edge.id)) {
      terminalLabels.set(edge.id, {});
    }
    terminalLabels.get(edge.id).endRight = endEdgeLabelRight;
    setTerminalWidth(fo, edge.endLabelRight);
  }
  return labelElement;
}, "insertEdgeLabel");
function setTerminalWidth(fo, value) {
  if (getConfig().flowchart.htmlLabels && fo) {
    fo.style.width = value.length * 9 + "px";
    fo.style.height = "12px";
  }
}
__name(setTerminalWidth, "setTerminalWidth");
var positionEdgeLabel = /* @__PURE__ */ __name((edge, paths) => {
  log.debug("Moving label abc88 ", edge.id, edge.label, edgeLabels.get(edge.id), paths);
  let path = paths.updatedPath ? paths.updatedPath : paths.originalPath;
  const siteConfig = getConfig();
  const { subGraphTitleTotalMargin } = getSubGraphTitleMargins(siteConfig);
  if (edge.label) {
    const el = edgeLabels.get(edge.id);
    let x = edge.x;
    let y = edge.y;
    if (path) {
      const pos = utils_default.calcLabelPosition(path);
      log.debug(
        "Moving label " + edge.label + " from (",
        x,
        ",",
        y,
        ") to (",
        pos.x,
        ",",
        pos.y,
        ") abc88"
      );
      if (paths.updatedPath) {
        x = pos.x;
        y = pos.y;
      }
    }
    el.attr("transform", `translate(${x}, ${y + subGraphTitleTotalMargin / 2})`);
  }
  if (edge.startLabelLeft) {
    const el = terminalLabels.get(edge.id).startLeft;
    let x = edge.x;
    let y = edge.y;
    if (path) {
      const pos = utils_default.calcTerminalLabelPosition(edge.arrowTypeStart ? 10 : 0, "start_left", path);
      x = pos.x;
      y = pos.y;
    }
    el.attr("transform", `translate(${x}, ${y})`);
  }
  if (edge.startLabelRight) {
    const el = terminalLabels.get(edge.id).startRight;
    let x = edge.x;
    let y = edge.y;
    if (path) {
      const pos = utils_default.calcTerminalLabelPosition(
        edge.arrowTypeStart ? 10 : 0,
        "start_right",
        path
      );
      x = pos.x;
      y = pos.y;
    }
    el.attr("transform", `translate(${x}, ${y})`);
  }
  if (edge.endLabelLeft) {
    const el = terminalLabels.get(edge.id).endLeft;
    let x = edge.x;
    let y = edge.y;
    if (path) {
      const pos = utils_default.calcTerminalLabelPosition(edge.arrowTypeEnd ? 10 : 0, "end_left", path);
      x = pos.x;
      y = pos.y;
    }
    el.attr("transform", `translate(${x}, ${y})`);
  }
  if (edge.endLabelRight) {
    const el = terminalLabels.get(edge.id).endRight;
    let x = edge.x;
    let y = edge.y;
    if (path) {
      const pos = utils_default.calcTerminalLabelPosition(edge.arrowTypeEnd ? 10 : 0, "end_right", path);
      x = pos.x;
      y = pos.y;
    }
    el.attr("transform", `translate(${x}, ${y})`);
  }
}, "positionEdgeLabel");
var outsideNode = /* @__PURE__ */ __name((node, point2) => {
  const x = node.x;
  const y = node.y;
  const dx = Math.abs(point2.x - x);
  const dy = Math.abs(point2.y - y);
  const w = node.width / 2;
  const h = node.height / 2;
  return dx >= w || dy >= h;
}, "outsideNode");
var intersection = /* @__PURE__ */ __name((node, outsidePoint, insidePoint) => {
  log.debug(`intersection calc abc89:
  outsidePoint: ${JSON.stringify(outsidePoint)}
  insidePoint : ${JSON.stringify(insidePoint)}
  node        : x:${node.x} y:${node.y} w:${node.width} h:${node.height}`);
  const x = node.x;
  const y = node.y;
  const dx = Math.abs(x - insidePoint.x);
  const w = node.width / 2;
  let r = insidePoint.x < outsidePoint.x ? w - dx : w + dx;
  const h = node.height / 2;
  const Q = Math.abs(outsidePoint.y - insidePoint.y);
  const R = Math.abs(outsidePoint.x - insidePoint.x);
  if (Math.abs(y - outsidePoint.y) * w > Math.abs(x - outsidePoint.x) * h) {
    let q = insidePoint.y < outsidePoint.y ? outsidePoint.y - h - y : y - h - outsidePoint.y;
    r = R * q / Q;
    const res = {
      x: insidePoint.x < outsidePoint.x ? insidePoint.x + r : insidePoint.x - R + r,
      y: insidePoint.y < outsidePoint.y ? insidePoint.y + Q - q : insidePoint.y - Q + q
    };
    if (r === 0) {
      res.x = outsidePoint.x;
      res.y = outsidePoint.y;
    }
    if (R === 0) {
      res.x = outsidePoint.x;
    }
    if (Q === 0) {
      res.y = outsidePoint.y;
    }
    log.debug(`abc89 top/bottom calc, Q ${Q}, q ${q}, R ${R}, r ${r}`, res);
    return res;
  } else {
    if (insidePoint.x < outsidePoint.x) {
      r = outsidePoint.x - w - x;
    } else {
      r = x - w - outsidePoint.x;
    }
    let q = Q * r / R;
    let _x = insidePoint.x < outsidePoint.x ? insidePoint.x + R - r : insidePoint.x - R + r;
    let _y = insidePoint.y < outsidePoint.y ? insidePoint.y + q : insidePoint.y - q;
    log.debug(`sides calc abc89, Q ${Q}, q ${q}, R ${R}, r ${r}`, { _x, _y });
    if (r === 0) {
      _x = outsidePoint.x;
      _y = outsidePoint.y;
    }
    if (R === 0) {
      _x = outsidePoint.x;
    }
    if (Q === 0) {
      _y = outsidePoint.y;
    }
    return { x: _x, y: _y };
  }
}, "intersection");
var cutPathAtIntersect = /* @__PURE__ */ __name((_points, boundaryNode) => {
  log.warn("abc88 cutPathAtIntersect", _points, boundaryNode);
  let points = [];
  let lastPointOutside = _points[0];
  let isInside = false;
  _points.forEach((point2) => {
    log.info("abc88 checking point", point2, boundaryNode);
    if (!outsideNode(boundaryNode, point2) && !isInside) {
      const inter = intersection(boundaryNode, lastPointOutside, point2);
      log.debug("abc88 inside", point2, lastPointOutside, inter);
      log.debug("abc88 intersection", inter, boundaryNode);
      let pointPresent = false;
      points.forEach((p) => {
        pointPresent = pointPresent || p.x === inter.x && p.y === inter.y;
      });
      if (!points.some((e) => e.x === inter.x && e.y === inter.y)) {
        points.push(inter);
      } else {
        log.warn("abc88 no intersect", inter, points);
      }
      isInside = true;
    } else {
      log.warn("abc88 outside", point2, lastPointOutside);
      lastPointOutside = point2;
      if (!isInside) {
        points.push(point2);
      }
    }
  });
  log.debug("returning points", points);
  return points;
}, "cutPathAtIntersect");
function extractCornerPoints(points) {
  const cornerPoints = [];
  const cornerPointPositions = [];
  for (let i = 1; i < points.length - 1; i++) {
    const prev = points[i - 1];
    const curr = points[i];
    const next = points[i + 1];
    if (prev.x === curr.x && curr.y === next.y && Math.abs(curr.x - next.x) > 5 && Math.abs(curr.y - prev.y) > 5) {
      cornerPoints.push(curr);
      cornerPointPositions.push(i);
    } else if (prev.y === curr.y && curr.x === next.x && Math.abs(curr.x - prev.x) > 5 && Math.abs(curr.y - next.y) > 5) {
      cornerPoints.push(curr);
      cornerPointPositions.push(i);
    }
  }
  return { cornerPoints, cornerPointPositions };
}
__name(extractCornerPoints, "extractCornerPoints");
var findAdjacentPoint = /* @__PURE__ */ __name(function(pointA, pointB, distance) {
  const xDiff = pointB.x - pointA.x;
  const yDiff = pointB.y - pointA.y;
  const length = Math.sqrt(xDiff * xDiff + yDiff * yDiff);
  const ratio = distance / length;
  return { x: pointB.x - ratio * xDiff, y: pointB.y - ratio * yDiff };
}, "findAdjacentPoint");
var fixCorners = /* @__PURE__ */ __name(function(lineData) {
  const { cornerPointPositions } = extractCornerPoints(lineData);
  const newLineData = [];
  for (let i = 0; i < lineData.length; i++) {
    if (cornerPointPositions.includes(i)) {
      const prevPoint = lineData[i - 1];
      const nextPoint = lineData[i + 1];
      const cornerPoint = lineData[i];
      const newPrevPoint = findAdjacentPoint(prevPoint, cornerPoint, 5);
      const newNextPoint = findAdjacentPoint(nextPoint, cornerPoint, 5);
      const xDiff = newNextPoint.x - newPrevPoint.x;
      const yDiff = newNextPoint.y - newPrevPoint.y;
      newLineData.push(newPrevPoint);
      const a = Math.sqrt(2) * 2;
      let newCornerPoint = { x: cornerPoint.x, y: cornerPoint.y };
      if (Math.abs(nextPoint.x - prevPoint.x) > 10 && Math.abs(nextPoint.y - prevPoint.y) >= 10) {
        log.debug(
          "Corner point fixing",
          Math.abs(nextPoint.x - prevPoint.x),
          Math.abs(nextPoint.y - prevPoint.y)
        );
        const r = 5;
        if (cornerPoint.x === newPrevPoint.x) {
          newCornerPoint = {
            x: xDiff < 0 ? newPrevPoint.x - r + a : newPrevPoint.x + r - a,
            y: yDiff < 0 ? newPrevPoint.y - a : newPrevPoint.y + a
          };
        } else {
          newCornerPoint = {
            x: xDiff < 0 ? newPrevPoint.x - a : newPrevPoint.x + a,
            y: yDiff < 0 ? newPrevPoint.y - r + a : newPrevPoint.y + r - a
          };
        }
      } else {
        log.debug(
          "Corner point skipping fixing",
          Math.abs(nextPoint.x - prevPoint.x),
          Math.abs(nextPoint.y - prevPoint.y)
        );
      }
      newLineData.push(newCornerPoint, newNextPoint);
    } else {
      newLineData.push(lineData[i]);
    }
  }
  return newLineData;
}, "fixCorners");
var insertEdge = /* @__PURE__ */ __name(function(elem, edge, clusterDb, diagramType, startNode, endNode, id) {
  const { handDrawnSeed } = getConfig();
  let points = edge.points;
  let pointsHasChanged = false;
  const tail = startNode;
  var head = endNode;
  if (head.intersect && tail.intersect) {
    points = points.slice(1, edge.points.length - 1);
    points.unshift(tail.intersect(points[0]));
    log.debug(
      "Last point APA12",
      edge.start,
      "-->",
      edge.end,
      points[points.length - 1],
      head,
      head.intersect(points[points.length - 1])
    );
    points.push(head.intersect(points[points.length - 1]));
  }
  if (edge.toCluster) {
    log.info("to cluster abc88", clusterDb.get(edge.toCluster));
    points = cutPathAtIntersect(edge.points, clusterDb.get(edge.toCluster).node);
    pointsHasChanged = true;
  }
  if (edge.fromCluster) {
    log.debug(
      "from cluster abc88",
      clusterDb.get(edge.fromCluster),
      JSON.stringify(points, null, 2)
    );
    points = cutPathAtIntersect(points.reverse(), clusterDb.get(edge.fromCluster).node).reverse();
    pointsHasChanged = true;
  }
  let lineData = points.filter((p) => !Number.isNaN(p.y));
  lineData = fixCorners(lineData);
  let lastPoint = lineData[lineData.length - 1];
  if (lineData.length > 1) {
    lastPoint = lineData[lineData.length - 1];
    const secondLastPoint = lineData[lineData.length - 2];
    const diffX = (lastPoint.x - secondLastPoint.x) / 2;
    const diffY = (lastPoint.y - secondLastPoint.y) / 2;
    const midPoint = { x: secondLastPoint.x + diffX, y: secondLastPoint.y + diffY };
    lineData.splice(-1, 0, midPoint);
  }
  let curve = curveBasis;
  if (edge.curve) {
    curve = edge.curve;
  }
  const { x, y } = getLineFunctionsWithOffset(edge);
  const lineFunction = line().x(x).y(y).curve(curve);
  let strokeClasses;
  switch (edge.thickness) {
    case "normal":
      strokeClasses = "edge-thickness-normal";
      break;
    case "thick":
      strokeClasses = "edge-thickness-thick";
      break;
    case "invisible":
      strokeClasses = "edge-thickness-invisible";
      break;
    default:
      strokeClasses = "edge-thickness-normal";
  }
  switch (edge.pattern) {
    case "solid":
      strokeClasses += " edge-pattern-solid";
      break;
    case "dotted":
      strokeClasses += " edge-pattern-dotted";
      break;
    case "dashed":
      strokeClasses += " edge-pattern-dashed";
      break;
    default:
      strokeClasses += " edge-pattern-solid";
  }
  let svgPath;
  let linePath = lineFunction(lineData);
  const edgeStyles = Array.isArray(edge.style) ? edge.style : [edge.style];
  if (edge.look === "handDrawn") {
    const rc = rough2.svg(elem);
    Object.assign([], lineData);
    const svgPathNode = rc.path(linePath, {
      roughness: 0.3,
      seed: handDrawnSeed
    });
    strokeClasses += " transition";
    svgPath = select3(svgPathNode).select("path").attr("id", edge.id).attr("class", " " + strokeClasses + (edge.classes ? " " + edge.classes : "")).attr("style", edgeStyles ? edgeStyles.reduce((acc, style) => acc + ";" + style, "") : "");
    let d = svgPath.attr("d");
    svgPath.attr("d", d);
    elem.node().appendChild(svgPath.node());
  } else {
    svgPath = elem.append("path").attr("d", linePath).attr("id", edge.id).attr("class", " " + strokeClasses + (edge.classes ? " " + edge.classes : "")).attr("style", edgeStyles ? edgeStyles.reduce((acc, style) => acc + ";" + style, "") : "");
  }
  let url = "";
  if (getConfig().flowchart.arrowMarkerAbsolute || getConfig().state.arrowMarkerAbsolute) {
    url = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search;
    url = url.replace(/\(/g, "\\(").replace(/\)/g, "\\)");
  }
  log.info("arrowTypeStart", edge.arrowTypeStart);
  log.info("arrowTypeEnd", edge.arrowTypeEnd);
  addEdgeMarkers(svgPath, edge, url, id, diagramType);
  let paths = {};
  if (pointsHasChanged) {
    paths.updatedPath = points;
  }
  paths.originalPath = edge.points;
  return paths;
}, "insertEdge");

// src/rendering-util/rendering-elements/markers.js
var insertMarkers = /* @__PURE__ */ __name((elem, markerArray, type, id) => {
  markerArray.forEach((markerName) => {
    markers[markerName](elem, type, id);
  });
}, "insertMarkers");
var extension = /* @__PURE__ */ __name((elem, type, id) => {
  log.trace("Making markers for ", id);
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-extensionStart").attr("class", "marker extension " + type).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 1,7 L18,13 V 1 Z");
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-extensionEnd").attr("class", "marker extension " + type).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 1,1 V 13 L18,7 Z");
}, "extension");
var composition = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-compositionStart").attr("class", "marker composition " + type).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-compositionEnd").attr("class", "marker composition " + type).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
}, "composition");
var aggregation = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-aggregationStart").attr("class", "marker aggregation " + type).attr("refX", 18).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-aggregationEnd").attr("class", "marker aggregation " + type).attr("refX", 1).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L1,7 L9,1 Z");
}, "aggregation");
var dependency = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-dependencyStart").attr("class", "marker dependency " + type).attr("refX", 6).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("path").attr("d", "M 5,7 L9,13 L1,7 L9,1 Z");
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-dependencyEnd").attr("class", "marker dependency " + type).attr("refX", 13).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 28).attr("orient", "auto").append("path").attr("d", "M 18,7 L9,13 L14,7 L9,1 Z");
}, "dependency");
var lollipop = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-lollipopStart").attr("class", "marker lollipop " + type).attr("refX", 13).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("circle").attr("stroke", "black").attr("fill", "transparent").attr("cx", 7).attr("cy", 7).attr("r", 6);
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-lollipopEnd").attr("class", "marker lollipop " + type).attr("refX", 1).attr("refY", 7).attr("markerWidth", 190).attr("markerHeight", 240).attr("orient", "auto").append("circle").attr("stroke", "black").attr("fill", "transparent").attr("cx", 7).attr("cy", 7).attr("r", 6);
}, "lollipop");
var point = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("marker").attr("id", id + "_" + type + "-pointEnd").attr("class", "marker " + type).attr("viewBox", "0 0 10 10").attr("refX", 5).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 8).attr("markerHeight", 8).attr("orient", "auto").append("path").attr("d", "M 0 0 L 10 5 L 0 10 z").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
  elem.append("marker").attr("id", id + "_" + type + "-pointStart").attr("class", "marker " + type).attr("viewBox", "0 0 10 10").attr("refX", 4.5).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 8).attr("markerHeight", 8).attr("orient", "auto").append("path").attr("d", "M 0 5 L 10 10 L 10 0 z").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
}, "point");
var circle = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("marker").attr("id", id + "_" + type + "-circleEnd").attr("class", "marker " + type).attr("viewBox", "0 0 10 10").attr("refX", 11).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("circle").attr("cx", "5").attr("cy", "5").attr("r", "5").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
  elem.append("marker").attr("id", id + "_" + type + "-circleStart").attr("class", "marker " + type).attr("viewBox", "0 0 10 10").attr("refX", -1).attr("refY", 5).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("circle").attr("cx", "5").attr("cy", "5").attr("r", "5").attr("class", "arrowMarkerPath").style("stroke-width", 1).style("stroke-dasharray", "1,0");
}, "circle");
var cross = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("marker").attr("id", id + "_" + type + "-crossEnd").attr("class", "marker cross " + type).attr("viewBox", "0 0 11 11").attr("refX", 12).attr("refY", 5.2).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("path").attr("d", "M 1,1 l 9,9 M 10,1 l -9,9").attr("class", "arrowMarkerPath").style("stroke-width", 2).style("stroke-dasharray", "1,0");
  elem.append("marker").attr("id", id + "_" + type + "-crossStart").attr("class", "marker cross " + type).attr("viewBox", "0 0 11 11").attr("refX", -1).attr("refY", 5.2).attr("markerUnits", "userSpaceOnUse").attr("markerWidth", 11).attr("markerHeight", 11).attr("orient", "auto").append("path").attr("d", "M 1,1 l 9,9 M 10,1 l -9,9").attr("class", "arrowMarkerPath").style("stroke-width", 2).style("stroke-dasharray", "1,0");
}, "cross");
var barb = /* @__PURE__ */ __name((elem, type, id) => {
  elem.append("defs").append("marker").attr("id", id + "_" + type + "-barbEnd").attr("refX", 19).attr("refY", 7).attr("markerWidth", 20).attr("markerHeight", 14).attr("markerUnits", "userSpaceOnUse").attr("orient", "auto").append("path").attr("d", "M 19,7 L9,13 L14,7 L9,1 Z");
}, "barb");
var markers = {
  extension,
  composition,
  aggregation,
  dependency,
  lollipop,
  point,
  circle,
  cross,
  barb
};
var markers_default = insertMarkers;

// src/rendering-util/rendering-elements/shapes/util.js
import { select as select4 } from "d3";
var labelHelper = /* @__PURE__ */ __name(async (parent, node, _classes) => {
  let cssClasses;
  const useHtmlLabels = node.useHtmlLabels || evaluate(getConfig().flowchart.htmlLabels);
  if (!_classes) {
    cssClasses = "node default";
  } else {
    cssClasses = _classes;
  }
  const shapeSvg = parent.insert("g").attr("class", cssClasses).attr("id", node.domId || node.id);
  const labelEl = shapeSvg.insert("g").attr("class", "label").attr("style", node.labelStyle);
  let label;
  if (node.label === void 0) {
    label = "";
  } else {
    label = typeof node.label === "string" ? node.label : node.label[0];
  }
  let text;
  text = await createText(labelEl, sanitizeText(decodeEntities(label), getConfig()), {
    useHtmlLabels,
    width: node.width || getConfig().flowchart.wrappingWidth,
    cssClasses: "markdown-node-label",
    style: node.labelStyle
  });
  let bbox = text.getBBox();
  const halfPadding = node.padding / 2;
  if (evaluate(getConfig().flowchart.htmlLabels)) {
    const div = text.children[0];
    const dv = select4(text);
    const images = div.getElementsByTagName("img");
    if (images) {
      const noImgText = label.replace(/<img[^>]*>/g, "").trim() === "";
      await Promise.all(
        [...images].map(
          (img) => new Promise((res) => {
            function setupImage() {
              img.style.display = "flex";
              img.style.flexDirection = "column";
              if (noImgText) {
                const bodyFontSize = getConfig().fontSize ? getConfig().fontSize : window.getComputedStyle(document.body).fontSize;
                const enlargingFactor = 5;
                const width = parseInt(bodyFontSize, 10) * enlargingFactor + "px";
                img.style.minWidth = width;
                img.style.maxWidth = width;
              } else {
                img.style.width = "100%";
              }
              res(img);
            }
            __name(setupImage, "setupImage");
            setTimeout(() => {
              if (img.complete) {
                setupImage();
              }
            });
            img.addEventListener("error", setupImage);
            img.addEventListener("load", setupImage);
          })
        )
      );
    }
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  if (useHtmlLabels) {
    labelEl.attr("transform", "translate(" + -bbox.width / 2 + ", " + -bbox.height / 2 + ")");
  } else {
    labelEl.attr("transform", "translate(0, " + -bbox.height / 2 + ")");
  }
  if (node.centerLabel) {
    labelEl.attr("transform", "translate(" + -bbox.width / 2 + ", " + -bbox.height / 2 + ")");
  }
  labelEl.insert("rect", ":first-child");
  return { shapeSvg, bbox, halfPadding, label: labelEl };
}, "labelHelper");
var updateNodeBounds = /* @__PURE__ */ __name((node, element) => {
  const bbox = element.node().getBBox();
  node.width = bbox.width;
  node.height = bbox.height;
}, "updateNodeBounds");
var getNodeClasses = /* @__PURE__ */ __name((node, extra) => (node.look === "handDrawn" ? "rough-node" : "node") + " " + node.cssClasses + " " + (extra || ""), "getNodeClasses");

// src/rendering-util/rendering-elements/intersect/intersect-node.js
function intersectNode(node, point2) {
  return node.intersect(point2);
}
__name(intersectNode, "intersectNode");
var intersect_node_default = intersectNode;

// src/rendering-util/rendering-elements/intersect/intersect-ellipse.js
function intersectEllipse(node, rx, ry, point2) {
  var cx = node.x;
  var cy = node.y;
  var px = cx - point2.x;
  var py = cy - point2.y;
  var det = Math.sqrt(rx * rx * py * py + ry * ry * px * px);
  var dx = Math.abs(rx * ry * px / det);
  if (point2.x < cx) {
    dx = -dx;
  }
  var dy = Math.abs(rx * ry * py / det);
  if (point2.y < cy) {
    dy = -dy;
  }
  return { x: cx + dx, y: cy + dy };
}
__name(intersectEllipse, "intersectEllipse");
var intersect_ellipse_default = intersectEllipse;

// src/rendering-util/rendering-elements/intersect/intersect-circle.js
function intersectCircle(node, rx, point2) {
  return intersect_ellipse_default(node, rx, rx, point2);
}
__name(intersectCircle, "intersectCircle");
var intersect_circle_default = intersectCircle;

// src/rendering-util/rendering-elements/intersect/intersect-line.js
function intersectLine(p1, p2, q1, q2) {
  var a1, a2, b1, b2, c1, c2;
  var r1, r2, r3, r4;
  var denom, offset, num;
  var x, y;
  a1 = p2.y - p1.y;
  b1 = p1.x - p2.x;
  c1 = p2.x * p1.y - p1.x * p2.y;
  r3 = a1 * q1.x + b1 * q1.y + c1;
  r4 = a1 * q2.x + b1 * q2.y + c1;
  if (r3 !== 0 && r4 !== 0 && sameSign(r3, r4)) {
    return;
  }
  a2 = q2.y - q1.y;
  b2 = q1.x - q2.x;
  c2 = q2.x * q1.y - q1.x * q2.y;
  r1 = a2 * p1.x + b2 * p1.y + c2;
  r2 = a2 * p2.x + b2 * p2.y + c2;
  if (r1 !== 0 && r2 !== 0 && sameSign(r1, r2)) {
    return;
  }
  denom = a1 * b2 - a2 * b1;
  if (denom === 0) {
    return;
  }
  offset = Math.abs(denom / 2);
  num = b1 * c2 - b2 * c1;
  x = num < 0 ? (num - offset) / denom : (num + offset) / denom;
  num = a2 * c1 - a1 * c2;
  y = num < 0 ? (num - offset) / denom : (num + offset) / denom;
  return { x, y };
}
__name(intersectLine, "intersectLine");
function sameSign(r1, r2) {
  return r1 * r2 > 0;
}
__name(sameSign, "sameSign");
var intersect_line_default = intersectLine;

// src/rendering-util/rendering-elements/intersect/intersect-polygon.js
function intersectPolygon(node, polyPoints, point2) {
  let x1 = node.x;
  let y1 = node.y;
  let intersections = [];
  let minX = Number.POSITIVE_INFINITY;
  let minY = Number.POSITIVE_INFINITY;
  if (typeof polyPoints.forEach === "function") {
    polyPoints.forEach(function(entry) {
      minX = Math.min(minX, entry.x);
      minY = Math.min(minY, entry.y);
    });
  } else {
    minX = Math.min(minX, polyPoints.x);
    minY = Math.min(minY, polyPoints.y);
  }
  let left = x1 - node.width / 2 - minX;
  let top = y1 - node.height / 2 - minY;
  for (let i = 0; i < polyPoints.length; i++) {
    let p1 = polyPoints[i];
    let p2 = polyPoints[i < polyPoints.length - 1 ? i + 1 : 0];
    let intersect = intersect_line_default(
      node,
      point2,
      { x: left + p1.x, y: top + p1.y },
      { x: left + p2.x, y: top + p2.y }
    );
    if (intersect) {
      intersections.push(intersect);
    }
  }
  if (!intersections.length) {
    return node;
  }
  if (intersections.length > 1) {
    intersections.sort(function(p, q) {
      let pdx = p.x - point2.x;
      let pdy = p.y - point2.y;
      let distp = Math.sqrt(pdx * pdx + pdy * pdy);
      let qdx = q.x - point2.x;
      let qdy = q.y - point2.y;
      let distq = Math.sqrt(qdx * qdx + qdy * qdy);
      return distp < distq ? -1 : distp === distq ? 0 : 1;
    });
  }
  return intersections[0];
}
__name(intersectPolygon, "intersectPolygon");
var intersect_polygon_default = intersectPolygon;

// src/rendering-util/rendering-elements/intersect/index.js
var intersect_default = {
  node: intersect_node_default,
  circle: intersect_circle_default,
  ellipse: intersect_ellipse_default,
  polygon: intersect_polygon_default,
  rect: intersect_rect_default
};

// src/rendering-util/rendering-elements/shapes/drawRect.ts
import rough3 from "roughjs";
var drawRect = /* @__PURE__ */ __name(async (parent, node, options) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const totalWidth = Math.max(bbox.width + options.labelPaddingX * 2, node?.width || 0);
  const totalHeight = Math.max(bbox.height + options.labelPaddingY * 2, node?.height || 0);
  const x = -totalWidth / 2;
  const y = -totalHeight / 2;
  let rect2;
  let { rx, ry } = node;
  const { cssStyles } = node;
  if (options?.rx && options.ry) {
    rx = options.rx;
    ry = options.ry;
  }
  if (node.look === "handDrawn") {
    const rc = rough3.svg(shapeSvg);
    const options2 = userNodeOverrides(node, {});
    const roughNode = rx || ry ? rc.path(createRoundedRectPathD(x, y, totalWidth, totalHeight, rx || 0), options2) : rc.rectangle(x, y, totalWidth, totalHeight, options2);
    rect2 = shapeSvg.insert(() => roughNode, ":first-child");
    rect2.attr("class", "basic label-container").attr("style", cssStyles);
  } else {
    rect2 = shapeSvg.insert("rect", ":first-child");
    rect2.attr("class", "basic label-container").attr("style", nodeStyles).attr("rx", rx).attr("data-id", "abc").attr("data-et", "node").attr("ry", ry).attr("x", x).attr("y", y).attr("width", totalWidth).attr("height", totalHeight);
  }
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "drawRect");

// src/rendering-util/rendering-elements/shapes/state.ts
var state = /* @__PURE__ */ __name(async (parent, node) => {
  const options = {
    rx: 5,
    ry: 5,
    classes: "flowchart-node"
  };
  return drawRect(parent, node, options);
}, "state");

// src/rendering-util/rendering-elements/shapes/roundedRect.ts
var roundedRect = /* @__PURE__ */ __name(async (parent, node) => {
  const options = {
    rx: 5,
    ry: 5,
    classes: "",
    labelPaddingX: (node?.padding || 0) * 1,
    labelPaddingY: (node?.padding || 0) * 1
  };
  return drawRect(parent, node, options);
}, "roundedRect");

// src/rendering-util/rendering-elements/shapes/squareRect.ts
var squareRect2 = /* @__PURE__ */ __name(async (parent, node) => {
  const options = {
    rx: 0,
    ry: 0,
    classes: "",
    labelPaddingX: (node?.padding || 0) * 2,
    labelPaddingY: (node?.padding || 0) * 1
  };
  return drawRect(parent, node, options);
}, "squareRect");

// src/rendering-util/rendering-elements/shapes/stateStart.ts
import rough4 from "roughjs";
var stateStart = /* @__PURE__ */ __name((parent, node) => {
  const { themeVariables } = getConfig();
  const { lineColor } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", "node default").attr("id", node.domId || node.id);
  let circle3;
  if (node.look === "handDrawn") {
    const rc = rough4.svg(shapeSvg);
    const roughNode = rc.circle(0, 0, 14, solidStateFill(lineColor));
    circle3 = shapeSvg.insert(() => roughNode);
  } else {
    circle3 = shapeSvg.insert("circle", ":first-child");
  }
  circle3.attr("class", "state-start").attr("r", 7).attr("width", 14).attr("height", 14);
  updateNodeBounds(node, circle3);
  node.intersect = function(point2) {
    return intersect_default.circle(node, 7, point2);
  };
  return shapeSvg;
}, "stateStart");

// src/rendering-util/rendering-elements/shapes/stateEnd.ts
import rough5 from "roughjs";
var stateEnd = /* @__PURE__ */ __name((parent, node) => {
  const { themeVariables } = getConfig();
  const { lineColor } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", "node default").attr("id", node.domId || node.id);
  let circle3;
  let innerCircle;
  if (node.look === "handDrawn") {
    const rc = rough5.svg(shapeSvg);
    const roughNode = rc.circle(0, 0, 14, { ...solidStateFill(lineColor), roughness: 0.5 });
    const roughInnerNode = rc.circle(0, 0, 5, { ...solidStateFill(lineColor), fillStyle: "solid" });
    circle3 = shapeSvg.insert(() => roughNode);
    innerCircle = shapeSvg.insert(() => roughInnerNode);
  } else {
    innerCircle = shapeSvg.insert("circle", ":first-child");
    circle3 = shapeSvg.insert("circle", ":first-child");
    circle3.attr("class", "state-start").attr("r", 7).attr("width", 14).attr("height", 14);
    innerCircle.attr("class", "state-end").attr("r", 5).attr("width", 10).attr("height", 10);
  }
  updateNodeBounds(node, circle3);
  node.intersect = function(point2) {
    return intersect_default.circle(node, 7, point2);
  };
  return shapeSvg;
}, "stateEnd");

// src/rendering-util/rendering-elements/shapes/forkJoin.ts
import rough6 from "roughjs";
var forkJoin = /* @__PURE__ */ __name((parent, node, dir) => {
  const { themeVariables } = getConfig();
  const { lineColor } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", "node default").attr("id", node.domId || node.id);
  let width = 70;
  let height = 10;
  if (dir === "LR") {
    width = 10;
    height = 70;
  }
  const x = -1 * width / 2;
  const y = -1 * height / 2;
  let shape;
  if (node.look === "handDrawn") {
    const rc = rough6.svg(shapeSvg);
    const roughNode = rc.rectangle(x, y, width, height, solidStateFill(lineColor));
    shape = shapeSvg.insert(() => roughNode);
  } else {
    shape = shapeSvg.append("rect").attr("x", x).attr("y", y).attr("width", width).attr("height", height).attr("class", "fork-join");
  }
  updateNodeBounds(node, shape);
  let nodeHeight = 0;
  let nodeWidth = 0;
  let nodePadding = 10;
  if (node.height) {
    nodeHeight = node.height;
  }
  if (node.width) {
    nodeWidth = node.width;
  }
  if (node.padding) {
    nodePadding = node.padding;
  }
  node.height = nodeHeight + nodePadding / 2;
  node.width = nodeWidth + nodePadding / 2;
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "forkJoin");

// src/rendering-util/rendering-elements/shapes/choice.ts
import rough7 from "roughjs";
var choice = /* @__PURE__ */ __name((parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { themeVariables } = getConfig();
  const { lineColor } = themeVariables;
  const shapeSvg = parent.insert("g").attr("class", "node default").attr("id", node.domId || node.id);
  const s = 28;
  const points = [
    { x: 0, y: s / 2 },
    { x: s / 2, y: 0 },
    { x: 0, y: -s / 2 },
    { x: -s / 2, y: 0 }
  ];
  let choice2;
  if (node.look === "handDrawn") {
    const rc = rough7.svg(shapeSvg);
    const pointArr = points.map(function(d) {
      return [d.x, d.y];
    });
    const roughNode = rc.polygon(pointArr, solidStateFill(lineColor));
    choice2 = shapeSvg.insert(() => roughNode);
  } else {
    choice2 = shapeSvg.insert("polygon", ":first-child").attr(
      "points",
      points.map(function(d) {
        return d.x + "," + d.y;
      }).join(" ")
    );
  }
  choice2.attr("class", "state-start").attr("r", 7).attr("width", 28).attr("height", 28).attr("style", nodeStyles);
  node.width = 28;
  node.height = 28;
  node.intersect = function(point2) {
    return intersect_default.circle(node, 14, point2);
  };
  return shapeSvg;
}, "choice");

// src/rendering-util/rendering-elements/shapes/note.ts
import rough8 from "roughjs";
var note = /* @__PURE__ */ __name(async (parent, node) => {
  const { themeVariables, handDrawnSeed } = getConfig();
  const { noteBorderColor, noteBkgColor } = themeVariables;
  const useHtmlLabels = node.useHtmlLabels;
  if (!useHtmlLabels) {
    node.centerLabel = true;
  }
  const { shapeSvg, bbox } = await labelHelper(parent, node, "node " + node.cssClasses);
  log.info("Classes = ", node.cssClasses);
  const { cssStyles } = node;
  let rect2;
  const totalWidth = bbox.width + node.padding;
  const totalHeight = bbox.height + node.padding;
  const x = -totalWidth / 2;
  const y = -totalHeight / 2;
  if (node.look === "handDrawn") {
    const rc = rough8.svg(shapeSvg);
    const roughNode = rc.rectangle(x, y, totalWidth, totalHeight, {
      roughness: 0.7,
      fill: noteBkgColor,
      fillWeight: 3,
      seed: handDrawnSeed,
      // fillStyle: 'solid', // solid fill'
      stroke: noteBorderColor
    });
    rect2 = shapeSvg.insert(() => roughNode, ":first-child");
    rect2.attr("class", "basic label-container").attr("style", cssStyles);
  } else {
    rect2 = shapeSvg.insert("rect", ":first-child");
    rect2.attr("rx", node.rx).attr("ry", node.ry).attr("x", x).attr("y", y).attr("width", totalWidth).attr("height", totalHeight);
  }
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "note");

// src/rendering-util/rendering-elements/shapes/stadium.ts
import rough9 from "roughjs";
var stadium = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const h = bbox.height + node.padding;
  const w = bbox.width + h / 4 + node.padding;
  let rect2;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough9.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createRoundedRectPathD(-w / 2, -h / 2, w, h, h / 2);
    const roughNode = rc.path(pathData, options);
    rect2 = shapeSvg.insert(() => roughNode, ":first-child");
    rect2.attr("class", "basic label-container").attr("style", cssStyles);
  } else {
    rect2 = shapeSvg.insert("rect", ":first-child");
    rect2.attr("class", "basic label-container").attr("style", nodeStyles).attr("rx", h / 2).attr("ry", h / 2).attr("x", -w / 2).attr("y", -h / 2).attr("width", w).attr("height", h);
  }
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "stadium");

// src/rendering-util/rendering-elements/shapes/rectWithTitle.ts
import { select as select5 } from "d3";
import rough10 from "roughjs";
var rectWithTitle = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  let classes;
  if (!node.cssClasses) {
    classes = "node default";
  } else {
    classes = "node " + node.cssClasses;
  }
  const shapeSvg = parent.insert("g").attr("class", classes).attr("id", node.domId || node.id);
  const g = shapeSvg.insert("g");
  const label = shapeSvg.insert("g").attr("class", "label").attr("style", nodeStyles);
  const description = node.description;
  const title = node.label;
  const text = label.node().appendChild(await createLabel_default(title, node.labelStyle, true, true));
  let bbox = { width: 0, height: 0 };
  if (evaluate(getConfig()?.flowchart?.htmlLabels)) {
    const div2 = text.children[0];
    const dv2 = select5(text);
    bbox = div2.getBoundingClientRect();
    dv2.attr("width", bbox.width);
    dv2.attr("height", bbox.height);
  }
  log.info("Text 2", description);
  const textRows = description || [];
  const titleBox = text.getBBox();
  const descr = label.node().appendChild(
    await createLabel_default(
      textRows.join ? textRows.join("<br/>") : textRows,
      node.labelStyle,
      true,
      true
    )
  );
  const div = descr.children[0];
  const dv = select5(descr);
  bbox = div.getBoundingClientRect();
  dv.attr("width", bbox.width);
  dv.attr("height", bbox.height);
  const halfPadding = (node.padding || 0) / 2;
  select5(descr).attr(
    "transform",
    "translate( " + (bbox.width > titleBox.width ? 0 : (titleBox.width - bbox.width) / 2) + ", " + (titleBox.height + halfPadding + 5) + ")"
  );
  select5(text).attr(
    "transform",
    "translate( " + (bbox.width < titleBox.width ? 0 : -(titleBox.width - bbox.width) / 2) + ", 0)"
  );
  bbox = label.node().getBBox();
  label.attr(
    "transform",
    "translate(" + -bbox.width / 2 + ", " + (-bbox.height / 2 - halfPadding + 3) + ")"
  );
  const totalWidth = bbox.width + (node.padding || 0);
  const totalHeight = bbox.height + (node.padding || 0);
  const x = -bbox.width / 2 - halfPadding;
  const y = -bbox.height / 2 - halfPadding;
  let rect2;
  let innerLine;
  if (node.look === "handDrawn") {
    const rc = rough10.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const roughNode = rc.path(
      createRoundedRectPathD(x, y, totalWidth, totalHeight, node.rx || 0),
      options
    );
    const roughLine = rc.line(
      -bbox.width / 2 - halfPadding,
      -bbox.height / 2 - halfPadding + titleBox.height + halfPadding,
      bbox.width / 2 + halfPadding,
      -bbox.height / 2 - halfPadding + titleBox.height + halfPadding,
      options
    );
    innerLine = shapeSvg.insert(() => {
      log.debug("Rough node insert CXC", roughNode);
      return roughLine;
    }, ":first-child");
    rect2 = shapeSvg.insert(() => {
      log.debug("Rough node insert CXC", roughNode);
      return roughNode;
    }, ":first-child");
  } else {
    rect2 = g.insert("rect", ":first-child");
    innerLine = g.insert("line");
    rect2.attr("class", "outer title-state").attr("style", nodeStyles).attr("x", -bbox.width / 2 - halfPadding).attr("y", -bbox.height / 2 - halfPadding).attr("width", bbox.width + (node.padding || 0)).attr("height", bbox.height + (node.padding || 0));
    innerLine.attr("class", "divider").attr("x1", -bbox.width / 2 - halfPadding).attr("x2", bbox.width / 2 + halfPadding).attr("y1", -bbox.height / 2 - halfPadding + titleBox.height + halfPadding).attr("y2", -bbox.height / 2 - halfPadding + titleBox.height + halfPadding);
  }
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "rectWithTitle");

// src/rendering-util/rendering-elements/shapes/subroutine.ts
import rough11 from "roughjs";

// src/rendering-util/rendering-elements/shapes/insertPolygonShape.ts
function insertPolygonShape(parent, w, h, points) {
  return parent.insert("polygon", ":first-child").attr(
    "points",
    points.map(function(d) {
      return d.x + "," + d.y;
    }).join(" ")
  ).attr("class", "label-container").attr("transform", "translate(" + -w / 2 + "," + h / 2 + ")");
}
__name(insertPolygonShape, "insertPolygonShape");

// src/rendering-util/rendering-elements/shapes/subroutine.ts
var subroutine = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const halfPadding = (node?.padding || 0) / 2;
  const w = bbox.width + node.padding;
  const h = bbox.height + node.padding;
  const x = -bbox.width / 2 - halfPadding;
  const y = -bbox.height / 2 - halfPadding;
  const points = [
    { x: 0, y: 0 },
    { x: w, y: 0 },
    { x: w, y: -h },
    { x: 0, y: -h },
    { x: 0, y: 0 },
    { x: -8, y: 0 },
    { x: w + 8, y: 0 },
    { x: w + 8, y: -h },
    { x: -8, y: -h },
    { x: -8, y: 0 }
  ];
  if (node.look === "handDrawn") {
    const rc = rough11.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const roughNode = rc.rectangle(x - 8, y, w + 16, h, options);
    const l1 = rc.line(x, y, x, y + h, options);
    const l2 = rc.line(x + w, y, x + w, y + h, options);
    shapeSvg.insert(() => l1, ":first-child");
    shapeSvg.insert(() => l2, ":first-child");
    const rect2 = shapeSvg.insert(() => roughNode, ":first-child");
    const { cssStyles } = node;
    rect2.attr("class", "basic label-container").attr("style", cssStyles);
    updateNodeBounds(node, rect2);
  } else {
    const el = insertPolygonShape(shapeSvg, w, h, points);
    if (nodeStyles) {
      el.attr("style", nodeStyles);
    }
    updateNodeBounds(node, el);
  }
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "subroutine");

// src/rendering-util/rendering-elements/shapes/cylinder.ts
import rough12 from "roughjs";
var createCylinderPathD = /* @__PURE__ */ __name((x, y, width, height, rx, ry) => {
  return [
    `M${x},${y + ry}`,
    `a${rx},${ry} 0,0,0 ${width},0`,
    `a${rx},${ry} 0,0,0 ${-width},0`,
    `l0,${height}`,
    `a${rx},${ry} 0,0,0 ${width},0`,
    `l0,${-height}`
  ].join(" ");
}, "createCylinderPathD");
var createOuterCylinderPathD = /* @__PURE__ */ __name((x, y, width, height, rx, ry) => {
  return [
    `M${x},${y + ry}`,
    `M${x + width},${y + ry}`,
    `a${rx},${ry} 0,0,0 ${-width},0`,
    `l0,${height}`,
    `a${rx},${ry} 0,0,0 ${width},0`,
    `l0,${-height}`
  ].join(" ");
}, "createOuterCylinderPathD");
var createInnerCylinderPathD = /* @__PURE__ */ __name((x, y, width, height, rx, ry) => {
  return [`M${x - width / 2},${-height / 2}`, `a${rx},${ry} 0,0,0 ${width},0`].join(" ");
}, "createInnerCylinderPathD");
var cylinder = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w = bbox.width + node.padding;
  const rx = w / 2;
  const ry = rx / (2.5 + w / 50);
  const h = bbox.height + ry + node.padding;
  let cylinder2;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough12.svg(shapeSvg);
    const outerPathData = createOuterCylinderPathD(0, 0, w, h, rx, ry);
    const innerPathData = createInnerCylinderPathD(0, ry, w, h, rx, ry);
    const outerNode = rc.path(outerPathData, userNodeOverrides(node, {}));
    const innerLine = rc.path(innerPathData, userNodeOverrides(node, { fill: "none" }));
    cylinder2 = shapeSvg.insert(() => innerLine, ":first-child");
    cylinder2 = shapeSvg.insert(() => outerNode, ":first-child");
    cylinder2.attr("class", "basic label-container");
    if (cssStyles) {
      cylinder2.attr("style", cssStyles);
    }
  } else {
    const pathData = createCylinderPathD(0, 0, w, h, rx, ry);
    cylinder2 = shapeSvg.insert("path", ":first-child").attr("d", pathData).attr("class", "basic label-container").attr("style", cssStyles).attr("style", nodeStyles);
  }
  cylinder2.attr("label-offset-y", ry);
  cylinder2.attr("transform", `translate(${-w / 2}, ${-(h / 2 + ry)})`);
  updateNodeBounds(node, cylinder2);
  node.intersect = function(point2) {
    const pos = intersect_default.rect(node, point2);
    const x = pos.x - (node.x ?? 0);
    if (rx != 0 && (Math.abs(x) < (node.width ?? 0) / 2 || Math.abs(x) == (node.width ?? 0) / 2 && Math.abs(pos.y - (node.y ?? 0)) > (node.height ?? 0) / 2 - ry)) {
      let y = ry * ry * (1 - x * x / (rx * rx));
      if (y > 0) {
        y = Math.sqrt(y);
      }
      y = ry - y;
      if (point2.y - (node.y ?? 0) > 0) {
        y = -y;
      }
      pos.y += y;
    }
    return pos;
  };
  return shapeSvg;
}, "cylinder");

// src/rendering-util/rendering-elements/shapes/circle.ts
import rough13 from "roughjs";
var circle2 = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox, halfPadding } = await labelHelper(parent, node, getNodeClasses(node));
  const radius = bbox.width / 2 + halfPadding;
  let circleElem;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough13.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const roughNode = rc.circle(0, 0, radius * 2, options);
    circleElem = shapeSvg.insert(() => roughNode, ":first-child");
    circleElem.attr("class", "basic label-container").attr("style", cssStyles);
  } else {
    circleElem = shapeSvg.insert("circle", ":first-child").attr("class", "basic label-container").attr("style", nodeStyles).attr("r", radius).attr("cx", 0).attr("cy", 0);
  }
  updateNodeBounds(node, circleElem);
  node.intersect = function(point2) {
    log.info("Circle intersect", node, radius, point2);
    return intersect_default.circle(node, radius, point2);
  };
  return shapeSvg;
}, "circle");

// src/rendering-util/rendering-elements/shapes/doubleCircle.ts
import rough14 from "roughjs";
var doublecircle = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox, halfPadding } = await labelHelper(parent, node, getNodeClasses(node));
  const gap = 5;
  const outerRadius = bbox.width / 2 + halfPadding + gap;
  const innerRadius = bbox.width / 2 + halfPadding;
  let circleGroup;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough14.svg(shapeSvg);
    const outerOptions = userNodeOverrides(node, { roughness: 0.2, strokeWidth: 2.5 });
    const innerOptions = userNodeOverrides(node, { roughness: 0.2, strokeWidth: 1.5 });
    const outerRoughNode = rc.circle(0, 0, outerRadius * 2, outerOptions);
    const innerRoughNode = rc.circle(0, 0, innerRadius * 2, innerOptions);
    circleGroup = shapeSvg.insert("g", ":first-child");
    circleGroup.attr("class", node.cssClasses).attr("style", cssStyles);
    circleGroup.node()?.appendChild(outerRoughNode);
    circleGroup.node()?.appendChild(innerRoughNode);
  } else {
    circleGroup = shapeSvg.insert("g", ":first-child");
    const outerCircle = circleGroup.insert("circle", ":first-child");
    const innerCircle = circleGroup.insert("circle");
    circleGroup.attr("class", "basic label-container").attr("style", nodeStyles);
    outerCircle.attr("class", "outer-circle").attr("style", nodeStyles).attr("r", outerRadius).attr("cx", 0).attr("cy", 0);
    innerCircle.attr("class", "inner-circle").attr("style", nodeStyles).attr("r", innerRadius).attr("cx", 0).attr("cy", 0);
  }
  updateNodeBounds(node, circleGroup);
  node.intersect = function(point2) {
    log.info("DoubleCircle intersect", node, outerRadius, point2);
    return intersect_default.circle(node, outerRadius, point2);
  };
  return shapeSvg;
}, "doublecircle");

// src/rendering-util/rendering-elements/shapes/rectLeftInvArrow.ts
import rough15 from "roughjs";
var createPolygonPathD = /* @__PURE__ */ __name((x, y, width, height) => {
  return [
    `M${x - height / 2},${y}`,
    `L${x + width},${y}`,
    `L${x + width},${y - height}`,
    `L${x - height / 2},${y - height}`,
    `L${x},${y - height / 2}`,
    "Z"
  ].join(" ");
}, "createPolygonPathD");
var rect_left_inv_arrow = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w = bbox.width + node.padding;
  const h = bbox.height + node.padding;
  const points = [
    { x: -h / 2, y: 0 },
    { x: w, y: 0 },
    { x: w, y: -h },
    { x: -h / 2, y: -h },
    { x: 0, y: -h / 2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough15.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createPolygonPathD(0, 0, w, h);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w / 2}, ${h / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w, h, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w + h;
  node.height = h;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "rect_left_inv_arrow");

// src/rendering-util/rendering-elements/shapes/question.ts
import rough16 from "roughjs";
var createDecisionBoxPathD = /* @__PURE__ */ __name((x, y, size) => {
  return [
    `M${x + size / 2},${y}`,
    `L${x + size},${y - size / 2}`,
    `L${x + size / 2},${y - size}`,
    `L${x},${y - size / 2}`,
    "Z"
  ].join(" ");
}, "createDecisionBoxPathD");
var question = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w = bbox.width + node.padding;
  const h = bbox.height + node.padding;
  const s = w + h;
  const points = [
    { x: s / 2, y: 0 },
    { x: s, y: -s / 2 },
    { x: s / 2, y: -s },
    { x: 0, y: -s / 2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough16.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createDecisionBoxPathD(0, 0, s);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-s / 2}, ${s / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, s, s, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    log.debug(
      "APA12 Intersect called SPLIT\npoint:",
      point2,
      "\nnode:\n",
      node,
      "\nres:",
      intersect_default.polygon(node, points, point2)
    );
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "question");

// src/rendering-util/rendering-elements/shapes/hexagon.ts
import rough17 from "roughjs";
var createHexagonPathD = /* @__PURE__ */ __name((x, y, width, height, m) => {
  return [
    `M${x + m},${y}`,
    `L${x + width - m},${y}`,
    `L${x + width},${y - height / 2}`,
    `L${x + width - m},${y - height}`,
    `L${x + m},${y - height}`,
    `L${x},${y - height / 2}`,
    "Z"
  ].join(" ");
}, "createHexagonPathD");
var hexagon = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const f = 4;
  const h = bbox.height + node.padding;
  const m = h / f;
  const w = bbox.width + 2 * m + node.padding;
  const points = [
    { x: m, y: 0 },
    { x: w - m, y: 0 },
    { x: w, y: -h / 2 },
    { x: w - m, y: -h },
    { x: m, y: -h },
    { x: 0, y: -h / 2 }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough17.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createHexagonPathD(0, 0, w, h, m);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w / 2}, ${h / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w, h, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w;
  node.height = h;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "hexagon");

// src/rendering-util/rendering-elements/shapes/leanRight.ts
import rough18 from "roughjs";
var createLeanRightPathD = /* @__PURE__ */ __name((x, y, width, height) => {
  return [
    `M${x - 2 * height / 6},${y}`,
    `L${x + width - height / 6},${y}`,
    `L${x + width + 2 * height / 6},${y - height}`,
    `L${x + height / 6},${y - height}`,
    "Z"
  ].join(" ");
}, "createLeanRightPathD");
var lean_right = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w = bbox.width + node.padding;
  const h = bbox.height + node.padding;
  const points = [
    { x: -2 * h / 6, y: 0 },
    { x: w - h / 6, y: 0 },
    { x: w + 2 * h / 6, y: -h },
    { x: h / 6, y: -h }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough18.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createLeanRightPathD(0, 0, w, h);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w / 2}, ${h / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w, h, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w;
  node.height = h;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "lean_right");

// src/rendering-util/rendering-elements/shapes/leanLeft.ts
import rough19 from "roughjs";
var createLeanLeftPathD = /* @__PURE__ */ __name((x, y, width, height) => {
  return [
    `M${x + 2 * height / 6},${y}`,
    `L${x + width + height / 6},${y}`,
    `L${x + width - 2 * height / 6},${y - height}`,
    `L${x - height / 6},${y - height}`,
    "Z"
  ].join(" ");
}, "createLeanLeftPathD");
var lean_left = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w = bbox.width + node.padding;
  const h = bbox.height + node.padding;
  const points = [
    { x: 2 * h / 6, y: 0 },
    { x: w + h / 6, y: 0 },
    { x: w - 2 * h / 6, y: -h },
    { x: -h / 6, y: -h }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough19.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createLeanLeftPathD(0, 0, w, h);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w / 2}, ${h / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w, h, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w;
  node.height = h;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "lean_left");

// src/rendering-util/rendering-elements/shapes/trapezoid.ts
import rough20 from "roughjs";
var createTrapezoidPathD = /* @__PURE__ */ __name((x, y, width, height) => {
  return [
    `M${x - 2 * height / 6},${y}`,
    `L${x + width + 2 * height / 6},${y}`,
    `L${x + width - height / 6},${y - height}`,
    `L${x + height / 6},${y - height}`,
    "Z"
  ].join(" ");
}, "createTrapezoidPathD");
var trapezoid = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w = bbox.width + node.padding;
  const h = bbox.height + node.padding;
  const points = [
    { x: -2 * h / 6, y: 0 },
    { x: w + 2 * h / 6, y: 0 },
    { x: w - h / 6, y: -h },
    { x: h / 6, y: -h }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough20.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createTrapezoidPathD(0, 0, w, h);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w / 2}, ${h / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w, h, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w;
  node.height = h;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "trapezoid");

// src/rendering-util/rendering-elements/shapes/invertedTrapezoid.ts
import rough21 from "roughjs";
var createInvertedTrapezoidPathD = /* @__PURE__ */ __name((x, y, width, height) => {
  return [
    `M${x + height / 6},${y}`,
    `L${x + width - height / 6},${y}`,
    `L${x + width + 2 * height / 6},${y - height}`,
    `L${x - 2 * height / 6},${y - height}`,
    "Z"
  ].join(" ");
}, "createInvertedTrapezoidPathD");
var inv_trapezoid = /* @__PURE__ */ __name(async (parent, node) => {
  const { labelStyles, nodeStyles } = styles2String(node);
  node.labelStyle = labelStyles;
  const { shapeSvg, bbox } = await labelHelper(parent, node, getNodeClasses(node));
  const w = bbox.width + node.padding;
  const h = bbox.height + node.padding;
  const points = [
    { x: h / 6, y: 0 },
    { x: w - h / 6, y: 0 },
    { x: w + 2 * h / 6, y: -h },
    { x: -2 * h / 6, y: -h }
  ];
  let polygon;
  const { cssStyles } = node;
  if (node.look === "handDrawn") {
    const rc = rough21.svg(shapeSvg);
    const options = userNodeOverrides(node, {});
    const pathData = createInvertedTrapezoidPathD(0, 0, w, h);
    const roughNode = rc.path(pathData, options);
    polygon = shapeSvg.insert(() => roughNode, ":first-child").attr("transform", `translate(${-w / 2}, ${h / 2})`);
    if (cssStyles) {
      polygon.attr("style", cssStyles);
    }
  } else {
    polygon = insertPolygonShape(shapeSvg, w, h, points);
  }
  if (nodeStyles) {
    polygon.attr("style", nodeStyles);
  }
  node.width = w;
  node.height = h;
  updateNodeBounds(node, polygon);
  node.intersect = function(point2) {
    return intersect_default.polygon(node, points, point2);
  };
  return shapeSvg;
}, "inv_trapezoid");

// src/rendering-util/rendering-elements/shapes/labelRect.ts
var labelRect = /* @__PURE__ */ __name(async (parent, node) => {
  const { shapeSvg } = await labelHelper(parent, node, "label");
  const rect2 = shapeSvg.insert("rect", ":first-child");
  const totalWidth = 0.1;
  const totalHeight = 0.1;
  rect2.attr("width", totalWidth).attr("height", totalHeight);
  shapeSvg.attr("class", "label edgeLabel");
  updateNodeBounds(node, rect2);
  node.intersect = function(point2) {
    return intersect_default.rect(node, point2);
  };
  return shapeSvg;
}, "labelRect");

// src/rendering-util/rendering-elements/nodes.js
var shapes2 = {
  state,
  stateStart,
  stateEnd,
  fork: forkJoin,
  join: forkJoin,
  choice,
  note,
  roundedRect,
  rectWithTitle,
  squareRect: squareRect2,
  stadium,
  subroutine,
  cylinder,
  circle: circle2,
  doublecircle,
  odd: rect_left_inv_arrow,
  diamond: question,
  hexagon,
  lean_right,
  lean_left,
  trapezoid,
  inv_trapezoid,
  labelRect
};
var nodeElems = /* @__PURE__ */ new Map();
var insertNode = /* @__PURE__ */ __name(async (elem, node, dir) => {
  let newEl;
  let el;
  if (node.shape === "rect") {
    if (node.rx && node.ry) {
      node.shape = "roundedRect";
    } else {
      node.shape = "squareRect";
    }
  }
  if (node.link) {
    let target;
    if (getConfig().securityLevel === "sandbox") {
      target = "_top";
    } else if (node.linkTarget) {
      target = node.linkTarget || "_blank";
    }
    newEl = elem.insert("svg:a").attr("xlink:href", node.link).attr("target", target);
    el = await shapes2[node.shape](newEl, node, dir);
  } else {
    el = await shapes2[node.shape](elem, node, dir);
    newEl = el;
  }
  if (node.tooltip) {
    el.attr("title", node.tooltip);
  }
  nodeElems.set(node.id, newEl);
  if (node.haveCallback) {
    nodeElems.get(node.id).attr("class", nodeElems.get(node.id).attr("class") + " clickable");
  }
  return newEl;
}, "insertNode");
var setNodeElem = /* @__PURE__ */ __name((elem, node) => {
  nodeElems.set(node.id, elem);
}, "setNodeElem");
var clear3 = /* @__PURE__ */ __name(() => {
  nodeElems.clear();
}, "clear");
var positionNode = /* @__PURE__ */ __name((node) => {
  const el = nodeElems.get(node.id);
  log.trace(
    "Transforming node",
    node.diff,
    node,
    "translate(" + (node.x - node.width / 2 - 5) + ", " + node.width / 2 + ")"
  );
  const padding = 8;
  const diff = node.diff || 0;
  if (node.clusterNode) {
    el.attr(
      "transform",
      "translate(" + (node.x + diff - node.width / 2) + ", " + (node.y - node.height / 2 - padding) + ")"
    );
  } else {
    el.attr("transform", "translate(" + node.x + ", " + node.y + ")");
  }
  return diff;
}, "positionNode");

export {
  insertCluster,
  clear,
  clear2,
  insertEdgeLabel,
  positionEdgeLabel,
  insertEdge,
  markers_default,
  labelHelper,
  updateNodeBounds,
  insertNode,
  setNodeElem,
  clear3,
  positionNode
};
