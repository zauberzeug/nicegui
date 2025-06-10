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
      const href = a.getAttribute("href");
      if (href.startsWith("/") && a.target !== "_blank" && !a.hasAttribute("download")) {
        e.preventDefault();
        this.$emit("navigate", href);
      }
    });
  },
};
