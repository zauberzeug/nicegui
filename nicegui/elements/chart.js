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
      this.chart.update(this.options);
    },
  },
  props: {
    options: Object,
  },
};
