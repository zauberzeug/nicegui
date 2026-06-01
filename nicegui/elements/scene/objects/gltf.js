import SceneLib from "nicegui-scene";
const { THREE, GLTFLoader } = SceneLib;

const gltf_loader = new GLTFLoader();

export default class GLTF {
    mesh
    loaded = false
    pendingMaterialInfo = null

    create_mesh(url) {
        this.mesh = new THREE.Group();
        gltf_loader.load(
            url,
            (gltf) => {
                this.mesh.add(gltf.scene);
                this.loaded = true;
                if (this.pendingMaterialInfo != null) {
                    const { color, opacity, side } = this.pendingMaterialInfo;
                    this.pendingMaterialInfo = null;
                    this.apply_material(color, opacity, side);
                }
            },
            undefined,
            (error) => console.error(error),
        );
        return this.mesh;
    }
    apply_material(color, opacity, side) {
        if (!this.loaded) {
            this.pendingMaterialInfo = { color, opacity, side };
            return;
        }
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
        this.mesh.traverse((child) => child.isMesh && child.material && apply(child.material));
    }
}
