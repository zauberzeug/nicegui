import { toRaw } from "vue";
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";
import { loadResource } from "../../static/utils/resources.js";
import { uPlot } from "nicegui-uplot";

// Based on uplot-vue by @skalinichev (https://github.com/skalinichev/uplot-wrappers)
export default {
  template: "<div></div>",
  props: {
    options: Object,
    data: Array,
    keepZoom: Boolean,
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
    // follow the dark mode, which Quasar toggles via a class on the body
    this.themeObserver = new MutationObserver(() => {
      this._updateColors();
      this.chart?.redraw(false);
    });
    this.themeObserver.observe(document.body, { attributes: true, attributeFilter: ["class"] });
    this._create();
  },
  unmounted() {
    this.resizeObserver?.disconnect();
    this.themeObserver?.disconnect();
    this._destroy();
  },
  // NiceGUI replaces the whole prop on every update, so the watchers need not be deep.
  // toRaw avoids Vue's reactive proxies, which would slow down uPlot's drawing loops considerably.
  watch: {
    options(options, prevOptions) {
      if (!this.chart) return;
      // width and height are ignored; ":"-prefixed functions are still source strings here
      const withoutSize = ({ width, height, ...rest }) => JSON.stringify(rest);
      if (withoutSize(prevOptions) !== withoutSize(options)) this._create();
    },
    data(data, prevData) {
      if (!this.chart) return;
      data = toRaw(data);
      prevData = toRaw(prevData);
      // NiceGUI sends all props on every update, so unchanged data must not trigger setData
      const same = (a, b) =>
        a.length === b.length && a.every((s, i) => s.length === b[i].length && s.every((v, j) => v === b[i][j]));
      if (same(prevData, data)) return;
      const keepScales = this.keepZoom && this._isZoomed(prevData[0]);
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
    _updateColors() {
      const [r, g, b] = getComputedStyle(this.$el).color.match(/[\d.]+/g);
      let background = "#fff";
      for (let el = this.$el; el; el = el.parentElement) {
        const color = getComputedStyle(el).backgroundColor;
        if (color !== "transparent" && !/^rgba\(.*, 0\)$/.test(color)) {
          background = color;
          break;
        }
      }
      this.colors = { text: `rgb(${r}, ${g}, ${b})`, faint: `rgba(${r}, ${g}, ${b}, 0.1)`, background };
    },
    _applyColorDefaults(options) {
      // uPlot hard-codes black and white for these, so derive them from the page unless the user sets them
      const text = () => this.colors.text;
      const faint = () => this.colors.faint;
      const background = () => this.colors.background;
      const axes = options.axes ?? [];
      options.axes = [axes[0], axes[1], ...axes.slice(2)].map((axis = {}) => ({
        stroke: text,
        ...axis,
        grid: { stroke: faint, ...axis.grid },
        ticks: { stroke: faint, ...axis.ticks },
      }));
      options.series = options.series?.map((series, i) =>
        i === 0 ? series : { ...series, points: { fill: background, ...series?.points } },
      );
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
      this._updateColors();
      this._applyColorDefaults(options);
      const { width, height } = this._hostSize();
      if (!width || !height) return; // wait for the host to get a size
      options.width = width;
      options.height = height;
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
