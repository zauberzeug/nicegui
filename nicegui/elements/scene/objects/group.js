import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default {
    create_mesh() {
        return new THREE.Group();
    }
}
