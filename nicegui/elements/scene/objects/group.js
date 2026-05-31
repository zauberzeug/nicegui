import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default class Group {
    create_mesh() {
        return new THREE.Group();
    }
}
