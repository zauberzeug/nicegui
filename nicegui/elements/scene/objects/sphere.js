import { THREE } from "nicegui-scene";

export default class Sphere {
  create_geometry(...args) {
    return new THREE.SphereGeometry(...args);
  }
}
