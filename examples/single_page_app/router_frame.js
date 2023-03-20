export default {
  template: `<div>Test</div>`,
  mounted() {
    window.addEventListener("popstate", (event) => {
      if (event.state && event.state.page) {
        console.log(event.state.page);
      }
    });
  },
  props: {},
};
