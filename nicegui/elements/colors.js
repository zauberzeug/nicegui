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
    if (this.customColors) {
      let customCSS = "";
      for (let customColor in this.customColors) {
        const colorName = customColor.replaceAll("_", "-");
        const colorVar = "--q-" + colorName;
        document.body.style.setProperty(colorVar, this.customColors[customColor]);
        customCSS += `.text-${colorName} { color: var(${colorVar}) !important; }\n`;
        customCSS += `.bg-${colorName} { background-color: var(${colorVar}) !important; }\n`;
      }
      const style = document.createElement("style");
      style.innerHTML = customCSS;
      style.dataset.niceguiCustomColors = "";
      document.head.querySelectorAll("[data-nicegui-custom-colors]").forEach((el) => el.remove());
      document.getElementsByTagName("head")[0].appendChild(style);
    }
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
