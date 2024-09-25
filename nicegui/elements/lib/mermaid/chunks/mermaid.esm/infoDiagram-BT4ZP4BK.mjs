import {
  parse
} from "./chunk-M52XIDDU.mjs";
import "./chunk-76YUXBKW.mjs";
import "./chunk-W7WFRJCB.mjs";
import {
  version
} from "./chunk-ZIY44AE2.mjs";
import {
  selectSvgElement
} from "./chunk-VNRP4OIW.mjs";
import {
  configureSvgSize,
  log
} from "./chunk-DD37ZF33.mjs";
import "./chunk-HCCMVKPJ.mjs";
import "./chunk-3YXWICEL.mjs";
import "./chunk-HBGMPAD7.mjs";
import "./chunk-TZBO7MLI.mjs";
import "./chunk-GRZAG2UZ.mjs";
import "./chunk-HD3LK5B5.mjs";
import {
  __name
} from "./chunk-DLQEHMXD.mjs";

// src/diagrams/info/infoParser.ts
var parser = {
  parse: /* @__PURE__ */ __name(async (input) => {
    const ast = await parse("info", input);
    log.debug(ast);
  }, "parse")
};

// src/diagrams/info/infoDb.ts
var DEFAULT_INFO_DB = { version };
var getVersion = /* @__PURE__ */ __name(() => DEFAULT_INFO_DB.version, "getVersion");
var db = {
  getVersion
};

// src/diagrams/info/infoRenderer.ts
var draw = /* @__PURE__ */ __name((text, id, version2) => {
  log.debug("rendering info diagram\n" + text);
  const svg = selectSvgElement(id);
  configureSvgSize(svg, 100, 400, true);
  const group = svg.append("g");
  group.append("text").attr("x", 100).attr("y", 40).attr("class", "version").attr("font-size", 32).style("text-anchor", "middle").text(`v${version2}`);
}, "draw");
var renderer = { draw };

// src/diagrams/info/infoDiagram.ts
var diagram = {
  parser,
  db,
  renderer
};
export {
  diagram
};
