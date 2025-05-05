import mermaid from "mermaid";

let is_running = false;
const queue = [];

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
        const { svg, bindFunctions } = await mermaid.render(this.$el.id + "_mermaid", content)
        this.$el.innerHTML = svg;

        if (bindFunctions) {
          bindFunctions(this.$el);
        }
      } catch (error) {
        console.error(error);
        this.$emit("error", error);
      }
    },
  },
  props: {
    config: Object,
    content: String,
  },
};
