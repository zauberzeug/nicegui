import SceneLib from "nicegui-scene";
const { THREE, GLTFLoader } = SceneLib;

const gltf_loader = new GLTFLoader();

export default class GLTF {
  mesh;
  loaded = false;
  pendingMaterialInfo = null;

  create_mesh(url) {
    this.mesh = new THREE.Group();
    gltf_loader.load(
      url,
      (gltf) => {
        this.mesh.add(gltf.scene);
        this.loaded = true;
        if (this.pendingMaterialInfo != null) {
          const material_info = this.pendingMaterialInfo;
          this.pendingMaterialInfo = null;
          this.apply_material(material_info);
        }
      },
      undefined,
      (error) => console.error("GLTF load error:", error),
    );
    return this.mesh;
  }
  apply_material(material_info) {
    if (!this.loaded) {
      this.pendingMaterialInfo = material_info;
      return;
    }
    this.mesh.traverse((child) => child.material && SceneLib.apply_material(child.material, material_info));
  }
}
