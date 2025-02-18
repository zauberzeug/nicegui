import { loadResource } from "../../static/utils/resources.js";

export default {
  template: `<div></div>`,
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await loadResource(window.path_prefix + this.codehilite_css_url);
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
