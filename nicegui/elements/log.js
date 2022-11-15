export default {
  template: "<textarea disabled></textarea>",
  data() {
    return {
      num_lines: 0,
    };
  },
  methods: {
    push(line) {
      const decoded = decodeURIComponent(line);
      const textarea = this.$el;
      textarea.innerHTML += (this.num_lines ? "\n" : "") + decoded;
      textarea.scrollTop = textarea.scrollHeight;
      this.num_lines += decoded.split("\n").length;
      while (this.max_lines && this.num_lines > this.max_lines) {
        const index = textarea.innerHTML.indexOf("\n");
        if (index == -1) break;
        textarea.innerHTML = textarea.innerHTML.slice(index + 1);
        this.num_lines -= 1;
      }
    },
  },
  props: {
    max_lines: Number,
  },
};
