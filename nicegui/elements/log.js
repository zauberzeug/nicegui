export default {
  template: `<q-scroll-area ref="qRef"><slot></slot></q-scroll-area>`,
  data() {
    return {
      shouldScroll: true,
    };
  },
  beforeUpdate() {
    if (this.$refs.qRef && document.body.contains(this.$refs.qRef.$el)) {
      this.shouldScroll =
        this.$refs.qRef.$el.childNodes[0].scrollTop + this.$refs.qRef.$el.childNodes[0].clientHeight >=
        this.$refs.qRef.$el.childNodes[0].scrollHeight;
    }
  },
  updated() {
    if (this.$refs.qRef && this.shouldScroll) {
      this.$nextTick(() => this.$refs.qRef.setScrollPosition("vertical", Number.MAX_SAFE_INTEGER));
    }
  },
};
