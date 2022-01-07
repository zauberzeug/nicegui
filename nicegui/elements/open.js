Vue.component("open", {
  template: `<span v-bind:id="jp_props.id" :class="jp_props.classes" :style="jp_props.style"></span>`,
  mounted() {
    comp_dict[this.$props.jp_props.id] = this;
    console.log("Mounted!");
  },
  methods: {
    redirect(line) {
      window.location.href = line;
    },
  },
  props: {
    jp_props: Object,
  },
});
