import { CSS2DObject } from "nicegui-scene";

export default class Text {
  create_mesh(text, style) {
    const div = document.createElement("div");
    div.textContent = text;
    div.style.cssText = style;
    return new CSS2DObject(div);
  }
}
