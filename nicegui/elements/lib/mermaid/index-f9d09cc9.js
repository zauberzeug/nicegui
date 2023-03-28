import { layout } from "dagre-d3-es/src/dagre/index.js";
import * as graphlibJson from "dagre-d3-es/src/graphlib/json.js";
import { c as createLabel, i as intersectRect, a as insertMarkers, b as clear$2, d as clear$3, u as updateNodeBounds, s as setNodeElem, e as insertNode, f as insertEdgeLabel, p as positionNode, g as insertEdge, h as positionEdgeLabel } from "./edges-65da65dc.js";
import { l as log, j as evaluate, g as getConfig } from "./config-389b86ff.js";
import * as graphlib from "dagre-d3-es/src/graphlib/index.js";
import { select } from "d3";
let clusterDb = {};
let descendants = {};
let parents = {};
const clear$1 = () => {
  descendants = {};
  parents = {};
  clusterDb = {};
};
const isDescendant = (id, ancenstorId) => {
  log.trace("In isDecendant", ancenstorId, " ", id, " = ", descendants[ancenstorId].includes(id));
  if (descendants[ancenstorId].includes(id)) {
    return true;
  }
  return false;
};
const edgeInCluster = (edge, clusterId) => {
  log.info("Decendants of ", clusterId, " is ", descendants[clusterId]);
  log.info("Edge is ", edge);
  if (edge.v === clusterId) {
    return false;
  }
  if (edge.w === clusterId) {
    return false;
  }
  if (!descendants[clusterId]) {
    log.debug("Tilt, ", clusterId, ",not in decendants");
    return false;
  }
  return descendants[clusterId].includes(edge.v) || isDescendant(edge.v, clusterId) || isDescendant(edge.w, clusterId) || descendants[clusterId].includes(edge.w);
};
const copy = (clusterId, graph, newGraph, rootId) => {
  log.warn(
    "Copying children of ",
    clusterId,
    "root",
    rootId,
    "data",
    graph.node(clusterId),
    rootId
  );
  const nodes = graph.children(clusterId) || [];
  if (clusterId !== rootId) {
    nodes.push(clusterId);
  }
  log.warn("Copying (nodes) clusterId", clusterId, "nodes", nodes);
  nodes.forEach((node) => {
    if (graph.children(node).length > 0) {
      copy(node, graph, newGraph, rootId);
    } else {
      const data = graph.node(node);
      log.info("cp ", node, " to ", rootId, " with parent ", clusterId);
      newGraph.setNode(node, data);
      if (rootId !== graph.parent(node)) {
        log.warn("Setting parent", node, graph.parent(node));
        newGraph.setParent(node, graph.parent(node));
      }
      if (clusterId !== rootId && node !== clusterId) {
        log.debug("Setting parent", node, clusterId);
        newGraph.setParent(node, clusterId);
      } else {
        log.info("In copy ", clusterId, "root", rootId, "data", graph.node(clusterId), rootId);
        log.debug(
          "Not Setting parent for node=",
          node,
          "cluster!==rootId",
          clusterId !== rootId,
          "node!==clusterId",
          node !== clusterId
        );
      }
      const edges = graph.edges(node);
      log.debug("Copying Edges", edges);
      edges.forEach((edge) => {
        log.info("Edge", edge);
        const data2 = graph.edge(edge.v, edge.w, edge.name);
        log.info("Edge data", data2, rootId);
        try {
          if (edgeInCluster(edge, rootId)) {
            log.info("Copying as ", edge.v, edge.w, data2, edge.name);
            newGraph.setEdge(edge.v, edge.w, data2, edge.name);
            log.info("newGraph edges ", newGraph.edges(), newGraph.edge(newGraph.edges()[0]));
          } else {
            log.info(
              "Skipping copy of edge ",
              edge.v,
              "-->",
              edge.w,
              " rootId: ",
              rootId,
              " clusterId:",
              clusterId
            );
          }
        } catch (e) {
          log.error(e);
        }
      });
    }
    log.debug("Removing node", node);
    graph.removeNode(node);
  });
};
const extractDescendants = (id, graph) => {
  const children = graph.children(id);
  let res = [...children];
  for (const child of children) {
    parents[child] = id;
    res = [...res, ...extractDescendants(child, graph)];
  }
  return res;
};
const findNonClusterChild = (id, graph) => {
  log.trace("Searching", id);
  const children = graph.children(id);
  log.trace("Searching children of id ", id, children);
  if (children.length < 1) {
    log.trace("This is a valid node", id);
    return id;
  }
  for (const child of children) {
    const _id = findNonClusterChild(child, graph);
    if (_id) {
      log.trace("Found replacement for", id, " => ", _id);
      return _id;
    }
  }
};
const getAnchorId = (id) => {
  if (!clusterDb[id]) {
    return id;
  }
  if (!clusterDb[id].externalConnections) {
    return id;
  }
  if (clusterDb[id]) {
    return clusterDb[id].id;
  }
  return id;
};
const adjustClustersAndEdges = (graph, depth) => {
  if (!graph || depth > 10) {
    log.debug("Opting out, no graph ");
    return;
  } else {
    log.debug("Opting in, graph ");
  }
  graph.nodes().forEach(function(id) {
    const children = graph.children(id);
    if (children.length > 0) {
      log.warn(
        "Cluster identified",
        id,
        " Replacement id in edges: ",
        findNonClusterChild(id, graph)
      );
      descendants[id] = extractDescendants(id, graph);
      clusterDb[id] = { id: findNonClusterChild(id, graph), clusterData: graph.node(id) };
    }
  });
  graph.nodes().forEach(function(id) {
    const children = graph.children(id);
    const edges = graph.edges();
    if (children.length > 0) {
      log.debug("Cluster identified", id, descendants);
      edges.forEach((edge) => {
        if (edge.v !== id && edge.w !== id) {
          const d1 = isDescendant(edge.v, id);
          const d2 = isDescendant(edge.w, id);
          if (d1 ^ d2) {
            log.warn("Edge: ", edge, " leaves cluster ", id);
            log.warn("Decendants of XXX ", id, ": ", descendants[id]);
            clusterDb[id].externalConnections = true;
          }
        }
      });
    } else {
      log.debug("Not a cluster ", id, descendants);
    }
  });
  graph.edges().forEach(function(e) {
    const edge = graph.edge(e);
    log.warn("Edge " + e.v + " -> " + e.w + ": " + JSON.stringify(e));
    log.warn("Edge " + e.v + " -> " + e.w + ": " + JSON.stringify(graph.edge(e)));
    let v = e.v;
    let w = e.w;
    log.warn(
      "Fix XXX",
      clusterDb,
      "ids:",
      e.v,
      e.w,
      "Translating: ",
      clusterDb[e.v],
      " --- ",
      clusterDb[e.w]
    );
    if (clusterDb[e.v] && clusterDb[e.w] && clusterDb[e.v] === clusterDb[e.w]) {
      log.warn("Fixing and trixing link to self - removing XXX", e.v, e.w, e.name);
      log.warn("Fixing and trixing - removing XXX", e.v, e.w, e.name);
      v = getAnchorId(e.v);
      w = getAnchorId(e.w);
      graph.removeEdge(e.v, e.w, e.name);
      const specialId = e.w + "---" + e.v;
      graph.setNode(specialId, {
        domId: specialId,
        id: specialId,
        labelStyle: "",
        labelText: edge.label,
        padding: 0,
        shape: "labelRect",
        style: ""
      });
      const edge1 = JSON.parse(JSON.stringify(edge));
      const edge2 = JSON.parse(JSON.stringify(edge));
      edge1.label = "";
      edge1.arrowTypeEnd = "none";
      edge2.label = "";
      edge1.fromCluster = e.v;
      edge2.toCluster = e.v;
      graph.setEdge(v, specialId, edge1, e.name + "-cyclic-special");
      graph.setEdge(specialId, w, edge2, e.name + "-cyclic-special");
    } else if (clusterDb[e.v] || clusterDb[e.w]) {
      log.warn("Fixing and trixing - removing XXX", e.v, e.w, e.name);
      v = getAnchorId(e.v);
      w = getAnchorId(e.w);
      graph.removeEdge(e.v, e.w, e.name);
      if (v !== e.v) {
        edge.fromCluster = e.v;
      }
      if (w !== e.w) {
        edge.toCluster = e.w;
      }
      log.warn("Fix Replacing with XXX", v, w, e.name);
      graph.setEdge(v, w, edge, e.name);
    }
  });
  log.warn("Adjusted Graph", graphlibJson.write(graph));
  extractor(graph, 0);
  log.trace(clusterDb);
};
const extractor = (graph, depth) => {
  log.warn("extractor - ", depth, graphlibJson.write(graph), graph.children("D"));
  if (depth > 10) {
    log.error("Bailing out");
    return;
  }
  let nodes = graph.nodes();
  let hasChildren = false;
  for (const node of nodes) {
    const children = graph.children(node);
    hasChildren = hasChildren || children.length > 0;
  }
  if (!hasChildren) {
    log.debug("Done, no node has children", graph.nodes());
    return;
  }
  log.debug("Nodes = ", nodes, depth);
  for (const node of nodes) {
    log.debug(
      "Extracting node",
      node,
      clusterDb,
      clusterDb[node] && !clusterDb[node].externalConnections,
      !graph.parent(node),
      graph.node(node),
      graph.children("D"),
      " Depth ",
      depth
    );
    if (!clusterDb[node]) {
      log.debug("Not a cluster", node, depth);
    } else if (!clusterDb[node].externalConnections && // !graph.parent(node) &&
    graph.children(node) && graph.children(node).length > 0) {
      log.warn(
        "Cluster without external connections, without a parent and with children",
        node,
        depth
      );
      const graphSettings = graph.graph();
      let dir = graphSettings.rankdir === "TB" ? "LR" : "TB";
      if (clusterDb[node] && clusterDb[node].clusterData && clusterDb[node].clusterData.dir) {
        dir = clusterDb[node].clusterData.dir;
        log.warn("Fixing dir", clusterDb[node].clusterData.dir, dir);
      }
      const clusterGraph = new graphlib.Graph({
        multigraph: true,
        compound: true
      }).setGraph({
        rankdir: dir,
        // Todo: set proper spacing
        nodesep: 50,
        ranksep: 50,
        marginx: 8,
        marginy: 8
      }).setDefaultEdgeLabel(function() {
        return {};
      });
      log.warn("Old graph before copy", graphlibJson.write(graph));
      copy(node, graph, clusterGraph, node);
      graph.setNode(node, {
        clusterNode: true,
        id: node,
        clusterData: clusterDb[node].clusterData,
        labelText: clusterDb[node].labelText,
        graph: clusterGraph
      });
      log.warn("New graph after copy node: (", node, ")", graphlibJson.write(clusterGraph));
      log.debug("Old graph after copy", graphlibJson.write(graph));
    } else {
      log.warn(
        "Cluster ** ",
        node,
        " **not meeting the criteria !externalConnections:",
        !clusterDb[node].externalConnections,
        " no parent: ",
        !graph.parent(node),
        " children ",
        graph.children(node) && graph.children(node).length > 0,
        graph.children("D"),
        depth
      );
      log.debug(clusterDb);
    }
  }
  nodes = graph.nodes();
  log.warn("New list of nodes", nodes);
  for (const node of nodes) {
    const data = graph.node(node);
    log.warn(" Now next level", node, data);
    if (data.clusterNode) {
      extractor(data.graph, depth + 1);
    }
  }
};
const sorter = (graph, nodes) => {
  if (nodes.length === 0) {
    return [];
  }
  let result = Object.assign(nodes);
  nodes.forEach((node) => {
    const children = graph.children(node);
    const sorted = sorter(graph, children);
    result = [...result, ...sorted];
  });
  return result;
};
const sortNodesByHierarchy = (graph) => sorter(graph, graph.children());
const rect = (parent, node) => {
  log.trace("Creating subgraph rect for ", node.id, node);
  const shapeSvg = parent.insert("g").attr("class", "cluster" + (node.class ? " " + node.class : "")).attr("id", node.id);
  const rect2 = shapeSvg.insert("rect", ":first-child");
  const label = shapeSvg.insert("g").attr("class", "cluster-label");
  const text = label.node().appendChild(createLabel(node.labelText, node.labelStyle, void 0, true));
  let bbox = text.getBBox();
  if (evaluate(getConfig().flowchart.htmlLabels)) {
    const div = text.children[0];
    const dv = select(text);
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  const padding = 0 * node.padding;
  const halfPadding = padding / 2;
  const width = node.width <= bbox.width + padding ? bbox.width + padding : node.width;
  if (node.width <= bbox.width + padding) {
    node.diff = (bbox.width - node.width) / 2 - node.padding / 2;
  } else {
    node.diff = -node.padding / 2;
  }
  log.trace("Data ", node, JSON.stringify(node));
  rect2.attr("style", node.style).attr("rx", node.rx).attr("ry", node.ry).attr("x", node.x - width / 2).attr("y", node.y - node.height / 2 - halfPadding).attr("width", width).attr("height", node.height + padding);
  label.attr(
    "transform",
    // This puts the labal on top of the box instead of inside it
    // 'translate(' + (node.x - bbox.width / 2) + ', ' + (node.y - node.height / 2 - bbox.height) + ')'
    "translate(" + (node.x - bbox.width / 2) + ", " + (node.y - node.height / 2) + ")"
  );
  const rectBox = rect2.node().getBBox();
  node.width = rectBox.width;
  node.height = rectBox.height;
  node.intersect = function(point) {
    return intersectRect(node, point);
  };
  return shapeSvg;
};
const noteGroup = (parent, node) => {
  const shapeSvg = parent.insert("g").attr("class", "note-cluster").attr("id", node.id);
  const rect2 = shapeSvg.insert("rect", ":first-child");
  const padding = 0 * node.padding;
  const halfPadding = padding / 2;
  rect2.attr("rx", node.rx).attr("ry", node.ry).attr("x", node.x - node.width / 2 - halfPadding).attr("y", node.y - node.height / 2 - halfPadding).attr("width", node.width + padding).attr("height", node.height + padding).attr("fill", "none");
  const rectBox = rect2.node().getBBox();
  node.width = rectBox.width;
  node.height = rectBox.height;
  node.intersect = function(point) {
    return intersectRect(node, point);
  };
  return shapeSvg;
};
const roundedWithTitle = (parent, node) => {
  const shapeSvg = parent.insert("g").attr("class", node.classes).attr("id", node.id);
  const rect2 = shapeSvg.insert("rect", ":first-child");
  const label = shapeSvg.insert("g").attr("class", "cluster-label");
  const innerRect = shapeSvg.append("rect");
  const text = label.node().appendChild(createLabel(node.labelText, node.labelStyle, void 0, true));
  let bbox = text.getBBox();
  if (evaluate(getConfig().flowchart.htmlLabels)) {
    const div = text.children[0];
    const dv = select(text);
    bbox = div.getBoundingClientRect();
    dv.attr("width", bbox.width);
    dv.attr("height", bbox.height);
  }
  bbox = text.getBBox();
  const padding = 0 * node.padding;
  const halfPadding = padding / 2;
  const width = node.width <= bbox.width + node.padding ? bbox.width + node.padding : node.width;
  if (node.width <= bbox.width + node.padding) {
    node.diff = (bbox.width + node.padding * 0 - node.width) / 2;
  } else {
    node.diff = -node.padding / 2;
  }
  rect2.attr("class", "outer").attr("x", node.x - width / 2 - halfPadding).attr("y", node.y - node.height / 2 - halfPadding).attr("width", width + padding).attr("height", node.height + padding);
  innerRect.attr("class", "inner").attr("x", node.x - width / 2 - halfPadding).attr("y", node.y - node.height / 2 - halfPadding + bbox.height - 1).attr("width", width + padding).attr("height", node.height + padding - bbox.height - 3);
  label.attr(
    "transform",
    "translate(" + (node.x - bbox.width / 2) + ", " + (node.y - node.height / 2 - node.padding / 3 + (evaluate(getConfig().flowchart.htmlLabels) ? 5 : 3)) + ")"
  );
  const rectBox = rect2.node().getBBox();
  node.height = rectBox.height;
  node.intersect = function(point) {
    return intersectRect(node, point);
  };
  return shapeSvg;
};
const divider = (parent, node) => {
  const shapeSvg = parent.insert("g").attr("class", node.classes).attr("id", node.id);
  const rect2 = shapeSvg.insert("rect", ":first-child");
  const padding = 0 * node.padding;
  const halfPadding = padding / 2;
  rect2.attr("class", "divider").attr("x", node.x - node.width / 2 - halfPadding).attr("y", node.y - node.height / 2).attr("width", node.width + padding).attr("height", node.height + padding);
  const rectBox = rect2.node().getBBox();
  node.width = rectBox.width;
  node.height = rectBox.height;
  node.diff = -node.padding / 2;
  node.intersect = function(point) {
    return intersectRect(node, point);
  };
  return shapeSvg;
};
const shapes = { rect, roundedWithTitle, noteGroup, divider };
let clusterElems = {};
const insertCluster = (elem, node) => {
  log.trace("Inserting cluster");
  const shape = node.shape || "rect";
  clusterElems[node.id] = shapes[shape](elem, node);
};
const clear = () => {
  clusterElems = {};
};
const recursiveRender = (_elem, graph, diagramtype, parentCluster) => {
  log.info("Graph in recursive render: XXX", graphlibJson.write(graph), parentCluster);
  const dir = graph.graph().rankdir;
  log.trace("Dir in recursive render - dir:", dir);
  const elem = _elem.insert("g").attr("class", "root");
  if (!graph.nodes()) {
    log.info("No nodes found for", graph);
  } else {
    log.info("Recursive render XXX", graph.nodes());
  }
  if (graph.edges().length > 0) {
    log.trace("Recursive edges", graph.edge(graph.edges()[0]));
  }
  const clusters = elem.insert("g").attr("class", "clusters");
  const edgePaths = elem.insert("g").attr("class", "edgePaths");
  const edgeLabels = elem.insert("g").attr("class", "edgeLabels");
  const nodes = elem.insert("g").attr("class", "nodes");
  graph.nodes().forEach(function(v) {
    const node = graph.node(v);
    if (parentCluster !== void 0) {
      const data = JSON.parse(JSON.stringify(parentCluster.clusterData));
      log.info("Setting data for cluster XXX (", v, ") ", data, parentCluster);
      graph.setNode(parentCluster.id, data);
      if (!graph.parent(v)) {
        log.trace("Setting parent", v, parentCluster.id);
        graph.setParent(v, parentCluster.id, data);
      }
    }
    log.info("(Insert) Node XXX" + v + ": " + JSON.stringify(graph.node(v)));
    if (node && node.clusterNode) {
      log.info("Cluster identified", v, node.width, graph.node(v));
      const o = recursiveRender(nodes, node.graph, diagramtype, graph.node(v));
      const newEl = o.elem;
      updateNodeBounds(node, newEl);
      node.diff = o.diff || 0;
      log.info("Node bounds (abc123)", v, node, node.width, node.x, node.y);
      setNodeElem(newEl, node);
      log.warn("Recursive render complete ", newEl, node);
    } else {
      if (graph.children(v).length > 0) {
        log.info("Cluster - the non recursive path XXX", v, node.id, node, graph);
        log.info(findNonClusterChild(node.id, graph));
        clusterDb[node.id] = { id: findNonClusterChild(node.id, graph), node };
      } else {
        log.info("Node - the non recursive path", v, node.id, node);
        insertNode(nodes, graph.node(v), dir);
      }
    }
  });
  graph.edges().forEach(function(e) {
    const edge = graph.edge(e.v, e.w, e.name);
    log.info("Edge " + e.v + " -> " + e.w + ": " + JSON.stringify(e));
    log.info("Edge " + e.v + " -> " + e.w + ": ", e, " ", JSON.stringify(graph.edge(e)));
    log.info("Fix", clusterDb, "ids:", e.v, e.w, "Translateing: ", clusterDb[e.v], clusterDb[e.w]);
    insertEdgeLabel(edgeLabels, edge);
  });
  graph.edges().forEach(function(e) {
    log.info("Edge " + e.v + " -> " + e.w + ": " + JSON.stringify(e));
  });
  log.info("#############################################");
  log.info("###                Layout                 ###");
  log.info("#############################################");
  log.info(graph);
  layout(graph);
  log.info("Graph after layout:", graphlibJson.write(graph));
  let diff = 0;
  sortNodesByHierarchy(graph).forEach(function(v) {
    const node = graph.node(v);
    log.info("Position " + v + ": " + JSON.stringify(graph.node(v)));
    log.info(
      "Position " + v + ": (" + node.x,
      "," + node.y,
      ") width: ",
      node.width,
      " height: ",
      node.height
    );
    if (node && node.clusterNode) {
      positionNode(node);
    } else {
      if (graph.children(v).length > 0) {
        insertCluster(clusters, node);
        clusterDb[node.id].node = node;
      } else {
        positionNode(node);
      }
    }
  });
  graph.edges().forEach(function(e) {
    const edge = graph.edge(e);
    log.info("Edge " + e.v + " -> " + e.w + ": " + JSON.stringify(edge), edge);
    const paths = insertEdge(edgePaths, e, edge, clusterDb, diagramtype, graph);
    positionEdgeLabel(edge, paths);
  });
  graph.nodes().forEach(function(v) {
    const n = graph.node(v);
    log.info(v, n.type, n.diff);
    if (n.type === "group") {
      diff = n.diff;
    }
  });
  return { elem, diff };
};
const render = (elem, graph, markers, diagramtype, id) => {
  insertMarkers(elem, markers, diagramtype, id);
  clear$2();
  clear$3();
  clear();
  clear$1();
  log.warn("Graph at first:", graphlibJson.write(graph));
  adjustClustersAndEdges(graph);
  log.warn("Graph after:", graphlibJson.write(graph));
  recursiveRender(elem, graph, diagramtype);
};
export {
  render as r
};
//# sourceMappingURL=index-f9d09cc9.js.map
