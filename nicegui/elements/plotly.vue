<template>
  <div></div>
</template>

<script>
export default {
  async mounted() {
    await this.$nextTick();
    this.update();
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

      // re-use plotly instance if config is the same
      if (JSON.stringify(options.config) == JSON.stringify(this.last_options.config)) {
        Plotly.react(this.$el.id, this.options.data, this.options.layout);
      } else {
        Plotly.newPlot(this.$el.id, this.options.data, this.options.layout, options.config);
      }

      // store last options
      this.last_options = options;
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
</style>
