export default {
  template: `<q-scroll-area ref="qRef"><slot></slot></q-scroll-area>`,
  data() {
    return {
      shouldScroll: true,
    };
  },
  beforeUpdate() {
    if (this.$refs.qRef) {
      this.shouldScroll = this.$refs.qRef.getScroll().verticalPercentage == 1.0;
    }
  },
  updated() {
    if (this.$refs.qRef && this.shouldScroll) {
      this.$nextTick(() => this.$refs.qRef.setScrollPosition("vertical", Number.MAX_SAFE_INTEGER));
    }
  },
};
