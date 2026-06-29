import * as CM from "nicegui-codemirror";

class TextWidget extends CM.WidgetType {
  constructor(text, cls, html) {
    super();
    this.text = text;
    this.cls = cls || "";
    this.html = !!html;
  }
  eq(other) {
    return other.text === this.text && other.cls === this.cls && other.html === this.html;
  }
  toDOM() {
    const span = document.createElement("span");
    if (this.cls) span.className = this.cls;
    if (this.html) {
      span.setHTML(this.text);
    } else {
      span.textContent = this.text;
    }
    return span;
  }
  ignoreEvent() {
    return false;
  }
}

// Zero-width range so CM6's RangeSet.map() carries each tooltip through edits.
class TooltipValue extends CM.RangeValue {
  constructor(content) {
    super();
    this.content = content;
  }
}

const setTooltipsEffect = CM.StateEffect.define();

const tooltipField = CM.StateField.define({
  create() {
    return CM.RangeSet.empty;
  },
  update(set, tr) {
    set = set.map(tr.changes);
    for (const effect of tr.effects) {
      if (effect.is(setTooltipsEffect)) {
        set = CM.RangeSet.of(effect.value, true);
      }
    }
    return set;
  },
});

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
    decorations: Array,
    decorationTextHtml: Boolean,
    keymap: Array,
    lineTooltips: Object,
    lineTooltipHtml: Boolean,
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
    decorations: {
      deep: true,
      handler(newDecorations) {
        this.setDecorations(newDecorations);
      },
    },
    keymap() {
      this.setKeymap();
    },
    lineTooltips(newTooltips) {
      this.setLineTooltips(newTooltips);
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
    setDecorations(decorations) {
      if (!this.editor || !this.decorationsConfig) return;
      const all = [];
      for (const spec of decorations || []) {
        const dec = this._createDecoration(spec);
        if (dec) all.push(dec);
      }
      const decorationSet = CM.Decoration.set(all, true);
      this.editor.dispatch({
        effects: this.decorationsConfig.reconfigure([CM.EditorView.decorations.of(decorationSet)]),
      });
    },
    _createDecoration(spec) {
      const doc = this.editor.state.doc;
      if (spec.kind === "mark") {
        if (spec.from > spec.to) {
          console.error("codemirror: mark decoration has from > to", spec);
          return null;
        }
        const from = Math.max(0, Math.min(spec.from, doc.length));
        const to = Math.max(from, Math.min(spec.to, doc.length));
        const markSpec = {};
        if (spec.class) markSpec.class = spec.class;
        if (spec.attributes) markSpec.attributes = spec.attributes;
        if (spec.inclusiveStart !== undefined) markSpec.inclusiveStart = spec.inclusiveStart;
        if (spec.inclusiveEnd !== undefined) markSpec.inclusiveEnd = spec.inclusiveEnd;
        return CM.Decoration.mark(markSpec).range(from, to);
      }
      if (spec.kind === "line") {
        const lineNum = Math.max(1, Math.min(spec.line, doc.lines));
        const line = doc.line(lineNum);
        const lineSpec = {};
        if (spec.class) lineSpec.class = spec.class;
        if (spec.attributes) lineSpec.attributes = spec.attributes;
        return CM.Decoration.line(lineSpec).range(line.from);
      }
      if (spec.kind === "replace") {
        if (spec.from > spec.to) {
          console.error("codemirror: replace decoration has from > to", spec);
          return null;
        }
        const from = Math.max(0, Math.min(spec.from, doc.length));
        const to = Math.max(from, Math.min(spec.to, doc.length));
        if (spec.block) {
          // CodeMirror requires block-replace ranges to span full lines; otherwise it throws
          // out of editor.dispatch and breaks the editor for the rest of the page.
          const fromLine = doc.lineAt(from);
          const toLine = doc.lineAt(to);
          if (from !== fromLine.from || to !== toLine.to) {
            console.error("codemirror: block replace decoration must cover full lines", spec);
            return null;
          }
        }
        const replaceSpec = {};
        if (spec.inclusive !== undefined) replaceSpec.inclusive = spec.inclusive;
        if (spec.block) replaceSpec.block = true;
        if (spec.text !== undefined) replaceSpec.widget = new TextWidget(spec.text, spec.class, this.decorationTextHtml);
        else if (spec.class) replaceSpec.class = spec.class;
        return CM.Decoration.replace(replaceSpec).range(from, to);
      }
      if (spec.kind === "widget") {
        const pos = Math.max(0, Math.min(spec.position, doc.length));
        return CM.Decoration.widget({
          widget: new TextWidget(spec.text, spec.class, this.decorationTextHtml),
          side: spec.side ?? 1,
        }).range(pos);
      }
      console.error("codemirror: unknown decoration kind", spec);
      return null;
    },
    buildUserKeymap() {
      return (this.keymap || []).map(({ key, mac, linux, win, preventDefault }) => ({
        key,
        mac, // unset mac will fall back to key
        linux, // unset linux will fall back to key
        win, // unset win will fall back to key
        run: () => {
          this.$emit("keybinding", { key });
          return preventDefault;
        },
      }));
    },
    setKeymap() {
      if (!this.editor) return;
      this.editor.dispatch({
        effects: this.userKeymapConfig.reconfigure(CM.keymap.of(this.buildUserKeymap())),
      });
      this.validateUserKeymap();
    },
    validateUserKeymap() {
      if (!this.editor || !(this.keymap || []).length) return;
      try {
        // Force CodeMirror to build its combined keymap now instead of lazily on the first keydown:
        // a chord whose prefix is also a standalone binding (incl. basicSetup's, e.g. "Mod-a Mod-b"
        // vs. the built-in Mod-a) throws here rather than silently killing every keybinding later.
        CM.runScopeHandlers(this.editor, new KeyboardEvent("keydown", { key: "Unidentified" }), "editor");
      } catch (error) {
        logAndEmit("error", `ui.codemirror: ${error.message}`);
      }
    },
    setLineTooltips(tooltips) {
      if (!this.editor) return;
      const doc = this.editor.state.doc;
      const ranges = [];
      for (const [line, content] of Object.entries(tooltips || {})) {
        const lineNum = parseInt(line);
        if (lineNum >= 1 && lineNum <= doc.lines) {
          const pos = doc.line(lineNum).from;
          ranges.push(new TooltipValue(content).range(pos, pos));
        } else {
          logAndEmit("warning", `line_tooltips: line ${lineNum} out of range [1, ${doc.lines}]`);
        }
      }
      this.editor.dispatch({ effects: setTooltipsEffect.of(ranges) });
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

      const lineTooltip = CM.hoverTooltip((view, pos) => {
        const set = view.state.field(tooltipField);
        const line = view.state.doc.lineAt(pos);
        let content = null;
        set.between(line.from, line.to, (_from, _to, value) => {
          content = value.content;
          return false; // at most one tooltip per line — stop after the first match
        });
        if (content === null) return null;
        const renderHtml = self.lineTooltipHtml;
        return {
          pos: line.from,
          above: true,
          create() {
            const dom = document.createElement("div");
            if (renderHtml) dom.setHTML(content);
            else dom.textContent = content;
            return { dom };
          },
        };
      });

      const extensions = [
        CM.basicSetup,
        changeSender,
        tooltipField,
        lineTooltip,
        // Enables the Tab key to indent the current lines https://codemirror.net/examples/tab/
        CM.keymap.of([CM.indentWithTab]),
        // User keymap: Prec.high so they win over basicSetup defaults like Mod-z.
        CM.Prec.high(this.userKeymapConfig.of(CM.keymap.of(this.buildUserKeymap()))),
        // Sets indentation https://codemirror.net/docs/ref/#language.indentUnit
        CM.indentUnit.of(this.indent),
        // We will set these Compartments later and dynamically through props
        this.themeConfig.of([]),
        this.languageConfig.of([]),
        this.editableConfig.of([]),
        this.lineWrappingConfig.of([]),
        this.decorationsConfig.of([]),
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
    this.decorationsConfig = new CM.Compartment();
    this.userKeymapConfig = new CM.Compartment();

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
    if (this.decorations && this.decorations.length > 0) {
      this.setDecorations(this.decorations);
    }
    this.setLineTooltips(this.lineTooltips);
    this.validateUserKeymap();
  },
};
