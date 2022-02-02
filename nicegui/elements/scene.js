var scene;
var camera;
var orbitControls;
var texture_loader = new THREE.TextureLoader();
var stl_loader = new THREE.STLLoader();
var objects = new Map();

const None = null;
const False = false;
const True = true;

Vue.component("scene", {
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
    ground.object_id = "ground";
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
        hits: raycaster
          .intersectObjects(scene.children, true)
          .filter((o) => o.object.object_id)
          .map((o) => ({
            object_id: o.object.object_id,
            point: o.point,
          })),
        click_type: mouseEvent.type,
        shift_key: mouseEvent.shiftKey,
      };
      send_to_server(event, "event");
    };
    document.getElementById(this.$props.jp_props.id).onclick = click_handler;
    document.getElementById(this.$props.jp_props.id).ondblclick = click_handler;

    comp_dict[this.$props.jp_props.id] = this;

    const sendConnectEvent = () => {
      if (websocket_id === "") return;
      const event = {
        event_type: "onConnect",
        vue_type: this.$props.jp_props.vue_type,
        id: this.$props.jp_props.id,
        page_id: page_id,
        websocket_id: websocket_id,
      };
      send_to_server(event, "event");
      clearInterval(connectInterval);
    };
    const connectInterval = setInterval(sendConnectEvent, 100);
  },

  updated() {},

  methods: {
    create(type, id, parent_id, ...args) {
      let mesh;
      if (type == "group") {
        mesh = new THREE.Group();
      } else if (type == "line") {
        const start = new THREE.Vector3(...args[0]);
        const end = new THREE.Vector3(...args[1]);
        const geometry = new THREE.BufferGeometry().setFromPoints([start, end]);
        const material = new THREE.LineBasicMaterial({ transparent: true });
        mesh = new THREE.Line(geometry, material);
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
      } else if (type == "texture") {
        const url = args[0];
        const coords = args[1];
        const geometry = new THREE.BufferGeometry();
        const nI = coords[0].length;
        const nJ = coords.length;
        const vertices = [];
        const indices = [];
        const uvs = [];
        for (let j = 0; j < nJ; ++j) {
          for (let i = 0; i < nI; ++i) {
            const XYZ = coords[j][i] || [0, 0, 0];
            vertices.push(...XYZ);
            uvs.push(i / (nI - 1), j / (nJ - 1));
          }
        }
        for (let j = 0; j < nJ - 1; ++j) {
          for (let i = 0; i < nI - 1; ++i) {
            if (
              coords[j][i] &&
              coords[j][i + 1] &&
              coords[j + 1][i] &&
              coords[j + 1][i + 1]
            ) {
              const idx00 = i + j * nI;
              const idx10 = i + j * nI + 1;
              const idx01 = i + j * nI + nI;
              const idx11 = i + j * nI + 1 + nI;
              indices.push(idx00, idx10, idx01);
              indices.push(idx10, idx11, idx01);
            }
          }
        }
        geometry.setIndex(new THREE.Uint32BufferAttribute(indices, 1));
        geometry.setAttribute(
          "position",
          new THREE.Float32BufferAttribute(vertices, 3)
        );
        geometry.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
        geometry.computeVertexNormals();
        geometry.computeFaceNormals();
        const texture = texture_loader.load(url);
        texture.flipY = false;
        texture.minFilter = THREE.LinearFilter;
        const material = new THREE.MeshLambertMaterial({
          map: texture,
          side: THREE.DoubleSide,
        });
        mesh = new THREE.Mesh(geometry, material);
      } else {
        let geometry;
        const wireframe = args.pop();
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
        if (type == "stl") {
          const url = args[0];
          geometry = new THREE.BufferGeometry();
          stl_loader.load(url, (geometry) => (mesh.geometry = geometry));
        }
        let material;
        if (wireframe) {
          mesh = new THREE.LineSegments(
            new THREE.EdgesGeometry(geometry),
            new THREE.LineBasicMaterial({ transparent: true })
          );
        } else {
          material = new THREE.MeshPhongMaterial({ transparent: true });
          mesh = new THREE.Mesh(geometry, material);
        }
      }
      mesh.object_id = id;
      objects.set(id, mesh);
      objects.get(parent_id).add(objects.get(id));
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
    scale(object_id, sx, sy, sz) {
      objects.get(object_id).scale.set(sx, sy, sz);
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
