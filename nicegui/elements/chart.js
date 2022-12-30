export default {
  template: "<div></div>",
  mounted() {
    for (const extra of this.extras) {
      console.log("loading extra " + extra);
      import(extra)
        .then((module) => {
          console.log("loaded extra " + extra);
        })
        .catch((err) => {
          console.log("error loading extra " + extra);
          console.log(err);
        });
    }
    setTimeout(() => {
      this.chart = Highcharts.chart(this.$el, this.options);
      this.chart.reflow();
    }, 1000);
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
