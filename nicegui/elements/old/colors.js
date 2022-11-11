Vue.component("colors", {
  template: `<span v-bind:id="jp_props.id" style="display:none"></span>`,
  mounted() {
    var colors = this.$props.jp_props.options;
    for (var color in colors) {
      document.body.style.setProperty("--q-color-" + color, colors[color]);
    }
  },
  props: {
    jp_props: Object,
  },
});
