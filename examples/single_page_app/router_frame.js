export default {
  template: "<div><slot></slot></div>",
  mounted() {
    window.addEventListener("popstate", (event) => {
      if (event.state?.page) {
        this.$emit("open", event.state.page);
      }
    });
    const connectInterval = setInterval(async () => {
      if (window.socket.id === undefined) return;
      this.$emit("open", window.location.pathname);
      clearInterval(connectInterval);
    }, 10);
  },
  props: {},
};
