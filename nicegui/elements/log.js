var lines = [];

Vue.component("log", {
  template: `<div v-bind:id="jp_props.id">Hello!</div>`,
  mounted() {
    comp_dict[this.$props.jp_props.id] = this;
  },
  methods: {
    push(line) {
      lines.push(line);
      document.getElementById(this.$props.jp_props.id).innerText = lines;
    },
  },
  updated() {},
  props: {
    jp_props: Object,
  },
});
