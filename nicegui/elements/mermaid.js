export default {
  template: `<div></div>`,
  mounted() {
    this.update(this.content);
  },
  methods: {
    update(content) {
      mermaid.render("mermaid" + this.$el.id, content, (svg) => (this.$el.innerHTML = svg));
    },
  },
  props: {
    content: String,
  },
};
