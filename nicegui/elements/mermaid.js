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
      queue.push({ element: this.$el, content: content });
      if (is_running) return;
      is_running = true;
      while (queue.length) {
        const { element, content } = queue.shift();
        try {
          const { svg, bindFunctions } = await mermaid.render(element.id + "_mermaid", content);
          element.innerHTML = svg;
          bindFunctions?.(element);
          if (this.clickInstance) {
            await this.$nextTick();
            this.attachClickHandlers(element);
          };
        } catch (error) {
          const { svg, bindFunctions } = await mermaid.render(element.id + "_mermaid", "error");
          element.innerHTML = svg;
          bindFunctions?.(element);
          const mermaidErrorFormat = { str: error.message, message: error.message, hash: error.name, error };
          console.error(mermaidErrorFormat);
          this.$emit("error", mermaidErrorFormat);
        }
      }
      is_running = false;
    },
    attachClickHandlers(element) {
      const clickables = element.querySelectorAll("g.node");
      console.log(clickables)
      clickables.forEach(node => {
        if (node.getAttribute('data-listener-added')) return;
        node.setAttribute('data-listener-added', 'true');
        node.style.cursor = "pointer";

        const nodeText = node.textContent.trim();
        const nodeId = node.id;

        node.addEventListener("click", () => {
          this.$emit("nodeClick", {
            node: this.getNodeName(nodeId),
            nodeId,
            nodeText,
          });
        });
      });
    },
    getNodeName(domId) {
      if (!domId) return undefined;
      const parts = domId.split("-");
      if (parts.length >= 3) return parts.slice(1, -1).join("-");
      if (parts.length === 2) return parts[1];
      return domId;
    },
  },
  props: {
    config: Object,
    content: String,
    clickInstance: Boolean,
  },
};
