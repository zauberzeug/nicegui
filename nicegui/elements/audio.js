export default {
  template: `<audio :controls="controls" :autoplay="autoplay" :muted="muted" :src="computed_src" />`,
  props: {
    controls: Boolean,
    autoplay: Boolean,
    muted: Boolean,
    src: String,
  },
  data: function () {
    return {
      computed_src: undefined,
    };
  },
  mounted() {
    setTimeout(() => this.compute_src(), 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  updated() {
    this.compute_src();
  },
  methods: {
    compute_src() {
      this.computed_src = (this.src.startsWith("/") ? window.path_prefix : "") + this.src;
    },
    seek(seconds) {
      this.$el.currentTime = seconds;
    },
    play() {
      this.$el.play();
    },
    pause() {
      this.$el.pause();
    },
  },
};
