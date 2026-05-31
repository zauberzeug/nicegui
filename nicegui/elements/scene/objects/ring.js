
import SceneLib from "nicegui-scene";
const {
    THREE,
} = SceneLib;
export default {
    create_geometry(...args) {
        return new THREE.RingGeometry(...args);
    }
}
