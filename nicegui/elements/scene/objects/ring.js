import { THREE } from "nicegui-scene";

export default class Ring {
  create_geometry(...args) {
    return new THREE.RingGeometry(...args);
  }
}
