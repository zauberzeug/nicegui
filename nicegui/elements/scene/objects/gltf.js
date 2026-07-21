import SceneLib from "nicegui-scene";
const { THREE, GLTFLoader, SimpleMaterialLoader } = SceneLib;

const gltf_loader = new GLTFLoader();
const material_loader = new SimpleMaterialLoader();

export default class GLTF {
  mesh
  loaded = false
  pendingMaterialInfo = null

  create_mesh(url) {
    this.mesh = new THREE.Group();
    gltf_loader.load(
      url,
      (gltf) => {
        this.mesh.add(gltf.scene);
        this.loaded = true;
        if (this.pendingMaterialInfo != null) {
          const { color, opacity, side } = this.pendingMaterialInfo;
          this.pendingMaterialInfo = null;
          this.apply_material(color, opacity, side);
        }
      },
      undefined,
      (error) => console.error("GLTF load error:", error),
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
