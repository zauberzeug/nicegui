import "xterm";

export default {
  template: "<div></div>",
  props: {
    options: Array,
  },
  async mounted() {
    this.terminal = new Terminal();
    this.terminal.open(this.$el)
    
    this.terminal.onData((e) => this.$emit(`data`, e));
  },
  methods: {
    write(data) {
      return this.terminal.write(data);
    },
  },
};
