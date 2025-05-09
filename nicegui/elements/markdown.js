import { loadResource } from "../../static/utils/resources.js";

export default {
  template: `<div></div>`,
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await loadResource(window.path_prefix + this.codehilite_css_url);
    if (this.use_mermaid) {
      this.mermaid = (await import("mermaid")).default;
      this.mermaid.initialize({ startOnLoad: false });
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
        try {
          if (pre.children[0].innerText != this.lastContent) {
            const { svg, bindFunctions } = await this.mermaid.render(this.$el.id + "_mermaid_" + i, pre.children[0].innerText);
            this.lastSvg = svg;
            this.lastBindFunctions = bindFunctions;
            this.lastContent = pre.children[0].innerText;
          }
          this.addMermaidToElement(pre, this.lastSvg, this.lastBindFunctions);
        } catch (error) {
          const { svg, bindFunctions } = await this.mermaid.render(this.$el.id + "_mermaid_" + i, "error");
          this.addMermaidToElement(pre, svg, bindFunctions);
          const mermaidErrorFormat = { str: error.message, message: error.message, hash: error.name, error };
          console.error(mermaidErrorFormat);
        }
      });
    },
    addMermaidToElement(element, svg, bindFunctions) {
      const svgElement = document.createElement("div")
      svgElement.classList.add("mermaid-svg");
      svgElement.innerHTML = svg;
      bindFunctions?.(svgElement);
      element.querySelectorAll(".mermaid-svg").forEach((svg) => {
        svg.remove();
      });
      element.appendChild(svgElement);
    }
  },
  props: {
    codehilite_css_url: String,
    use_mermaid: {
      required: false,
      default: false,
      type: Boolean,
    },
  },
};
