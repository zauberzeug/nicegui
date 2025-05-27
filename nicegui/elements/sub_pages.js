export default {
  template: "<slot></slot>",
  mounted() {
    const initial_path = window.location.pathname;
    window.addEventListener("popstate", (event) => {
      console.log("popstate", event);
      this.$emit("open", event.state?.page || window.location.pathname);
    });
    window.addEventListener("pushstate", (event) => {
      console.log("pushstate", event);
      this.$emit("open", event.state?.page || window.location.pathname);
    });

    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[href]");
      e.preventDefault();
      if (!a) return;
      const path = a.getAttribute("href");
      history.pushState({}, "", path);
      this.$emit("open", path);
      console.log("click", path);
    });
  },
};
