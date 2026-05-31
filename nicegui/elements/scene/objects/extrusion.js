
import SceneLib from "nicegui-scene";
const {
    THREE,
} = SceneLib;
export default {
    create_geometry(outline, height) {
        const shape = new THREE.Shape();
        const outline = args[0];
        const height = args[1];
        shape.autoClose = true;
        if (outline.length) {
            shape.moveTo(outline[0][0], outline[0][1]);
            outline.slice(1).forEach((p) => shape.lineTo(p[0], p[1]));
        }
        const settings = { depth: height, bevelEnabled: false };
        return new THREE.ExtrudeGeometry(shape, settings);
    }
}
