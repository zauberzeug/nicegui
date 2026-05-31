import SceneLib from "nicegui-scene";
const {
    THREE,
} = SceneLib;
export default class QuadraticBezierTube {
    create_geometry(...args) {
        const curve = new THREE.QuadraticBezierCurve3(
            new THREE.Vector3(...args[0]),
            new THREE.Vector3(...args[1]),
            new THREE.Vector3(...args[2]),
        );
        return new THREE.TubeGeometry(curve, ...args.slice(3));
    }
}
