var scene;
var camera;
var orbitControls;
var objects = new Map();

Vue.component("three", {
  template: `<canvas v-bind:id="jp_props.id"></div>`,

  mounted() {
    scene = new THREE.Scene();
    objects.set("scene", scene);

    const width = this.$props.jp_props.options.width;
    const height = this.$props.jp_props.options.height;

    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.up = new THREE.Vector3(0, 0, 1);
    camera.position.set(0, -3, 5);

    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const light = new THREE.DirectionalLight(0xffffff, 0.3);
    light.position.set(5, 10, 40);
    scene.add(light);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      canvas: document.getElementById(this.$props.jp_props.id),
    });
    renderer.setClearColor("#eee");
    renderer.setSize(width, height);

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(100, 100),
      new THREE.MeshPhongMaterial({ color: "#eee" })
    );
    ground.translateZ(-0.01);
    ground.name = "ground";
    scene.add(ground);

    const grid = new THREE.GridHelper(100, 100);
    grid.material.transparent = true;
    grid.material.opacity = 0.2;
    grid.rotateX(Math.PI / 2);
    scene.add(grid);

    orbitControls = new THREE.OrbitControls(camera, renderer.domElement);

    const render = function () {
      requestAnimationFrame(() => setTimeout(() => render(), 1000 / 20));
      renderer.render(scene, camera);
    };
    render();

    const raycaster = new THREE.Raycaster();
    const click_handler = (mouseEvent) => {
      let x = (mouseEvent.offsetX / renderer.domElement.width) * 2 - 1;
      let y = -(mouseEvent.offsetY / renderer.domElement.height) * 2 + 1;
      raycaster.setFromCamera({ x: x, y: y }, camera);
      const event = {
        event_type: "onClick",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
        objects: raycaster
          .intersectObjects(scene.children, true)
          .filter((o) => o.object.name)
          .map((o) => ({ name: o.object.name, point: o.point })),
        click_type: mouseEvent.type,
        shift_key: mouseEvent.shiftKey,
      };
      send_to_server(event, "event");
    };
    document.getElementById(this.$props.jp_props.id).onclick = click_handler;
    document.getElementById(this.$props.jp_props.id).ondblclick = click_handler;

    comp_dict[this.$props.jp_props.id] = this;

    setTimeout(() => {
      const event = {
        event_type: "onConnect",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
      };
      send_to_server(event, "event");
    }, 100);
  },

  updated() {},

  methods: {
    create(type, id, parent_id, ...args) {
      let mesh;
      if (type == "group") {
        mesh = new THREE.Group();
      } else if (type == "curve") {
        const curve = new THREE.CubicBezierCurve3(
          new THREE.Vector3(...args[0]),
          new THREE.Vector3(...args[1]),
          new THREE.Vector3(...args[2]),
          new THREE.Vector3(...args[3])
        );
        const points = curve.getPoints(args[4] - 1);
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({ transparent: true });
        mesh = new THREE.Line(geometry, material);
      } else {
        let geometry;
        if (type == "box") geometry = new THREE.BoxGeometry(...args);
        if (type == "sphere") geometry = new THREE.SphereGeometry(...args);
        if (type == "cylinder") geometry = new THREE.CylinderGeometry(...args);
        if (type == "extrusion") {
          const shape = new THREE.Shape();
          const outline = args[0];
          const height = args[1];
          shape.autoClose = true;
          shape.moveTo(outline[0][0], outline[0][1]);
          outline.slice(1).forEach((p) => shape.lineTo(p[0], p[1]));
          const settings = { depth: height, bevelEnabled: false };
          geometry = new THREE.ExtrudeGeometry(shape, settings);
        }
        const material = new THREE.MeshPhongMaterial({ transparent: true });
        if (geometry) mesh = new THREE.Mesh(geometry, material);
      }
      if (mesh) {
        objects.set(id, mesh);
        objects.get(parent_id).add(objects.get(id));
      }
    },
    material(object_id, color, opacity) {
      const material = objects.get(object_id).material;
      if (!material) return;
      material.color.set(color);
      material.opacity = opacity;
    },
    move(object_id, x, y, z) {
      objects.get(object_id).position.set(x, y, z);
    },
    rotate(object_id, R) {
      const R4 = new THREE.Matrix4().makeBasis(
        new THREE.Vector3(...R[0]),
        new THREE.Vector3(...R[1]),
        new THREE.Vector3(...R[2])
      );
      objects.get(object_id).rotation.setFromRotationMatrix(R4.transpose());
    },
    delete(object_id) {
      objects.get(object_id).removeFromParent();
      objects.delete(object_id);
    },
  },

  props: {
    jp_props: Object,
  },
});
