export default {
  mounted() {
    for (let name in this.$props) {
      if (name === "customColors") {
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
        document.getElementsByTagName('head')[0].appendChild(style);
        continue;
      }
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
    customColors: Object,
  },
};
