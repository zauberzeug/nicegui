var num_lines = 0;

Vue.component("log", {
  template: `<textarea v-bind:id="jp_props.id" :class="jp_props.classes" :style="jp_props.style" disabled></textarea>`,
  mounted() {
    comp_dict[this.$props.jp_props.id] = this;
  },
  methods: {
    push(line) {
      const decoded = decodeURIComponent(line);
      const textarea = document.getElementById(this.$props.jp_props.id);
      textarea.innerHTML += (num_lines ? "\n" : "") + decoded;
      textarea.scrollTop = textarea.scrollHeight;
      num_lines += decoded.split("\n").length;

      const max_lines = this.$props.jp_props.options.max_lines;
      while (max_lines != null && num_lines > max_lines) {
        const index = textarea.innerHTML.indexOf("\n");
        if (index == -1) break;
        textarea.innerHTML = textarea.innerHTML.slice(index + 1);
        num_lines -= 1;
      }
    },
  },
  props: {
    jp_props: Object,
  },
});
