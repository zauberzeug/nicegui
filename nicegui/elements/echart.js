export default {
  template: "<div></div>",
  mounted() {
    this.chart = echarts.init(this.$el);
    this.chart.setOption(this.options);
    new ResizeObserver(this.chart.resize).observe(this.$el);
  },
  beforeDestroy() {
    this.chart.dispose();
  },
  beforeUnmount() {
    this.chart.dispose();
  },
  methods: {
    update_chart() {
      this.chart.setOption(this.options);
    },
  },
  props: {
    options: Object,
  },
};
