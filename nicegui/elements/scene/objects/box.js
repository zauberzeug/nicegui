import SceneLib from "nicegui-scene";
const {
    THREE,
} = SceneLib;

export default class Box {
    create_geometry(...args) {
        return new THREE.BoxGeometry(...args);
    }
}
