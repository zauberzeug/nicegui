import SceneLib from "nicegui-scene";
const {
    THREE,
} = SceneLib;
export default class Sphere {
    create_geometry(...args) {
        return new THREE.SphereGeometry(...args);
    }
}
