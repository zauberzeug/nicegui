import { mermaid } from "nicegui-mermaid";

let is_running = false;
const queue = [];

// These diagram types build their DOM IDs as "<svg_id>-<type>-<node_id>-<index>"; all others use "<svg_id>-<node_id>".
const INDEXED_DIAGRAM_TYPES = ["flowchart-v2", "flowchart-elk", "class", "classDiagram", "stateDiagram", "er"];

function extractNodeId(domId, svgId, diagramType) {
  const prefix = svgId + "-";
  if (!domId.startsWith(prefix)) return domId; // unexpected shape: hand back the raw ID rather than mis-parse it
  const id = domId.slice(prefix.length);
  return INDEXED_DIAGRAM_TYPES.includes(diagramType) ? id.split("-").slice(1, -1).join("-") : id;
}

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
          const svgId = element.id + "_mermaid";
          const { svg, bindFunctions, diagramType } = await mermaid.render(svgId, content);
          element.innerHTML = svg;
          bindFunctions?.(element);
          if (clickable) {
            element.querySelectorAll("g.node").forEach((node) => {
              node.style.cursor = "pointer";
              node.addEventListener("click", () =>
                getElement(element).$emit("node_click", extractNodeId(node.id, svgId, diagramType)),
              );
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
