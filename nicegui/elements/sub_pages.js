export default {
  template: `
    <div class="nicegui-column">
      <slot></slot>
    </div>
  `,
  mounted() {
    window.addEventListener("popstate", (event) => {
      this.$emit("open", event.state?.page || window.location.pathname);
    });
    window.addEventListener("pushstate", (event) => {
      this.$emit("open", event.state?.page || window.location.pathname);
    });

    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[href]");
      if (!a) return;
      e.preventDefault();
      const path = a.getAttribute("href");
      history.pushState({}, "", path);
      this.$emit("open", path);
    });
  },
};
