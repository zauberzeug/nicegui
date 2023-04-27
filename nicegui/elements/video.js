export default {
  template: `<video :controls="controls" :autoplay="autoplay" :muted="muted" :src="src" />`,
  methods: {
    seek(seconds) {
      this.$el.currentTime = seconds;
    },
  },
  props: {
    controls: Boolean,
    autoplay: Boolean,
    muted: Boolean,
    src: String,
  },
};
