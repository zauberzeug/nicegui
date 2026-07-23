import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

window.__tracer = { created: [], values: [] };

export default class Tracer {
  mesh;

  create_mesh(label) {
    const geometry = new THREE.SphereGeometry(0.1, 8, 8);
    const material = new THREE.MeshBasicMaterial({ color: 0xff00ff });
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.userData.label = label;
    window.__tracer.created.push({ label });  // NOTE: for selenium
    return this.mesh;
  }

  set_value(value) {
    window.__tracer.values.push({ id: this.mesh.object_id, value }); // NOTE: for selenium
  }
}
