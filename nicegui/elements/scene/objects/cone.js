import { THREE } from "nicegui-scene";

export default class Cone {
  create_geometry(...args) {
    return new THREE.ConeGeometry(...args);
  }
}
