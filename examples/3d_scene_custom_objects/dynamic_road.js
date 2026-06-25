import SceneLib from "nicegui-scene";
const { THREE, SimpleMaterialLoader } = SceneLib;

function buildCurve(spec) {
  const V = (p) => new THREE.Vector3(p[0], p[1], p[2]);
  switch (spec.type) {
    case 'cubic':
      return new THREE.CubicBezierCurve3(V(spec.v0), V(spec.v1), V(spec.v2), V(spec.v3));
    case 'quadratic':
      return new THREE.QuadraticBezierCurve3(V(spec.v0), V(spec.v1), V(spec.v2));
    case 'line':
      return new THREE.LineCurve3(V(spec.v0), V(spec.v1));
    case 'catmullrom':
      return new THREE.CatmullRomCurve3(
        spec.points.map(V),
        spec.closed ?? false,
        spec.curveType ?? 'centripetal',
        spec.tension ?? 0.5,
      );
    default:
      console.error(`dynamic_road: unknown curve type "${spec.type}"`, spec);
      return null;
  }
}

let material_loader = new SimpleMaterialLoader();

export default class DynamicRoad {
  group; road; directionLine; arrows;
  width; thickness; latestMaterial; latestArrowColor;

  create_mesh(curves, width, thickness) {
    this.width = width;
    this.thickness = thickness;
    this.group = new THREE.Group();
    this._build(curves);
    return this.group;
  }

  _build(curves) {
    const curvePath = new THREE.CurvePath();
    for (const spec of curves) {
      const c = buildCurve(spec);
      if (c) curvePath.add(c);
    }
    const halfW = this.width / 2;
    const halfT = this.thickness / 2;
    const shape = new THREE.Shape();
    shape.moveTo(-halfT, -halfW);
    shape.lineTo(halfT, -halfW);
    shape.lineTo(halfT, halfW);
    shape.lineTo(-halfT, halfW);
    shape.lineTo(-halfT, -halfW);
    const roadGeometry = new THREE.ExtrudeGeometry(shape, {
      extrudePath: curvePath, steps: 200, bevelEnabled: false,
    });
    const roadMaterial = new THREE.MeshStandardMaterial({
      roughness: 0.8, metalness: 0.1,
    });
    this.road = new THREE.Mesh(roadGeometry, roadMaterial);

    const STEPS = 200;
    const spinePts = curvePath.getSpacedPoints(STEPS);
    const lift = this.thickness;
    const topPts = spinePts.map((p) => new THREE.Vector3(p.x, p.y, p.z + lift));
    this.directionLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(topPts),
      new THREE.LineBasicMaterial({ color: 0xffff00 }),
    );
    const arrowSize = Math.max(this.width * 0.5, 0.1);
    this.arrows = [0.2, 0.5, 0.8].map((t) => {
      const i = Math.round(t * STEPS);
      const dir = curvePath.getTangentAt(t).normalize();
      return new THREE.ArrowHelper(dir, topPts[i], arrowSize, 0xffff00, arrowSize * 0.5, arrowSize * 0.4);
    });
    this.group.add(this.road);
    this.group.add(this.directionLine);
    for (const a of this.arrows) this.group.add(a);
    if (this.latestMaterial) {
      const { color, opacity, side } = this.latestMaterial
      this.apply_material(color, opacity, side)
    }
    if (this.latestArrowColor) {
      this.set_arrow_color(this.latestArrowColor)
    }
  }

  set_curves(curves) {
    this.road.geometry.dispose();
    this.road.material.dispose();
    this.directionLine.geometry.dispose();
    this.directionLine.material.dispose();
    for (const a of this.arrows) {
      a.line.geometry.dispose();
      a.line.material.dispose();
      a.cone.geometry.dispose();
      a.cone.material.dispose();
    }
    this.group.clear();
    this._build(curves);
  }

  set_arrow_color(color) {
    console.log("YAY")
    this.latestArrowColor = color
    this.directionLine.material.color.set(color);
    for (const a of this.arrows) a.setColor(new THREE.Color(color));
  }

  apply_material(color, opacity, side) {
    this.latestMaterial = { color, opacity, side }
    material_loader.apply(this.road.material, color, opacity, side)
  }
}
