Vue.component("log", {
  template: `<textarea v-bind:id="jp_props.id" :class="jp_props.classes" :style="jp_props.style"></textarea>`,
  mounted() {
    comp_dict[this.$props.jp_props.id] = this;
  },
  methods: {
    push(line) {
      const textarea = document.getElementById(this.$props.jp_props.id);
      textarea.innerHTML += (textarea.innerHTML ? "\n" : "") + line;
      textarea.scrollTop = textarea.scrollHeight;
    },
  },
  props: {
    jp_props: Object,
  },
});
