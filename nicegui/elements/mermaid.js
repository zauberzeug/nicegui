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
      this.$el.setAttribute("mermaid_content", content);
      queue.push(this.$el);
      if (is_running) return;
      is_running = true;
      while (queue.length) {
        try {
          let element = queue.shift();

          const { svg, bindFunctions } = await mermaid.render(element.id+"_mermaid", element.getAttribute("mermaid_content"))

          element.innerHTML = svg;

          if (bindFunctions) {
            bindFunctions(element);
          }
        } catch (error) {
          console.error(error);
          this.$emit("error", error);
        }
      }
      is_running = false;
    },
  },
  props: {
    config: Object,
    content: String,
  },
};
