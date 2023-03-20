export default {
  template: `<div><slot></slot></div>`,
  mounted() {
    window.addEventListener("popstate", (event) => {
      if (event.state && event.state.page) {
        console.log(event.state.page);
        this.$emit("open", event.state.page);
      }
    });
  },
  props: {},
};
