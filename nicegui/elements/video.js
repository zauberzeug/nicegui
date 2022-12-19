export default {
  template: `
    <video :controls="this.controls" :autoplay="this.autoplay" :muted="this.muted">
      <source :src="this.src" :type="this.type">
    </video>
  `,
  props: {
    controls: Boolean,
    autoplay: Boolean,
    muted: Boolean,
    src: String,
    type: String,
  },
};
