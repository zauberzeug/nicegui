import SceneLib from "nicegui-scene";
const { CSS3DObject } = SceneLib;

export default class Text3D {
    create_mesh(text, style) {
        const div = document.createElement("div");
        div.textContent = text;
        div.style.cssText = "userSelect:none;" + style;
        return new CSS3DObject(div);
    }
}
