import { p as parser, d as db, s as styles } from "./styles-d6ad8edb.js";
import { l as log, g as getConfig, f as select, e as common } from "./config-b4fa35bb.js";
import { G as Graph } from "./layout-4663fc19.js";
import { r as render } from "./index-a1a98052.js";
import { u as utils, z as interpolateToCurve, x as curveLinear, y as getStylesFromArray } from "./utils-872dfc50.js";
import { s as setupGraphViewbox } from "./setupGraphViewbox-16a0ba81.js";
import "./mermaidAPI-6f22a815.js";
import "./errorRenderer-ebf63d74.js";
import "./commonDb-7f40ab5a.js";
import "./isPlainObject-91dd8bc9.js";
import "./array-b7dcf730.js";
import "./constant-b644328d.js";
import "./edges-62a01f73.js";
import "./svgDraw-9e97e6db.js";
const sanitizeText = (txt) => common.sanitizeText(txt, getConfig());
let conf = {
  dividerMargin: 10,
  padding: 5,
  textHeight: 10,
  curve: void 0
};
const addClasses = function(classes, g, _id, diagObj) {
  const keys = Object.keys(classes);
  log.info("keys:", keys);
  log.info(classes);
  keys.forEach(function(id) {
    var _a, _b;
    const vertex = classes[id];
    let cssClassStr = "";
    if (vertex.cssClasses.length > 0) {
      cssClassStr = cssClassStr + " " + vertex.cssClasses.join(" ");
    }
    const styles2 = { labelStyle: "", style: "" };
    const vertexText = vertex.label ?? vertex.id;
    const radius = 0;
    const shape = "class_box";
    const node = {
      labelStyle: styles2.labelStyle,
      shape,
      labelText: sanitizeText(vertexText),
      classData: vertex,
      rx: radius,
      ry: radius,
      class: cssClassStr,
      style: styles2.style,
      id: vertex.id,
      domId: vertex.domId,
      tooltip: diagObj.db.getTooltip(vertex.id) || "",
      haveCallback: vertex.haveCallback,
      link: vertex.link,
      width: vertex.type === "group" ? 500 : void 0,
      type: vertex.type,
      // TODO V10: Flowchart ? Keeping flowchart for backwards compatibility. Remove in next major release
      padding: ((_a = getConfig().flowchart) == null ? void 0 : _a.padding) ?? ((_b = getConfig().class) == null ? void 0 : _b.padding)
    };
    g.setNode(vertex.id, node);
    log.info("setNode", node);
  });
};
const addNotes = function(notes, g, startEdgeId, classes) {
  log.info(notes);
  notes.forEach(function(note, i) {
    var _a, _b;
    const vertex = note;
    const cssNoteStr = "";
    const styles2 = { labelStyle: "", style: "" };
    const vertexText = vertex.text;
    const radius = 0;
    const shape = "note";
    const node = {
      labelStyle: styles2.labelStyle,
      shape,
      labelText: sanitizeText(vertexText),
      noteData: vertex,
      rx: radius,
      ry: radius,
      class: cssNoteStr,
      style: styles2.style,
      id: vertex.id,
      domId: vertex.id,
      tooltip: "",
      type: "note",
      // TODO V10: Flowchart ? Keeping flowchart for backwards compatibility. Remove in next major release
      padding: ((_a = getConfig().flowchart) == null ? void 0 : _a.padding) ?? ((_b = getConfig().class) == null ? void 0 : _b.padding)
    };
    g.setNode(vertex.id, node);
    log.info("setNode", node);
    if (!vertex.class || !(vertex.class in classes)) {
      return;
    }
    const edgeId = startEdgeId + i;
    const edgeData = {
      id: `edgeNote${edgeId}`,
      //Set relationship style and line type
      classes: "relation",
      pattern: "dotted",
      // Set link type for rendering
      arrowhead: "none",
      //Set edge extra labels
      startLabelRight: "",
      endLabelLeft: "",
      //Set relation arrow types
      arrowTypeStart: "none",
      arrowTypeEnd: "none",
      style: "fill:none",
      labelStyle: "",
      curve: interpolateToCurve(conf.curve, curveLinear)
    };
    g.setEdge(vertex.id, vertex.class, edgeData, edgeId);
  });
};
const addRelations = function(relations, g) {
  const conf2 = getConfig().flowchart;
  let cnt = 0;
  relations.forEach(function(edge) {
    var _a;
    cnt++;
    const edgeData = {
      //Set relationship style and line type
      classes: "relation",
      pattern: edge.relation.lineType == 1 ? "dashed" : "solid",
      id: "id" + cnt,
      // Set link type for rendering
      arrowhead: edge.type === "arrow_open" ? "none" : "normal",
      //Set edge extra labels
      startLabelRight: edge.relationTitle1 === "none" ? "" : edge.relationTitle1,
      endLabelLeft: edge.relationTitle2 === "none" ? "" : edge.relationTitle2,
      //Set relation arrow types
      arrowTypeStart: getArrowMarker(edge.relation.type1),
      arrowTypeEnd: getArrowMarker(edge.relation.type2),
      style: "fill:none",
      labelStyle: "",
      curve: interpolateToCurve(conf2 == null ? void 0 : conf2.curve, curveLinear)
    };
    log.info(edgeData, edge);
    if (edge.style !== void 0) {
      const styles2 = getStylesFromArray(edge.style);
      edgeData.style = styles2.style;
      edgeData.labelStyle = styles2.labelStyle;
    }
    edge.text = edge.title;
    if (edge.text === void 0) {
      if (edge.style !== void 0) {
        edgeData.arrowheadStyle = "fill: #333";
      }
    } else {
      edgeData.arrowheadStyle = "fill: #333";
      edgeData.labelpos = "c";
      if (((_a = getConfig().flowchart) == null ? void 0 : _a.htmlLabels) ?? getConfig().htmlLabels) {
        edgeData.labelType = "html";
        edgeData.label = '<span class="edgeLabel">' + edge.text + "</span>";
      } else {
        edgeData.labelType = "text";
        edgeData.label = edge.text.replace(common.lineBreakRegex, "\n");
        if (edge.style === void 0) {
          edgeData.style = edgeData.style || "stroke: #333; stroke-width: 1.5px;fill:none";
        }
        edgeData.labelStyle = edgeData.labelStyle.replace("color:", "fill:");
      }
    }
    g.setEdge(edge.id1, edge.id2, edgeData, cnt);
  });
};
const setConf = function(cnf) {
  conf = {
    ...conf,
    ...cnf
  };
};
const draw = function(text, id, _version, diagObj) {
  log.info("Drawing class - ", id);
  const conf2 = getConfig().flowchart ?? getConfig().class;
  const securityLevel = getConfig().securityLevel;
  log.info("config:", conf2);
  const nodeSpacing = (conf2 == null ? void 0 : conf2.nodeSpacing) ?? 50;
  const rankSpacing = (conf2 == null ? void 0 : conf2.rankSpacing) ?? 50;
  const g = new Graph({
    multigraph: true,
    compound: true
  }).setGraph({
    rankdir: diagObj.db.getDirection(),
    nodesep: nodeSpacing,
    ranksep: rankSpacing,
    marginx: 8,
    marginy: 8
  }).setDefaultEdgeLabel(function() {
    return {};
  });
  const classes = diagObj.db.getClasses();
  const relations = diagObj.db.getRelations();
  const notes = diagObj.db.getNotes();
  log.info(relations);
  addClasses(classes, g, id, diagObj);
  addRelations(relations, g);
  addNotes(notes, g, relations.length + 1, classes);
  let sandboxElement;
  if (securityLevel === "sandbox") {
    sandboxElement = select("#i" + id);
  }
  const root = securityLevel === "sandbox" ? (
    // @ts-ignore Ignore type error for now
    select(sandboxElement.nodes()[0].contentDocument.body)
  ) : select("body");
  const svg = root.select(`[id="${id}"]`);
  const element = root.select("#" + id + " g");
  render(
    element,
    g,
    ["aggregation", "extension", "composition", "dependency", "lollipop"],
    "classDiagram",
    id
  );
  utils.insertTitle(svg, "classTitleText", (conf2 == null ? void 0 : conf2.titleTopMargin) ?? 5, diagObj.db.getDiagramTitle());
  setupGraphViewbox(g, svg, conf2 == null ? void 0 : conf2.diagramPadding, conf2 == null ? void 0 : conf2.useMaxWidth);
  if (!(conf2 == null ? void 0 : conf2.htmlLabels)) {
    const doc = securityLevel === "sandbox" ? sandboxElement.nodes()[0].contentDocument : document;
    const labels = doc.querySelectorAll('[id="' + id + '"] .edgeLabel .label');
    for (const label of labels) {
      const dim = label.getBBox();
      const rect = doc.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("rx", 0);
      rect.setAttribute("ry", 0);
      rect.setAttribute("width", dim.width);
      rect.setAttribute("height", dim.height);
      label.insertBefore(rect, label.firstChild);
    }
  }
};
function getArrowMarker(type) {
  let marker;
  switch (type) {
    case 0:
      marker = "aggregation";
      break;
    case 1:
      marker = "extension";
      break;
    case 2:
      marker = "composition";
      break;
    case 3:
      marker = "dependency";
      break;
    case 4:
      marker = "lollipop";
      break;
    default:
      marker = "none";
  }
  return marker;
}
const renderer = {
  setConf,
  draw
};
const diagram = {
  parser,
  db,
  renderer,
  styles,
  init: (cnf) => {
    if (!cnf.class) {
      cnf.class = {};
    }
    cnf.class.arrowMarkerAbsolute = cnf.arrowMarkerAbsolute;
    db.clear();
  }
};
export {
  diagram
};
//# sourceMappingURL=classDiagram-v2-8096aa52.js.map
