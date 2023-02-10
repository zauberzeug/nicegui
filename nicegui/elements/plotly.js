export default {
  template: `<div></div>`,
  mounted() {
    setTimeout(() => {
      import(window.path_prefix + this.lib).then(() => {
        this.chart = Plotly.newPlot(this.$el.id, this.options);
      });
    }, 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  methods: {
    update(options) {
      this.chart.update(options);
    },
  },
  props: {
    options: Object,
    lib: String,
  },
};
