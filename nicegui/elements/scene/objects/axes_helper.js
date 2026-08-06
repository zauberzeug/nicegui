import { THREE } from "nicegui-scene";

export default class AxesHelper {
  create_mesh(length) {
    const mesh = new THREE.AxesHelper(length);
    mesh.material.transparent = true;
    return mesh;
  }
}
