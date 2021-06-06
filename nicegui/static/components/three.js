Vue.component("three", {
  template: `<canvas v-bind:id="jp_props.id"></div>`,
  mounted() {
    const scene = new THREE.Scene();

    const width = 400;
    const height = 300;

    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 4;

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
  },
  props: {
    jp_props: Object,
  },
});
