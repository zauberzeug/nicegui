export default {
  mounted() {
    if (!this.atRule) {
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
      return;
    }
    const colors = {
      "--q-primary": this.primary,
      "--q-secondary": this.secondary,
      "--q-accent": this.accent,
      "--q-dark": this.dark,
      "--q-dark-page": this.darkPage,
      "--q-positive": this.positive,
      "--q-negative": this.negative,
      "--q-info": this.info,
      "--q-warning": this.warning,
    };
    let css = Object.entries(colors)
      .map(([k, v]) => `  body { ${k}: ${v} !important; }`)
      .join("\n");
    for (const [color, value] of Object.entries(this.customColors || {})) {
      const name = color.replaceAll("_", "-");
      const varName = "--q-" + name;
      css += `\n  body { ${varName}: ${value} !important; }`;
      css += `\n  .text-${name} { color: var(${varName}) !important; }`;
      css += `\n  .bg-${name} { background-color: var(${varName}) !important; }`;
    }
    this.styleEl = document.createElement("style");
    this.styleEl.innerHTML = `${this.atRule} {\n${css}\n}`;
    document.head.appendChild(this.styleEl);
  },
  unmounted() {
    this.styleEl?.remove();
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
    atRule: String,
    customColors: Object,
  },
};
