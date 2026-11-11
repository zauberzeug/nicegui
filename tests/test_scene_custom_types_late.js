import { THREE } from "nicegui-scene";

export default class LateBox {
  create_geometry(size) {
    return new THREE.BoxGeometry(size, size, size);
  }
}
