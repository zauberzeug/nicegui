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
      try {
        const { svg, bindFunctions } = await mermaid.render(this.$el.id + "_mermaid", content);
        this.$el.innerHTML = svg;
        bindFunctions?.(this.$el);

        if (this.clickInstance) {
          const handlerName = this.getHandlerName();
          window[handlerName] = (nodeId, nodeText) => {
            this.$emit("nodeClick", {
              node: this.getNodeName(nodeId),
              nodeId,
              nodeText,
            });
          };

          this.$nextTick(() => {
            this.attachClickHandlers(this.getHandlerName());
          });
        };

      } catch (error) {
        const { svg, bindFunctions } = await mermaid.render(this.$el.id + "_mermaid", "error");
        this.$el.innerHTML = svg;
        bindFunctions?.(this.$el);
        const mermaidErrorFormat = { str: error.message, message: error.message, hash: error.name, error };
        console.error(mermaidErrorFormat);
        this.$emit("error", mermaidErrorFormat);
      }
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
