<template>
  <div></div>
</template>

<script>
export default {
  async mounted() {
    await import("plotly");
    this.update();
  },
  methods: {
    update() {
      // wait for plotly to be loaded
      if (typeof Plotly === "undefined") {
        setTimeout(this.update, 10);
        return;
      }

      // default responsive to true
      const options = this.options;
      if (options.config === undefined) options.config = { responsive: true };
      if (options.config.responsive === undefined) options.config.responsive = true;

      // re-use plotly instance if config is the same
      if (JSON.stringify(options.config) == JSON.stringify(this.last_options.config)) {
        Plotly.react(this.$el.id, this.options.data, this.options.layout);
      } else {
        Plotly.newPlot(this.$el.id, this.options.data, this.options.layout, options.config);
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
      last_options: {},
    };
  },
  props: {
    options: Object,
  },
};
</script>

<style>
/*
  fix styles to correctly render modebar, otherwise large buttons with unwanted line breaks are shown,
  possibly due to other CSS libraries overriding default styles affecting plotly styling.
*/
.js-plotly-plot .plotly .modebar-group {
  display: flex;
}
.js-plotly-plot .plotly .modebar-btn {
  display: flex;
}
.js-plotly-plot .plotly .modebar-btn svg {
  position: static;
}
/*
  fix overflow when adding borders to the plotly plot
*/
.js-plotly-plot {
  box-sizing: content-box;
}
</style>
