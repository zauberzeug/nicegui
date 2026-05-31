import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default class PointCloud {
    mesh

    create_mesh(points, colors, point_size) {
        const geometry = new THREE.BufferGeometry();
        const material = new THREE.PointsMaterial({ size: point_size, transparent: true });
        this.mesh = new THREE.Points(geometry, material);
        this.set_points(points, colors);
        return this.mesh
    }

    set_points(position, color) {
        const geometry = this.mesh.geometry
        geometry.setAttribute("position", new THREE.Float32BufferAttribute(position.flat(), 3));
        if (color === null) {
            geometry.deleteAttribute("color");
        } else {
            geometry.setAttribute("color", new THREE.Float32BufferAttribute(color.flat(), 3));
        }
    }
}
