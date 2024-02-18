export default {
  template: '<div style="position: absolute"></div>',
  mounted() {
    this.interval = setInterval(() => {
      const rect = this.$el.getBoundingClientRect();
      if (rect.bottom > -window.innerHeight && rect.top < 2 * window.innerHeight) {
        this.$emit("intersection");
      }
    }, 100);
  },
  methods: {
    stop() {
      clearInterval(this.interval);
    },
  },
};
