export default {
  template: `<div></div>`,
  async mounted() {
    this.ensure_codehilite_css();
    if (this.use_mermaid) {
      this.mermaid = (await import("mermaid")).default;
      this.renderMermaid();
    }
  },
  data() {
    return {
      mermaid: null,
    };
  },
  updated() {
    this.renderMermaid();
  },
  methods: {
    renderMermaid() {
      this.$el.querySelectorAll(".mermaid-pre").forEach(async (pre, i) => {
        await this.mermaid.run({ nodes: [pre.children[0]] });
      });
    },
    ensure_codehilite_css() {
      if (!document.querySelector(`style[data-codehilite-css]`)) {
        const style = document.createElement("style");
        style.setAttribute("data-codehilite-css", "");
        style.innerHTML = this.codehilite_css;
        document.head.appendChild(style);
      }
    },
  },
  props: {
    codehilite_css: String,
    use_mermaid: {
      required: false,
      default: false,
      type: Boolean,
    },
  },
};
