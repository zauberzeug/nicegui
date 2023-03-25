export default {
  template: `<audio :controls="controls" :autoplay="autoplay" :muted="muted" :src="src" />`,
  props: {
    controls: Boolean,
    autoplay: Boolean,
    muted: Boolean,
    src: String,
  },
};
