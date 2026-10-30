import { THREE } from "nicegui-scene";

export default class Polyline {
  create_mesh(points, colors, dashed, dash_size, gap_size) {
    const geometry = new THREE.BufferGeometry().setFromPoints(points.map((p) => new THREE.Vector3(...p)));
    if (colors) geometry.setAttribute("color", new THREE.Float32BufferAttribute(colors.flat(), 3));
    const options = { transparent: true, vertexColors: !!colors };
    const material = dashed
      ? new THREE.LineDashedMaterial({ ...options, dashSize: dash_size, gapSize: gap_size })
      : new THREE.LineBasicMaterial(options);
    const mesh = new THREE.Line(geometry, material);
    if (dashed) mesh.computeLineDistances();
    return mesh;
  }
}
