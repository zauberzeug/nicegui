import SceneLib from "nicegui-scene";
const {
    THREE,
} = SceneLib;
export default class Cylinder {
    create_geometry(...args) {
        return new THREE.CylinderGeometry(...args);
    }
}
