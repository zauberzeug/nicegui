export default {
  mounted() {
    this.notification = Quasar.Notify.create(this.options);
  },
  updated() {
    this.notification(this.options);
  },
  props: {
    options: Object,
  },
};
