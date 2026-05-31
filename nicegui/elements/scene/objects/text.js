import SceneLib from "nicegui-scene";
const { CSS2DObject } = SceneLib;

export default {
    create_mesh(text, style) {
        const div = document.createElement("div");
        div.textContent = text;
        div.style.cssText = style;
        return new CSS2DObject(div);
    }
}
