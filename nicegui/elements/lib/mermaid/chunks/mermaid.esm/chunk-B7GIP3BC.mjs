import {
  clone_default,
  isUndefined_default,
  map_default
} from "./chunk-TZBO7MLI.mjs";
import {
  __name
} from "./chunk-DLQEHMXD.mjs";

// ../../node_modules/.pnpm/dagre-d3-es@7.0.10/node_modules/dagre-d3-es/src/graphlib/json.js
function write(g) {
  var json = {
    options: {
      directed: g.isDirected(),
      multigraph: g.isMultigraph(),
      compound: g.isCompound()
    },
    nodes: writeNodes(g),
    edges: writeEdges(g)
  };
  if (!isUndefined_default(g.graph())) {
    json.value = clone_default(g.graph());
  }
  return json;
}
__name(write, "write");
function writeNodes(g) {
  return map_default(g.nodes(), function(v) {
    var nodeValue = g.node(v);
    var parent = g.parent(v);
    var node = { v };
    if (!isUndefined_default(nodeValue)) {
      node.value = nodeValue;
    }
    if (!isUndefined_default(parent)) {
      node.parent = parent;
    }
    return node;
  });
}
__name(writeNodes, "writeNodes");
function writeEdges(g) {
  return map_default(g.edges(), function(e) {
    var edgeValue = g.edge(e);
    var edge = { v: e.v, w: e.w };
    if (!isUndefined_default(e.name)) {
      edge.name = e.name;
    }
    if (!isUndefined_default(edgeValue)) {
      edge.value = edgeValue;
    }
    return edge;
  });
}
__name(writeEdges, "writeEdges");

export {
  write
};
