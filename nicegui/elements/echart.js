export default {
  template: "<div></div>",
  mounted() {
    setTimeout(() => {
      this.chart = echarts.init(this.$el);
      this.chart.setOption(this.options);
      this.chart.resize();
    }, 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  beforeDestroy() {
    this.destroyChart();
  },
  beforeUnmount() {
    this.destroyChart();
  },
  methods: {
    update_chart() {
      if (this.chart) {
        this.chart.setOption(this.options);
      }
    },
    destroyChart() {
      if (this.chart) {
        this.chart.dispose();
      }
    },
  },
  props: {
    options: Object,
  },
};
