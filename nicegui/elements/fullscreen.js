export default {
  props: {
    requireEscapeHold: Boolean,
  },
  mounted() {
    document.addEventListener("fullscreenchange", this.handleFullscreenChange);
    document.addEventListener("mozfullscreenchange", this.handleFullscreenChange);
    document.addEventListener("webkitfullscreenchange", this.handleFullscreenChange);
    document.addEventListener("msfullscreenchange", this.handleFullscreenChange);
  },
  unmounted() {
    document.removeEventListener("fullscreenchange", this.handleFullscreenChange);
    document.removeEventListener("mozfullscreenchange", this.handleFullscreenChange);
    document.removeEventListener("webkitfullscreenchange", this.handleFullscreenChange);
    document.removeEventListener("msfullscreenchange", this.handleFullscreenChange);
  },
  methods: {
    handleFullscreenChange() {
      this.$emit("update:model-value", Quasar.AppFullscreen.isActive);
    },
    enter() {
      Quasar.AppFullscreen.request().then(() => {
        if (this.requireEscapeHold && navigator.keyboard && typeof navigator.keyboard.lock === "function") {
          navigator.keyboard.lock(["Escape"]);
        }
      });
    },
    exit() {
      Quasar.AppFullscreen.exit();
    },
  },
};
