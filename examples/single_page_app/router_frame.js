export default {
  template: `<div><slot></slot></div>`,
  mounted() {
    window.addEventListener("popstate", (event) => {
      if (event.state && event.state.page) {
        this.$emit("open", event.state.page);
      }
    });
    console.log(window.location.pathname);
    this.$nextTick(() => {
      // FIXME this delay is a hack to make sure the event can actually be handled by the backend
      setTimeout(() => {
        this.$emit("open", window.location.pathname);
      }, 1000);
    });
  },
  props: {},
};
