export default {
  template: '<div style="position: absolute"></div>',
  mounted() {
    this.observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          this.observer.disconnect();
          this.$emit("intersection");
        }
      },
      { rootMargin: "100% 0px 100% 0px" },
    );
    this.observer.observe(this.$el);
  },
  unmounted() {
    this.observer.disconnect();
  },
};
