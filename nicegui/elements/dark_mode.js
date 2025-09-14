export default {
  mounted() {
    this.update();
  },
  updated() {
    this.update();
  },
  methods: {
    update() {
      Quasar.Dark.set(this.value === null ? "auto" : this.value);
    },
  },
  props: {
    value: Boolean,
  },
};
