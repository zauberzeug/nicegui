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
      diagrams: {},
    };
  },
  updated() {
    this.renderMermaid();
  },
  methods: {
    renderMermaid() {
      // render new diagrams
      const usedKeys = new Set();
      this.$el.querySelectorAll(".mermaid-pre").forEach(async (pre, i) => {
        const key = pre.children[0].innerText + "\n" + i;
        usedKeys.add(key);
        if (!this.diagrams[key]) {
          try {
            this.diagrams[key] = await this.mermaid.render(this.$el.id + "_mermaid_" + i, pre.children[0].innerText);
          } catch (error) {
            this.diagrams[key] = await this.mermaid.render(this.$el.id + "_mermaid_" + i, "error");
            console.error(error);
          }
        }
        const svgElement = document.createElement("div");
        svgElement.classList.add("mermaid-svg");
        svgElement.innerHTML = this.diagrams[key].svg;
        this.diagrams[key].bindFunctions?.(svgElement);
        pre.querySelectorAll(".mermaid-svg").forEach((svg) => svg.remove());
        pre.appendChild(svgElement);
      });

      // prune cached diagrams that are not used anymore
      for (const key in this.diagrams) {
        if (!usedKeys.has(key)) {
          delete this.diagrams[key];
        }
      }
    },
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
