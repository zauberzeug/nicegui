export default {
  props: {
    language: String,
    theme: String,
    value: String,
    minimap: Boolean,
  },

  template: `<div ref="editor" style="width: 100%; height: 100%;"></div>`,

  async mounted() {
    await this.loadMonacoResources();
    this.initMonacoEditor();
  },

  methods: {
    loadMonacoResources() {
      // Load Monaco Editor resources asynchronously
      return new Promise((resolve, reject) => {
        // Check if Monaco is already loaded
        if (window.monaco) {
          resolve();
          return;
        }

        // Load Monaco Loader script
        const script = document.createElement("script");
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.29.0/min/vs/loader.js";
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    },

    initMonacoEditor() {
      // Wait for Monaco to be initialized
      require.config({ paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.29.0/min/vs" } });
      require(["vs/editor/editor.main"], () => {
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
      });
    },
  },
};
