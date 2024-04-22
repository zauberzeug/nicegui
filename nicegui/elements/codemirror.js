export default {
  template: `
    <div></div>
  `,
  props: {
    value: String,
    language: String,
    theme: String,
    resource_path: String,
    lineWrapping: Boolean,
    minHeight: String,
    fixedHeight: String,
    maxHeight: String,
    disable: Boolean,
    indent: String,
    highlightWhitespace: Boolean,
  },
  watch: {
    value(new_value) {
      this.set_editor_value(new_value);
    },
    language(new_language) {
      this.set_language(new_language);
    },
    theme(new_theme) {
      this.set_theme(new_theme);
    },
    disable(new_disable) {
      this.set_disabled(new_disable);
    },
  },
  data() {
    return {
      editorPromise: new Promise((resolve) => {
        this.resolveEditor = resolve;
      }),
    };
  },
  methods: {
    // Find the language's extension by its name. Case insensitive.
    find_language(name) {
      for (const language of this.languages)
        for (const alias of [language.name, ...language.alias])
          if (name.toLowerCase() === alias.toLowerCase()) return language;

      console.error(`Language not found: ${this.language}`);
      console.info("Supported languages names:", languages.map((lang) => lang.name).join(", "));
      return null;
    },
    // Get the names of all supported languages
    async get_languages() {
      if (!this.editor) await this.editorPromise;
      // Over 100 supported languages: https://github.com/codemirror/language-data/blob/main/src/language-data.ts
      return this.languages.map((lang) => lang.name);
    },
    set_language(language) {
      const lang_description = this.find_language(language, this.languages);
      if (!lang_description) {
        console.error("Language not found:", language);
        return;
      }

      lang_description.load().then((extension) => {
        this.editor.dispatch({
          effects: this.languageConfig.reconfigure([extension]),
        });
      });
    },
    async get_themes() {
      if (!this.editor) await this.editorPromise;
      // `this.themes` also contains some non-theme objects
      // The real themes are Arrays
      return Object.keys(this.themes).filter((key) => Array.isArray(this.themes[key]));
    },
    set_theme(theme) {
      const new_theme = this.themes[theme];
      if (new_theme === undefined) {
        console.error("Theme not found:", theme);
        return;
      }
      this.editor.dispatch({
        effects: this.themeConfig.reconfigure([new_theme]),
      });
    },
    set_editor_value(value) {
      if (!this.editor) return;
      if (this.editor.state.doc.toString() === value) return;

      this.emitting = false;
      this.editor.dispatch({ changes: { from: 0, to: this.editor.state.doc.length, insert: value } });
      this.emitting = true;
    },
    set_disabled(disabled) {
      this.editor.dispatch({
        effects: this.editableConfig.reconfigure(this.editableStates[!disabled]),
      });
    },
  },
  async mounted() {
    const {
      EditorView,
      Compartment,
      basicSetup,
      keymap,
      indentWithTab,
      languages,
      themes,
      oneDark,
      indentUnit,
      highlightWhitespace,
    } = await import(`${this.resource_path}/editor.js`);

    // This flag is used to prevent emitting the same value
    // again when the editor was just updated from the server
    this.emitting = true;

    const changeListener = EditorView.updateListener.of((update) => {
      if (!this.emitting) return;
      if (!update.docChanged) return;
      const value = update.state.doc.toString();
      this.$emit("update:value", value);
    });

    // The Compartments are used to change the properties of the editor ("extensions") dynamically
    this.themes = { ...themes, oneDark: oneDark };
    this.themeConfig = new Compartment();
    this.languages = languages;
    this.languageConfig = new Compartment();
    this.editableConfig = new Compartment();
    this.editableStates = { true: EditorView.editable.of(true), false: EditorView.editable.of(false) };

    const extensions = [
      basicSetup,
      changeListener,
      // Enables the Tab key to indent the current lines https://codemirror.net/examples/tab/
      keymap.of([indentWithTab]),
      // Sets indentation https://codemirror.net/docs/ref/#language.indentUnit
      indentUnit.of(this.indent),
      // We will set these compartments later and dynamically through props
      this.themeConfig.of([]),
      this.languageConfig.of([]),
      this.editableConfig.of([]),
    ];

    if (this.lineWrapping) extensions.push(EditorView.lineWrapping);
    if (this.highlightWhitespace) extensions.push([highlightWhitespace()]);

    // Convenience function to add theme properties below
    const addToTheme = (content) => {
      extensions.push(EditorView.theme(content));
    };

    // Setting the height properly through tailwind is likely not possible,
    // so we use the recommended ways from https://codemirror.net/examples/styling/
    if (this.fixedHeight) {
      addToTheme({
        "&": { height: this.fixedHeight },
        ".cm-scroller": { overflow: "auto" },
      });
    } else {
      if (this.maxHeight)
        addToTheme({
          "&": { "max-height": this.maxHeight },
          ".cm-scroller": { overflow: "auto" },
        });
      if (this.minHeight)
        addToTheme({
          ".cm-content, .cm-gutter": { minHeight: this.minHeight },
        });
    }

    this.editor = new EditorView({
      doc: this.value,
      extensions: extensions,
      parent: this.$el,
    });

    this.resolveEditor(this.editor);

    this.set_language(this.language);
    this.set_theme(this.theme);
    this.set_disabled(this.disable);
  },
};
