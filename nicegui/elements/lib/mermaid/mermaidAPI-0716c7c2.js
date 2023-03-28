import { select } from "d3";
import { serialize, compile, stringify } from "stylis";
import { g as getConfig, l as log, f as setConfig, h as getSiteConfig, u as updateSiteConfig, r as reset, i as defaultConfig, s as setLogLevel, a as addDirective, j as evaluate, k as saveConfigFromInitialize, t as theme, m as setSiteConfig } from "./config-389b86ff.js";
import { a as registerDiagram, r as registerLazyLoadedDiagrams, d as detectType, g as getDiagram, e as extractFrontMatter, b as getDiagramLoader, U as UnknownDiagramError, p as parseDirective, u as utils, c as directiveSanitizer, f as getStyles } from "./utils-d5eeff82.js";
import { r as renderer } from "./errorRenderer-d05351b9.js";
import DOMPurify from "dompurify";
import isEmpty from "lodash-es/isEmpty.js";
const version = "10.0.2";
const id$i = "c4";
const detector$i = (txt) => {
  return txt.match(/^\s*C4Context|C4Container|C4Component|C4Dynamic|C4Deployment/) !== null;
};
const loader$i = async () => {
  const { diagram } = await import("./c4Diagram-f9e67060.js");
  return { id: id$i, diagram };
};
const plugin$i = {
  id: id$i,
  detector: detector$i,
  loader: loader$i
};
const c4 = plugin$i;
const id$h = "flowchart";
const detector$h = (txt, config) => {
  var _a, _b;
  if (((_a = config == null ? void 0 : config.flowchart) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper" || ((_b = config == null ? void 0 : config.flowchart) == null ? void 0 : _b.defaultRenderer) === "elk") {
    return false;
  }
  return txt.match(/^\s*graph/) !== null;
};
const loader$h = async () => {
  const { diagram } = await import("./flowDiagram-42bb1e4d.js");
  return { id: id$h, diagram };
};
const plugin$h = {
  id: id$h,
  detector: detector$h,
  loader: loader$h
};
const flowchart = plugin$h;
const id$g = "flowchart-v2";
const detector$g = (txt, config) => {
  var _a, _b, _c;
  if (((_a = config == null ? void 0 : config.flowchart) == null ? void 0 : _a.defaultRenderer) === "dagre-d3" || ((_b = config == null ? void 0 : config.flowchart) == null ? void 0 : _b.defaultRenderer) === "elk") {
    return false;
  }
  if (txt.match(/^\s*graph/) !== null && ((_c = config == null ? void 0 : config.flowchart) == null ? void 0 : _c.defaultRenderer) === "dagre-wrapper") {
    return true;
  }
  return txt.match(/^\s*flowchart/) !== null;
};
const loader$g = async () => {
  const { diagram } = await import("./flowDiagram-v2-4c9a7611.js");
  return { id: id$g, diagram };
};
const plugin$g = {
  id: id$g,
  detector: detector$g,
  loader: loader$g
};
const flowchartV2 = plugin$g;
const id$f = "er";
const detector$f = (txt) => {
  return txt.match(/^\s*erDiagram/) !== null;
};
const loader$f = async () => {
  const { diagram } = await import("./erDiagram-25977acd.js");
  return { id: id$f, diagram };
};
const plugin$f = {
  id: id$f,
  detector: detector$f,
  loader: loader$f
};
const er = plugin$f;
const id$e = "gitGraph";
const detector$e = (txt) => {
  return txt.match(/^\s*gitGraph/) !== null;
};
const loader$e = async () => {
  const { diagram } = await import("./gitGraphDiagram-30dcca6d.js");
  return { id: id$e, diagram };
};
const plugin$e = {
  id: id$e,
  detector: detector$e,
  loader: loader$e
};
const git = plugin$e;
const id$d = "gantt";
const detector$d = (txt) => {
  return txt.match(/^\s*gantt/) !== null;
};
const loader$d = async () => {
  const { diagram } = await import("./ganttDiagram-41439120.js");
  return { id: id$d, diagram };
};
const plugin$d = {
  id: id$d,
  detector: detector$d,
  loader: loader$d
};
const gantt = plugin$d;
const id$c = "info";
const detector$c = (txt) => {
  return txt.match(/^\s*info/) !== null;
};
const loader$c = async () => {
  const { diagram } = await import("./infoDiagram-1b335302.js");
  return { id: id$c, diagram };
};
const plugin$c = {
  id: id$c,
  detector: detector$c,
  loader: loader$c
};
const info = plugin$c;
const id$b = "pie";
const detector$b = (txt) => {
  return txt.match(/^\s*pie/) !== null;
};
const loader$b = async () => {
  const { diagram } = await import("./pieDiagram-905ac727.js");
  return { id: id$b, diagram };
};
const plugin$b = {
  id: id$b,
  detector: detector$b,
  loader: loader$b
};
const pie = plugin$b;
const id$a = "requirement";
const detector$a = (txt) => {
  return txt.match(/^\s*requirement(Diagram)?/) !== null;
};
const loader$a = async () => {
  const { diagram } = await import("./requirementDiagram-84e9ae78.js");
  return { id: id$a, diagram };
};
const plugin$a = {
  id: id$a,
  detector: detector$a,
  loader: loader$a
};
const requirement = plugin$a;
const id$9 = "sequence";
const detector$9 = (txt) => {
  return txt.match(/^\s*sequenceDiagram/) !== null;
};
const loader$9 = async () => {
  const { diagram } = await import("./sequenceDiagram-2c95880e.js");
  return { id: id$9, diagram };
};
const plugin$9 = {
  id: id$9,
  detector: detector$9,
  loader: loader$9
};
const sequence = plugin$9;
const id$8 = "class";
const detector$8 = (txt, config) => {
  var _a;
  if (((_a = config == null ? void 0 : config.class) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper") {
    return false;
  }
  return txt.match(/^\s*classDiagram/) !== null;
};
const loader$8 = async () => {
  const { diagram } = await import("./classDiagram-4456d403.js");
  return { id: id$8, diagram };
};
const plugin$8 = {
  id: id$8,
  detector: detector$8,
  loader: loader$8
};
const classDiagram = plugin$8;
const id$7 = "classDiagram";
const detector$7 = (txt, config) => {
  var _a;
  if (txt.match(/^\s*classDiagram/) !== null && ((_a = config == null ? void 0 : config.class) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper") {
    return true;
  }
  return txt.match(/^\s*classDiagram-v2/) !== null;
};
const loader$7 = async () => {
  const { diagram } = await import("./classDiagram-v2-539b00ca.js");
  return { id: id$7, diagram };
};
const plugin$7 = {
  id: id$7,
  detector: detector$7,
  loader: loader$7
};
const classDiagramV2 = plugin$7;
const id$6 = "state";
const detector$6 = (txt, config) => {
  var _a;
  if (((_a = config == null ? void 0 : config.state) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper") {
    return false;
  }
  return txt.match(/^\s*stateDiagram/) !== null;
};
const loader$6 = async () => {
  const { diagram } = await import("./stateDiagram-95825141.js");
  return { id: id$6, diagram };
};
const plugin$6 = {
  id: id$6,
  detector: detector$6,
  loader: loader$6
};
const state = plugin$6;
const id$5 = "stateDiagram";
const detector$5 = (text, config) => {
  var _a, _b;
  if (text.match(/^\s*stateDiagram-v2/) !== null) {
    return true;
  }
  if (text.match(/^\s*stateDiagram/) && ((_a = config == null ? void 0 : config.state) == null ? void 0 : _a.defaultRenderer) === "dagre-wrapper") {
    return true;
  }
  if (text.match(/^\s*stateDiagram/) && ((_b = config == null ? void 0 : config.state) == null ? void 0 : _b.defaultRenderer) === "dagre-wrapper") {
    return true;
  }
  return false;
};
const loader$5 = async () => {
  const { diagram } = await import("./stateDiagram-v2-1cc5d8ed.js");
  return { id: id$5, diagram };
};
const plugin$5 = {
  id: id$5,
  detector: detector$5,
  loader: loader$5
};
const stateV2 = plugin$5;
const id$4 = "journey";
const detector$4 = (txt) => {
  return txt.match(/^\s*journey/) !== null;
};
const loader$4 = async () => {
  const { diagram } = await import("./journeyDiagram-ded66ec9.js");
  return { id: id$4, diagram };
};
const plugin$4 = {
  id: id$4,
  detector: detector$4,
  loader: loader$4
};
const journey = plugin$4;
const id$3 = "error";
const detector$3 = (text) => {
  return text.toLowerCase().trim() === "error";
};
const loader$3 = async () => {
  const { diagram } = await import("./errorDiagram-bb949655.js");
  return { id: id$3, diagram };
};
const plugin$3 = {
  id: id$3,
  detector: detector$3,
  loader: loader$3
};
const error = plugin$3;
const id$2 = "flowchart-elk";
const detector$2 = (txt, config) => {
  var _a;
  if (
    // If diagram explicitly states flowchart-elk
    txt.match(/^\s*flowchart-elk/) || // If a flowchart/graph diagram has their default renderer set to elk
    txt.match(/^\s*flowchart|graph/) && ((_a = config == null ? void 0 : config.flowchart) == null ? void 0 : _a.defaultRenderer) === "elk"
  ) {
    return true;
  }
  return false;
};
const loader$2 = async () => {
  const { diagram } = await import("./flowchart-elk-definition-c9fc5e04.js");
  return { id: id$2, diagram };
};
const plugin$2 = {
  id: id$2,
  detector: detector$2,
  loader: loader$2
};
const flowchartElk = plugin$2;
const id$1 = "timeline";
const detector$1 = (txt) => {
  return txt.match(/^\s*timeline/) !== null;
};
const loader$1 = async () => {
  const { diagram } = await import("./timeline-definition-24ebf147.js");
  return { id: id$1, diagram };
};
const plugin$1 = {
  id: id$1,
  detector: detector$1,
  loader: loader$1
};
const timeline = plugin$1;
const id = "mindmap";
const detector = (txt) => {
  return txt.match(/^\s*mindmap/) !== null;
};
const loader = async () => {
  const { diagram } = await import("./mindmap-definition-c8a05b8a.js");
  return { id, diagram };
};
const plugin = {
  id,
  detector,
  loader
};
const mindmap = plugin;
let hasLoadedDiagrams = false;
const addDiagrams = () => {
  if (hasLoadedDiagrams) {
    return;
  }
  hasLoadedDiagrams = true;
  registerDiagram(
    "---",
    // --- diagram type may appear if YAML front-matter is not parsed correctly
    {
      db: {
        clear: () => {
        }
      },
      styles: {},
      // should never be used
      renderer: {},
      // should never be used
      parser: {
        parser: { yy: {} },
        parse: () => {
          throw new Error(
            "Diagrams beginning with --- are not valid. If you were trying to use a YAML front-matter, please ensure that you've correctly opened and closed the YAML front-matter with un-indented `---` blocks"
          );
        }
      },
      init: () => null
      // no op
    },
    (text) => {
      return text.toLowerCase().trimStart().startsWith("---");
    }
  );
  registerLazyLoadedDiagrams(
    error,
    c4,
    classDiagramV2,
    classDiagram,
    er,
    gantt,
    info,
    pie,
    requirement,
    sequence,
    flowchartElk,
    flowchartV2,
    flowchart,
    mindmap,
    timeline,
    git,
    stateV2,
    state,
    journey
  );
};
class Diagram {
  constructor(text) {
    var _a, _b;
    this.text = text;
    this.type = "graph";
    this.text += "\n";
    const cnf = getConfig();
    try {
      this.type = detectType(text, cnf);
    } catch (e) {
      this.type = "error";
      this.detectError = e;
    }
    const diagram = getDiagram(this.type);
    log.debug("Type " + this.type);
    this.db = diagram.db;
    (_b = (_a = this.db).clear) == null ? void 0 : _b.call(_a);
    this.renderer = diagram.renderer;
    this.parser = diagram.parser;
    const originalParse = this.parser.parse.bind(this.parser);
    this.parser.parse = (text2) => originalParse(extractFrontMatter(text2, this.db));
    this.parser.parser.yy = this.db;
    if (diagram.init) {
      diagram.init(cnf);
      log.info("Initialized diagram " + this.type, cnf);
    }
    this.parse();
  }
  parse() {
    var _a, _b;
    if (this.detectError) {
      throw this.detectError;
    }
    (_b = (_a = this.db).clear) == null ? void 0 : _b.call(_a);
    this.parser.parse(this.text);
  }
  async render(id2, version2) {
    await this.renderer.draw(this.text, id2, version2, this);
  }
  getParser() {
    return this.parser;
  }
  getType() {
    return this.type;
  }
}
const getDiagramFromText = async (text) => {
  const type = detectType(text, getConfig());
  try {
    getDiagram(type);
  } catch (error2) {
    const loader2 = getDiagramLoader(type);
    if (!loader2) {
      throw new UnknownDiagramError(`Diagram ${type} not found.`);
    }
    const { id: id2, diagram } = await loader2();
    registerDiagram(id2, diagram);
  }
  return new Diagram(text);
};
let interactionFunctions = [];
const addFunction = (func) => {
  interactionFunctions.push(func);
};
const attachFunctions = () => {
  interactionFunctions.forEach((f) => {
    f();
  });
  interactionFunctions = [];
};
const SVG_ROLE = "graphics-document document";
function setA11yDiagramInfo(svg, diagramType) {
  svg.attr("role", SVG_ROLE);
  if (!isEmpty(diagramType)) {
    svg.attr("aria-roledescription", diagramType);
  }
}
function addSVGa11yTitleDescription(svg, a11yTitle, a11yDesc, baseId) {
  if (svg.insert === void 0) {
    return;
  }
  if (a11yTitle || a11yDesc) {
    if (a11yDesc) {
      const descId = "chart-desc-" + baseId;
      svg.attr("aria-describedby", descId);
      svg.insert("desc", ":first-child").attr("id", descId).text(a11yDesc);
    }
    if (a11yTitle) {
      const titleId = "chart-title-" + baseId;
      svg.attr("aria-labelledby", titleId);
      svg.insert("title", ":first-child").attr("id", titleId).text(a11yTitle);
    }
  } else {
    return;
  }
}
const CLASSDEF_DIAGRAMS = ["graph", "flowchart", "flowchart-v2", "stateDiagram", "stateDiagram-v2"];
const MAX_TEXTLENGTH = 5e4;
const MAX_TEXTLENGTH_EXCEEDED_MSG = "graph TB;a[Maximum text size in diagram exceeded];style a fill:#faa";
const SECURITY_LVL_SANDBOX = "sandbox";
const SECURITY_LVL_LOOSE = "loose";
const XMLNS_SVG_STD = "http://www.w3.org/2000/svg";
const XMLNS_XLINK_STD = "http://www.w3.org/1999/xlink";
const XMLNS_XHTML_STD = "http://www.w3.org/1999/xhtml";
const IFRAME_WIDTH = "100%";
const IFRAME_HEIGHT = "100%";
const IFRAME_STYLES = "border:0;margin:0;";
const IFRAME_BODY_STYLE = "margin:0";
const IFRAME_SANDBOX_OPTS = "allow-top-navigation-by-user-activation allow-popups";
const IFRAME_NOT_SUPPORTED_MSG = 'The "iframe" tag is not supported by your browser.';
const DOMPURIFY_TAGS = ["foreignobject"];
const DOMPURIFY_ATTR = ["dominant-baseline"];
async function parse(text, parseOptions) {
  addDiagrams();
  let error2;
  try {
    const diagram = await getDiagramFromText(text);
    diagram.parse();
  } catch (err) {
    error2 = err;
  }
  if (parseOptions == null ? void 0 : parseOptions.suppressErrors) {
    return error2 === void 0;
  }
  if (error2) {
    throw error2;
  }
}
const encodeEntities = function(text) {
  let txt = text;
  txt = txt.replace(/style.*:\S*#.*;/g, function(s) {
    return s.substring(0, s.length - 1);
  });
  txt = txt.replace(/classDef.*:\S*#.*;/g, function(s) {
    return s.substring(0, s.length - 1);
  });
  txt = txt.replace(/#\w+;/g, function(s) {
    const innerTxt = s.substring(1, s.length - 1);
    const isInt = /^\+?\d+$/.test(innerTxt);
    if (isInt) {
      return "ﬂ°°" + innerTxt + "¶ß";
    } else {
      return "ﬂ°" + innerTxt + "¶ß";
    }
  });
  return txt;
};
const decodeEntities = function(text) {
  let txt = text;
  txt = txt.replace(/ﬂ°°/g, "&#");
  txt = txt.replace(/ﬂ°/g, "&");
  txt = txt.replace(/¶ß/g, ";");
  return txt;
};
const cssImportantStyles = (cssClass, element, cssClasses = []) => {
  return `
.${cssClass} ${element} { ${cssClasses.join(" !important; ")} !important; }`;
};
const createCssStyles = (config, graphType, classDefs = {}) => {
  var _a;
  let cssStyles = "";
  if (config.themeCSS !== void 0) {
    cssStyles += `
${config.themeCSS}`;
  }
  if (config.fontFamily !== void 0) {
    cssStyles += `
:root { --mermaid-font-family: ${config.fontFamily}}`;
  }
  if (config.altFontFamily !== void 0) {
    cssStyles += `
:root { --mermaid-alt-font-family: ${config.altFontFamily}}`;
  }
  if (!isEmpty(classDefs) && CLASSDEF_DIAGRAMS.includes(graphType)) {
    const htmlLabels = config.htmlLabels || ((_a = config.flowchart) == null ? void 0 : _a.htmlLabels);
    const cssHtmlElements = ["> *", "span"];
    const cssShapeElements = ["rect", "polygon", "ellipse", "circle", "path"];
    const cssElements = htmlLabels ? cssHtmlElements : cssShapeElements;
    for (const classId in classDefs) {
      const styleClassDef = classDefs[classId];
      if (!isEmpty(styleClassDef.styles)) {
        cssElements.forEach((cssElement) => {
          cssStyles += cssImportantStyles(styleClassDef.id, cssElement, styleClassDef.styles);
        });
      }
      if (!isEmpty(styleClassDef.textStyles)) {
        cssStyles += cssImportantStyles(styleClassDef.id, "tspan", styleClassDef.textStyles);
      }
    }
  }
  return cssStyles;
};
const createUserStyles = (config, graphType, classDefs, svgId) => {
  const userCSSstyles = createCssStyles(config, graphType, classDefs);
  const allStyles = getStyles(graphType, userCSSstyles, config.themeVariables);
  return serialize(compile(`${svgId}{${allStyles}}`), stringify);
};
const cleanUpSvgCode = (svgCode = "", inSandboxMode, useArrowMarkerUrls) => {
  let cleanedUpSvg = svgCode;
  if (!useArrowMarkerUrls && !inSandboxMode) {
    cleanedUpSvg = cleanedUpSvg.replace(/marker-end="url\(.*?#/g, 'marker-end="url(#');
  }
  cleanedUpSvg = decodeEntities(cleanedUpSvg);
  cleanedUpSvg = cleanedUpSvg.replace(/<br>/g, "<br/>");
  return cleanedUpSvg;
};
const putIntoIFrame = (svgCode = "", svgElement) => {
  const height = svgElement ? svgElement.viewBox.baseVal.height + "px" : IFRAME_HEIGHT;
  const base64encodedSrc = btoa('<body style="' + IFRAME_BODY_STYLE + '">' + svgCode + "</body>");
  return `<iframe style="width:${IFRAME_WIDTH};height:${height};${IFRAME_STYLES}" src="data:text/html;base64,${base64encodedSrc}" sandbox="${IFRAME_SANDBOX_OPTS}">
  ${IFRAME_NOT_SUPPORTED_MSG}
</iframe>`;
};
const appendDivSvgG = (parentRoot, id2, enclosingDivId, divStyle, svgXlink) => {
  const enclosingDiv = parentRoot.append("div");
  enclosingDiv.attr("id", enclosingDivId);
  if (divStyle) {
    enclosingDiv.attr("style", divStyle);
  }
  const svgNode = enclosingDiv.append("svg").attr("id", id2).attr("width", "100%").attr("xmlns", XMLNS_SVG_STD);
  if (svgXlink) {
    svgNode.attr("xmlns:xlink", svgXlink);
  }
  svgNode.append("g");
  return parentRoot;
};
function sandboxedIframe(parentNode, iFrameId) {
  return parentNode.append("iframe").attr("id", iFrameId).attr("style", "width: 100%; height: 100%;").attr("sandbox", "");
}
const removeExistingElements = (doc, id2, divId, iFrameId) => {
  var _a, _b, _c;
  (_a = doc.getElementById(id2)) == null ? void 0 : _a.remove();
  (_b = doc.getElementById(divId)) == null ? void 0 : _b.remove();
  (_c = doc.getElementById(iFrameId)) == null ? void 0 : _c.remove();
};
const render = async function(id2, text, svgContainingElement) {
  var _a, _b, _c, _d;
  addDiagrams();
  reset();
  const graphInit = utils.detectInit(text);
  if (graphInit) {
    directiveSanitizer(graphInit);
    addDirective(graphInit);
  }
  const config = getConfig();
  log.debug(config);
  if (text.length > ((config == null ? void 0 : config.maxTextSize) ?? MAX_TEXTLENGTH)) {
    text = MAX_TEXTLENGTH_EXCEEDED_MSG;
  }
  text = text.replace(/\r\n?/g, "\n");
  const idSelector = "#" + id2;
  const iFrameID = "i" + id2;
  const iFrameID_selector = "#" + iFrameID;
  const enclosingDivID = "d" + id2;
  const enclosingDivID_selector = "#" + enclosingDivID;
  let root = select("body");
  const isSandboxed = config.securityLevel === SECURITY_LVL_SANDBOX;
  const isLooseSecurityLevel = config.securityLevel === SECURITY_LVL_LOOSE;
  const fontFamily = config.fontFamily;
  if (svgContainingElement !== void 0) {
    if (svgContainingElement) {
      svgContainingElement.innerHTML = "";
    }
    if (isSandboxed) {
      const iframe = sandboxedIframe(select(svgContainingElement), iFrameID);
      root = select(iframe.nodes()[0].contentDocument.body);
      root.node().style.margin = 0;
    } else {
      root = select(svgContainingElement);
    }
    appendDivSvgG(root, id2, enclosingDivID, `font-family: ${fontFamily}`, XMLNS_XLINK_STD);
  } else {
    removeExistingElements(document, id2, enclosingDivID, iFrameID);
    if (isSandboxed) {
      const iframe = sandboxedIframe(select("body"), iFrameID);
      root = select(iframe.nodes()[0].contentDocument.body);
      root.node().style.margin = 0;
    } else {
      root = select("body");
    }
    appendDivSvgG(root, id2, enclosingDivID);
  }
  text = encodeEntities(text);
  let diag;
  let parseEncounteredException;
  try {
    diag = await getDiagramFromText(text);
  } catch (error2) {
    diag = new Diagram("error");
    parseEncounteredException = error2;
  }
  const element = root.select(enclosingDivID_selector).node();
  const graphType = diag.type;
  const svg = element.firstChild;
  const firstChild = svg.firstChild;
  const diagramClassDefs = CLASSDEF_DIAGRAMS.includes(graphType) ? diag.renderer.getClasses(text, diag) : {};
  const rules = createUserStyles(
    config,
    graphType,
    // @ts-ignore convert renderer to TS.
    diagramClassDefs,
    idSelector
  );
  const style1 = document.createElement("style");
  style1.innerHTML = rules;
  svg.insertBefore(style1, firstChild);
  try {
    await diag.renderer.draw(text, id2, version, diag);
  } catch (e) {
    renderer.draw(text, id2, version);
    throw e;
  }
  const svgNode = root.select(`${enclosingDivID_selector} svg`);
  const a11yTitle = (_b = (_a = diag.db).getAccTitle) == null ? void 0 : _b.call(_a);
  const a11yDescr = (_d = (_c = diag.db).getAccDescription) == null ? void 0 : _d.call(_c);
  addA11yInfo(graphType, svgNode, a11yTitle, a11yDescr);
  root.select(`[id="${id2}"]`).selectAll("foreignobject > *").attr("xmlns", XMLNS_XHTML_STD);
  let svgCode = root.select(enclosingDivID_selector).node().innerHTML;
  log.debug("config.arrowMarkerAbsolute", config.arrowMarkerAbsolute);
  svgCode = cleanUpSvgCode(svgCode, isSandboxed, evaluate(config.arrowMarkerAbsolute));
  if (isSandboxed) {
    const svgEl = root.select(enclosingDivID_selector + " svg").node();
    svgCode = putIntoIFrame(svgCode, svgEl);
  } else if (!isLooseSecurityLevel) {
    svgCode = DOMPurify.sanitize(svgCode, {
      ADD_TAGS: DOMPURIFY_TAGS,
      ADD_ATTR: DOMPURIFY_ATTR
    });
  }
  attachFunctions();
  const tmpElementSelector = isSandboxed ? iFrameID_selector : enclosingDivID_selector;
  const node = select(tmpElementSelector).node();
  if (node && "remove" in node) {
    node.remove();
  }
  if (parseEncounteredException) {
    throw parseEncounteredException;
  }
  return {
    svg: svgCode,
    bindFunctions: diag.db.bindFunctions
  };
};
function initialize(options = {}) {
  var _a;
  if ((options == null ? void 0 : options.fontFamily) && !((_a = options.themeVariables) == null ? void 0 : _a.fontFamily)) {
    if (!options.themeVariables) {
      options.themeVariables = {};
    }
    options.themeVariables.fontFamily = options.fontFamily;
  }
  saveConfigFromInitialize(options);
  if ((options == null ? void 0 : options.theme) && options.theme in theme) {
    options.themeVariables = theme[options.theme].getThemeVariables(
      options.themeVariables
    );
  } else if (options) {
    options.themeVariables = theme.default.getThemeVariables(options.themeVariables);
  }
  const config = typeof options === "object" ? setSiteConfig(options) : getSiteConfig();
  setLogLevel(config.logLevel);
  addDiagrams();
}
function addA11yInfo(graphType, svgNode, a11yTitle, a11yDescr) {
  setA11yDiagramInfo(svgNode, graphType);
  addSVGa11yTitleDescription(svgNode, a11yTitle, a11yDescr, svgNode.attr("id"));
}
const mermaidAPI = Object.freeze({
  render,
  parse,
  parseDirective,
  initialize,
  getConfig,
  setConfig,
  getSiteConfig,
  updateSiteConfig,
  reset: () => {
    reset();
  },
  globalReset: () => {
    reset(defaultConfig);
  },
  defaultConfig
});
setLogLevel(getConfig().logLevel);
reset(getConfig());
export {
  addFunction as a,
  decodeEntities as d,
  mermaidAPI as m
};
//# sourceMappingURL=mermaidAPI-0716c7c2.js.map
