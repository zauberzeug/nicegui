export default {
  mounted() {
    document.addEventListener("fullscreenchange", this.handleFullscreenChange);
    document.addEventListener("webkitfullscreenchange", this.handleFullscreenChange);
    document.addEventListener("msfullscreenchange", this.handleFullscreenChange);
  },

  unmounted() {
    document.removeEventListener("fullscreenchange", this.handleFullscreenChange);
    document.removeEventListener("webkitfullscreenchange", this.handleFullscreenChange);
    document.removeEventListener("msfullscreenchange", this.handleFullscreenChange);
  },

  methods: {
    handleFullscreenChange() {
      const state = this.getState();
      this.$emit("fullscreen_change", state);
    },

    getState() {
      return Quasar.AppFullscreen.isActive;
    },

    enter(blockEscapeKey) {
      Quasar.AppFullscreen.request().then(() => {
        if (blockEscapeKey && navigator.keyboard && typeof navigator.keyboard.lock === "function") {
          navigator.keyboard.lock(["Escape"]);
        }
      });
    },

    exit() {
      Quasar.AppFullscreen.exit();
    },

    toggle(blockEscapeKey) {
      if (this.getState()) {
        return this.exit();
      } else {
        return this.enter(blockEscapeKey);
      }
    },
  },
};
