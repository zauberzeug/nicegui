import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";
import { uPlot, optionsUpdateState, dataMatch } from "nicegui-uplot";

// Based on uplot-vue by @skalinichev (https://github.com/skalinichev/uplot-wrappers)
export default {
  template: "<div></div>",
  props: {
    options: { type: Object, required: true },
    data: { type: Array, required: true },
    scaleMode: { type: String, required: false },
  },
  data() {
    return {
      _chart: null,
      _uPlot: null,
    };
  },
  async mounted() {
    this._uPlot = uPlot;
    await this._create();
  },
  unmounted() {
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
            this._chart.setSize({ width: options.width, height: options.height });
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
      this._chart = new this._uPlot(options, this.$props.data, this.$el);
    },
  },
};
