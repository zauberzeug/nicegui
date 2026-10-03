import { THREE } from "nicegui-scene";

window.__tracer_load_count = (window.__tracer_load_count || 0) + 1;

export default class Tracer {
  mesh;

  create_mesh(label) {
    this.mesh = new THREE.Mesh(new THREE.SphereGeometry(0.1), new THREE.MeshBasicMaterial());
    this.mesh.userData.label = label;
    return this.mesh;
  }

  set_value(value) {
    this.mesh.scale.setScalar(value);
  }
}
