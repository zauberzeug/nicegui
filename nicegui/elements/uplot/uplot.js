import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";
import { uPlot, optionsUpdateState, dataMatch } from "nicegui-uplot";

// Based on uplot-vue by @skalinichev (https://github.com/skalinichev/uplot-wrappers)
export default {
  template: "<div></div>",
  props: {
    options: { type: Object, required: true },
    data: { type: Array, required: true },
    scaleMode: { type: String, required: false, default: "reset" },
  },
  data() {
    return {
      _chart: null,
      _uPlot: null,
      _chrome: 0, // measured height of uPlot's title + legend, reserved so they fit inside the host
      _resizeFrame: null,
    };
  },
  async mounted() {
    this._uPlot = uPlot;
    await this._create();
    // uPlot needs explicit width/height as initial dimensions; the ResizeObserver then keeps the
    // chart in sync with the host element afterwards (same approach as ui.echart), so it can follow
    // its container when sized via CSS classes.
    this.resizeObserver = new ResizeObserver(() => this._resize());
    this.resizeObserver.observe(this.$el);
  },
  unmounted() {
    this.resizeObserver?.disconnect();
    cancelAnimationFrame(this._resizeFrame);
    this._destroy();
  },
  watch: {
    options: {
      handler(options, prevOptions) {
        (async () => {
          let next = { ...options };
          let prev = { ...prevOptions };
          convertDynamicProperties(next, true);
          convertDynamicProperties(prev, true);
          const optionsState = optionsUpdateState(prev, next);
          if (!this._chart || optionsState === "create") {
            this._destroy();
            await this._create();
          } else if (optionsState === "update") {
            // Size is governed by the host element (see _resize), not by options.width/height,
            // which only act as the initial dimensions.
            this._resize();
          }
        })();
      },
      deep: true,
    },
    data: {
      handler(data, prevData) {
        (async () => {
          if (!this._chart) {
            await this._create();
          } else if (!dataMatch(prevData, data)) {
            const mode = this.$props.scaleMode;
            if (mode === "preserve_all") {
              this._chart.setData(data, false);
              this._chart.redraw();
            } else if (mode === "preserve_zoom") {
              this._chart.setData(data);
              var min = Math.min(...prevData[0]);
              var max = Math.max(...prevData[0]);
              if (this._chart.scales.x.max != max || this._chart.scales.x.min != min) {
                this._restoreZoomState();
              }
            } else {
              this._chart.setData(data);
            }
          }
        })();
      },
      deep: true,
    },
  },
  methods: {
    _resize() {
      // Match the chart to its host element. This runs both from the ResizeObserver (on genuine
      // container resizes) and right after (re)creating the chart, because a programmatic recreate
      // does not change the host's size and would otherwise leave the chart at options.width/height.
      if (!this._chart) return;
      const width = this.$el.offsetWidth;
      const height = this.$el.offsetHeight;
      if (!width || !height) return;
      // uPlot renders the title and legend as DOM siblings of the plot, so reserve room for them and
      // shrink the plot to keep the whole chart inside the host box instead of overflowing it (like
      // ui.echart). Their height is only known once laid out and can change (e.g. the legend wrapping
      // to another row), so apply the last known value now and re-measure on the next frame.
      this._chart.setSize({ width, height: Math.max(0, height - this._chrome) });
      cancelAnimationFrame(this._resizeFrame);
      this._resizeFrame = requestAnimationFrame(() => {
        if (!this._chart) return;
        const chrome = this._chart.root.offsetHeight - this._chart.height;
        if (chrome >= 0 && chrome !== this._chrome) {
          this._chrome = chrome;
          this._resize();
        }
      });
    },
    _restoreZoomState() {
      if (this._chart) {
        const zoom = {};
        for (const [key, scale] of Object.entries(this._chart.scales)) {
          if (scale && typeof scale.min === "number" && typeof scale.max === "number") {
            zoom[key] = { min: scale.min, max: scale.max };
          }
        }
        if (zoom) {
          for (const [key, state] of Object.entries(zoom)) {
            if (
              this._chart.scales &&
              this._chart.scales[key] &&
              typeof state.min === "number" &&
              typeof state.max === "number"
            ) {
              this._chart.setScale(key, { min: state.min, max: state.max });
            }
          }
        }
      }
    },
    _destroy() {
      if (this._chart) {
        this._chart.destroy();
        this._chart = null;
      }
    },
    async _create() {
      if (!this._uPlot) return;
      if (this._chart) {
        this._destroy();
      }
      let options = { ...this.$props.options };
      convertDynamicProperties(options, true);
      // Create at the host's current size (when laid out) so the title/legend lay out for the final
      // width from the start; options.width/height only act as a fallback for the initial render.
      if (this.$el.offsetWidth) options.width = this.$el.offsetWidth;
      if (this.$el.offsetHeight) options.height = this.$el.offsetHeight;
      this._chart = new this._uPlot(options, this.$props.data, this.$el);
      this._resize();
    },
  },
};
