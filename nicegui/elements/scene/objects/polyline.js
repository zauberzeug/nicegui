import { THREE } from "nicegui-scene";

export default class Polyline {
  create_mesh(points, colors, dashed, dash_size, gap_size) {
    const pts = points.map((p) => new THREE.Vector3(p[0], p[1], p[2]));
    const geometry = new THREE.BufferGeometry().setFromPoints(pts);
    const useVertexColors = !!colors;
    if (useVertexColors) {
      const flat = new Float32Array(colors.length * 3);
      for (let i = 0; i < colors.length; i++) {
        flat[i * 3] = colors[i][0];
        flat[i * 3 + 1] = colors[i][1];
        flat[i * 3 + 2] = colors[i][2];
      }
      geometry.setAttribute("color", new THREE.BufferAttribute(flat, 3));
    }
    let mesh;
    if (dashed) {
      const material = new THREE.LineDashedMaterial({
        transparent: true,
        dashSize: dash_size,
        gapSize: gap_size,
        vertexColors: useVertexColors,
      });
      mesh = new THREE.Line(geometry, material);
      mesh.computeLineDistances();
    } else {
      const material = new THREE.LineBasicMaterial({
        transparent: true,
        vertexColors: useVertexColors,
      });
      mesh = new THREE.Line(geometry, material);
    }
    return mesh;
  }
}
