import SceneLib from "nicegui-scene";
const {
  SimpleMaterialLoader,
  CSS2DRenderer,
  CSS3DRenderer,
  DragControls,
  MapControls,
  OrbitControls,
  TrackballControls,
  THREE,
  TWEEN,
  Stats,
} = SceneLib;

async function get_object(objects, object_id) {
  const object = objects.get(object_id);
  if (object === undefined) return;
  if (object.ready_promise) {
    try {
      await object.ready_promise;
    } catch {
      // the scene's `create` method already logged the failure; do nothing here
      return;
    }
  }
  return object
}

function get_managed_parent_and_fill_metadata(object) {
  // Unmanaged objects created by custom components may have children that
  // have an empty "object_id"; this will use the ID of parent for those objects
  let current_object = object;
  while (current_object) {
    if (current_object.managed) {
      object.object_id = current_object.object_id
      object.name = current_object.name
      return current_object;
    }
    current_object = current_object.parent
  }
}


export default {
  template: `
    <div style="position:relative" data-initializing>
      <canvas style="position:relative"></canvas>
      <div style="position:absolute;pointer-events:none;top:0"></div>
      <div style="position:absolute;pointer-events:none;top:0"></div>
      <div style="position:absolute;display:none;inset:0;cursor:pointer">WebGL context lost. Click to re-initialize.</div>
    </div>`,

  mounted() {
    let resolve_init;
    this.init_promise = new Promise((resolve) => {
      resolve_init = resolve;
    });

    this.objects = new Map();
    this.scene = new THREE.Scene();
    this.scene.object_id = "scene";
    this.scene.managed = true;
    this.objects.set("scene", { id: "scene", mesh: this.scene });

    this.clock = new THREE.Clock();
    this.draggable_objects = [];

    if (this.showStats) {
      this.stats = new Stats();
      this.stats.domElement.style.position = "absolute";
      this.stats.domElement.style.top = "0px";
      this.$el.appendChild(this.stats.domElement);
    }

    window["scene_" + this.$el.id] = this.scene; // NOTE: for selenium tests only

    if (this.cameraType === "perspective") {
      this.camera = new THREE.PerspectiveCamera(
        this.cameraParams.fov,
        this.width / this.height,
        this.cameraParams.near,
        this.cameraParams.far,
      );
    } else {
      this.camera = new THREE.OrthographicCamera(
        (-this.cameraParams.size / 2) * (this.width / this.height),
        (this.cameraParams.size / 2) * (this.width / this.height),
        this.cameraParams.size / 2,
        -this.cameraParams.size / 2,
        this.cameraParams.near,
        this.cameraParams.far,
      );
    }
    this.look_at = new THREE.Vector3(0, 0, 0);
    this.camera.lookAt(this.look_at);
    this.camera.up = new THREE.Vector3(0, 0, 1);
    this.camera.position.set(0, -3, 5);

    this.scene.add(new THREE.AmbientLight(0xffffff, 0.7 * Math.PI));
    const light = new THREE.DirectionalLight(0xffffff, 0.3 * Math.PI);
    light.position.set(5, 10, 40);
    this.scene.add(light);

    this.renderer = undefined;
    try {
      this.renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true,
        canvas: this.$el.children[0],
      });
    } catch {
      this.$el.innerHTML = "Could not create WebGL renderer.";
      this.$el.style.width = this.width + "px";
      this.$el.style.height = this.height + "px";
      this.$el.style.padding = "10px";
      this.$el.style.border = "1px solid silver";
      return;
    }
    this.renderer.setClearColor(this.backgroundColor);
    this.renderer.setSize(this.width, this.height);

    this.renderer.domElement.addEventListener("webglcontextlost", (event) => {
      event.preventDefault();
      this.$el.children[0].style.visibility = "hidden";
      this.$el.children[1].style.visibility = "hidden";
      this.$el.children[2].style.visibility = "hidden";
      this.$el.children[3].style.display = "block";
      this.$el.addEventListener(
        "click",
        () => {
          const elementDefinition = mounted_app.elements[this.$el.id.slice(1)];
          const originalTag = elementDefinition.tag;
          elementDefinition.tag = "";
          this.$nextTick(() => (elementDefinition.tag = originalTag));
        },
        { once: true },
      );
    });

    this.text_renderer = new CSS2DRenderer({
      element: this.$el.children[1],
    });
    this.text_renderer.setSize(this.width, this.height);

    this.text3d_renderer = new CSS3DRenderer({
      element: this.$el.children[2],
    });
    this.text3d_renderer.setSize(this.width, this.height);

    this.$nextTick(() => this.resize());
    window.addEventListener("resize", this.resize, false);
    window.addEventListener("DOMContentLoaded", this.resize, false);

    const gridSize = this.grid[0] || 100;
    const gridDivisions = this.grid[1] || 100;
    if (this.grid) {
      const ground = new THREE.Mesh(
        new THREE.PlaneGeometry(gridSize, gridSize),
        new THREE.MeshPhongMaterial({ color: this.backgroundColor }),
      );
      ground.translateZ(-0.01);
      ground.object_id = "ground";
      this.scene.add(ground);

      const grid = new THREE.GridHelper(gridSize, gridDivisions);
      grid.material.transparent = true;
      grid.material.opacity = 0.2;
      grid.rotateX(Math.PI / 2);
      this.scene.add(grid);
    }
    this.controlClass = { trackball: TrackballControls, map: MapControls }[this.controlType] || OrbitControls;
    this.controls = new this.controlClass(this.camera, this.renderer.domElement);
    this.drag_controls = new DragControls(this.draggable_objects, this.camera, this.renderer.domElement);
    this.drag_controls.transformGroup = true;
    const applyConstraint = (constraint, position) => {
      if (!constraint) return;
      const [variable, expression] = constraint.split("=").map((s) => s.trim());
      position[variable] = eval(expression.replace(/x|y|z/g, (match) => `(${position[match]})`));
    };
    const handleDrag = (event) => {
      this.dragConstraints.split(",").forEach((constraint) => applyConstraint(constraint, event.object.position));
      get_managed_parent_and_fill_metadata(event.object)
      this.$emit(event.type, {
        type: event.type,
        object_id: event.object.object_id,
        object_name: event.object.name,
        x: event.object.position.x,
        y: event.object.position.y,
        z: event.object.position.z,
      });
      if (event.type === "dragstart") this.controls.enabled = false;
      if (event.type === "dragend") this.controls.enabled = true;
    };
    this.drag_controls.addEventListener("dragstart", handleDrag);
    this.drag_controls.addEventListener("drag", handleDrag);
    this.drag_controls.addEventListener("dragend", handleDrag);

    const render = () => {
      requestAnimationFrame(() => setTimeout(() => render(), 1000 / this.fps));
      this.camera_tween?.update();
      this.controls.update(this.clock.getDelta());
      this.renderer.render(this.scene, this.camera);
      this.text_renderer.render(this.scene, this.camera);
      this.text3d_renderer.render(this.scene, this.camera);
      if (this.stats) this.stats.update();
    };
    render();

    const raycaster = new THREE.Raycaster();
    const click_handler = (mouseEvent) => {
      let x = (mouseEvent.offsetX / this.renderer.domElement.width) * 2 - 1;
      let y = -(mouseEvent.offsetY / this.renderer.domElement.height) * 2 + 1;
      raycaster.setFromCamera({ x: x, y: y }, this.camera);
      this.$emit("click3d", {
        hits: raycaster
          .intersectObjects(this.scene.children, true)
          .filter((o) => {
            return Boolean(get_managed_parent_and_fill_metadata(o.object))
          })
          .map((o) => ({
            object_id: o.object.object_id,
            object_name: o.object.name,
            point: o.point,
          })),
        click_type: mouseEvent.type,
        button: mouseEvent.button,
        alt_key: mouseEvent.altKey,
        ctrl_key: mouseEvent.ctrlKey,
        meta_key: mouseEvent.metaKey,
        shift_key: mouseEvent.shiftKey,
      });
    };
    this.clickEvents.forEach((event) => this.$el.addEventListener(event, click_handler));

    this.material_loader = new SimpleMaterialLoader();

    const connectInterval = setInterval(() => {
      if (window.socket.id === undefined) return;
      resolve_init();
      this.resize();
      this.$el.removeAttribute("data-initializing");
      this.$emit("init");
      clearInterval(connectInterval);
    }, 100);
  },

  beforeUnmount() {
    window.removeEventListener("resize", this.resize);
    window.removeEventListener("DOMContentLoaded", this.resize);
  },

  methods: {
    async create(import_name, id, parent_id, ...args) {
      // Initial bootstrapping
      let resolve_ready, reject_ready;
      const ready_promise = new Promise((resolve, reject) => {
        resolve_ready = resolve;
        reject_ready = reject;
      });
      ready_promise.catch(() => {}); // suppress unhandled rejection if no method ever accesses this object
      let object = {
        id, ready_promise
      }
      this.objects.set(id, object);
      await this.init_promise;

      try {
        // Find the component class
        let component_class;
        component_class = (await import(import_name)).default;
        const component = new component_class();

        // Create the object
        let mesh;
        if (typeof component.create_geometry == "function") {
          const wireframe = args.pop()
          const geometry = await component.create_geometry(...args)
          if (wireframe) {
            mesh = new THREE.LineSegments(
              new THREE.EdgesGeometry(geometry),
              new THREE.LineBasicMaterial({ transparent: true }),
            );
          } else {
            const material = new THREE.MeshPhongMaterial({ transparent: true });
            mesh = new THREE.Mesh(geometry, material);
          }
        }
        else if (typeof component.create_mesh == "function") {
          mesh = await component.create_mesh(...args);
        } else {
          throw new Error(`The "${component_class}" 3D component doesn't export a "create_geometry" or "create_mesh" method.`)
        }

        // Update the references and notify about creation
        mesh.object_id = id;
        mesh.managed = true;
        object.mesh = mesh
        object.component = component
        if (typeof object.component.created == "function") {
          await object.component.created();
        }
        resolve_ready();
      } catch (reason) {
        console.error(`Failed to create object (component="${import_name}", id=${id}, args=${args}): ${reason}`);
        reject_ready();
        return;
      }

      // Attach to scene
      const parent = await get_object(this.objects, parent_id);
      parent.mesh.add(object.mesh);
    },
    async name(object_id, name) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      object.mesh.name = name;
    },
    async material(object_id, color, opacity, side) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      if (typeof object.component.apply_material === "function") {
        await object.component.apply_material(color, opacity, side)
      } else if (object.mesh.material) {
        this.material_loader.apply(object.mesh.material, color, opacity, side);
      } else {
        console.warn(`A material change was requested for object ${object_id} but the mesh doesn't support materials`)
      }
    },
    async move(object_id, x, y, z) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      object.mesh.position.set(x, y, z);
    },
    async scale(object_id, sx, sy, sz) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      object.mesh.scale.set(sx, sy, sz);
    },
    async rotate(object_id, R) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      const R4 = new THREE.Matrix4().makeBasis(
        new THREE.Vector3(...R[0]),
        new THREE.Vector3(...R[1]),
        new THREE.Vector3(...R[2]),
      );
      object.mesh.rotation.setFromRotationMatrix(R4.transpose());
    },
    async visible(object_id, value) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      object.mesh.visible = value;
    },
    async draggable(object_id, value) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      if (value) this.draggable_objects.push(object.mesh);
      else {
        const index = this.draggable_objects.indexOf(object.mesh);
        if (index != -1) this.draggable_objects.splice(index, 1);
      }
    },
    async delete(object_id) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      object.mesh.removeFromParent();
      this.draggable(object_id, false)
      this.objects.delete(object_id);
    },
    async run_method_on_component(object_id, method_name, ...args) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      return await object.component[method_name](...args);
    },
    async attach(object_id, parent_id, x, y, z, R) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      const parent = await get_object(this.objects, parent_id)
      if (!parent) return;
      parent.mesh.add(object.mesh);
      this.move(object_id, x, y, z);
      this.rotate(object_id, R);
    },
    async detach(object_id, x, y, z, R) {
      const object = await get_object(this.objects, object_id)
      if (!object) return;
      object.mesh.removeFromParent();
      this.attach(object_id, this.scene.object_id, x, y, z, R)
    },
    move_camera(x, y, z, look_at_x, look_at_y, look_at_z, up_x, up_y, up_z, duration) {
      if (this.camera_tween) this.camera_tween.stop();
      const camera_up_changed = up_x !== null || up_y !== null || up_z !== null;
      this.camera_tween = new TWEEN.Tween([
        this.camera.position.x,
        this.camera.position.y,
        this.camera.position.z,
        this.camera.up.x,
        this.camera.up.y,
        this.camera.up.z,
        this.look_at.x,
        this.look_at.y,
        this.look_at.z,
      ])
        .to(
          [
            x === null ? this.camera.position.x : x,
            y === null ? this.camera.position.y : y,
            z === null ? this.camera.position.z : z,
            up_x === null ? this.camera.up.x : up_x,
            up_y === null ? this.camera.up.y : up_y,
            up_z === null ? this.camera.up.z : up_z,
            look_at_x === null ? this.look_at.x : look_at_x,
            look_at_y === null ? this.look_at.y : look_at_y,
            look_at_z === null ? this.look_at.z : look_at_z,
          ],
          duration * 1000,
        )
        .onUpdate((p) => {
          this.camera.position.set(p[0], p[1], p[2]);
          this.camera.up.set(p[3], p[4], p[5]); // before calling lookAt
          this.look_at.set(p[6], p[7], p[8]);
          this.camera.lookAt(p[6], p[7], p[8]);
          this.controls.target.set(p[6], p[7], p[8]);
        })
        .onComplete(() => {
          if (camera_up_changed) {
            this.controls.dispose();
            this.controls = new this.controlClass(this.camera, this.renderer.domElement);
            this.controls.target.copy(this.look_at);
            this.camera.lookAt(this.look_at);
          }
        })
        .start();
    },
    get_camera() {
      return {
        position: this.camera.position,
        up: this.camera.up,
        rotation: this.camera.rotation,
        quaternion: this.camera.quaternion,
        type: this.camera.type,
        fov: this.camera.fov,
        aspect: this.camera.aspect,
        near: this.camera.near,
        far: this.camera.far,
        left: this.camera.left,
        right: this.camera.right,
        top: this.camera.top,
        bottom: this.camera.bottom,
      };
    },
    resize() {
      const { clientWidth, clientHeight } = this.$el;
      this.renderer.setSize(clientWidth, clientHeight);
      this.text_renderer.setSize(clientWidth, clientHeight);
      this.text3d_renderer.setSize(clientWidth, clientHeight);
      this.camera.aspect = clientWidth / clientHeight;
      if (this.cameraType === "orthographic") {
        this.camera.left = (-this.camera.aspect * this.cameraParams.size) / 2;
        this.camera.right = (this.camera.aspect * this.cameraParams.size) / 2;
      }
      this.camera.updateProjectionMatrix();
    },
  },

  props: {
    width: Number,
    height: Number,
    grid: Object,
    cameraType: String,
    cameraParams: Object,
    clickEvents: Array,
    dragConstraints: String,
    backgroundColor: String,
    fps: Number,
    showStats: Boolean,
    controlType: String,
  },
};
