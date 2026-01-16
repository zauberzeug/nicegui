export default {
  template: `<q-header ref="qRef"><slot></slot></q-header>`,
  mounted() {
    if (this.addScrollPadding) {
      this.resizeObserver = new ResizeObserver(() => {
        document.documentElement.style.scrollPaddingTop = `${this.$el.offsetHeight}px`;
      }).observe(this.$el);
    }
  },
  unmounted() {
    this.resizeObserver?.disconnect();
  },
  props: {
    addScrollPadding: Boolean,
  },
};
