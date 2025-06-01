import mermaid from "mermaid";

export default {
  template: `<div></div>`,
  data: () => ({
    last_content: "",
  }),
  mounted() {
    this.initialize();
    this.update(this.content);
  },
  methods: {
    initialize() {
      try {
        mermaid.initialize(this.config || {});
      } catch (error) {
        console.error(error);
        this.$emit("error", error);
      }
    },
    async update(content) {
      if (this.last_content === content) return;
      this.last_content = content;
      try {
        const { svg, bindFunctions } = await mermaid.render(this.$el.id + "_mermaid", content);
        this.$el.innerHTML = svg;
        bindFunctions?.(this.$el);
      } catch (error) {
        const { svg, bindFunctions } = await mermaid.render(this.$el.id + "_mermaid", "error");
        this.$el.innerHTML = svg;
        bindFunctions?.(this.$el);
        const mermaidErrorFormat = { str: error.message, message: error.message, hash: error.name, error };
        console.error(mermaidErrorFormat);
        this.$emit("error", mermaidErrorFormat);
      }
    },
  },
  props: {
    config: Object,
    content: String,
  },
};
