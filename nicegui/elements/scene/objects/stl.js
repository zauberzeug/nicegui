import SceneLib from "nicegui-scene";
const { THREE, STLLoader, SimpleMaterialLoader } = SceneLib;

const stl_loader = new STLLoader();
const material_loader = new SimpleMaterialLoader();

export default class STL {
  mesh
  loaded = false
  pendingMaterialInfo = null

  create_mesh(url, wireframe) {
    this.mesh = new THREE.Group();
    stl_loader.load(
      url,
      (geometry) => {
        const child = wireframe
          ? new THREE.LineSegments(new THREE.EdgesGeometry(geometry), new THREE.LineBasicMaterial({ transparent: true }))
          : new THREE.Mesh(geometry, new THREE.MeshPhongMaterial({ transparent: true }));
        this.mesh.add(child);
        this.loaded = true;
        if (this.pendingMaterialInfo != null) {
          const { color, opacity, side } = this.pendingMaterialInfo;
          this.pendingMaterialInfo = null;
          this.apply_material(color, opacity, side);
        }
      },
      undefined,
      (error) => console.error("STL load error:", error),
    );
    return this.mesh;
  }
  apply_material(color, opacity, side) {
    if (!this.loaded) {
      this.pendingMaterialInfo = { color, opacity, side };
      return;
    }
    this.mesh.traverse((child) => child.material && material_loader.apply(child.material, color, opacity, side));
  }
}
