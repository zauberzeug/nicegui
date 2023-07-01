import { S as Selection, o as root, q as array } from "./config-b4fa35bb.js";
function selectAll(selector) {
  return typeof selector === "string" ? new Selection([document.querySelectorAll(selector)], [document.documentElement]) : new Selection([array(selector)], root);
}
export {
  selectAll as s
};
//# sourceMappingURL=selectAll-b147441f.js.map
