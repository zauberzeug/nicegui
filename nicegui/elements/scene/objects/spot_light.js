import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default {
    create_mesh(color, intensity, distance, angle, penumbra, decay) {
        const mesh = new THREE.Group();
        const light = new THREE.SpotLight(color, intensity, distance, angle, penumbra, decay);
        light.position.set(0, 0, 0);
        light.target = new THREE.Object3D();
        light.target.position.set(1, 0, 0);
        mesh.add(light);
        mesh.add(light.target);
        return mesh;
    }
}
