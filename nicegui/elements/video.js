export default {
  template: `<video ref="videoPlayer" :controls="controls" :autoplay="autoplay" :muted="muted" :src="src" :type="type" />`,
  props: {
    controls: Boolean,
    autoplay: Boolean,
    muted: Boolean,
    src: String,
    type: String,
  },
};
