export default {
  template: "<div></div>",
  mounted() {
    setTimeout(() => {
      const imports = this.extras.map((extra) => import(window.path_prefix + extra));
      Promise.allSettled(imports).then(() => {
        this.chart = echarts.init(this.$el);
        this.chart.setOption(this.options);
        this.chart.resize();
      });
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
        console.log(this.options);
        this.chart.setOption(this.options);
      }
    },
    destroyChart() {
      if (this.chart) {
        this.chart.destroy();
      }
    },
  },
  props: {
    options: Object,
    extras: Array,
  },
};
