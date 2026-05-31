import SceneLib from "nicegui-scene";
const { THREE, GLTFLoader } = SceneLib;

const gltf_loader = new GLTFLoader();

export default {
    create_mesh(url) {
        const mesh = new THREE.Group();
        mesh.userData.isGltf = true;
        mesh.userData.loaded = false;
        gltf_loader.load(
            url,
            (gltf) => {
                mesh.add(gltf.scene);
                mesh.userData.loaded = true;
                if (mesh.userData.pendingMaterialInfo) {
                    const { color, opacity, side } = mesh.userData.pendingMaterialInfo;
                    delete mesh.userData.pendingMaterialInfo;
                    const vertexColors = color === null;
                    const apply = (material) => {
                        (Array.isArray(material) ? material : [material]).forEach((m) => {
                            m.color.set(vertexColors ? "#ffffff" : color);
                            m.needsUpdate = m.vertexColors != vertexColors;
                            m.vertexColors = vertexColors;
                            m.opacity = opacity;
                            if (side === "front") m.side = THREE.FrontSide;
                            else if (side === "back") m.side = THREE.BackSide;
                            else m.side = THREE.DoubleSide;
                        });
                    };
                    mesh.traverse((child) => child.isMesh && child.material && apply(child.material));
                }
            },
            undefined,
            (error) => console.error(error),
        );
        return mesh;
    }
}
