export default {
  template: "<div></div>",
  mounted() {
    setTimeout(() => {
      const imports = this.extras.map((extra) => import(window.path_prefix + extra));
      Promise.allSettled(imports).then(() => {
        this.seriesCount = this.options.series ? this.options.series.length : 0;
        if (!this.options.plotOptions) {
          this.options.plotOptions = {};
        }
        if (!this.options.plotOptions.series) {
          this.options.plotOptions.series = {};
        }
        if (!this.options.plotOptions.series.point) {
          this.options.plotOptions.series.point = {};
        }
        if (!this.options.plotOptions.series.point.events) {
          this.options.plotOptions.series.point.events = {};
        }
        // if (this.on_event_set === true) {
        if (true) {
          this.options.plotOptions.series.point.events.click = (e) => {
            this.$emit("on_event", {
              event_type: "point_click",
              point_index: e.point.index,
              point_x: e.point.x,
              point_y: e.point.y,
              series_index: e.point.series.index,
            });
          };
        }
        // if (this.on_drag_drop_set === true) {
        if (true) {
          this.options.plotOptions.series.point.events.dragStart = (e) => {
            this.$emit("on_point_drag_drop", {
              event_type: "point_drag_start",
            });
          };
          this.options.plotOptions.series.point.events.drag = (e) => {
            this.$emit("on_point_drag_drop", {
              event_type: "point_drag",
              point_index: e.target.index,
              point_x: e.target.x,
              point_y: e.target.y,
              series_index: e.target.series.index,
            });
          };
          this.options.plotOptions.series.point.events.drop = (e) => {
            this.$emit("on_point_drag_drop", {
              event_type: "point_drop",
              point_index: e.target.index,
              point_x: e.target.x,
              point_y: e.target.y,
              series_name: e.target.series.name,
              series_index: e.target.series.index,
              series_x: e.target.series.xData,
              series_y: e.target.series.yData,
            });
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
