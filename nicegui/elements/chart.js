export default {
  template: "<div></div>",
  mounted() {
    setTimeout(() => {
      const imports = this.extras.map((extra) => import(window.path_prefix + extra));
      Promise.allSettled(imports).then(() => {
        this.seriesCount = this.options.series ? this.options.series.length : 0;
        this.options.plotOptions = this.options.plotOptions ?? {};
        this.options.plotOptions.series = this.options.plotOptions.series ?? {};
        this.options.plotOptions.series.point = this.options.plotOptions.series.point ?? {};
        this.options.plotOptions.series.point.events = this.options.plotOptions.series.point.events ?? {};
        function uncycle(e) {
          // Highcharts events are cyclic, so we need to uncycle them
          let { point, target, ...rest } = e;
          point = point ?? target;
          return {
            ...rest,
            point_index: point?.index,
            point_x: point?.x,
            point_y: point?.y,
            series_index: point?.series?.index,
          };
        }
        this.options.plotOptions.series.point.events.click = (e) => this.$emit("pointClick", uncycle(e));
        this.options.plotOptions.series.point.events.dragStart = (e) => this.$emit("pointDragStart", uncycle(e));
        this.options.plotOptions.series.point.events.drag = (e) => this.$emit("pointDrag", uncycle(e));
        this.options.plotOptions.series.point.events.drop = (e) => this.$emit("pointDrop", uncycle(e));
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
