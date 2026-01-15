export default {
  template: `<q-scroll-area ref="qRef" @scroll="onScroll"><slot></slot></q-scroll-area>`,
  data() {
    return {
      shouldScroll: true,
      lastHeight: NaN,
    };
  },
  updated() {
    if (this.shouldScroll) {
      this.$nextTick(() => this.$refs.qRef.setScrollPosition("vertical", Number.MAX_SAFE_INTEGER));
    }
  },
  methods: {
    onScroll(info) {
      if (info.verticalContainerSize === 0 || info.horizontalContainerSize === 0) return;
      if (info.verticalContainerSize !== this.lastHeight) {
        this.lastHeight = info.verticalContainerSize;
        return;
      }
      this.shouldScroll = this.$refs.qRef.getScroll().verticalPercentage === 1.0;
    },
  },
};
