export default {
  template: `<component :is="tag"></component>`,
  data() {
    return { previousInnerHTML: null };
  },
  mounted() {
    this.renderContent();
  },
  updated() {
    this.renderContent();
  },
  methods: {
    renderContent() {
      if (this.innerHTML === this.previousInnerHTML) return;
      if (this.sanitize) {
        this.$el.setHTML(this.innerHTML);
      } else {
        this.$el.innerHTML = this.innerHTML;
      }
      this.previousInnerHTML = this.innerHTML;
    },
  },
  props: {
    innerHTML: String,
    sanitize: Boolean,
    tag: String,
  },
};
