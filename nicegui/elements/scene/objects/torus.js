import { THREE } from "nicegui-scene";

export default class Torus {
  create_geometry(...args) {
    return new THREE.TorusGeometry(...args);
  }
}
