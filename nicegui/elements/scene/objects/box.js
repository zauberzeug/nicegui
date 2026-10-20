import { THREE } from "nicegui-scene";

export default class Box {
  create_geometry(...args) {
    return new THREE.BoxGeometry(...args);
  }
}
