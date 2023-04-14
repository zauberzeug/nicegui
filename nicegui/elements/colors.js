export default {
  mounted() {
    for (let name in this.$props) {
      document.body.style.setProperty("--q-" + name, this.$props[name]);
    }
  },
  props: {
    primary: String,
    secondary: String,
    accent: String,
    dark: String,
    positive: String,
    negative: String,
    info: String,
    warning: String,
  },
};
