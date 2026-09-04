export default {
  mounted() {
    this.update();
  },
  updated() {
    this.update();
  },
  methods: {
    update() {
      setDark(this.value);
    },
  },
  props: {
    value: Boolean,
  },
};
