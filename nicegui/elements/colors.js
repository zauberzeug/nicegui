export default {
  mounted() {
    for (let name in this.$props) {
      document.body.style.setProperty("--q-" + name.replace("_", "-"), this.$props[name]);
    }
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
