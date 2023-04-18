export default {
  template: `<a :href="computed_href" :target="target"><slot></slot></a>`,
  mounted() {
    setTimeout(this.compute_href, 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  updated() {
    this.compute_href();
  },
  methods: {
    compute_href() {
      this.computed_href = (this.href.startsWith("/") ? window.path_prefix : "") + this.href;
    },
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
