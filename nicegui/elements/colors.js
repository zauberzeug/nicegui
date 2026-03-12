export default {
  mounted() {
    document.body.style.setProperty("--q-primary", this.primary);
    document.body.style.setProperty("--q-secondary", this.secondary);
    document.body.style.setProperty("--q-accent", this.accent);
    document.body.style.setProperty("--q-dark", this.dark);
    document.body.style.setProperty("--q-dark-page", this.darkPage);
    document.body.style.setProperty("--q-positive", this.positive);
    document.body.style.setProperty("--q-negative", this.negative);
    document.body.style.setProperty("--q-info", this.info);
    document.body.style.setProperty("--q-warning", this.warning);
    applyColors(this.customColors);
  },
  props: {
    primary: String,
    secondary: String,
    accent: String,
    dark: String,
    darkPage: String,
    positive: String,
    negative: String,
    info: String,
    warning: String,
    customColors: Object,
  },
};
