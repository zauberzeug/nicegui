
import SceneLib from "nicegui-scene";
const {
  THREE,
} = SceneLib;
export default class Ring {
  create_geometry(...args) {
    return new THREE.RingGeometry(...args);
  }
}
