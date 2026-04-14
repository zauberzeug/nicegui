export default {
  template: `<div><slot v-if="shouldRender"></slot></div>`,
  data() {
    return {
      shouldRender: false,
    };
  },
  mounted() {
    this.$nextTick(() => {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          this.shouldRender = true;
        });
      });
    });
  },
};
