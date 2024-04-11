<template>
  <div></div>
</template>

<script>
export default {
  async mounted() {
    await this.$nextTick();
    this.update();
    this.set_handlers();
  },
  updated() {
    this.update();
  },
  methods: {
    update() {
      // default responsive to true
      const options = this.options;
      if (options.config === undefined) options.config = { responsive: true };
      if (options.config.responsive === undefined) options.config.responsive = true;

      // Plotly.react can be used to create a new plot and to update it efficiently
      // https://plotly.com/javascript/plotlyjs-function-reference/#plotlyreact
      Plotly.react(this.$el.id, this.options.data, this.options.layout, options.config);
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
</style>
