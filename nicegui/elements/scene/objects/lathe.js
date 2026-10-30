import { THREE } from "nicegui-scene";

export default class Lathe {
  create_geometry(points, ...args) {
    const pts = points.map((p) => new THREE.Vector2(p[0], p[1]));
    return new THREE.LatheGeometry(pts, ...args);
  }
}
