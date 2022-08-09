var scene;
var look_at;
var camera;
var camera_tween;
var orbitControls;
var texture_loader = new THREE.TextureLoader();
var stl_loader = new THREE.STLLoader();
var objects = new Map();

const None = null;
const False = false;
const True = true;

function texture_geometry(coords) {
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
      if (coords[j][i] && coords[j][i + 1] && coords[j + 1][i] && coords[j + 1][i + 1]) {
        const idx00 = i + j * nI;
        const idx10 = i + j * nI + 1;
        const idx01 = i + j * nI + nI;
        const idx11 = i + j * nI + 1 + nI;
        indices.push(idx10, idx00, idx01);
        indices.push(idx11, idx10, idx01);
      }
    }
  }
  geometry.setIndex(new THREE.Uint32BufferAttribute(indices, 1));
  geometry.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
  geometry.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
  geometry.computeVertexNormals();
  geometry.computeFaceNormals();
  return geometry;
}

function texture_material(texture) {
  texture.flipY = false;
  texture.minFilter = THREE.LinearFilter;
  return new THREE.MeshLambertMaterial({
    map: texture,
    side: THREE.DoubleSide,
  });
}

Vue.component("scene", {
  template: `
    <div v-bind:id="jp_props.id" style="position:relative">
      <canvas style="position:relative"></canvas>
      <div style="position:absolute;pointer-events:none;top:0"></div>
      <div style="position:absolute;pointer-events:none;top:0"></div>
    </div>`,

  mounted() {
    scene = new THREE.Scene();
    objects.set("scene", scene);

    const width = this.$props.jp_props.options.width;
    const height = this.$props.jp_props.options.height;

    look_at = new THREE.Vector3(0, 0, 0);
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.lookAt(look_at);
    camera.up = new THREE.Vector3(0, 0, 1);
    camera.position.set(0, -3, 5);

    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const light = new THREE.DirectionalLight(0xffffff, 0.3);
    light.position.set(5, 10, 40);
    scene.add(light);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      canvas: document.getElementById(this.$props.jp_props.id).children[0],
    });
    renderer.setClearColor("#eee");
    renderer.setSize(width, height);

    const text_renderer = new THREE.CSS2DRenderer({
      element: document.getElementById(this.$props.jp_props.id).children[1],
    });
    text_renderer.setSize(width, height);

    const text3d_renderer = new THREE.CSS3DRenderer({
      element: document.getElementById(this.$props.jp_props.id).children[2],
    });
    text3d_renderer.setSize(width, height);

    const ground = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), new THREE.MeshPhongMaterial({ color: "#eee" }));
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
      TWEEN.update();
      renderer.render(scene, camera);
      text_renderer.render(scene, camera);
      text3d_renderer.render(scene, camera);
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
      } else if (type == "text") {
        const div = document.createElement("div");
        div.textContent = args[0];
        div.style.cssText = args[1];
        mesh = new THREE.CSS2DObject(div);
      } else if (type == "text3d") {
        const div = document.createElement("div");
        div.textContent = args[0];
        div.style.cssText = "userSelect:none;" + args[1];
        mesh = new THREE.CSS3DObject(div);
      } else if (type == "texture") {
        const url = args[0];
        const coords = args[1];
        const geometry = texture_geometry(coords);
        const material = texture_material(texture_loader.load(url));
        mesh = new THREE.Mesh(geometry, material);
      } else if (type == "spot_light") {
        mesh = new THREE.Group();
        const light = new THREE.SpotLight(...args);
        light.position.set(0, 0, 0);
        light.target = new THREE.Object3D();
        light.target.position.set(1, 0, 0);
        mesh.add(light);
        mesh.add(light.target);
      } else {
        let geometry;
        const wireframe = args.pop();
        if (type == "box") geometry = new THREE.BoxGeometry(...args);
        if (type == "sphere") geometry = new THREE.SphereGeometry(...args);
        if (type == "cylinder") geometry = new THREE.CylinderGeometry(...args);
        if (type == "ring") geometry = new THREE.RingGeometry(...args);
        if (type == "quadratic_bezier_tube") {
          const curve = new THREE.QuadraticBezierCurve3(
            new THREE.Vector3(...args[0]),
            new THREE.Vector3(...args[1]),
            new THREE.Vector3(...args[2])
          );
          geometry = new THREE.TubeGeometry(curve, ...args.slice(3));
        }
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
    material(object_id, color, opacity, side) {
      const material = objects.get(object_id).material;
      if (!material) return;
      material.color.set(color);
      material.opacity = opacity;
      if (side == "front") material.side = THREE.FrontSide;
      else if (side == "back") material.side = THREE.BackSide;
      else material.side = THREE.DoubleSide;
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
    visible(object_id, value) {
      objects.get(object_id).visible = value;
    },
    delete(object_id) {
      objects.get(object_id).removeFromParent();
      objects.delete(object_id);
    },
    set_texture_url(object_id, url) {
      const obj = objects.get(object_id);
      if (obj.busy) return;
      obj.busy = true;
      const on_success = (texture) => {
        obj.material = texture_material(texture);
        obj.busy = false;
      };
      const on_error = () => (obj.busy = false);
      texture_loader.load(url, on_success, undefined, on_error);
    },
    set_texture_coordinates(object_id, coords) {
      objects.get(object_id).geometry = texture_geometry(coords);
    },
    move_camera(x, y, z, look_at_x, look_at_y, look_at_z, up_x, up_y, up_z, duration) {
      if (camera_tween) camera_tween.stop();
      camera_tween = new TWEEN.Tween([
        camera.position.x,
        camera.position.y,
        camera.position.z,
        camera.up.x,
        camera.up.y,
        camera.up.z,
        look_at.x,
        look_at.y,
        look_at.z,
      ])
        .to(
          [
            x === null ? camera.position.x : x,
            y === null ? camera.position.y : y,
            z === null ? camera.position.z : z,
            up_x === null ? camera.up.x : up_x,
            up_y === null ? camera.up.y : up_y,
            up_z === null ? camera.up.z : up_z,
            look_at_x === null ? look_at.x : look_at_x,
            look_at_y === null ? look_at.y : look_at_y,
            look_at_z === null ? look_at.z : look_at_z,
          ],
          duration * 1000
        )
        .onUpdate((p) => {
          camera.position.set(p[0], p[1], p[2]);
          camera.up.set(p[3], p[4], p[5]); // NOTE: before calling lookAt
          look_at.set(p[6], p[7], p[8]);
          camera.lookAt(p[6], p[7], p[8]);
        })
        .start();
    },
  },

  props: {
    jp_props: Object,
  },
});
