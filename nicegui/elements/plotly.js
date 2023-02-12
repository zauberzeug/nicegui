export default {
  template: `<div></div>`,
  mounted() {
    setTimeout(() => {
      import(window.path_prefix + this.lib).then(() => {
        Plotly.newPlot(this.$el.id, this.options.data, this.options.layout);
      });
    }, 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  methods: {
    update(options) {
      Plotly.newPlot(this.$el.id, options.data, options.layout);
    },
  },
  props: {
    options: Object,
    lib: String,
  },
};
