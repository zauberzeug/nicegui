export default {
  template: `
    <div>
      <slot></slot>
    </div>
  `,
  mounted() {
    window.addEventListener("popstate", (event) => this.$emit("open", event.state?.page || window.location.pathname));
    window.addEventListener("pushstate", (event) => this.$emit("open", event.state?.page || window.location.pathname));
    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[href]");
      if (a && a.target !== "_blank" && !a.hasAttribute("download")) {
        const href = a.getAttribute("href");
        if (href.startsWith("/")) {
          e.preventDefault();
          this.$emit("navigate", href);
        }
      }
    });
  },
};
