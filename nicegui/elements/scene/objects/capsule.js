import { THREE } from "nicegui-scene";

export default class Capsule {
  create_geometry(...args) {
    return new THREE.CapsuleGeometry(...args);
  }
}
