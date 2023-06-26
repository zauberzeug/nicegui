import { d as db, p as parser } from "./flowDb-88762a1f.js";
import { select, curveLinear, line } from "d3";
import { a as insertMarkers, e as insertNode, f as insertEdgeLabel } from "./edges-65da65dc.js";
import { addHtmlLabel } from "dagre-d3-es/src/dagre-js/label/add-html-label.js";
import { l as log, g as getConfig, j as evaluate, d as common } from "./config-389b86ff.js";
import { s as setupGraphViewbox } from "./setupGraphViewbox-e35e4124.js";
import { m as getStylesFromArray, n as interpolateToCurve } from "./utils-d5eeff82.js";
import ELK from "elkjs/lib/elk.bundled.js";
import "./mermaidAPI-0716c7c2.js";
import "stylis";
import "./errorRenderer-d05351b9.js";
import "dompurify";
import "lodash-es/isEmpty.js";
import "./commonDb-2ace122b.js";
import "./svgDraw-6a237a99.js";
import "dayjs";
import "khroma";
import "@braintree/sanitize-url";
import "lodash-es/memoize.js";
const findCommonAncestor = (id1, id2, treeData) => {
  const { parentById } = treeData;
  const visited = /* @__PURE__ */ new Set();
  let currentId = id1;
  while (currentId) {
    visited.add(currentId);
    if (currentId === id2) {
      return currentId;
    }
    currentId = parentById[currentId];
  }
  currentId = id2;
  while (currentId) {
    if (visited.has(currentId)) {
      return currentId;
    }
    currentId = parentById[currentId];
  }
  return "root";
};
const elk = new ELK();
const portPos = {};
const conf = {};
let nodeDb = {};
const addVertices = function(vert, svgId, root, doc, diagObj, parentLookupDb, graph) {
  const svg = root.select(`[id="${svgId}"]`);
  const nodes = svg.insert("g").attr("class", "nodes");
  const keys = Object.keys(vert);
  keys.forEach(function(id) {
    const vertex = vert[id];
    let classStr = "default";
    if (vertex.classes.length > 0) {
      classStr = vertex.classes.join(" ");
    }
    const styles2 = getStylesFromArray(vertex.styles);
    let vertexText = vertex.text !== void 0 ? vertex.text : vertex.id;
    let vertexNode;
    const labelData = { width: 0, height: 0 };
    if (evaluate(getConfig().flowchart.htmlLabels)) {
      const node2 = {
        label: vertexText.replace(
          /fa[blrs]?:fa-[\w-]+/g,
          (s) => `<i class='${s.replace(":", " ")}'></i>`
        )
      };
      vertexNode = addHtmlLabel(svg, node2).node();
      const bbox = vertexNode.getBBox();
      labelData.width = bbox.width;
      labelData.height = bbox.height;
      labelData.labelNode = vertexNode;
      vertexNode.parentNode.removeChild(vertexNode);
    } else {
      const svgLabel = doc.createElementNS("http://www.w3.org/2000/svg", "text");
      svgLabel.setAttribute("style", styles2.labelStyle.replace("color:", "fill:"));
      const rows = vertexText.split(common.lineBreakRegex);
      for (const row of rows) {
        const tspan = doc.createElementNS("http://www.w3.org/2000/svg", "tspan");
        tspan.setAttributeNS("http://www.w3.org/XML/1998/namespace", "xml:space", "preserve");
        tspan.setAttribute("dy", "1em");
        tspan.setAttribute("x", "1");
        tspan.textContent = row;
        svgLabel.appendChild(tspan);
      }
      vertexNode = svgLabel;
      const bbox = vertexNode.getBBox();
      labelData.width = bbox.width;
      labelData.height = bbox.height;
      labelData.labelNode = vertexNode;
    }
    const ports = [
      {
        id: vertex.id + "-west",
        layoutOptions: {
          "port.side": "WEST"
        }
      },
      {
        id: vertex.id + "-east",
        layoutOptions: {
          "port.side": "EAST"
        }
      },
      {
        id: vertex.id + "-south",
        layoutOptions: {
          "port.side": "SOUTH"
        }
      },
      {
        id: vertex.id + "-north",
        layoutOptions: {
          "port.side": "NORTH"
        }
      }
    ];
    let radious = 0;
    let _shape = "";
    let layoutOptions = {};
    switch (vertex.type) {
      case "round":
        radious = 5;
        _shape = "rect";
        break;
      case "square":
        _shape = "rect";
        break;
      case "diamond":
        _shape = "question";
        layoutOptions = {
          portConstraints: "FIXED_SIDE"
        };
        break;
      case "hexagon":
        _shape = "hexagon";
        break;
      case "odd":
        _shape = "rect_left_inv_arrow";
        break;
      case "lean_right":
        _shape = "lean_right";
        break;
      case "lean_left":
        _shape = "lean_left";
        break;
      case "trapezoid":
        _shape = "trapezoid";
        break;
      case "inv_trapezoid":
        _shape = "inv_trapezoid";
        break;
      case "odd_right":
        _shape = "rect_left_inv_arrow";
        break;
      case "circle":
        _shape = "circle";
        break;
      case "ellipse":
        _shape = "ellipse";
        break;
      case "stadium":
        _shape = "stadium";
        break;
      case "subroutine":
        _shape = "subroutine";
        break;
      case "cylinder":
        _shape = "cylinder";
        break;
      case "group":
        _shape = "rect";
        break;
      case "doublecircle":
        _shape = "doublecircle";
        break;
      default:
        _shape = "rect";
    }
    const node = {
      labelStyle: styles2.labelStyle,
      shape: _shape,
      labelText: vertexText,
      rx: radious,
      ry: radious,
      class: classStr,
      style: styles2.style,
      id: vertex.id,
      link: vertex.link,
      linkTarget: vertex.linkTarget,
      tooltip: diagObj.db.getTooltip(vertex.id) || "",
      domId: diagObj.db.lookUpDomId(vertex.id),
      haveCallback: vertex.haveCallback,
      width: vertex.type === "group" ? 500 : void 0,
      dir: vertex.dir,
      type: vertex.type,
      props: vertex.props,
      padding: getConfig().flowchart.padding
    };
    let boundingBox;
    let nodeEl;
    if (node.type !== "group") {
      nodeEl = insertNode(nodes, node, vertex.dir);
      boundingBox = nodeEl.node().getBBox();
    }
    const data = {
      id: vertex.id,
      ports: vertex.type === "diamond" ? ports : [],
      // labelStyle: styles.labelStyle,
      // shape: _shape,
      layoutOptions,
      labelText: vertexText,
      labelData,
      // labels: [{ text: vertexText }],
      // rx: radius,
      // ry: radius,
      // class: classStr,
      // style: styles.style,
      // link: vertex.link,
      // linkTarget: vertex.linkTarget,
      // tooltip: diagObj.db.getTooltip(vertex.id) || '',
      domId: diagObj.db.lookUpDomId(vertex.id),
      // haveCallback: vertex.haveCallback,
      width: boundingBox == null ? void 0 : boundingBox.width,
      height: boundingBox == null ? void 0 : boundingBox.height,
      // dir: vertex.dir,
      type: vertex.type,
      // props: vertex.props,
      // padding: getConfig().flowchart.padding,
      // boundingBox,
      el: nodeEl,
      parent: parentLookupDb.parentById[vertex.id]
    };
    nodeDb[node.id] = data;
  });
  return graph;
};
const getNextPosition = (position, edgeDirection, graphDirection) => {
  const portPos2 = {
    TB: {
      in: {
        north: "north"
      },
      out: {
        south: "west",
        west: "east",
        east: "south"
      }
    },
    LR: {
      in: {
        west: "west"
      },
      out: {
        east: "south",
        south: "north",
        north: "east"
      }
    },
    RL: {
      in: {
        east: "east"
      },
      out: {
        west: "north",
        north: "south",
        south: "west"
      }
    },
    BT: {
      in: {
        south: "south"
      },
      out: {
        north: "east",
        east: "west",
        west: "north"
      }
    }
  };
  portPos2.TD = portPos2.TB;
  log.info("abc88", graphDirection, edgeDirection, position);
  return portPos2[graphDirection][edgeDirection][position];
};
const getNextPort = (node, edgeDirection, graphDirection) => {
  log.info("getNextPort abc88", { node, edgeDirection, graphDirection });
  if (!portPos[node]) {
    switch (graphDirection) {
      case "TB":
      case "TD":
        portPos[node] = {
          inPosition: "north",
          outPosition: "south"
        };
        break;
      case "BT":
        portPos[node] = {
          inPosition: "south",
          outPosition: "north"
        };
        break;
      case "RL":
        portPos[node] = {
          inPosition: "east",
          outPosition: "west"
        };
        break;
      case "LR":
        portPos[node] = {
          inPosition: "west",
          outPosition: "east"
        };
        break;
    }
  }
  const result = edgeDirection === "in" ? portPos[node].inPosition : portPos[node].outPosition;
  if (edgeDirection === "in") {
    portPos[node].inPosition = getNextPosition(
      portPos[node].inPosition,
      edgeDirection,
      graphDirection
    );
  } else {
    portPos[node].outPosition = getNextPosition(
      portPos[node].outPosition,
      edgeDirection,
      graphDirection
    );
  }
  return result;
};
const getEdgeStartEndPoint = (edge, dir) => {
  let source = edge.start;
  let target = edge.end;
  const sourceId = source;
  const targetId = target;
  const startNode = nodeDb[source];
  const endNode = nodeDb[target];
  if (!startNode || !endNode) {
    return { source, target };
  }
  if (startNode.type === "diamond") {
    source = `${source}-${getNextPort(source, "out", dir)}`;
  }
  if (endNode.type === "diamond") {
    target = `${target}-${getNextPort(target, "in", dir)}`;
  }
  return { source, target, sourceId, targetId };
};
const addEdges = function(edges, diagObj, graph, svg) {
  log.info("abc78 edges = ", edges);
  const labelsEl = svg.insert("g").attr("class", "edgeLabels");
  let linkIdCnt = {};
  let dir = diagObj.db.getDirection();
  let defaultStyle;
  let defaultLabelStyle;
  if (edges.defaultStyle !== void 0) {
    const defaultStyles = getStylesFromArray(edges.defaultStyle);
    defaultStyle = defaultStyles.style;
    defaultLabelStyle = defaultStyles.labelStyle;
  }
  edges.forEach(function(edge) {
    var linkIdBase = "L-" + edge.start + "-" + edge.end;
    if (linkIdCnt[linkIdBase] === void 0) {
      linkIdCnt[linkIdBase] = 0;
      log.info("abc78 new entry", linkIdBase, linkIdCnt[linkIdBase]);
    } else {
      linkIdCnt[linkIdBase]++;
      log.info("abc78 new entry", linkIdBase, linkIdCnt[linkIdBase]);
    }
    let linkId = linkIdBase + "-" + linkIdCnt[linkIdBase];
    log.info("abc78 new link id to be used is", linkIdBase, linkId, linkIdCnt[linkIdBase]);
    var linkNameStart = "LS-" + edge.start;
    var linkNameEnd = "LE-" + edge.end;
    const edgeData = { style: "", labelStyle: "" };
    edgeData.minlen = edge.length || 1;
    if (edge.type === "arrow_open") {
      edgeData.arrowhead = "none";
    } else {
      edgeData.arrowhead = "normal";
    }
    edgeData.arrowTypeStart = "arrow_open";
    edgeData.arrowTypeEnd = "arrow_open";
    switch (edge.type) {
      case "double_arrow_cross":
        edgeData.arrowTypeStart = "arrow_cross";
      case "arrow_cross":
        edgeData.arrowTypeEnd = "arrow_cross";
        break;
      case "double_arrow_point":
        edgeData.arrowTypeStart = "arrow_point";
      case "arrow_point":
        edgeData.arrowTypeEnd = "arrow_point";
        break;
      case "double_arrow_circle":
        edgeData.arrowTypeStart = "arrow_circle";
      case "arrow_circle":
        edgeData.arrowTypeEnd = "arrow_circle";
        break;
    }
    let style = "";
    let labelStyle = "";
    switch (edge.stroke) {
      case "normal":
        style = "fill:none;";
        if (defaultStyle !== void 0) {
          style = defaultStyle;
        }
        if (defaultLabelStyle !== void 0) {
          labelStyle = defaultLabelStyle;
        }
        edgeData.thickness = "normal";
        edgeData.pattern = "solid";
        break;
      case "dotted":
        edgeData.thickness = "normal";
        edgeData.pattern = "dotted";
        edgeData.style = "fill:none;stroke-width:2px;stroke-dasharray:3;";
        break;
      case "thick":
        edgeData.thickness = "thick";
        edgeData.pattern = "solid";
        edgeData.style = "stroke-width: 3.5px;fill:none;";
        break;
    }
    if (edge.style !== void 0) {
      const styles2 = getStylesFromArray(edge.style);
      style = styles2.style;
      labelStyle = styles2.labelStyle;
    }
    edgeData.style = edgeData.style += style;
    edgeData.labelStyle = edgeData.labelStyle += labelStyle;
    if (edge.interpolate !== void 0) {
      edgeData.curve = interpolateToCurve(edge.interpolate, curveLinear);
    } else if (edges.defaultInterpolate !== void 0) {
      edgeData.curve = interpolateToCurve(edges.defaultInterpolate, curveLinear);
    } else {
      edgeData.curve = interpolateToCurve(conf.curve, curveLinear);
    }
    if (edge.text === void 0) {
      if (edge.style !== void 0) {
        edgeData.arrowheadStyle = "fill: #333";
      }
    } else {
      edgeData.arrowheadStyle = "fill: #333";
      edgeData.labelpos = "c";
    }
    edgeData.labelType = "text";
    edgeData.label = edge.text.replace(common.lineBreakRegex, "\n");
    if (edge.style === void 0) {
      edgeData.style = edgeData.style || "stroke: #333; stroke-width: 1.5px;fill:none;";
    }
    edgeData.labelStyle = edgeData.labelStyle.replace("color:", "fill:");
    edgeData.id = linkId;
    edgeData.classes = "flowchart-link " + linkNameStart + " " + linkNameEnd;
    const labelEl = insertEdgeLabel(labelsEl, edgeData);
    const { source, target, sourceId, targetId } = getEdgeStartEndPoint(edge, dir);
    log.debug("abc78 source and target", source, target);
    graph.edges.push({
      id: "e" + edge.start + edge.end,
      sources: [source],
      targets: [target],
      sourceId,
      targetId,
      labelEl,
      labels: [
        {
          width: edgeData.width,
          height: edgeData.height,
          orgWidth: edgeData.width,
          orgHeight: edgeData.height,
          text: edgeData.label,
          layoutOptions: {
            "edgeLabels.inline": "true",
            "edgeLabels.placement": "CENTER"
          }
        }
      ],
      edgeData
    });
  });
  return graph;
};
const addMarkersToEdge = function(svgPath, edgeData, diagramType, arrowMarkerAbsolute) {
  let url = "";
  if (arrowMarkerAbsolute) {
    url = window.location.protocol + "//" + window.location.host + window.location.pathname + window.location.search;
    url = url.replace(/\(/g, "\\(");
    url = url.replace(/\)/g, "\\)");
  }
  switch (edgeData.arrowTypeStart) {
    case "arrow_cross":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-crossStart)");
      break;
    case "arrow_point":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-pointStart)");
      break;
    case "arrow_barb":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-barbStart)");
      break;
    case "arrow_circle":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-circleStart)");
      break;
    case "aggregation":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-aggregationStart)");
      break;
    case "extension":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-extensionStart)");
      break;
    case "composition":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-compositionStart)");
      break;
    case "dependency":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-dependencyStart)");
      break;
    case "lollipop":
      svgPath.attr("marker-start", "url(" + url + "#" + diagramType + "-lollipopStart)");
      break;
  }
  switch (edgeData.arrowTypeEnd) {
    case "arrow_cross":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-crossEnd)");
      break;
    case "arrow_point":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-pointEnd)");
      break;
    case "arrow_barb":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-barbEnd)");
      break;
    case "arrow_circle":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-circleEnd)");
      break;
    case "aggregation":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-aggregationEnd)");
      break;
    case "extension":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-extensionEnd)");
      break;
    case "composition":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-compositionEnd)");
      break;
    case "dependency":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-dependencyEnd)");
      break;
    case "lollipop":
      svgPath.attr("marker-end", "url(" + url + "#" + diagramType + "-lollipopEnd)");
      break;
  }
};
const getClasses = function(text, diagObj) {
  log.info("Extracting classes");
  diagObj.db.clear("ver-2");
  try {
    diagObj.parse(text);
    return diagObj.db.getClasses();
  } catch (e) {
    return {};
  }
};
const addSubGraphs = function(db2) {
  const parentLookupDb = { parentById: {}, childrenById: {} };
  const subgraphs = db2.getSubGraphs();
  log.info("Subgraphs - ", subgraphs);
  subgraphs.forEach(function(subgraph) {
    subgraph.nodes.forEach(function(node) {
      parentLookupDb.parentById[node] = subgraph.id;
      if (parentLookupDb.childrenById[subgraph.id] === void 0) {
        parentLookupDb.childrenById[subgraph.id] = [];
      }
      parentLookupDb.childrenById[subgraph.id].push(node);
    });
  });
  subgraphs.forEach(function(subgraph) {
    ({ id: subgraph.id });
    if (parentLookupDb.parentById[subgraph.id] !== void 0) {
      parentLookupDb.parentById[subgraph.id];
    }
  });
  return parentLookupDb;
};
const calcOffset = function(src, dest, parentLookupDb) {
  const ancestor = findCommonAncestor(src, dest, parentLookupDb);
  if (ancestor === void 0 || ancestor === "root") {
    return { x: 0, y: 0 };
  }
  const ancestorOffset = nodeDb[ancestor].offset;
  return { x: ancestorOffset.posX, y: ancestorOffset.posY };
};
const insertEdge = function(edgesEl, edge, edgeData, diagObj, parentLookupDb) {
  const offset = calcOffset(edge.sourceId, edge.targetId, parentLookupDb);
  const src = edge.sections[0].startPoint;
  const dest = edge.sections[0].endPoint;
  const segments = edge.sections[0].bendPoints ? edge.sections[0].bendPoints : [];
  const segPoints = segments.map((segment) => [segment.x + offset.x, segment.y + offset.y]);
  const points = [
    [src.x + offset.x, src.y + offset.y],
    ...segPoints,
    [dest.x + offset.x, dest.y + offset.y]
  ];
  const curve = line().curve(curveLinear);
  const edgePath = edgesEl.insert("path").attr("d", curve(points)).attr("class", "path").attr("fill", "none");
  const edgeG = edgesEl.insert("g").attr("class", "edgeLabel");
  const edgeWithLabel = select(edgeG.node().appendChild(edge.labelEl));
  const box = edgeWithLabel.node().firstChild.getBoundingClientRect();
  edgeWithLabel.attr("width", box.width);
  edgeWithLabel.attr("height", box.height);
  edgeG.attr(
    "transform",
    `translate(${edge.labels[0].x + offset.x}, ${edge.labels[0].y + offset.y})`
  );
  addMarkersToEdge(edgePath, edgeData, diagObj.type, diagObj.arrowMarkerAbsolute);
};
const insertChildren = (nodeArray, parentLookupDb) => {
  nodeArray.forEach((node) => {
    if (!node.children) {
      node.children = [];
    }
    const childIds = parentLookupDb.childrenById[node.id];
    if (childIds) {
      childIds.forEach((childId) => {
        node.children.push(nodeDb[childId]);
      });
    }
    insertChildren(node.children, parentLookupDb);
  });
};
const draw = async function(text, id, _version, diagObj) {
  var _a;
  diagObj.db.clear();
  nodeDb = {};
  diagObj.db.setGen("gen-2");
  diagObj.parser.parse(text);
  const renderEl = select("body").append("div").attr("style", "height:400px").attr("id", "cy");
  let graph = {
    id: "root",
    layoutOptions: {
      "elk.hierarchyHandling": "INCLUDE_CHILDREN",
      "org.eclipse.elk.padding": "[top=100, left=100, bottom=110, right=110]",
      "elk.layered.spacing.edgeNodeBetweenLayers": "30",
      // 'elk.layered.mergeEdges': 'true',
      "elk.direction": "DOWN"
      // 'elk.ports.sameLayerEdges': true,
      // 'nodePlacement.strategy': 'SIMPLE',
    },
    children: [],
    edges: []
  };
  log.info("Drawing flowchart using v3 renderer", elk);
  let dir = diagObj.db.getDirection();
  switch (dir) {
    case "BT":
      graph.layoutOptions["elk.direction"] = "UP";
      break;
    case "TB":
      graph.layoutOptions["elk.direction"] = "DOWN";
      break;
    case "LR":
      graph.layoutOptions["elk.direction"] = "RIGHT";
      break;
    case "RL":
      graph.layoutOptions["elk.direction"] = "LEFT";
      break;
  }
  const { securityLevel, flowchart: conf2 } = getConfig();
  let sandboxElement;
  if (securityLevel === "sandbox") {
    sandboxElement = select("#i" + id);
  }
  const root = securityLevel === "sandbox" ? select(sandboxElement.nodes()[0].contentDocument.body) : select("body");
  const doc = securityLevel === "sandbox" ? sandboxElement.nodes()[0].contentDocument : document;
  const svg = root.select(`[id="${id}"]`);
  const markers = ["point", "circle", "cross"];
  insertMarkers(svg, markers, diagObj.type, diagObj.arrowMarkerAbsolute);
  const vert = diagObj.db.getVertices();
  let subG;
  const subGraphs = diagObj.db.getSubGraphs();
  log.info("Subgraphs - ", subGraphs);
  for (let i = subGraphs.length - 1; i >= 0; i--) {
    subG = subGraphs[i];
    diagObj.db.addVertex(subG.id, subG.title, "group", void 0, subG.classes, subG.dir);
  }
  const subGraphsEl = svg.insert("g").attr("class", "subgraphs");
  const parentLookupDb = addSubGraphs(diagObj.db);
  graph = addVertices(vert, id, root, doc, diagObj, parentLookupDb, graph);
  const edgesEl = svg.insert("g").attr("class", "edges edgePath");
  const edges = diagObj.db.getEdges();
  graph = addEdges(edges, diagObj, graph, svg);
  const nodes = Object.keys(nodeDb);
  nodes.forEach((nodeId) => {
    const node = nodeDb[nodeId];
    if (!node.parent) {
      graph.children.push(node);
    }
    if (parentLookupDb.childrenById[nodeId] !== void 0) {
      node.labels = [
        {
          text: node.labelText,
          layoutOptions: {
            "nodeLabels.placement": "[H_CENTER, V_TOP, INSIDE]"
          },
          width: node.labelData.width,
          height: node.labelData.height
        }
      ];
      delete node.x;
      delete node.y;
      delete node.width;
      delete node.height;
    }
  });
  insertChildren(graph.children, parentLookupDb);
  log.info("after layout", JSON.stringify(graph, null, 2));
  const g = await elk.layout(graph);
  drawNodes(0, 0, g.children, svg, subGraphsEl, diagObj, 0);
  log.info("after layout", g);
  (_a = g.edges) == null ? void 0 : _a.map((edge) => {
    insertEdge(edgesEl, edge, edge.edgeData, diagObj, parentLookupDb);
  });
  setupGraphViewbox({}, svg, conf2.diagramPadding, conf2.useMaxWidth);
  renderEl.remove();
};
const drawNodes = (relX, relY, nodeArray, svg, subgraphsEl, diagObj, depth) => {
  nodeArray.forEach(function(node) {
    if (node) {
      nodeDb[node.id].offset = {
        posX: node.x + relX,
        posY: node.y + relY,
        x: relX,
        y: relY,
        depth,
        width: node.width,
        height: node.height
      };
      if (node.type === "group") {
        const subgraphEl = subgraphsEl.insert("g").attr("class", "subgraph");
        subgraphEl.insert("rect").attr("class", "subgraph subgraph-lvl-" + depth % 5 + " node").attr("x", node.x + relX).attr("y", node.y + relY).attr("width", node.width).attr("height", node.height);
        const label = subgraphEl.insert("g").attr("class", "label");
        label.attr(
          "transform",
          `translate(${node.labels[0].x + relX + node.x}, ${node.labels[0].y + relY + node.y})`
        );
        label.node().appendChild(node.labelData.labelNode);
        log.info("Id (UGH)= ", node.type, node.labels);
      } else {
        log.info("Id (UGH)= ", node.id);
        node.el.attr(
          "transform",
          `translate(${node.x + relX + node.width / 2}, ${node.y + relY + node.height / 2})`
        );
      }
    }
  });
  nodeArray.forEach(function(node) {
    if (node && node.type === "group") {
      drawNodes(relX + node.x, relY + node.y, node.children, svg, subgraphsEl, diagObj, depth + 1);
    }
  });
};
const renderer = {
  getClasses,
  draw
};
const genSections = (options) => {
  let sections = "";
  for (let i = 0; i < 5; i++) {
    sections += `
      .subgraph-lvl-${i} {
        fill: ${options[`surface${i}`]};
        stroke: ${options[`surfacePeer${i}`]};
      }
    `;
  }
  return sections;
};
const getStyles = (options) => `.label {
    font-family: ${options.fontFamily};
    color: ${options.nodeTextColor || options.textColor};
  }
  .cluster-label text {
    fill: ${options.titleColor};
  }
  .cluster-label span {
    color: ${options.titleColor};
  }

  .label text,span {
    fill: ${options.nodeTextColor || options.textColor};
    color: ${options.nodeTextColor || options.textColor};
  }

  .node rect,
  .node circle,
  .node ellipse,
  .node polygon,
  .node path {
    fill: ${options.mainBkg};
    stroke: ${options.nodeBorder};
    stroke-width: 1px;
  }

  .node .label {
    text-align: center;
  }
  .node.clickable {
    cursor: pointer;
  }

  .arrowheadPath {
    fill: ${options.arrowheadColor};
  }

  .edgePath .path {
    stroke: ${options.lineColor};
    stroke-width: 2.0px;
  }

  .flowchart-link {
    stroke: ${options.lineColor};
    fill: none;
  }

  .edgeLabel {
    background-color: ${options.edgeLabelBackground};
    rect {
      opacity: 0.5;
      background-color: ${options.edgeLabelBackground};
      fill: ${options.edgeLabelBackground};
    }
    text-align: center;
  }

  .cluster rect {
    fill: ${options.clusterBkg};
    stroke: ${options.clusterBorder};
    stroke-width: 1px;
  }

  .cluster text {
    fill: ${options.titleColor};
  }

  .cluster span {
    color: ${options.titleColor};
  }
  /* .cluster div {
    color: ${options.titleColor};
  } */

  div.mermaidTooltip {
    position: absolute;
    text-align: center;
    max-width: 200px;
    padding: 2px;
    font-family: ${options.fontFamily};
    font-size: 12px;
    background: ${options.tertiaryColor};
    border: 1px solid ${options.border2};
    border-radius: 2px;
    pointer-events: none;
    z-index: 100;
  }

  .flowchartTitleText {
    text-anchor: middle;
    font-size: 18px;
    fill: ${options.textColor};
  }
  .subgraph {
    stroke-width:2;
    rx:3;
  }
  // .subgraph-lvl-1 {
  //   fill:#ccc;
  //   // stroke:black;
  // }
  ${genSections(options)}
`;
const styles = getStyles;
const diagram = {
  db,
  renderer,
  parser,
  styles
};
export {
  diagram
};
//# sourceMappingURL=flowchart-elk-definition-c9fc5e04.js.map
