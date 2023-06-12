export default {
  template: "<textarea disabled></textarea>",
  data() {
    return {
      num_lines: 0,
      total_count: 0,
    };
  },
  mounted() {
    const text = decodeURIComponent(this.lines);
    this.$el.innerHTML = text;
    this.num_lines = text ? text.split("\n").length : 0;
    this.total_count = this.num_lines;
  },
  methods: {
    push(line, total_count) {
      if (total_count === this.total_count) return;
      this.total_count = total_count;
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
    clear() {
      const textarea = this.$el;
      textarea.innerHTML = "";
      this.num_lines = 0;
    },
  },
  props: {
    max_lines: Number,
    lines: String,
  },
};
