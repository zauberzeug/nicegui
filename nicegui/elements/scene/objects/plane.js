import { THREE } from "nicegui-scene";

export default class Plane {
  create_geometry(...args) {
    return new THREE.PlaneGeometry(...args);
  }
}
