export default {
  template: "<div></div>",
  mounted() {
    this.chart = Highcharts.chart(this.$el, this.options);
    setTimeout(() => {
      this.chart.reflow();
    }, 0);
  },
  methods: {
    update_chart() {
      while (this.chart.series.length > this.options.series.length) this.chart.series[0].remove();
      while (this.chart.series.length < this.options.series.length) this.chart.addSeries({}, false);
      this.chart.update(this.options, false);
      this.chart.redraw();
    },
  },
  props: {
    options: Object,
  },
};
