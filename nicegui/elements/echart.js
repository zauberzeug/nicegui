export default {
  template: "<div></div>",
  mounted() {
    this.chart = echarts.init(this.$el);
    this.chart.setOption(this.options);
    this.chart.resize();
    function unpack(e) {
      return {
        component_type: e.componentType,
        series_type: e.seriesType,
        series_index: e.seriesIndex,
        series_name: e.seriesName,
        name: e.name,
        data_index: e.dataIndex,
        data: e.data,
        data_type: e.dataType,
        value: e.value
      };
    }
    this.chart.on('click', e => this.$emit("pointClick", unpack(e)));
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
