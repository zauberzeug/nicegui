import { toRaw } from "vue";
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";
import { uPlot, optionsChanged, dataMatch } from "nicegui-uplot";

// Based on uplot-vue by @skalinichev (https://github.com/skalinichev/uplot-wrappers)
export default {
  template: "<div></div>",
  props: {
    options: { type: Object, required: true },
    data: { type: Array, required: true },
    scaleMode: { type: String, required: false, default: "reset" },
  },
  created() {
    this.chart = null;
    this.chrome = 0; // measured height of uPlot's title + legend, reserved so they fit inside the host
    this.resizeFrame = null;
  },
  mounted() {
    this._create();
    // uPlot needs explicit width/height as initial dimensions; the ResizeObserver then keeps the
    // chart in sync with the host element afterwards (same approach as ui.echart), so it can follow
    // its container when sized via CSS classes.
    this.resizeObserver = new ResizeObserver(() => this._resize());
    this.resizeObserver.observe(this.$el);
  },
  unmounted() {
    this.resizeObserver?.disconnect();
    cancelAnimationFrame(this.resizeFrame);
    this._destroy();
  },
  // NiceGUI replaces the whole prop object on every update, so the watchers need not be deep.
  // The props are also unwrapped (toRaw) before handing them to uPlot, which indexes into the data
  // arrays in its drawing loops; Vue's reactive proxies would slow these down considerably.
  watch: {
    options(options, prevOptions) {
      // compare the raw options, so ":"-prefixed functions are compared by their source strings
      if (optionsChanged(toRaw(prevOptions), toRaw(options))) this._create();
    },
    data(data, prevData) {
      data = toRaw(data);
      prevData = toRaw(prevData);
      if (dataMatch(prevData, data)) return;
      let keepScales = this.scaleMode === "preserve_all";
      if (this.scaleMode === "preserve_zoom") {
        // keep the current scales only while zoomed in, else refit; x-values are sorted ascending,
        // so first/last are the range
        const xs = prevData[0];
        const x = this.chart.scales.x;
        keepScales = xs?.length > 0 && (x.min > xs[0] || x.max < xs[xs.length - 1]);
      }
      this.chart.setData(data, !keepScales);
      if (keepScales) this.chart.redraw(); // setData(data, false) updates the data but does not redraw
    },
  },
  methods: {
    _resize() {
      // Match the chart to its host element. This runs both from the ResizeObserver (on genuine
      // container resizes) and right after (re)creating the chart, because a programmatic recreate
      // does not change the host's size and would otherwise leave the chart at options.width/height.
      if (!this.chart) return;
      const width = this.$el.offsetWidth;
      const height = this.$el.offsetHeight;
      if (!width || !height) return;
      // uPlot renders the title and legend as DOM siblings of the plot, so reserve room for them and
      // shrink the plot to keep the whole chart inside the host box instead of overflowing it (like
      // ui.echart). Their height is only known once laid out and can change (e.g. the legend wrapping
      // to another row), so apply the last known value now and re-measure on the next frame.
      this.chart.setSize({ width, height: Math.max(0, height - this.chrome) });
      cancelAnimationFrame(this.resizeFrame);
      this.resizeFrame = requestAnimationFrame(() => {
        if (!this.chart) return;
        const chrome = this.chart.root.offsetHeight - this.chart.height;
        if (chrome >= 0 && chrome !== this.chrome) {
          this.chrome = chrome;
          this._resize();
        }
      });
    },
    _destroy() {
      this.chart?.destroy();
      this.chart = null;
    },
    _create() {
      this._destroy();
      // convert ":"-prefixed properties on a copy, so the prop itself keeps its source strings
      const options = structuredClone(toRaw(this.options));
      convertDynamicProperties(options, true);
      // Create at the host's current size (when laid out) so the title/legend lay out for the final
      // width from the start. The host defaults to options.width/height via CSS (see uplot.py), so
      // this normally matches the options; it differs only when CSS classes/.style() resize the host.
      if (this.$el.offsetWidth) options.width = this.$el.offsetWidth;
      if (this.$el.offsetHeight) options.height = this.$el.offsetHeight;
      this.chart = new uPlot(options, toRaw(this.data), this.$el);
      this._resize();
    },
  },
};
