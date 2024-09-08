export default {
  mounted() {
    for (let name in this.$props) {
      document.body.style.setProperty("--q-" + name, this.$props[name]);
    }
    document.body.style.setProperty("--q-dark-page", this.$props['dark_page']);
  },
  props: {
    primary: String,
    secondary: String,
    accent: String,
    dark: String,
    dark_page: String,
    positive: String,
    negative: String,
    info: String,
    warning: String,
  },
};
