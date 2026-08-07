import { apply_material, THREE, STLLoader } from "nicegui-scene";

const stl_loader = new STLLoader();

export default class STL {
  mesh;
  loaded = false;
  pendingMaterialInfo = null;

  create_mesh(url, wireframe) {
    this.mesh = new THREE.Group();
    stl_loader.load(
      url,
      (geometry) => {
        const child = wireframe
          ? new THREE.LineSegments(
              new THREE.EdgesGeometry(geometry),
              new THREE.LineBasicMaterial({ transparent: true }),
            )
          : new THREE.Mesh(geometry, new THREE.MeshPhongMaterial({ transparent: true }));
        this.mesh.add(child);
        this.loaded = true;
        if (this.pendingMaterialInfo != null) {
          const material_info = this.pendingMaterialInfo;
          this.pendingMaterialInfo = null;
          this.apply_material(material_info);
        }
      },
      undefined,
      (error) => console.error("STL load error:", error),
    );
    return this.mesh;
  }
  apply_material(material_info) {
    if (!this.loaded) {
      this.pendingMaterialInfo = material_info;
      return;
    }
    this.mesh.traverse((child) => child.material && apply_material(child.material, material_info));
  }
}
