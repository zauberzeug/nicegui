import * as CM from "nicegui-codemirror";

export default {
  template: `
    <div></div>
  `,
  props: {
    value: String,
    language: String,
    theme: String,
    lineWrapping: Boolean,
    disable: Boolean,
    indent: String,
    highlightWhitespace: Boolean,
    completions: Array,
    replaceLanguageCompletions: Boolean,
    completeWordsInDocument: Boolean,
    tooltipClass: String,
    id: String,
  },
  watch: {
    language(newLanguage) {
      this.setLanguage(newLanguage);
    },
    theme(newTheme) {
      this.setTheme(newTheme);
    },
    disable(newDisable) {
      this.setDisabled(newDisable);
    },
    lineWrapping(newLineWrapping) {
      this.setLineWrapping(newLineWrapping);
    },
    completions() {
      this.rebuildCompletions();
    },
    replaceLanguageCompletions() {
      this.rebuildCompletions();
    },
    completeWordsInDocument() {
      this.rebuildCompletions();
    },
    tooltipClass() {
      this.rebuildCompletions();
    },
  },
  data() {
    return {
      // To let other methods wait for the editor to be created because
      // they might be called by the server before the editor is created.
      editorPromise: new Promise((resolve) => {
        this.resolveEditor = resolve;
      }),
    };
  },
  beforeUnmount() {
    if (this.editor) {
      const element = mounted_app.elements[this.$props.id.slice(1)];
      if (element) element.props.value = this.editor.state.doc.toString();
    }
  },
  methods: {
    // Find the language's extension by its name. Case insensitive.
    findLanguage(name) {
      for (const language of this.languages)
        for (const alias of [language.name, ...language.alias])
          if (name.toLowerCase() === alias.toLowerCase()) return language;

      console.error(`Language not found: ${this.language}`);
      console.info("Supported language names:", languages.map((lang) => lang.name).join(", "));
      return null;
    },
    // Get the names of all supported languages
    async getLanguages() {
      if (!this.editor) await this.editorPromise;
      // Over 100 supported languages: https://github.com/codemirror/language-data/blob/main/src/language-data.ts
      return this.languages.map((lang) => lang.name).sort(Intl.Collator("en").compare);
    },
    setLanguage(language) {
      if (!language) {
        this.editor.dispatch({
          effects: this.languageConfig.reconfigure([]),
        });
        return;
      }

      const lang_description = this.findLanguage(language, this.languages);
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
    async getThemes() {
      if (!this.editor) await this.editorPromise;
      // `this.themes` also contains some non-theme objects
      // The real themes are Arrays
      return Object.keys(this.themes)
        .filter((key) => Array.isArray(this.themes[key]))
        .sort(Intl.Collator("en").compare);
    },
    setTheme(theme) {
      const new_theme = this.themes[theme];
      if (new_theme === undefined) {
        console.error("Theme not found:", theme);
        return;
      }
      this.editor.dispatch({
        effects: this.themeConfig.reconfigure([new_theme]),
      });
    },
    setEditorValueFromProps() {
      this.setEditorValue(this.value);
    },
    setEditorValue(value) {
      if (!this.editor) return;
      const old = this.editor.state.doc.toString();
      if (old === value) return;

      // Find the changed region so we only replace what differs.
      // This preserves cursor positions and selections outside the change.
      let start = 0;
      while (start < old.length && start < value.length && old[start] === value[start]) start++;
      let oldEnd = old.length;
      let newEnd = value.length;
      while (oldEnd > start && newEnd > start && old[oldEnd - 1] === value[newEnd - 1]) {
        oldEnd--;
        newEnd--;
      }

      this.emitting = false;
      this.editor.dispatch({ changes: { from: start, to: oldEnd, insert: value.slice(start, newEnd) } });
      this.emitting = true;
    },
    setDisabled(disabled) {
      this.editor.dispatch({
        effects: this.editableConfig.reconfigure(this.editableStates[!disabled]),
      });
    },
    setLineWrapping(wrap) {
      this.editor.dispatch({
        effects: this.lineWrappingConfig.reconfigure(wrap ? [CM.EditorView.lineWrapping] : []),
      });
    },
    buildCompletionSource(completions) {
      // setHTML (DOMPurify-backed polyfill) so plain text and sanitized HTML both render in the side panel.
      const renderInfo = (info) => () => {
        const div = document.createElement("div");
        div.setHTML(info);
        return div;
      };
      return (context) => {
        const word = context.matchBefore(/[\w.]+/);
        if (!word && !context.explicit) return null;
        const from = word ? word.from : context.pos;
        const options = completions.map((c) => {
          if (c.snippet && c.apply) {
            return CM.snippetCompletion(c.apply, {
              label: c.label,
              displayLabel: c.display_label,
              detail: c.detail,
              info: c.info ? renderInfo(c.info) : undefined,
              type: c.type,
              boost: typeof c.boost === "number" ? c.boost : undefined,
              commitCharacters: c.commit_characters,
              section: c.section,
              className: c.class_name,
            });
          }
          const opt = { label: c.label, apply: c.apply ?? c.label };
          if (c.display_label) opt.displayLabel = c.display_label;
          if (c.detail) opt.detail = c.detail;
          if (c.info) opt.info = renderInfo(c.info);
          if (c.type) opt.type = c.type;
          if (typeof c.boost === "number") opt.boost = c.boost;
          if (c.commit_characters) opt.commitCharacters = c.commit_characters;
          if (c.section) opt.section = c.section;
          if (c.class_name) opt.className = c.class_name;
          return opt;
        });
        return { from, options, validFor: /^[\w.]*$/ };
      };
    },
    rebuildCompletions() {
      if (!this.editor || !this.completionsConfig) return;
      const sources = [];
      if (this.completions && this.completions.length > 0) {
        sources.push(this.buildCompletionSource(this.completions));
      }
      if (this.completeWordsInDocument) {
        sources.push(CM.completeAnyWord);
      }
      const exts = [];
      const tooltipClass = this.tooltipClass || "";
      const optionClass = (c) => c.className || "";
      const tooltipClassFn = tooltipClass ? () => tooltipClass : undefined;
      if (this.replaceLanguageCompletions) {
        // Override mode: replaces language-pack completion sources entirely.
        // Register a single autocompletion() carrying both sources and styling so
        // the second autocompletion() call below is skipped (it would stack a
        // duplicate state field).
        exts.push(CM.autocompletion({
          override: sources,
          tooltipClass: tooltipClassFn,
          optionClass,
        }));
      } else {
        // Merge mode: register sources via languageData so they compose with the
        // active language pack's autocompletion (which basicSetup already enables).
        sources.forEach((src) => {
          exts.push(CM.EditorState.languageData.of(() => [{ autocomplete: src }]));
        });
        // Layer styling via Prec.highest only when needed, so it wins over
        // basicSetup's autocompletion config without re-registering the source.
        const hasClassName = this.completions && this.completions.some((c) => c.class_name);
        if (tooltipClass || hasClassName) {
          exts.push(CM.Prec.highest(CM.autocompletion({
            tooltipClass: tooltipClassFn,
            optionClass,
          })));
        }
      }
      // basicSetup's autocompletion() already registers the snippet keymap, so
      // Tab / Shift-Tab cycles snippet placeholders without extra wiring here.
      this.editor.dispatch({
        effects: this.completionsConfig.reconfigure(exts),
      });
    },
    triggerCompletion() {
      if (!this.editor) return;
      CM.startCompletion(this.editor);
    },
    setupExtensions() {
      const self = this;

      // Sends a ChangeSet https://codemirror.net/docs/ref/#state.ChangeSet
      // containing only the changes made to the document.
      // This could potentially be optimized further by sending updates
      // periodically instead of on every change and accumulating changesets
      // with ChangeSet.compose.
      const changeSender = CM.ViewPlugin.fromClass(
        class {
          update(update) {
            if (!update.docChanged) return;
            if (!self.emitting) return;
            self.$emit("update:value", update.changes);
          }
        },
      );

      const extensions = [
        CM.basicSetup,
        changeSender,
        // Enables the Tab key to indent the current lines https://codemirror.net/examples/tab/
        CM.keymap.of([CM.indentWithTab]),
        // Sets indentation https://codemirror.net/docs/ref/#language.indentUnit
        CM.indentUnit.of(this.indent),
        // We will set these Compartments later and dynamically through props
        this.themeConfig.of([]),
        this.languageConfig.of([]),
        this.editableConfig.of([]),
        this.lineWrappingConfig.of([]),
        this.completionsConfig.of([]),
        CM.EditorView.theme({
          "&": { height: "100%" },
          ".cm-scroller": { overflow: "auto" },
        }),
      ];

      if (this.highlightWhitespace) extensions.push([CM.highlightWhitespace()]);

      return extensions;
    },
  },
  async mounted() {
    // This is used to prevent emitting the value we just received from the server.
    this.emitting = true;

    // The Compartments are used to change the properties of the editor ("extensions") dynamically
    this.themes = { ...CM.themes, oneDark: CM.oneDark };
    this.themeConfig = new CM.Compartment();
    this.languages = CM.languages;
    this.languageConfig = new CM.Compartment();
    this.editableConfig = new CM.Compartment();
    this.editableStates = { true: CM.EditorView.editable.of(true), false: CM.EditorView.editable.of(false) };
    this.lineWrappingConfig = new CM.Compartment();
    this.completionsConfig = new CM.Compartment();

    const extensions = this.setupExtensions();

    this.editor = new CM.EditorView({
      doc: this.value,
      extensions: extensions,
      parent: this.$el,
    });

    this.resolveEditor(this.editor);

    this.setLanguage(this.language);
    this.setTheme(this.theme);
    this.setDisabled(this.disable);
    this.setLineWrapping(this.lineWrapping);
    this.rebuildCompletions();
  },
};
