export default {
  template: "<div></div>",
  mounted() {
    setTimeout(() => {
      const imports = this.extras.map((extra) => import(window.path_prefix + extra));
      Promise.allSettled(imports).then(() => {
        this.seriesCount = this.options.series ? this.options.series.length : 0;
        if ("dragDrop" in this.options.plotOptions.series) {
          this.options.plotOptions.series.point = {
            events: {
              drop: (e) => {
                this.$emit("change", {
                  series_name: e.target.series.name,
                  series_index: e.target.series.index,
                  series_xdata: e.target.series.xData,
                  series_ydata: e.target.series.yData,
                });
              },
            },
          };
        }
        this.chart = Highcharts[this.type](this.$el, this.options);
        this.chart.reflow();
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
        while (this.seriesCount > this.options.series.length) {
          this.chart.series[0].remove();
          this.seriesCount--;
        }
        while (this.seriesCount < this.options.series.length) {
          this.chart.addSeries({}, false);
          this.seriesCount++;
        }
        this.chart.update(this.options);
      }
    },
    destroyChart() {
      if (this.chart) {
        this.chart.destroy();
      }
    },
  },
  props: {
    type: String,
    options: Object,
    extras: Array,
  },
};
