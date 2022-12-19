export default {
  template: `
    <audio :controls="this.controls" :autoplay="this.autoplay" :muted="this.muted">
      <source :src="this.src" :type="this.type">
    </audio>
  `,
  props: {
    controls: Boolean,
    autoplay: Boolean,
    muted: Boolean,
    src: String,
    type: String,
  },
};
