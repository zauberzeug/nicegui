import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default class Curve {
    create_mesh(start, control1, control2, end, num_points) {
        const curve = new THREE.CubicBezierCurve3(
            new THREE.Vector3(...start),
            new THREE.Vector3(...control1),
            new THREE.Vector3(...control2),
            new THREE.Vector3(...end),
        );
        const geometry = new THREE.BufferGeometry().setFromPoints(curve.getPoints(num_points - 1));
        const material = new THREE.LineBasicMaterial({ transparent: true });
        return new THREE.Line(geometry, material);
    }
}
