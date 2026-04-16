export default {
  template: `
    <Teleport :to="target">
      <slot></slot>
    </Teleport>
  `,
  props: {
    anchorSelector: String,
  },
  data() {
    return { target: "#nicegui-keep-alive-cache" };
  },
  methods: {
    setAnchorReady(ready) {
      this.target = ready ? this.anchorSelector : "#nicegui-keep-alive-cache";
    },
  },
};
