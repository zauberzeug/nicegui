import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default class PulsingSphere {
  mesh;

  create_mesh(radius) {
    const geometry = new THREE.SphereGeometry(radius, 32, 16);
    const material = new THREE.MeshPhongMaterial({ color: 0x44aaff, transparent: true });
    this.mesh = new THREE.Mesh(geometry, material);
    return this.mesh;
  }

  set_scale(s) {
    this.mesh.scale.set(s, s, s);
  }
}
