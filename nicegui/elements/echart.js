export default {
  template: "<div></div>",
  mounted() {
    this.chart = echarts.init(this.$el);
    this.chart.setOption(this.options);
    new ResizeObserver(this.resize_chart).observe(this.$el);
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
    resize_chart() {
      if (this.chart) {
        this.chart.resize();
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
