export default {
  created () {
    document.addEventListener('visibilitychange', this.handle_visibility, false)
  },
  data() {
    return {
      value: 0,
    };
  },
  methods: {
    handle_visibility() {
      if (document.visibilityState === "visible") {
        this.value += 1;
        this.$emit("change", this.value);
      }
    }
  }
};
