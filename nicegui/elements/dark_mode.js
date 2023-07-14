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
      if (window.tailwind) {
        tailwind.config.darkMode = this.value === null ? "media" : "class";
        if (this.value) document.body.classList.add("dark");
        else document.body.classList.remove("dark");
      }
    },
  },
  props: {
    value: Boolean,
  },
};
