import { mermaid } from "nicegui-mermaid";

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
      queue.push({ element: this.$el, content: content, clickable: this.clickable });
      if (is_running) return;
      is_running = true;
      while (queue.length) {
        const { element, content, clickable } = queue.shift();
        try {
          const { svg, bindFunctions } = await mermaid.render(element.id + "_mermaid", content);
          element.innerHTML = svg;
          bindFunctions?.(element);
          if (clickable) {
            element.querySelectorAll("g.node").forEach((node) => {
              node.style.cursor = "pointer";
              node.addEventListener("click", () => getElement(element).$emit("node_click", node.id));
            });
          }
        } catch (error) {
          const { svg, bindFunctions } = await mermaid.render(element.id + "_mermaid", "error");
          element.innerHTML = svg;
          bindFunctions?.(element);
          const mermaidErrorFormat = { str: error.message, message: error.message, hash: error.name, error };
          console.error(mermaidErrorFormat);
          getElement(element).$emit("error", mermaidErrorFormat);
        }
      }
      is_running = false;
    },
  },
  props: {
    config: Object,
    content: String,
    clickable: Boolean,
  },
};
