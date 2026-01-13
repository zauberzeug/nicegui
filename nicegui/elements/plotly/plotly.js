export default {
  template: "<div></div>",
  async mounted() {
    const { Plotly } = await import("nicegui-plotly");
    this.Plotly = Plotly;
    this.update();
    this.$nextTick(() => {
      this.resizeObserver = new ResizeObserver(() => {
        if (this.options.config?.responsive === false) return;
        this.Plotly.Plots.resize(this.$el);
      });
      this.resizeObserver.observe(this.$el);
    });
  },
  unmounted() {
    this.resizeObserver?.disconnect();
  },
  methods: {
    update() {
      // wait for plotly to be loaded
      if (typeof this.Plotly === "undefined") {
        setTimeout(this.update, 10);
        return;
      }

      // default responsive to true
      const options = this.options;
      if (options.config?.responsive === true) options.config.responsive = undefined;

      // reuse plotly instance if config is the same
      if (this.last_options && JSON.stringify(options.config) === JSON.stringify(this.last_options.config)) {
        this.Plotly.react(this.$el, this.options, options.config);
      } else {
        this.Plotly.newPlot(this.$el, this.options, options.config);
        this.set_handlers();
      }

      // store last options
      this.last_options = options;
    },
    set_handlers() {
      // forward events
      for (const name of [
        // source: https://plotly.com/javascript/plotlyjs-events/
        "plotly_click",
        "plotly_legendclick",
        "plotly_selecting",
        "plotly_selected",
        "plotly_hover",
        "plotly_unhover",
        "plotly_legenddoubleclick",
        "plotly_restyle",
        "plotly_relayout",
        "plotly_webglcontextlost",
        "plotly_afterplot",
        "plotly_autosize",
        "plotly_deselect",
        "plotly_doubleclick",
        "plotly_redraw",
        "plotly_animated",
      ]) {
        this.$el.on(name, (event) => {
          const args = {
            ...event,
            points: event?.points?.map((p) => ({
              ...p,
              fullData: undefined,
              xaxis: undefined,
              yaxis: undefined,
            })),
            xaxes: undefined,
            yaxes: undefined,
          };
          this.$emit(name, args);
        });
      }
    },
  },
  data() {
    return {
      last_options: null,
    };
  },
  props: {
    options: Object,
  },
};
