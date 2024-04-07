import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: "<div></div>",
  mounted() {
    this.chart = echarts.init(this.$el);
    this.chart.on("click", (e) => this.$emit("pointClick", e));
    for (const event of [
      "click",
      "dblclick",
      "mousedown",
      "mousemove",
      "mouseup",
      "mouseover",
      "mouseout",
      "globalout",
      "contextmenu",
      "highlight",
      "downplay",
      "selectchanged",
      "legendselectchanged",
      "legendselected",
      "legendunselected",
      "legendselectall",
      "legendinverseselect",
      "legendscroll",
      "datazoom",
      "datarangeselected",
      "graphroam",
      "georoam",
      "treeroam",
      "timelinechanged",
      "timelineplaychanged",
      "restore",
      "dataviewchanged",
      "magictypechanged",
      "geoselectchanged",
      "geoselected",
      "geounselected",
      "axisareaselected",
      "brush",
      "brushEnd",
      "brushselected",
      "globalcursortaken",
      "rendered",
      "finished",
    ]) {
      this.chart.on(event, (e) => this.$emit(`chart:${event}`, e));
    }
    this.update_chart();
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
      convertDynamicProperties(this.options, true);
      this.chart.setOption(this.options, { notMerge: this.chart.options?.series.length != this.options.series.length });
    },
    run_chart_method(name, ...args) {
      if (name.startsWith(":")) {
        name = name.slice(1);
        args = args.map((arg) => new Function(`return (${arg})`)());
      }
      return runMethod(this.chart, name, args);
    },
  },
  props: {
    options: Object,
  },
};
