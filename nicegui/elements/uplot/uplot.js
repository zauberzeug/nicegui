import { toRaw } from "vue";
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";
import { loadResource } from "../../static/utils/resources.js";
import { uPlot, optionsChanged, dataMatch } from "nicegui-uplot";

// Based on uplot-vue by @skalinichev (https://github.com/skalinichev/uplot-wrappers)
export default {
  template: "<div></div>",
  props: {
    options: { type: Object, required: true },
    data: { type: Array, required: true },
    scaleMode: { type: String, required: false, default: "reset" },
    resourcePath: String,
  },
  created() {
    this.chart = null;
  },
  async mounted() {
    await this.$nextTick(); // wait for window.path_prefix to be set
    await loadResource(window.path_prefix + `${this.resourcePath}/uPlot.min.css`);
    // creates the chart once the host has a size (e.g. when revealed) and keeps it sized to the host afterwards
    this.resizeObserver = new ResizeObserver(() => (this.chart ? this._resize() : this._create()));
    this.resizeObserver.observe(this.$el);
    this._create();
  },
  unmounted() {
    this.resizeObserver?.disconnect();
    this._destroy();
  },
  // NiceGUI replaces the whole prop on every update, so the watchers need not be deep.
  // toRaw avoids Vue's reactive proxies, which would slow down uPlot's drawing loops considerably.
  watch: {
    options(options, prevOptions) {
      if (!this.chart) return;
      // compare the raw options, so ":"-prefixed functions are compared by their source strings
      if (optionsChanged(toRaw(prevOptions), toRaw(options))) this._create();
    },
    data(data, prevData) {
      if (!this.chart) return;
      data = toRaw(data);
      prevData = toRaw(prevData);
      if (dataMatch(prevData, data)) return;
      const keepScales =
        this.scaleMode === "preserve_all" || (this.scaleMode === "preserve_zoom" && this._isZoomed(prevData[0]));
      this.chart.setData(data, !keepScales);
      if (keepScales) this.chart.redraw(); // setData(data, false) does not redraw
    },
  },
  methods: {
    _hostSize() {
      const style = getComputedStyle(this.$el);
      return {
        width: Math.max(0, this.$el.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight)),
        height: Math.max(0, this.$el.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom)),
      };
    },
    _isZoomed(xs) {
      // the x scale differs from the range uPlot would fit to the previous data
      if (!xs?.length) return false;
      const key = this.chart.series[0].scale;
      const scale = this.chart.scales[key];
      const [min, max] = scale.range(
        this.chart,
        ...(scale.distr === 2 ? [0, xs.length - 1] : [xs[0], xs[xs.length - 1]]),
        key,
      );
      return scale.min !== min || scale.max !== max;
    },
    _resize() {
      const { width, height } = this._hostSize();
      if (!width || !height) return;
      // uPlot sizes only the plot, so reserve room for the title and legend around it
      const chrome = Math.max(0, this.chart.root.offsetHeight - this.chart.height);
      const plotHeight = Math.max(0, height - chrome);
      if (width === this.chart.width && plotHeight === this.chart.height) return; // setSize always redraws
      this.chart.setSize({ width, height: plotHeight });
    },
    _destroy() {
      this.chart?.destroy();
      this.chart = null;
    },
    _create() {
      this._destroy();
      // convert ":"-prefixed properties on a copy, so the prop keeps its source strings
      const options = structuredClone(toRaw(this.options));
      convertDynamicProperties(options, true);
      const { width, height } = this._hostSize();
      options.width = width || options.width;
      options.height = height || options.height;
      if (!options.width || !options.height) return; // wait for the host to get a size
      this.chart = new uPlot(options, toRaw(this.data), this.$el);
      this._resize();
      // the live legend can grow without resizing the host
      this.resizeObserver.disconnect();
      for (const el of [this.$el, ...this.chart.root.querySelectorAll(".u-title, .u-legend")]) {
        this.resizeObserver.observe(el);
      }
    },
  },
};
