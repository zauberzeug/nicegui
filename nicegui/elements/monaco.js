import { loadResource } from "../../static/utils/resources.js";
export default {
  props: {
    language: String,
    theme: String,
    value: String,
    minimap: Boolean,
  },

  template: `<div ref="editor" style="width: 100%; height: 100%;"></div>`,

  async mounted() {
    await loadResource("https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.47.0/min/vs/loader.js");
    this.initMonacoEditor();
  },

  methods: {
    initMonacoEditor() {
      // Wait for Monaco to be initialized
      // Monaco Editor is now initialized
      monaco.editor.create(this.$refs.editor, {
        value: this.value,
        language: this.language,
        theme: this.theme,
        automaticLayout: true, // Adjusts the editor's layout automatically
        minimap: {
          enabled: this.minimap, // Optionally disable the minimap
        },
      });
    },
  },
};
