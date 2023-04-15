export default {
  template: `<a :href="computed_href" :target="target"><slot></slot></a>`,
  mounted() {
    setTimeout(() => {
      this.computed_href = (this.href.startsWith("/") ? window.path_prefix : "") + this.href;
    }, 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  props: {
    href: String,
    target: String,
  },
  data: function () {
    return {
      computed_href: this.href,
    };
  },
};
