import * as THREE from "three";

export default {
  template: `
    <div style="position:relative">
      <canvas style="position:relative"></canvas>
    </div>`,

  async mounted() {
    await this.$nextTick();
    this.scene = getElement(this.scene_id).scene;

    if (this.camera_type === "perspective") {
      this.camera = new THREE.PerspectiveCamera(
        this.camera_params.fov,
        this.width / this.height,
        this.camera_params.near,
        this.camera_params.far
      );
    } else {
      this.camera = new THREE.OrthographicCamera(
        (-this.camera_params.size / 2) * (this.width / this.height),
        (this.camera_params.size / 2) * (this.width / this.height),
        this.camera_params.size / 2,
        -this.camera_params.size / 2,
        this.camera_params.near,
        this.camera_params.far
      );
    }
    this.look_at = new THREE.Vector3(0, 0, 0);
    this.camera.lookAt(this.look_at);
    this.camera.up = new THREE.Vector3(0, 0, 1);
    this.camera.position.set(0, -3, 5);

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
    this.renderer.setClearColor("#eee");
    this.renderer.setSize(this.width, this.height);

    this.$nextTick(() => this.resize());
    window.addEventListener("resize", this.resize, false);

    const render = () => {
      requestAnimationFrame(() => setTimeout(() => render(), 1000 / 20));
      TWEEN.update();
      this.renderer.render(this.scene, this.camera);
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
    this.$el.onclick = click_handler;
    this.$el.ondblclick = click_handler;

    const connectInterval = setInterval(() => {
      if (window.socket.id === undefined) return;
      this.$emit("init", { socket_id: window.socket.id });
      clearInterval(connectInterval);
    }, 100);
  },

  beforeDestroy() {
    window.removeEventListener("resize", this.resize);
  },

  methods: {
    move_camera(x, y, z, look_at_x, look_at_y, look_at_z, up_x, up_y, up_z, duration) {
      if (this.camera_tween) this.camera_tween.stop();
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
          duration * 1000
        )
        .onUpdate((p) => {
          this.camera.position.set(p[0], p[1], p[2]);
          this.camera.up.set(p[3], p[4], p[5]); // NOTE: before calling lookAt
          this.look_at.set(p[6], p[7], p[8]);
          this.camera.lookAt(p[6], p[7], p[8]);
        })
        .start();
    },
    resize() {
      const { clientWidth, clientHeight } = this.$el;
      this.renderer.setSize(clientWidth, clientHeight);
      this.camera.aspect = clientWidth / clientHeight;
      if (this.camera_type === "orthographic") {
        this.camera.left = (-this.camera.aspect * this.camera_params.size) / 2;
        this.camera.right = (this.camera.aspect * this.camera_params.size) / 2;
      }
      this.camera.updateProjectionMatrix();
    },
  },

  props: {
    width: Number,
    height: Number,
    camera_type: String,
    camera_params: Object,
    scene_id: String,
  },
};
