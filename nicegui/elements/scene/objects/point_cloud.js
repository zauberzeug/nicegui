import SceneLib from "nicegui-scene";
const { THREE } = SceneLib;

export default {
    create_mesh(points, colors, point_size) {
        const geometry = new THREE.BufferGeometry();
        const material = new THREE.PointsMaterial({ size: point_size, transparent: true });
        const mesh = new THREE.Points(geometry, material);
        this.set_points(mesh, points, colors);
        return mesh
    },
    set_points(mesh, position, color) {
        mesh.geometry.setAttribute("position", new THREE.Float32BufferAttribute(position.flat(), 3));
        if (color === null) {
            geometry.deleteAttribute("color");
        } else {
            geometry.setAttribute("color", new THREE.Float32BufferAttribute(color.flat(), 3));
        }
    }
}
