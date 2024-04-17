import { loadResource } from "../../static/utils/resources.js";

export default {
  template: `
    <div style="width: 100%">
      <textarea ref="myTextarea"></textarea>
    </div>
  `,
  props: {
    value: String,
    mode: String,
    theme: String,
  },
  updated() {
    if (this.codemirror && this.codemirror.getValue() !== this.value) this.codemirror.setValue(this.value);
  },
  async mounted() {
    // NOTE: both of these are actually CodeMirror v5
    const base6 = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7";
    const base5 = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.1";

    await Promise.all([
      loadResource(base6 + "/codemirror.min.css"),
      loadResource(base5 + `/theme/${this.theme}.min.css`),
      // codemirror.min.js must be loaded before any other codemirror .js files
      loadResource(base6 + "/codemirror.min.js").then(() =>
        Promise.all([
          loadResource(`${base6}/mode/${this.mode}/${this.mode}.min.js`),
          loadResource(base6 + "/addon/edit/closebrackets.min.js"),
        ])
      ),
    ]);

    const myTextarea = this.$refs.myTextarea;
    this.codemirror = CodeMirror.fromTextArea(myTextarea, {
      language: this.mode,
      theme: this.theme,
      lineNumbers: true,
      autoCloseBrackets: true,
      indentWithTabs: false,
      indentUnit: 4,
      tabSize: 4,
      smartIndent: true,
    });
    this.codemirror.on("change", () => {
      const value = this.codemirror.getValue();
      this.$emit("change", value);
      this.$emit("update:value", value);
    });
  },
};
