import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default class TorusKnot {
  mesh;
  radius;
  tube;

  create_mesh(radius, tube, p, q) {
    this.radius = radius;
    this.tube = tube;

    const geometry = new THREE.TorusKnotGeometry(radius, tube, 128, 16, p, q);
    const material = new THREE.MeshStandardMaterial({
      color: 0xcc33ff,
      roughness: 0.1,
      metalness: 0.8
    });

    this.mesh = new THREE.Mesh(geometry, material);
    return this.mesh;
  }

  update_topology(p, q) {
    this.mesh.geometry.dispose();
    this.mesh.geometry = new THREE.TorusKnotGeometry(this.radius, this.tube, 128, 16, p, q);
  }
}
