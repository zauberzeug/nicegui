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
  TransformControls,
  THREE,
  TWEEN,
  Stats,
} = SceneLib;

// Per-TransformControls axis-lock state. WeakMap keeps the entry alive only as long as the
// controls instance exists, and avoids polluting `tc.userData` (which user code may also use).
const transformAxisLocks = new WeakMap();

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
    this.transform_controls = new Map(); // object_id -> TransformControls instance
    this.dragging_count = 0;             // # of TransformControls currently being dragged
    this.userOrbitEnabled = true;        // user-intended orbit state; restored on drag end
    this.is_initialized = false;
    // Per-object pointer event substrate.
    // - interactiveObjects: three.js Object3D refs we raycast against on pointer events.
    //   Always exactly the set of objects with at least one handler registered or a hover effect set.
    // - objectHandlers: object_id -> Set<event_type> of event names the Python side is listening to.
    // - objectEffects: object_id -> {effect: 'glow'|'outline'|'tint', color: string|null} hover-effect spec.
    // - effectArtifacts: object_id -> internal three.js state used to render & tear down the effect.
    this.interactiveObjects = [];
    this.objectHandlers = new Map();
    this.objectEffects = new Map();
    this.effectArtifacts = new Map();
    this.hoveredObjectId = null;
    this._lastPointerMoveEmit = 0;

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

    // Hover-effect substrate. An effect-artifact entry holds the three.js objects that render the
    // effect, plus a snapshot of the source root's matrixWorld so we can skip per-frame syncs when
    // the source hasn't moved. Built when the source becomes hovered, torn down when un-hovered.
    this._hoverWorldPos = new THREE.Vector3();
    this._hoverWorldQuat = new THREE.Quaternion();
    this._hoverWorldScale = new THREE.Vector3();
    this._transformWP = new THREE.Vector3();

    this._buildEffectArtifact = (object_id, rootObject, spec) => {
      const color = spec.color ?? this.hoverColor ?? "#ffffff";
      if (spec.effect === "glow") {
        const group = new THREE.Group();
        rootObject.traverse((descendant) => {
          if (!descendant.isMesh || !descendant.geometry) return;
          const material = new THREE.MeshBasicMaterial({
            color,
            transparent: true,
            opacity: this.hoverOpacity ?? 0.2,
            side: THREE.BackSide,
            depthWrite: false,
          });
          const glow = new THREE.Mesh(descendant.geometry, material);
          glow.renderOrder = 999;
          glow.userData.effectSource = descendant;
          group.add(glow);
        });
        this.scene.add(group);
        return { effect: "glow", group, source: rootObject, lastMatrix: new THREE.Matrix4() };
      }
      if (spec.effect === "outline") {
        const group = new THREE.Group();
        rootObject.traverse((descendant) => {
          if (!descendant.isMesh || !descendant.geometry) return;
          const edges = new THREE.EdgesGeometry(descendant.geometry);
          const material = new THREE.LineBasicMaterial({ color, transparent: true });
          const line = new THREE.LineSegments(edges, material);
          line.renderOrder = 999;
          line.userData.effectSource = descendant;
          group.add(line);
        });
        this.scene.add(group);
        return { effect: "outline", group, source: rootObject, lastMatrix: new THREE.Matrix4() };
      }
      if (spec.effect === "tint") {
        // Per-instance material clone so shared materials aren't mutated.
        // Save the original material and the cloned-with-emissive material so we can restore on clear.
        const tinted = [];
        rootObject.traverse((descendant) => {
          if (!descendant.isMesh || !descendant.material || !descendant.material.emissive) return;
          const original = descendant.material;
          const clone = original.clone();
          clone.emissive = new THREE.Color(color);
          descendant.material = clone;
          tinted.push({ mesh: descendant, original, clone });
        });
        return { effect: "tint", tinted, source: rootObject, lastMatrix: null };
      }
      return null;
    };

    this._clearEffectArtifact = (object_id) => {
      const artifact = this.effectArtifacts.get(object_id);
      if (!artifact) return;
      if (artifact.effect === "glow" || artifact.effect === "outline") {
        for (const child of artifact.group.children) {
          if (child.material) child.material.dispose();
          if (child.geometry && artifact.effect === "outline") child.geometry.dispose();
        }
        if (artifact.group.parent) artifact.group.parent.remove(artifact.group);
      } else if (artifact.effect === "tint") {
        for (const { mesh, original, clone } of artifact.tinted) {
          if (mesh.material === clone) mesh.material = original;
          clone.dispose();
        }
      }
      this.effectArtifacts.delete(object_id);
    };

    this._syncEffectsIfDirty = () => {
      // Per-frame matrix-driven sync for glow/outline. Tint requires no sync (lives on the original mesh).
      const expansion = this.hoverScale ?? 1.05;
      for (const [object_id, artifact] of this.effectArtifacts) {
        if (artifact.effect !== "glow" && artifact.effect !== "outline") continue;
        artifact.source.updateMatrixWorld();
        if (artifact.lastMatrix.equals(artifact.source.matrixWorld)) continue;
        artifact.lastMatrix.copy(artifact.source.matrixWorld);
        for (const child of artifact.group.children) {
          const src = child.userData.effectSource;
          if (!src) continue;
          src.getWorldPosition(this._hoverWorldPos);
          src.getWorldQuaternion(this._hoverWorldQuat);
          src.getWorldScale(this._hoverWorldScale);
          child.position.copy(this._hoverWorldPos);
          child.quaternion.copy(this._hoverWorldQuat);
          if (artifact.effect === "glow") {
            child.scale.copy(this._hoverWorldScale).multiplyScalar(expansion);
          } else {
            child.scale.copy(this._hoverWorldScale);
          }
        }
      }
    };

    const render = () => {
      requestAnimationFrame(() => setTimeout(() => render(), 1000 / this.fps));
      this.camera_tween?.update();
      this.controls.update(this.clock.getDelta());
      this._syncEffectsIfDirty();
      this.renderer.render(this.scene, this.camera);
      this.text_renderer.render(this.scene, this.camera);
      this.text3d_renderer.render(this.scene, this.camera);
      if (this.stats) this.stats.update();
    };
    render();

    const raycaster = new THREE.Raycaster();

    // Walk parent chain to find the closest interactive ancestor (one we have handler/effect state for).
    const findInteractiveAncestor = (object) => {
      let obj = object;
      while (obj) {
        if (obj.object_id &&
            this.objects.has(obj.object_id) &&
            (this.objectHandlers.has(obj.object_id) || this.objectEffects.has(obj.object_id))) {
          return obj.object_id;
        }
        obj = obj.parent;
      }
      return null;
    };

    const raycastInteractive = (clientX, clientY) => {
      if (this.interactiveObjects.length === 0) return [];
      const rect = this.renderer.domElement.getBoundingClientRect();
      const x = ((clientX - rect.left) / rect.width) * 2 - 1;
      const y = -((clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera({ x, y }, this.camera);
      return raycaster.intersectObjects(this.interactiveObjects, true);
    };

    // Find the topmost interactive object_id under the cursor. Returns {id, point, localPoint} or nulls.
    const findHit = (clientX, clientY) => {
      const hits = raycastInteractive(clientX, clientY);
      for (const hit of hits) {
        const id = findInteractiveAncestor(hit.object);
        if (id) {
          const root = this.objects.get(id);
          // Local hit point: world → root local space
          const localPoint = root.worldToLocal(hit.point.clone());
          return { id, point: hit.point, localPoint };
        }
      }
      return { id: null, point: null, localPoint: null };
    };

    const buildPayload = (type, id, point, localPoint, mouseEvent) => ({
      type,
      object_id: id,
      object_name: this.objects.get(id)?.name ?? "",
      button: mouseEvent?.button ?? 0,
      alt_key: !!mouseEvent?.altKey,
      ctrl_key: !!mouseEvent?.ctrlKey,
      meta_key: !!mouseEvent?.metaKey,
      shift_key: !!mouseEvent?.shiftKey,
      x: localPoint?.x ?? 0,
      y: localPoint?.y ?? 0,
      z: localPoint?.z ?? 0,
      wx: point?.x ?? 0,
      wy: point?.y ?? 0,
      wz: point?.z ?? 0,
    });

    const emitPointerEvent = (type, id, point, localPoint, mouseEvent) => {
      if (!this.objectHandlers.get(id)?.has(type)) return;
      this.$emit("pointerevent", buildPayload(type, id, point, localPoint, mouseEvent));
    };

    this.renderer.domElement.addEventListener("pointermove", (e) => {
      if (this.interactiveObjects.length === 0 && !this.hoveredObjectId) return;
      const { id: newHoveredId, point, localPoint } = findHit(e.clientX, e.clientY);

      if (newHoveredId !== this.hoveredObjectId) {
        // Tear down effect on previously hovered object, then emit pointerout.
        if (this.hoveredObjectId) {
          this._clearEffectArtifact(this.hoveredObjectId);
          // Use empty point for pointerout — cursor has already left the object.
          emitPointerEvent("pointerout", this.hoveredObjectId, null, null, e);
        }
        // Build effect on newly hovered object, then emit pointerover.
        if (newHoveredId) {
          const spec = this.objectEffects.get(newHoveredId);
          if (spec) {
            const root = this.objects.get(newHoveredId);
            const artifact = this._buildEffectArtifact(newHoveredId, root, spec);
            if (artifact) this.effectArtifacts.set(newHoveredId, artifact);
          }
          emitPointerEvent("pointerover", newHoveredId, point, localPoint, e);
        }
        this.renderer.domElement.style.cursor = newHoveredId ? "pointer" : "";
        this.hoveredObjectId = newHoveredId;
      }

      // Continuous pointermove emission — throttled to ~60Hz to avoid websocket flooding.
      if (newHoveredId && this.objectHandlers.get(newHoveredId)?.has("pointermove")) {
        const now = performance.now();
        if (now - this._lastPointerMoveEmit > 16) {
          this._lastPointerMoveEmit = now;
          emitPointerEvent("pointermove", newHoveredId, point, localPoint, e);
        }
      }
    });

    const handlePerObjectMouseEvent = (eventType) => (e) => {
      const { id, point, localPoint } = findHit(e.clientX, e.clientY);
      if (id) {
        emitPointerEvent(eventType, id, point, localPoint, e);
      } else if (eventType === "click" || eventType === "dblclick" ||
                 eventType === "contextmenu" || eventType === "pointerdown") {
        // Scene-level pointer-missed for clicks that don't hit any interactive object.
        this.$emit("pointermissed", {
          type: eventType,
          button: e.button ?? 0,
          alt_key: !!e.altKey,
          ctrl_key: !!e.ctrlKey,
          meta_key: !!e.metaKey,
          shift_key: !!e.shiftKey,
        });
      }
    };

    this.renderer.domElement.addEventListener("pointerdown", handlePerObjectMouseEvent("pointerdown"));
    this.renderer.domElement.addEventListener("pointerup", handlePerObjectMouseEvent("pointerup"));
    this.renderer.domElement.addEventListener("click", handlePerObjectMouseEvent("click"));
    this.renderer.domElement.addEventListener("dblclick", handlePerObjectMouseEvent("dblclick"));
    this.renderer.domElement.addEventListener("contextmenu", handlePerObjectMouseEvent("contextmenu"));

    const click_handler = (mouseEvent) => {
      let x = (mouseEvent.offsetX / this.renderer.domElement.width) * 2 - 1;
      let y = -(mouseEvent.offsetY / this.renderer.domElement.height) * 2 + 1;
      raycaster.setFromCamera({ x: x, y: y }, this.camera);
      this.$emit("click3d", {
        hits: raycaster
          .intersectObjects(this.scene.children, true)
          .filter((o) => o.object.object_id)
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
    set_handler_types(object_id, types) {
      if (!this.objects.has(object_id)) return;
      const obj = this.objects.get(object_id);
      const next = Array.isArray(types) && types.length > 0 ? new Set(types) : null;
      const wasInteractive = this.objectHandlers.has(object_id) || this.objectEffects.has(object_id);
      if (next) {
        this.objectHandlers.set(object_id, next);
      } else {
        this.objectHandlers.delete(object_id);
      }
      const isInteractive = this.objectHandlers.has(object_id) || this.objectEffects.has(object_id);
      if (isInteractive && !wasInteractive) this.interactiveObjects.push(obj);
      else if (!isInteractive && wasInteractive) {
        const i = this.interactiveObjects.indexOf(obj);
        if (i !== -1) this.interactiveObjects.splice(i, 1);
        if (this.hoveredObjectId === object_id) {
          this._clearEffectArtifact(object_id);
          this.renderer.domElement.style.cursor = "";
          this.hoveredObjectId = null;
        }
      }
    },
    set_effect(object_id, effect, color) {
      if (!this.objects.has(object_id)) return;
      const obj = this.objects.get(object_id);
      const wasInteractive = this.objectHandlers.has(object_id) || this.objectEffects.has(object_id);
      if (effect === null || effect === undefined || effect === "none" || effect === false) {
        this.objectEffects.delete(object_id);
      } else {
        this.objectEffects.set(object_id, { effect, color: color ?? null });
      }
      const isInteractive = this.objectHandlers.has(object_id) || this.objectEffects.has(object_id);
      if (isInteractive && !wasInteractive) this.interactiveObjects.push(obj);
      else if (!isInteractive && wasInteractive) {
        const i = this.interactiveObjects.indexOf(obj);
        if (i !== -1) this.interactiveObjects.splice(i, 1);
      }
      // If currently hovered, rebuild artifact for the new spec (or clear if removed).
      if (this.hoveredObjectId === object_id) {
        this._clearEffectArtifact(object_id);
        const spec = this.objectEffects.get(object_id);
        if (spec) {
          const artifact = this._buildEffectArtifact(object_id, obj, spec);
          if (artifact) this.effectArtifacts.set(object_id, artifact);
        }
        if (!isInteractive) {
          this.renderer.domElement.style.cursor = "";
          this.hoveredObjectId = null;
        }
      }
    },
    has_handler(object_id, type) {
      return this.objectHandlers.get(object_id)?.has(type) ?? false;
    },
    has_effect(object_id) {
      return this.objectEffects.has(object_id);
    },
    is_interactive(object_id) {
      return this.objectHandlers.has(object_id) || this.objectEffects.has(object_id);
    },
    set_orbit_enabled(value) {
      this.userOrbitEnabled = !!value;
      // Only push to OrbitControls when no TransformControls drag is in progress.
      // Otherwise the dragging-changed handler will restore the latch when the drag ends.
      if (this.dragging_count === 0) this.controls.enabled = this.userOrbitEnabled;
    },
    enable_transform_controls(object_id, mode, size, visible_axes, space, rotation_snap) {
      if (!this.objects.has(object_id)) return false;
      // Reuse existing controls if already attached: just update mode / size / axes / space / snap.
      const existing = this.transform_controls.get(object_id);
      if (existing) {
        existing.setMode(mode);
        if (size !== undefined && size !== null) existing.setSize(size);
        if (space !== undefined && space !== null) existing.setSpace(space);
        if (rotation_snap !== undefined && rotation_snap !== null) existing.setRotationSnap(rotation_snap);
        this._applyTransformAxes(existing, mode, visible_axes);
        return true;
      }
      const object = this.objects.get(object_id);
      const tc = new TransformControls(this.camera, this.renderer.domElement);
      tc.attach(object);
      tc.setMode(mode);
      if (size !== undefined && size !== null) tc.setSize(size);
      if (space !== undefined && space !== null) tc.setSpace(space);
      if (rotation_snap !== undefined && rotation_snap !== null) tc.setRotationSnap(rotation_snap);
      this._applyTransformAxes(tc, mode, visible_axes);
      let isDragging = false;
      tc.addEventListener("dragging-changed", (event) => {
        isDragging = event.value;
        if (event.value) {
          this.dragging_count++;
          if (this.dragging_count === 1) this.controls.enabled = false;
        } else {
          this.dragging_count = Math.max(0, this.dragging_count - 1);
          // Restore to the user-intended orbit state, NOT unconditionally `true` —
          // otherwise a drag re-enables orbit even if the user disabled it via set_orbit_enabled.
          if (this.dragging_count === 0) this.controls.enabled = this.userOrbitEnabled;
        }
      });
      const emitTransform = (type) => {
        object.getWorldPosition(this._transformWP);
        this.$emit(type, {
          type,
          mode: tc.mode,
          object_id,
          object_name: object.name,
          x: object.position.x,
          y: object.position.y,
          z: object.position.z,
          rx: object.rotation.x,
          ry: object.rotation.y,
          rz: object.rotation.z,
          wx: this._transformWP.x,
          wy: this._transformWP.y,
          wz: this._transformWP.z,
        });
      };
      tc.addEventListener("change", () => {
        if (!isDragging) return;
        const lockAxis = transformAxisLocks.get(tc);
        if (tc.mode === "rotate" && lockAxis && tc.axis !== lockAxis) tc.axis = lockAxis;
        emitTransform("transform");
      });
      tc.addEventListener("mouseDown", () => {
        const lockAxis = transformAxisLocks.get(tc);
        if (lockAxis) tc.axis = lockAxis;
        emitTransform("transform_start");
      });
      tc.addEventListener("mouseUp", () => emitTransform("transform_end"));
      this.scene.add(tc.getHelper());
      tc.getHelper().traverse((child) => {
        child.object_id = `transformcontrols:${object_id}`;
      });
      this.transform_controls.set(object_id, tc);
      return true;
    },
    _applyTransformAxes(tc, mode, visible_axes) {
      if (visible_axes === undefined || visible_axes === null) {
        tc.showX = tc.showY = tc.showZ = true;
        transformAxisLocks.delete(tc);
        return;
      }
      tc.showX = visible_axes.includes("X");
      tc.showY = visible_axes.includes("Y");
      tc.showZ = visible_axes.includes("Z");
      if (mode === "rotate" && visible_axes.length === 1) {
        const axis = visible_axes[0];
        transformAxisLocks.set(tc, axis);
        tc.axis = axis;
      } else {
        transformAxisLocks.delete(tc);
      }
    },
    disable_transform_controls(object_id) {
      const tc = this.transform_controls.get(object_id);
      if (!tc) return;
      if (tc.dragging) {
        this.dragging_count = Math.max(0, this.dragging_count - 1);
      }
      tc.detach();
      this.scene.remove(tc.getHelper());
      tc.dispose();
      transformAxisLocks.delete(tc);
      this.transform_controls.delete(object_id);
      if (this.dragging_count === 0) this.controls.enabled = this.userOrbitEnabled;
    },
    set_transform_mode(object_id, mode) {
      const tc = this.transform_controls.get(object_id);
      if (tc) tc.setMode(mode);
    },
    set_transform_size(object_id, size) {
      const tc = this.transform_controls.get(object_id);
      if (tc) tc.setSize(size);
    },
    set_transform_space(object_id, space) {
      const tc = this.transform_controls.get(object_id);
      if (tc) tc.setSpace(space);
    },
    set_transform_rotation_snap(object_id, radians) {
      const tc = this.transform_controls.get(object_id);
      if (tc) tc.setRotationSnap(radians);
    },
    has_transform_controls(object_id) {
      return this.transform_controls.has(object_id);
    },
    delete(object_id) {
      if (!this.objects.has(object_id)) return;
      const object = this.objects.get(object_id);
      // Tear down any TransformControls attached to this object so the gizmo doesn't outlive the target.
      if (this.transform_controls.has(object_id)) {
        this.disable_transform_controls(object_id);
      }
      // If the deleted object was hovered, tear down its effect and reset cursor.
      if (this.hoveredObjectId === object_id) {
        this._clearEffectArtifact(object_id);
        this.renderer.domElement.style.cursor = "";
        this.hoveredObjectId = null;
      }
      // Drop interactive state for this object.
      this.objectHandlers.delete(object_id);
      this.objectEffects.delete(object_id);
      const interactiveIndex = this.interactiveObjects.indexOf(object);
      if (interactiveIndex !== -1) this.interactiveObjects.splice(interactiveIndex, 1);
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
        interactive, // optional trailing field: {handlers?: string[], effect?: {effect, color}}
      ] of data) {
        this.create(type, id, parent_id, ...args);
        this.name(id, name);
        this.material(id, color, opacity, side);
        this.move(id, x, y, z);
        this.rotate(id, R);
        this.scale(id, sx, sy, sz);
        this.visible(id, visible);
        this.draggable(id, draggable);
        if (interactive) {
          if (interactive.handlers) this.set_handler_types(id, interactive.handlers);
          if (interactive.effect) this.set_effect(id, interactive.effect.effect, interactive.effect.color);
        }
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
    hoverColor: String,
    hoverOpacity: Number,
    hoverScale: Number,
  },
};
