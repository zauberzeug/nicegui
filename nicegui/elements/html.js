export default {
  template: `<component :is="tag"></component>`,
  mounted() {
    this.renderContent();
  },
  updated() {
    this.renderContent();
  },
  methods: {
    renderContent() {
      if (this.sanitize) {
        this.$el.setHTML(this.innerHTML);
      } else {
        this.$el.innerHTML = this.innerHTML;
      }
    },
  },
  props: {
    innerHTML: String,
    sanitize: Boolean,
    tag: String,
  },
};
