import mermaid from "mermaid";
export default {
  template: `<div></div>`,
  data: () => ({
    last_content: "",
  }),
  mounted() {
    this.update(this.content);
  },
  methods: {
    update(content) {
      if (this.last_content === content) return;
      this.last_content = content;
      this.$el.innerHTML = content;
      this.$el.removeAttribute("data-processed");
      mermaid.run({ nodes: [this.$el] });
    },
  },
  props: {
    content: String,
  },
};
