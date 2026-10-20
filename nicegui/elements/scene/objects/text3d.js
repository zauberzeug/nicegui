import { CSS3DObject } from "nicegui-scene";

export default class Text3D {
  create_mesh(text, style) {
    const div = document.createElement("div");
    div.textContent = text;
    div.style.cssText = "user-select:none;" + style;
    return new CSS3DObject(div);
  }
}
