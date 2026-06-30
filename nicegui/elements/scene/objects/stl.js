import SceneLib from "nicegui-scene";
const {
  THREE,
  STLLoader
} = SceneLib;

const stl_loader = new STLLoader();

export default class STL {
  create_mesh(url, wireframe) {
    const geometry = new THREE.BufferGeometry();
    let mesh;
    if (wireframe) {
      mesh = new THREE.LineSegments(
        new THREE.EdgesGeometry(geometry),
        new THREE.LineBasicMaterial({ transparent: true }),
      );
    } else {
      const material = new THREE.MeshPhongMaterial({ transparent: true });
      mesh = new THREE.Mesh(geometry, material);
    }
    stl_loader.load(url, (geometry) => (mesh.geometry = geometry));
    return mesh
  }
}
