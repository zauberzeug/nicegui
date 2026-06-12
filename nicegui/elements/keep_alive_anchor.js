export default {
  template: `<div style="display: contents"></div>`, // make anchor transparent to layout for correct sizing of children
  props: {
    hostId: Number,
  },
  mounted() {
    this.$nextTick(() => getElement(this.hostId)?.setAnchorReady(true)); // wait for root app to be fully mounted
  },
  beforeUnmount() {
    getElement(this.hostId)?.setAnchorReady(false);
  },
};
