Vue.component("colors", {
  template: `<span v-bind:id="jp_props.id" :class="jp_props.classes" :style="jp_props.style"></span>`,
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
