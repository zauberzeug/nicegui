export default {
  template: "<div></div>",
  mounted() {
    this.chart = echarts.init(this.$el);
    this.chart.setOption(this.options);
    this.chart.resize();
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
