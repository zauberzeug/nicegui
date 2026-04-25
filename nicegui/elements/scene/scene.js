import SceneLib from "nicegui-scene";
const {
  CSS2DObject,
  CSS2DRenderer,
  CSS3DObject,
  CSS3DRenderer,
  DragControls,
  GLTFLoader,
  MapControls,
  OrbitControls,
  TrackballControls,
  STLLoader,
  ViewHelper,
  THREE,
  TWEEN,
  Stats,
} = SceneLib;

const INTERSECTION_AXIS_NORMALS = {
  x: new THREE.Vector3(1, 0, 0),
  y: new THREE.Vector3(0, 1, 0),
  z: new THREE.Vector3(0, 0, 1),
};

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
  return geometry;
}

function texture_material(texture) {
  texture.flipY = false;
  texture.minFilter = THREE.LinearFilter;
  return new THREE.MeshLambertMaterial({
    map: texture,
    side: THREE.DoubleSide,
    transparent: true,
  });
}

function set_point_cloud_data(position, color, geometry) {
  geometry.setAttribute("position", new THREE.Float32BufferAttribute(position.flat(), 3));
  if (color === null) {
    geometry.deleteAttribute("color");
  } else {
    geometry.setAttribute("color", new THREE.Float32BufferAttribute(color.flat(), 3));
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
    this.scene = new THREE.Scene();
    this.clock = new THREE.Clock();
    this.objects = new Map();
    this.objects.set("scene", this.scene);
    this.draggable_objects = [];
    this.is_initialized = false;

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

    // Pre-compute THREE.Plane objects for the configured intersection planes (rebuilt by setter).
    // Clone the normal so the per-axis singleton in INTERSECTION_AXIS_NORMALS is never mutated
    // (intersectPlane doesn't mutate today, but normalize/applyMatrix4 in a future caller would).
    this._buildIntersectionPlanes = () => {
      const specs = this.intersectionPlanes || [];
      this._intersectionPlanes = specs.map((spec) => {
        const normal = (INTERSECTION_AXIS_NORMALS[spec.axis] || INTERSECTION_AXIS_NORMALS.z).clone();
        return { name: spec.name, plane: new THREE.Plane(normal, -(spec.offset || 0)) };
      });
    };
    this._buildIntersectionPlanes();

    const render = () => {
      requestAnimationFrame(() => setTimeout(() => render(), 1000 / this.fps));
      this.camera_tween?.update();
      const delta = this.clock.getDelta();
      this.controls.update(delta);
      this.renderer.render(this.scene, this.camera);
      this.text_renderer.render(this.scene, this.camera);
      this.text3d_renderer.render(this.scene, this.camera);
      // Orientation inset: composite the ViewHelper into the configured corner using manual
      // viewport + scissor math (works on three.js < r184 which lacks `viewHelper.location`).
      // Only the inset path narrows the viewport, so the post-render reset below is sufficient
      // — no per-frame work when the inset isn't enabled.
      if (this.viewHelper) {
        const canvas = this.renderer.domElement;
        const opts = this._axes || {};
        const dpr = this.renderer.getPixelRatio();
        const sizePx = (opts.size ?? 128) * dpr;
        const mx = ((opts.marginX ?? opts.margin) ?? 0) * dpr;
        const my = ((opts.marginY ?? opts.margin) ?? 0) * dpr;
        const anchor = opts.anchor || "bottom-right";
        const x = anchor.includes("left") ? mx : canvas.width - sizePx - mx;
        // WebGL's viewport origin is bottom-left, so "top" anchors compute y from the top edge.
        const y = anchor.includes("top") ? canvas.height - sizePx - my : my;
        this.renderer.setViewport(x, y, sizePx, sizePx);
        this.renderer.setScissor(x, y, sizePx, sizePx);
        this.renderer.setScissorTest(true);
        const autoClear = this.renderer.autoClear;
        this.renderer.autoClear = false;
        this.viewHelper.render(this.renderer);
        this.renderer.autoClear = autoClear;
        this.renderer.setScissorTest(false);
        this.renderer.setViewport(0, 0, canvas.width, canvas.height);
        if (this.viewHelper.animating) this.viewHelper.update(delta);
      }
      if (this.stats) this.stats.update();
    };
    render();

    const raycaster = new THREE.Raycaster();
    raycaster.params.Line.threshold = this.raycasterThreshold ?? 1.0;
    raycaster.params.Points.threshold = this.raycasterThreshold ?? 1.0;
    this._raycaster = raycaster;
    const _intersection = new THREE.Vector3();
    // Forward pointerdown to viewHelper.handleClick so clicking an X/Y/Z axis sprite snap-animates
    // the camera. r180's handleClick has hardcoded `dim = 128` and assumes the inset is at the
    // canvas's bottom-right corner; we render the inset wherever the user configured (manual
    // scissor math), so we synthesize event coordinates that make handleClick's hardcoded math
    // compute the NDC of the click within OUR actual inset rect.
    //
    // _consumeNextClick is cleared on every pointerdown so a stale flag from an aborted gesture
    // (drag-out before pointerup) can't suppress an unrelated later click.
    const HANDLE_CLICK_DIM = 128;
    const dispatchInsetClick = (event) => {
      if (!this.viewHelper) return false;
      const canvas = this.renderer.domElement;
      const opts = this._axes || {};
      const insetSize = opts.size ?? 128;
      const marginX = (opts.marginX ?? opts.margin) ?? 0;
      const marginY = (opts.marginY ?? opts.margin) ?? 0;
      const anchor = opts.anchor || "bottom-right";
      const insetLeft = anchor.includes("left") ? marginX : canvas.clientWidth - insetSize - marginX;
      const insetTop = anchor.includes("top") ? marginY : canvas.clientHeight - insetSize - marginY;
      const localX = event.offsetX - insetLeft;
      const localY = event.offsetY - insetTop;
      if (localX < 0 || localX >= insetSize || localY < 0 || localY >= insetSize) return false;
      // NDC of the click within the inset rect, then back-project into the (clientX, clientY) that
      // r180's bottom-right/dim=128 handleClick math would have to read to derive that same NDC.
      const nx = (localX / insetSize) * 2 - 1;
      const ny = -((localY / insetSize) * 2 - 1);
      const rect = canvas.getBoundingClientRect();
      const fakeClientX = rect.left + (canvas.offsetWidth - HANDLE_CLICK_DIM) + ((nx + 1) / 2) * HANDLE_CLICK_DIM;
      const fakeClientY = rect.top + (canvas.offsetHeight - HANDLE_CLICK_DIM) + ((1 - ny) / 2) * HANDLE_CLICK_DIM;
      return this.viewHelper.handleClick({ clientX: fakeClientX, clientY: fakeClientY });
    };
    let _consumeNextClick = false;
    // Capture-phase + stopImmediatePropagation so we beat OrbitControls'/DragControls'
    // pointerdown listeners (registered earlier on the same element) and they don't try to
    // setPointerCapture / start a drag-rotate on what was meant to be an inset axis click.
    this.renderer.domElement.addEventListener("pointerdown", (event) => {
      _consumeNextClick = false;
      if (dispatchInsetClick(event)) {
        event.stopImmediatePropagation();
        _consumeNextClick = true;
      }
    }, true);
    const click_handler = (mouseEvent) => {
      if (_consumeNextClick) {
        _consumeNextClick = false;
        return;
      }
      const x = (mouseEvent.offsetX / this.renderer.domElement.width) * 2 - 1;
      const y = -(mouseEvent.offsetY / this.renderer.domElement.height) * 2 + 1;
      raycaster.setFromCamera({ x, y }, this.camera);
      const intersections = {};
      for (const { name, plane } of this._intersectionPlanes) {
        const hit = raycaster.ray.intersectPlane(plane, _intersection);
        intersections[name] = hit ? { x: _intersection.x, y: _intersection.y, z: _intersection.z } : null;
      }
      this.$emit("click3d", {
        hits: raycaster
          .intersectObjects(this.scene.children, true)
          .filter((o) => o.object.object_id)
          .map((o) => ({
            object_id: o.object.object_id,
            object_name: o.object.name,
            point: o.point,
          })),
        intersections,
        click_type: mouseEvent.type,
        button: mouseEvent.button,
        alt_key: mouseEvent.altKey,
        ctrl_key: mouseEvent.ctrlKey,
        meta_key: mouseEvent.metaKey,
        shift_key: mouseEvent.shiftKey,
      });
    };
    this.clickEvents.forEach((event) => this.$el.addEventListener(event, click_handler));

    this.texture_loader = new THREE.TextureLoader();
    this.stl_loader = new STLLoader();
    this.gltf_loader = new GLTFLoader();

    const connectInterval = setInterval(() => {
      if (window.socket.id === undefined) return;
      this.$emit("init");
      clearInterval(connectInterval);
    }, 100);
  },

  beforeUnmount() {
    window.removeEventListener("resize", this.resize);
    window.removeEventListener("DOMContentLoaded", this.resize);
  },

  methods: {
    create(type, id, parent_id, ...args) {
      if (!this.is_initialized) return;
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
          new THREE.Vector3(...args[3]),
        );
        const points = curve.getPoints(args[4] - 1);
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({ transparent: true });
        mesh = new THREE.Line(geometry, material);
      } else if (type == "text") {
        const div = document.createElement("div");
        div.textContent = args[0];
        div.style.cssText = args[1];
        mesh = new CSS2DObject(div);
      } else if (type == "text3d") {
        const div = document.createElement("div");
        div.textContent = args[0];
        div.style.cssText = "userSelect:none;" + args[1];
        mesh = new CSS3DObject(div);
      } else if (type == "texture") {
        const url = args[0];
        const coords = args[1];
        const geometry = texture_geometry(coords);
        const material = texture_material(this.texture_loader.load(url));
        mesh = new THREE.Mesh(geometry, material);
      } else if (type == "spot_light") {
        mesh = new THREE.Group();
        const light = new THREE.SpotLight(...args);
        light.position.set(0, 0, 0);
        light.target = new THREE.Object3D();
        light.target.position.set(1, 0, 0);
        mesh.add(light);
        mesh.add(light.target);
      } else if (type == "point_cloud") {
        const geometry = new THREE.BufferGeometry();
        const material = new THREE.PointsMaterial({ size: args[2], transparent: true });
        set_point_cloud_data(args[0], args[1], geometry);
        mesh = new THREE.Points(geometry, material);
      } else if (type == "gltf") {
        const url = args[0];
        mesh = new THREE.Group();
        this.gltf_loader.load(
          url,
          (gltf) => mesh.add(gltf.scene),
          undefined,
          (error) => console.error(error),
        );
      } else if (type == "axes_helper") {
        mesh = new THREE.AxesHelper(args[0]);
        mesh.material.transparent = true;
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
            new THREE.Vector3(...args[2]),
          );
          geometry = new THREE.TubeGeometry(curve, ...args.slice(3));
        }
        if (type == "extrusion") {
          const shape = new THREE.Shape();
          const outline = args[0];
          const height = args[1];
          shape.autoClose = true;
          if (outline.length) {
            shape.moveTo(outline[0][0], outline[0][1]);
            outline.slice(1).forEach((p) => shape.lineTo(p[0], p[1]));
          }
          const settings = { depth: height, bevelEnabled: false };
          geometry = new THREE.ExtrudeGeometry(shape, settings);
        }
        if (type == "stl") {
          const url = args[0];
          geometry = new THREE.BufferGeometry();
          this.stl_loader.load(url, (geometry) => (mesh.geometry = geometry));
        }
        let material;
        if (wireframe) {
          mesh = new THREE.LineSegments(
            new THREE.EdgesGeometry(geometry),
            new THREE.LineBasicMaterial({ transparent: true }),
          );
        } else {
          material = new THREE.MeshPhongMaterial({ transparent: true });
          mesh = new THREE.Mesh(geometry, material);
        }
      }
      mesh.object_id = id;
      this.objects.set(id, mesh);
      this.objects.get(parent_id).add(this.objects.get(id));
    },
    name(object_id, name) {
      if (!this.objects.has(object_id)) return;
      this.objects.get(object_id).name = name;
    },
    material(object_id, color, opacity, side) {
      if (!this.objects.has(object_id)) return;
      const material = this.objects.get(object_id).material;
      if (!material) return;
      const vertexColors = color === null;
      material.color.set(vertexColors ? "#ffffff" : color);
      material.needsUpdate = material.vertexColors != vertexColors;
      material.vertexColors = vertexColors;
      material.opacity = opacity;
      if (side == "front") material.side = THREE.FrontSide;
      else if (side == "back") material.side = THREE.BackSide;
      else material.side = THREE.DoubleSide;
    },
    move(object_id, x, y, z) {
      if (!this.objects.has(object_id)) return;
      this.objects.get(object_id).position.set(x, y, z);
    },
    scale(object_id, sx, sy, sz) {
      if (!this.objects.has(object_id)) return;
      this.objects.get(object_id).scale.set(sx, sy, sz);
    },
    rotate(object_id, R) {
      if (!this.objects.has(object_id)) return;
      const R4 = new THREE.Matrix4().makeBasis(
        new THREE.Vector3(...R[0]),
        new THREE.Vector3(...R[1]),
        new THREE.Vector3(...R[2]),
      );
      this.objects.get(object_id).rotation.setFromRotationMatrix(R4.transpose());
    },
    visible(object_id, value) {
      if (!this.objects.has(object_id)) return;
      this.objects.get(object_id).visible = value;
    },
    draggable(object_id, value) {
      if (!this.objects.has(object_id)) return;
      const object = this.objects.get(object_id);
      if (value) this.draggable_objects.push(object);
      else {
        const index = this.draggable_objects.indexOf(object);
        if (index != -1) this.draggable_objects.splice(index, 1);
      }
    },
    set_clipping_planes(object_id, planes) {
      if (!this.objects.has(object_id)) return;
      const clipPlanes = planes.map((p) =>
        new THREE.Plane(new THREE.Vector3(p.nx, p.ny, p.nz).normalize(), p.d));
      this.objects.get(object_id).traverse((child) => {
        if (!child.material) return;
        const mats = Array.isArray(child.material) ? child.material : [child.material];
        mats.forEach((mat) => {
          mat.clippingPlanes = clipPlanes;
          mat.clipIntersection = false; // union: clip where ANY plane clips
          mat.needsUpdate = true;
        });
      });
      // Local clipping is opt-in on the renderer; flip it the first time anyone sets clipping planes.
      this.renderer.localClippingEnabled = true;
    },
    clear_clipping_planes(object_id) {
      if (!this.objects.has(object_id)) return;
      this.objects.get(object_id).traverse((child) => {
        if (!child.material) return;
        const mats = Array.isArray(child.material) ? child.material : [child.material];
        mats.forEach((mat) => {
          mat.clippingPlanes = null;
          mat.needsUpdate = true;
        });
      });
    },
    set_axes_inset(opts) {
      this._axes = opts || {};
      if (this._axes.enabled) {
        if (!this.viewHelper) {
          this.viewHelper = new ViewHelper(this.camera, this.renderer.domElement);
          if (this.controls && this.controls.target) this.viewHelper.center = this.controls.target;
          // Re-apply previously configured labels/style — toggling enabled=False then True
          // disposes the helper, so labels would otherwise reset to the unlabeled default.
          if (this._axesLabels && this._axesLabels.enabled) this.set_axes_labels(this._axesLabels);
        }
      } else if (this.viewHelper) {
        if (this.viewHelper.dispose) this.viewHelper.dispose();
        this.viewHelper = null;
      }
    },
    set_axes_labels(opts) {
      this._axesLabels = opts;
      if (!this.viewHelper || !opts || !opts.enabled) return;
      const labels = Array.isArray(opts.labels) && opts.labels.length === 3
        ? opts.labels
        : ["X", "Y", "Z"];
      // Style first, then labels — both call updateLabels() internally and the label canvas
      // reads font/color/radius at paint time (see r180 ViewHelper.js getSpriteMaterial).
      this.viewHelper.setLabelStyle(opts.font ?? "24px Arial", opts.color ?? "#000000", opts.radius ?? 14);
      this.viewHelper.setLabels(labels[0], labels[1], labels[2]);
    },
    delete(object_id) {
      if (!this.objects.has(object_id)) return;
      const object = this.objects.get(object_id);
      object.removeFromParent();
      this.objects.delete(object_id);
      const index = this.draggable_objects.indexOf(object);
      if (index != -1) this.draggable_objects.splice(index, 1);
    },
    set_texture_url(object_id, url) {
      if (!this.objects.has(object_id)) return;
      const obj = this.objects.get(object_id);
      if (obj.busy) return;
      obj.busy = true;
      const on_success = (texture) => {
        obj.material = texture_material(texture);
        obj.busy = false;
      };
      const on_error = () => (obj.busy = false);
      this.texture_loader.load(url, on_success, undefined, on_error);
    },
    set_texture_coordinates(object_id, coords) {
      if (!this.objects.has(object_id)) return;
      this.objects.get(object_id).geometry = texture_geometry(coords);
    },
    set_points(object_id, position, color) {
      if (!this.objects.has(object_id)) return;
      const geometry = this.objects.get(object_id).geometry;
      set_point_cloud_data(position, color, geometry);
    },
    attach(object_id, parent_id, x, y, z, R) {
      if (!this.objects.has(object_id)) return;
      const object = this.objects.get(object_id);
      const parent = this.objects.get(parent_id);
      parent.add(object);
      this.move(object_id, x, y, z);
      this.rotate(object_id, R);
    },
    detach(object_id, x, y, z, R) {
      if (!this.objects.has(object_id)) return;
      const object = this.objects.get(object_id);
      object.removeFromParent();
      this.scene.add(object);
      this.move(object_id, x, y, z);
      this.rotate(object_id, R);
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
          this.camera.up.set(p[3], p[4], p[5]); // NOTE: before calling lookAt
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
    init_objects(data) {
      this.resize();
      this.$el.removeAttribute("data-initializing");
      this.is_initialized = true;
      for (const [
        type,
        id,
        parent_id,
        args,
        name,
        color,
        opacity,
        side,
        x,
        y,
        z,
        R,
        sx,
        sy,
        sz,
        visible,
        draggable,
      ] of data) {
        this.create(type, id, parent_id, ...args);
        this.name(id, name);
        this.material(id, color, opacity, side);
        this.move(id, x, y, z);
        this.rotate(id, R);
        this.scale(id, sx, sy, sz);
        this.visible(id, visible);
        this.draggable(id, draggable);
      }
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
    raycasterThreshold: Number,
    intersectionPlanes: Array,
  },
  watch: {
    raycasterThreshold(value) {
      if (!this._raycaster) return;
      const t = value ?? 1.0;
      this._raycaster.params.Line.threshold = t;
      this._raycaster.params.Points.threshold = t;
    },
    intersectionPlanes() {
      if (this._buildIntersectionPlanes) this._buildIntersectionPlanes();
    },
  },
};
