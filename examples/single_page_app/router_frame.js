export default {
  template: "<div><slot></slot></div>",
  mounted() {
    const initial_path = window.location.pathname;
    window.addEventListener("popstate", (event) => {
      this.$emit("open", event.state?.page || initial_path);
    });
    const connectInterval = setInterval(async () => {
      if (window.socket.id === undefined) return;
      this.$emit("open", window.location.pathname);
      clearInterval(connectInterval);
    }, 10);
  },
  props: {},
};
