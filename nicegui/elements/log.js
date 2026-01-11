export default {
  template: `<q-scroll-area ref="qRef" @scroll="onScroll"><slot></slot></q-scroll-area>`,
  data() {
    return {
      shouldScroll: true,
    };
  },
  updated() {
    if (this.$refs.qRef && this.shouldScroll) {
      this.$nextTick(() => this.$refs.qRef.setScrollPosition("vertical", Number.MAX_SAFE_INTEGER));
    }
  },
  methods: {
    onScroll() {
      if (!this.$refs.qRef.$el.childNodes[0].clientHeight) return;
      this.shouldScroll = this.$refs.qRef.getScroll().verticalPercentage == 1.0;
    },
  },
};
