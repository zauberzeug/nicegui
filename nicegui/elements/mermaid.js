export default {
  template: `<div></div>`,
  mounted() {
    this.update(this.$el.innerText);
  },
  methods: {
    update(content) {
      mermaid.render("mermaid" + this.$el.id, content, (svg) => (this.$el.innerHTML = svg));
    },
  },
};
