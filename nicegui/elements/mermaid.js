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
  beforeUnmount() {
    this.clearHandler();
  },
  methods: {
    getHandlerName() {
      return `nodeClick_${this.clickInstance}`;
    },
    clearHandler() {
      const handlerName = this.getHandlerName();
      if (window[handlerName]) delete window[handlerName];
    },
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
    attachClickHandlers(handlerName) {
      const clickables = this.$el.querySelectorAll("g.node.clickable");
      clickables.forEach(node => {
        node.removeAttribute("onclick");
        node.onclick = null;

        const newNode = node.cloneNode(true);
        node.parentNode.replaceChild(newNode, node);

        const nodeText = newNode.textContent.trim();
        newNode.addEventListener("click", () => {
          window[handlerName](newNode.id, nodeText);
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
    clickInstance: Number,
  },
};
