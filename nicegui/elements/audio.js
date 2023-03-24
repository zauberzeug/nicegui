export default {
  template: `<audio :controls="controls" :autoplay="autoplay" :muted="muted" :src="src" :type="type"/>`,
  props: {
    controls: Boolean,
    autoplay: Boolean,
    muted: Boolean,
    src: String,
    type: String,
  },
};
