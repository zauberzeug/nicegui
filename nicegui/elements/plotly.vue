<template>
  <div></div>
</template>

<script>
export default {
  mounted() {
    setTimeout(() => {
      this.ensureLibLoaded().then(() => {
        // initial rendering of chart
        Plotly.newPlot(this.$el.id, this.options.data, this.options.layout, this.options.config);

        // register resize observer on parent div to auto-resize Plotly chart
        const doResize = () => {
          // only call resize if actually visible, otherwise error in Plotly.js internals
          if (this.isHidden(this.$el)) return;
          Plotly.Plots.resize(this.$el);
        };

        // throttle Plotly resize calls for better performance
        // using HTML5 ResizeObserver on parent div
        this.resizeObserver = new ResizeObserver((entries) => {
          if (this.timeoutHandle) {
            clearTimeout(this.timeoutHandle);
          }
          this.timeoutHandle = setTimeout(doResize, this.throttleResizeMs);
        });
        this.resizeObserver.observe(this.$el);
      });
    }, 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  unmounted() {
    this.resizeObserver.disconnect();
    clearTimeout(this.timeoutHandle);
  },

  methods: {
    isHidden(gd) {
      // matches plotly's implementation, as it needs to in order
      // to only resize the plot when plotly is rendering it.
      // https://github.com/plotly/plotly.js/blob/e1d94b7afad94152db004b3bd5e6060010fbcc28/src/lib/index.js#L1278
      var display = window.getComputedStyle(gd).display;
      return !display || display === "none";
    },

    ensureLibLoaded() {
      // ensure Plotly imported (lazy-load)
      return import(window.path_prefix + this.lib);
    },

    update(options) {
      // ensure Plotly imported, otherwise first plot will fail in update call
      // because library not loaded yet
      this.ensureLibLoaded().then(() => {
        Plotly.newPlot(this.$el.id, options.data, options.layout, options.config);
      });
    },
  },

  data: function () {
    return {
      resizeObserver: undefined,
      timeoutHandle: undefined,
      throttleResizeMs: 100, // resize at most every 100 ms
    };
  },

  props: {
    options: Object,
    lib: String,
  },
};
</script>

<style>
/*
  fix styles to correctly render modebar, otherwise large
  buttons with unwanted line breaks are shown, possibly
  due to other CSS libraries overriding default styles
  affecting plotly styling.
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
