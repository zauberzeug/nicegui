import mermaid from "mermaid";

let is_running = false;
const queue = [];

export default {
  template: `<div></div>`,
  data: () => ({
    last_content: "",
  }),
  mounted() {
    this.update(this.content);
  },
  methods: {
    async update(content) {
      if (this.last_content === content) return;
      this.last_content = content;
      this.$el.innerHTML = content;
      this.$el.removeAttribute("data-processed");
      queue.push(this.$el);
      if (is_running) return;
      is_running = true;
      while (queue.length) {
        await mermaid.run({ nodes: [queue.shift()] });
      }
      is_running = false;
    },
  },
  props: {
    content: String,
  },
};
