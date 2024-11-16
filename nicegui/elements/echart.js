import "echarts";
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: "<div></div>",
  async mounted() {
    await new Promise((resolve) => setTimeout(resolve, 0)); // wait for Tailwind classes to be applied
    if (this.enable_3d) {
      await import("echarts-gl");
    }

    this.chart = echarts.init(this.$el, null, { renderer: this.renderer });
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

    // Prevent interruption of chart animations due to resize operations.
    // It is recommended to register the callbacks for such an event before setOption.
    const createResizeObserver = () => {
      new ResizeObserver(this.chart.resize).observe(this.$el);
      this.chart.off("finished", createResizeObserver);
    };
    this.chart.on("finished", createResizeObserver);

    this.update_chart();
  },
  beforeDestroy() {
    this.chart.dispose();
  },
  beforeUnmount() {
    this.chart.dispose();
  },
  methods: {
    update_chart() {
      if (!this.chart) {
        setTimeout(this.update_chart, 10);
        return;
      }
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
    enable_3d: Boolean,
    renderer: String,
  },
};
