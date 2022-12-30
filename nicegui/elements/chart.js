export default {
  template: "<div></div>",
  mounted() {
    const imports = this.extras.map((extra) => import(extra));
    Promise.allSettled(imports).then(() => {
      this.chart = Highcharts.chart(this.$el, this.options);
      this.chart.reflow();
    });
  },
  methods: {
    update_chart() {
      while (this.chart.series.length > this.options.series.length) this.chart.series[0].remove();
      while (this.chart.series.length < this.options.series.length) this.chart.addSeries({}, false);
      this.chart.update(this.options);
    },
  },
  props: {
    options: Object,
    extras: Array,
  },
};
