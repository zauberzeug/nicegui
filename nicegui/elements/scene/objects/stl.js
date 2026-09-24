import { apply_material, THREE, STLLoader } from "nicegui-scene";

const stl_loader = new STLLoader();

export default class STL {
  mesh;

  async create_mesh(url, wireframe) {
    const geometry = await stl_loader.loadAsync(url);
    this.mesh = new THREE.Group();
    this.mesh.add(
      wireframe
        ? new THREE.LineSegments(new THREE.EdgesGeometry(geometry), new THREE.LineBasicMaterial({ transparent: true }))
        : new THREE.Mesh(geometry, new THREE.MeshPhongMaterial({ transparent: true })),
    );
    return this.mesh;
  }
  apply_material(material_info) {
    this.mesh.traverse((child) => child.material && apply_material(child.material, material_info));
  }
}
