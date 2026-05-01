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

      console.error(`Language not found: ${name}`);
      console.info("Supported language names:", this.languages.map((lang) => lang.name).join(", "));
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

      const lang_description = this.findLanguage(language);
      if (!lang_description) {
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
    setDiagnostics(diagnostics) {
      if (!this.editor) return;
      const doc = this.editor.state.doc;
      const cmDiagnostics = [];
      for (const d of diagnostics) {
        if (!Number.isInteger(d.line) || d.line < 1 || d.line > doc.lines) {
          console.warn(`Diagnostic line out of range: ${d.line} (doc has ${doc.lines} lines)`);
          continue;
        }
        const line = doc.line(d.line);
        // Column values are 1-indexed; end_column is exclusive. Out-of-range values clamp to line bounds.
        const startOffset = Number.isInteger(d.column) ? Math.max(1, d.column) - 1 : 0;
        const endOffset = Number.isInteger(d.end_column) ? Math.max(1, d.end_column) - 1 : line.length;
        const from = Math.min(line.from + startOffset, line.to);
        const to = Math.min(line.from + endOffset, line.to);
        const message = d.message;
        cmDiagnostics.push({
          from,
          to: Math.max(from, to),
          severity: d.severity || "error",
          message,
          source: d.source ?? undefined,
          // setHTML (DOMPurify-backed polyfill) so plain text and sanitized HTML both render.
          renderMessage: () => {
            const span = document.createElement("span");
            span.setHTML(message);
            return span;
          },
        });
      }
      this.editor.dispatch(CM.setDiagnostics(this.editor.state, cmDiagnostics));
    },
    openLintPanel() {
      if (this.editor) CM.openLintPanel(this.editor);
    },
    closeLintPanel() {
      if (this.editor) CM.closeLintPanel(this.editor);
    },
    toggleLintPanel() {
      if (!this.editor) return;
      // @codemirror/lint exposes openLintPanel/closeLintPanel but no public "is open" predicate,
      // so check the rendered panel directly.
      const open = this.editor.dom.querySelector(".cm-panel-lint") !== null;
      (open ? CM.closeLintPanel : CM.openLintPanel)(this.editor);
    },
    getDiagnosticCount() {
      const counts = { error: 0, warning: 0, info: 0, hint: 0, total: 0 };
      if (!this.editor) return counts;
      CM.forEachDiagnostic(this.editor.state, (d) => {
        if (counts[d.severity] !== undefined) counts[d.severity] += 1;
        counts.total += 1;
      });
      return counts;
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
        // NOTE: do NOT use CM.lintGutter() here — it pulls in lintGutterTooltip,
        // a StateField that registers itself via showTooltip.from(field) and
        // returns null on most transactions. That null provider sits in the
        // showTooltip facet and silently suppresses the autocomplete popup
        // outside of paren contexts. CM.linter() installs lintState (so the
        // setDiagnostics() API still works and inline error marks render),
        // and its only tooltip is a hoverTooltip that fires on mouseover,
        // not on every keystroke. The empty source disables auto-linting.
        CM.linter(() => []),
        // Enables the Tab key to indent the current lines https://codemirror.net/examples/tab/
        CM.keymap.of([CM.indentWithTab]),
        // Sets indentation https://codemirror.net/docs/ref/#language.indentUnit
        CM.indentUnit.of(this.indent),
        // We will set these Compartments later and dynamically through props
        this.themeConfig.of([]),
        this.languageConfig.of([]),
        this.editableConfig.of([]),
        this.lineWrappingConfig.of([]),
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
  },
};
