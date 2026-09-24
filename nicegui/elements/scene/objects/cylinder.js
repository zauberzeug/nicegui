import { THREE } from "nicegui-scene";

export default class Cylinder {
  create_geometry(...args) {
    return new THREE.CylinderGeometry(...args);
  }
}
