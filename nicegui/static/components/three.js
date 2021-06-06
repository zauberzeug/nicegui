var camera;

Vue.component("three", {
  template: `<canvas v-bind:id="jp_props.id"></div>`,
  mounted() {
    const scene = new THREE.Scene();

    const width = 400;
    const height = 300;

    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = this.$props.jp_props.options.camera_z;

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      canvas: document.getElementById(this.$props.jp_props.id),
    });
    renderer.setClearColor("#ddd");
    renderer.setSize(width, height);

    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: "#433F81" });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    new THREE.OrbitControls(camera, renderer.domElement);

    const render = function () {
      requestAnimationFrame(render);
      renderer.render(scene, camera);
    };
    render();

    const raycaster = new THREE.Raycaster();
    document.getElementById(this.$props.jp_props.id).onclick = (mouseEvent) => {
      let x = (mouseEvent.offsetX / renderer.domElement.width) * 2 - 1;
      let y = -(mouseEvent.offsetY / renderer.domElement.height) * 2 + 1;
      raycaster.setFromCamera({ x: x, y: y }, camera);
      const objects = raycaster.intersectObjects(scene.children, true);
      console.log(objects);
      const event = {
        event_type: "onClick",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
        objects: objects,
      };
      send_to_server(event, "event");
    };
  },
  updated() {
    camera.position.z = this.$props.jp_props.options.camera_z;
  },
  props: {
    jp_props: Object,
  },
});
