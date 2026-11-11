import { apply_material, THREE, GLTFLoader } from "nicegui-scene";

const gltf_loader = new GLTFLoader();

export default class GLTF {
  mesh;

  async create_mesh(url) {
    const gltf = await gltf_loader.loadAsync(url);
    this.mesh = new THREE.Group();
    this.mesh.add(gltf.scene);
    return this.mesh;
  }
  apply_material(material_info) {
    this.mesh.traverse((child) => child.material && apply_material(child.material, material_info));
  }
}
