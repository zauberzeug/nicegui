import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default class Line {
  create_mesh(start, end) {
    const geometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(...start),
      new THREE.Vector3(...end),
    ]);
    const material = new THREE.LineBasicMaterial({ transparent: true });
    return new THREE.Line(geometry, material);
  }
}
