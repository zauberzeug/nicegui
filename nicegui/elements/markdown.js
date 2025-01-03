import { loadResource } from "../../static/utils/resources.js";

export default {
  template: `<div></div>`,
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await loadResource(window.path_prefix + this.codehilite_css_url);
    if (this.use_mermaid) {
      this.mermaid = (await import("mermaid")).default;
      await this.mermaid.initialize({ startOnLoad: false });
      await this.renderMermaid();
    }
  },
  data() {
    return {
      mermaid: null,
    };
  },
  updated() {
    if (this.mermaid) {
      this.renderMermaid();
    }
  },
  methods: {
    async renderMermaid() {
      const elements = this.$el.querySelectorAll(".mermaid-pre");
      for (const pre of elements) {
        try {
          await this.mermaid.run({ nodes: [pre.children[0]] });
        } catch (error) {
          console.error('Failed to render mermaid diagram:', error);
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
