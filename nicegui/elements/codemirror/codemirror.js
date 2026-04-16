import * as CM from "nicegui-codemirror";

// ── Line anchors: track document positions through edits ──
// Named sets of anchors, each with a string ID. CM6 remaps positions automatically.

class AnchorValue extends CM.RangeValue {
  constructor(id, setName) {
    super();
    this.id = id;
    this.setName = setName;
  }
  eq(other) { return this.id === other.id && this.setName === other.setName; }
}

const setAnchorsEffect = CM.StateEffect.define();   // value: {setName, ranges}
const clearAnchorsEffect = CM.StateEffect.define();  // value: setName | null

const anchorField = CM.StateField.define({
  create() { return CM.RangeSet.empty; },
  update(set, tr) {
    set = set.map(tr.changes);
    for (const effect of tr.effects) {
      if (effect.is(clearAnchorsEffect)) {
        if (effect.value === null) return CM.RangeSet.empty;
        const keep = [];
        const cursor = set.iter();
        while (cursor.value) {
          if (cursor.value.setName !== effect.value)
            keep.push(cursor.value.range(cursor.from, cursor.to));
          cursor.next();
        }
        return CM.RangeSet.of(keep, true);
      }
      if (effect.is(setAnchorsEffect)) {
        const { setName, ranges } = effect.value;
        const keep = [];
        const cursor = set.iter();
        while (cursor.value) {
          if (cursor.value.setName !== setName)
            keep.push(cursor.value.range(cursor.from, cursor.to));
          cursor.next();
        }
        return CM.RangeSet.of([...keep, ...ranges], true);
      }
    }
    return set;
  },
});

// ── Line tooltips: per-line hover metadata, position-mapped via RangeSet ──
// Each tooltip is a zero-width range pinned to the start of its line, so
// CM6's RangeSet.map() handles all position remapping through edits.

class TooltipValue extends CM.RangeValue {
  constructor(setName, meta) {
    super();
    this.setName = setName;
    this.meta = meta;
  }
}

const setTooltipsEffect = CM.StateEffect.define();   // value: {setName, ranges}
const clearTooltipsEffect = CM.StateEffect.define();  // value: setName | null

const tooltipField = CM.StateField.define({
  create() { return CM.RangeSet.empty; },
  update(set, tr) {
    set = set.map(tr.changes);
    for (const effect of tr.effects) {
      if (effect.is(clearTooltipsEffect)) {
        if (effect.value === null) return CM.RangeSet.empty;
        const keep = [];
        const cursor = set.iter();
        while (cursor.value) {
          if (cursor.value.setName !== effect.value)
            keep.push(cursor.value.range(cursor.from, cursor.to));
          cursor.next();
        }
        return CM.RangeSet.of(keep, true);
      }
      if (effect.is(setTooltipsEffect)) {
        const { setName, ranges } = effect.value;
        const keep = [];
        const cursor = set.iter();
        while (cursor.value) {
          if (cursor.value.setName !== setName)
            keep.push(cursor.value.range(cursor.from, cursor.to));
          cursor.next();
        }
        return CM.RangeSet.of([...keep, ...ranges], true);
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
    customCompletions: Array,
    decorations: Object,
    saveShortcutEnabled: Boolean,
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
    customCompletions(newCompletions) {
      this.setCustomCompletions(newCompletions);
    },
    decorations: {
      deep: true,
      handler(newDecorations) {
        this.setDecorations(newDecorations);
      },
    },
  },
  data() {
    return {
      // To let other methods wait for the editor to be created because
      // they might be called by the server before the editor is created.
      editorPromise: new Promise((resolve) => {
        this.resolveEditor = resolve;
      }),
      DOMPurify: null,
    };
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
    highlightLines(lineIndices, cssClass, durationMs) {
      if (!this.editor) return;

      // Build line decorations from indices (0-indexed to 1-indexed)
      const lineDecorations = lineIndices
        .filter(idx => idx >= 0 && idx < this.editor.state.doc.lines)
        .map(idx => ({
          kind: "line",
          line: idx + 1,
          class: cssClass,
        }));

      if (lineDecorations.length === 0) return;

      // Track highlight state locally (independent of prop-driven decorations)
      this._jsHighlight = lineDecorations;
      this._applyAllDecorations();

      // Scroll first line into view
      const firstLineNum = Math.min(...lineIndices) + 1;
      const line = this.editor.state.doc.line(
        Math.max(1, Math.min(firstLineNum, this.editor.state.doc.lines))
      );
      this.editor.dispatch({
        effects: CM.EditorView.scrollIntoView(line.from, { y: "center" }),
      });

      // Auto-remove after duration
      if (durationMs > 0) {
        clearTimeout(this._highlightTimer);
        this._highlightTimer = setTimeout(() => {
          this._jsHighlight = null;
          this._applyAllDecorations();
        }, durationMs);
      }
    },
    setCustomCompletions(completions) {
      if (!this.editor || !this.completionsConfig) return;
      if (!completions || completions.length === 0) {
        this.editor.dispatch({
          effects: this.completionsConfig.reconfigure([]),
        });
        return;
      }

      // Create a custom completion source from the provided completions
      const customCompletionSource = (context) => {
        // Get word before cursor
        const word = context.matchBefore(/[\w.]+/);
        if (!word && !context.explicit) return null;

        const from = word ? word.from : context.pos;
        const text = word ? word.text : "";

        // Filter completions that match the current input
        const matchingCompletions = completions.filter(c => {
          const label = c.label || "";
          return label.toLowerCase().startsWith(text.toLowerCase());
        }).map(c => ({
          label: c.label,
          detail: c.detail || "",
          info: c.info || "",
          apply: c.apply || c.label,
          type: c.type || "function",
        }));

        if (matchingCompletions.length === 0) return null;

        return {
          from: from,
          options: matchingCompletions,
          validFor: /^[\w.]*$/,
        };
      };

      // Create autocompletion extension with our custom source
      const completionExtension = CM.autocompletion({
        override: [customCompletionSource],
        activateOnTyping: true,
      });

      this.editor.dispatch({
        effects: this.completionsConfig.reconfigure([completionExtension]),
      });
    },
    revealLine(lineNumber) {
      if (!this.editor) return;
      const doc = this.editor.state.doc;
      const lineNum = Math.max(1, Math.min(lineNumber, doc.lines));
      const line = doc.line(lineNum);
      this.editor.dispatch({
        effects: CM.EditorView.scrollIntoView(line.from, { y: "center" }),
      });
    },
    // ── Line anchors ──
    setLineAnchors(anchors, setName) {
      if (!this.editor) return;
      const doc = this.editor.state.doc;
      const ranges = [];
      for (const a of anchors) {
        const lineNum = Math.max(1, Math.min(a.line, doc.lines));
        const pos = doc.line(lineNum).from;
        ranges.push(new AnchorValue(a.id, setName).range(pos, pos));
      }
      this.editor.dispatch({ effects: setAnchorsEffect.of({ setName, ranges }) });
    },
    clearLineAnchors(setName) {
      if (!this.editor) return;
      this.editor.dispatch({ effects: clearAnchorsEffect.of(setName ?? null) });
    },
    getLineAnchors() {
      if (!this.editor) return {};
      const field = this.editor.state.field(anchorField);
      const doc = this.editor.state.doc;
      const sets = {};
      const cursor = field.iter();
      while (cursor.value) {
        const sn = cursor.value.setName;
        if (!sets[sn]) sets[sn] = {};
        sets[sn][cursor.value.id] = doc.lineAt(cursor.from).number;
        cursor.next();
      }
      return sets;
    },
    // ── Diagnostics (linting) ──
    setDiagnosticsFromPython(diagnostics) {
      if (!this.editor) return;
      const doc = this.editor.state.doc;
      const cmDiagnostics = diagnostics.map(d => {
        let from = d.from;
        let to = d.to;
        if (from === undefined && d.line !== undefined) {
          const lineNum = Math.max(1, Math.min(d.line, doc.lines));
          const line = doc.line(lineNum);
          from = line.from;
          to = line.to;
        }
        return {
          from: Math.max(0, Math.min(from, doc.length)),
          to: Math.max(0, Math.min(to, doc.length)),
          severity: d.severity || "error",
          message: d.message || "",
          source: d.source || undefined,
        };
      });
      this.editor.dispatch(CM.setDiagnostics(this.editor.state, cmDiagnostics));
    },
    // ── Line tooltips ──
    setLineTooltips(tooltips, setName) {
      if (!this.editor) return;
      const doc = this.editor.state.doc;
      const ranges = [];
      for (const [line, data] of Object.entries(tooltips)) {
        const lineNum = parseInt(line);
        if (lineNum >= 1 && lineNum <= doc.lines) {
          const pos = doc.line(lineNum).from;
          ranges.push(new TooltipValue(setName, data).range(pos, pos));
        }
      }
      this.editor.dispatch({ effects: setTooltipsEffect.of({ setName, ranges }) });
    },
    clearLineTooltips(setName) {
      if (!this.editor) return;
      this.editor.dispatch({ effects: clearTooltipsEffect.of(setName ?? null) });
    },
    setDecorations(decorationSets) {
      // Prop-driven path — store and merge with JS-local state
      this._propDecorations = decorationSets;
      this._applyAllDecorations();
    },
    _applyAllDecorations() {
      if (!this.editor || !this.decorationsConfig) return;

      // Merge prop-driven decoration sets with JS-local highlight
      const merged = { ...(this._propDecorations || {}) };
      if (this._jsHighlight) {
        merged._highlight = this._jsHighlight;
      }

      if (Object.keys(merged).length === 0) {
        this.editor.dispatch({
          effects: this.decorationsConfig.reconfigure([]),
        });
        return;
      }

      const allDecorations = [];
      for (const specs of Object.values(merged)) {
        for (const spec of specs) {
          const dec = this.createDecoration(spec);
          if (dec) allDecorations.push(dec);
        }
      }

      const decorationSet = CM.Decoration.set(allDecorations, true);
      const decorationExtension = CM.EditorView.decorations.of(decorationSet);

      this.editor.dispatch({
        effects: this.decorationsConfig.reconfigure([decorationExtension]),
      });
    },
    createDecoration(spec) {
      const doc = this.editor.state.doc;

      if (spec.kind === "mark") {
        const from = Math.max(0, Math.min(spec.from, doc.length));
        const to = Math.max(from, Math.min(spec.to, doc.length));
        const markSpec = {};
        if (spec.class) markSpec.class = spec.class;
        if (spec.attributes) markSpec.attributes = spec.attributes;
        if (spec.inclusiveStart !== undefined) markSpec.inclusiveStart = spec.inclusiveStart;
        if (spec.inclusiveEnd !== undefined) markSpec.inclusiveEnd = spec.inclusiveEnd;
        return CM.Decoration.mark(markSpec).range(from, to);

      } else if (spec.kind === "line") {
        const lineNum = Math.max(1, Math.min(spec.line, doc.lines));
        const line = doc.line(lineNum);
        const lineSpec = {};
        if (spec.class) lineSpec.class = spec.class;
        if (spec.attributes) lineSpec.attributes = spec.attributes;
        return CM.Decoration.line(lineSpec).range(line.from);
      }
      return null;
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

      // Cursor line tracker — emits 1-indexed line number on cursor movement (debounced)
      const cursorTracker = CM.ViewPlugin.fromClass(
        class {
          constructor() { this._lastLine = 0; }
          update(update) {
            if (!update.selectionSet && !update.docChanged) return;
            const line = update.state.doc.lineAt(update.state.selection.main.head).number;
            if (line === this._lastLine) return;
            this._lastLine = line;
            if (self._cursorTimer) clearTimeout(self._cursorTimer);
            // NOTE: 30 ms debounce — short enough to feel immediate when arrow-keying through a file,
            // long enough to coalesce bursts during multi-line selection drags.
            self._cursorTimer = setTimeout(() => self.$emit("cursor-line", { line }), 30);
          }
        }
      );

      // Anchor position tracker — emits updated positions when doc changes remap anchors
      const anchorTracker = CM.ViewPlugin.fromClass(
        class {
          update(update) {
            if (!update.docChanged) return;
            const field = update.state.field(anchorField);
            if (field.size === 0) return;
            if (self._anchorTimer) clearTimeout(self._anchorTimer);
            // NOTE: 50 ms debounce — slightly longer than the cursor debounce because remapping is
            // only meaningful after a sequence of edits (e.g. paste, multi-cursor insert) settles.
            self._anchorTimer = setTimeout(() => {
              const doc = update.state.doc;
              const sets = {};
              const cursor = field.iter();
              while (cursor.value) {
                const sn = cursor.value.setName;
                if (!sets[sn]) sets[sn] = {};
                sets[sn][cursor.value.id] = doc.lineAt(cursor.from).number;
                cursor.next();
              }
              for (const [setName, anchors] of Object.entries(sets)) {
                self.$emit("anchor-positions", { set_name: setName, anchors });
              }
            }, 50);
          }
        }
      );

      // Hover tooltip: shows line metadata as key-value pairs
      const lineTooltip = CM.hoverTooltip((view, pos) => {
        const doc = view.state.doc;
        const line = doc.lineAt(pos);
        const set = view.state.field(tooltipField);
        if (set.size === 0) return null;

        const merged = {};
        set.between(line.from, line.to, (_from, _to, value) => {
          Object.assign(merged, value.meta);
        });
        if (Object.keys(merged).length === 0) return null;

        return {
          pos: line.from,
          above: true,
          create() {
            const dom = document.createElement("div");
            dom.className = "cm-line-tooltip";
            if (merged._html) {
              // NOTE: sanitize via DOMPurify to prevent XSS from untrusted line tooltip HTML.
              // Falls back to textContent if DOMPurify hasn't loaded yet (first hover after mount).
              if (self.DOMPurify) {
                dom.innerHTML = self.DOMPurify.sanitize(merged._html);
              } else {
                dom.textContent = merged._html;
              }
            } else {
              const parts = [];
              for (const [key, val] of Object.entries(merged)) {
                if (key.startsWith("_")) continue;
                if (Array.isArray(val)) {
                  for (const item of val) parts.push(`${key}: ${item}`);
                } else {
                  parts.push(`${key}: ${val}`);
                }
              }
              dom.textContent = parts.join("\n");
              dom.style.whiteSpace = "pre";
            }
            return { dom };
          },
        };
      });

      // Build the editor's custom keymap. Tab is always bound to indent;
      // Mod-s (Ctrl/Cmd+S) is only bound when the host opts in via the
      // `save-shortcut-enabled` prop, in which case the binding emits a
      // `save` event and suppresses the browser default.
      const customKeymap = [CM.indentWithTab];
      if (this.saveShortcutEnabled) {
        customKeymap.push({
          key: "Mod-s",
          preventDefault: true,
          run: () => {
            self.$emit("save");
            return true;
          },
        });
      }

      const extensions = [
        CM.basicSetup,
        changeSender,
        cursorTracker,
        anchorTracker,
        anchorField,
        tooltipField,
        // NOTE: do NOT use CM.lintGutter() here — it pulls in lintGutterTooltip,
        // a StateField that registers itself via showTooltip.from(field) and
        // returns null on most transactions. That null provider sits in the
        // showTooltip facet and silently suppresses the autocomplete popup
        // outside of paren contexts. CM.linter() installs lintState (so the
        // setDiagnostics() API still works and inline error marks render),
        // and its only tooltip is a hoverTooltip that fires on mouseover,
        // not on every keystroke. The empty source disables auto-linting.
        CM.linter(() => []),
        lineTooltip,
        // Enables the Tab key to indent the current lines https://codemirror.net/examples/tab/
        CM.keymap.of(customKeymap),
        // Sets indentation https://codemirror.net/docs/ref/#language.indentUnit
        CM.indentUnit.of(this.indent),
        // We will set these Compartments later and dynamically through props
        this.themeConfig.of([]),
        this.languageConfig.of([]),
        this.editableConfig.of([]),
        this.lineWrappingConfig.of([]),
        this.completionsConfig.of([]),
        this.decorationsConfig.of([]),
        CM.EditorView.theme({
          "&": { height: "100%" },
          ".cm-scroller": { overflow: "auto" },
        }),
        // Static decoration styles (installed once, not per-update)
        CM.EditorView.baseTheme({
          ".cm-diff-added": {
            backgroundColor: "rgba(0, 255, 0, 0.2)",
            borderRadius: "2px",
          },
          ".cm-diff-deleted": {
            backgroundColor: "rgba(255, 0, 0, 0.2)",
            textDecoration: "line-through",
          },
          ".cm-diff-line-added": {
            backgroundColor: "rgba(0, 255, 0, 0.1)",
          },
          ".cm-diff-line-deleted": {
            backgroundColor: "rgba(255, 0, 0, 0.1)",
          },
          ".cm-highlighted": {
            backgroundColor: "rgba(255, 255, 0, 0.3)",
          },
          // Line tooltip styling
          ".cm-line-tooltip": {
            padding: "4px 8px",
            fontSize: "0.85em",
            lineHeight: "1.4",
          },
        }),
      ];

      if (this.highlightWhitespace) extensions.push([CM.highlightWhitespace()]);

      return extensions;
    },
  },
  async mounted() {
    // This is used to prevent emitting the value we just received from the server.
    this.emitting = true;

    // Eagerly import DOMPurify for sanitizing per-line tooltip HTML.
    import('dompurify').then(({ default: DOMPurify }) => {
      this.DOMPurify = DOMPurify;
    });

    // The Compartments are used to change the properties of the editor ("extensions") dynamically
    this.themes = { ...CM.themes, oneDark: CM.oneDark };
    this.themeConfig = new CM.Compartment();
    this.languages = CM.languages;
    this.languageConfig = new CM.Compartment();
    this.editableConfig = new CM.Compartment();
    this.editableStates = { true: CM.EditorView.editable.of(true), false: CM.EditorView.editable.of(false) };
    this.lineWrappingConfig = new CM.Compartment();
    this.completionsConfig = new CM.Compartment();
    this.decorationsConfig = new CM.Compartment();

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
    if (this.customCompletions) {
      this.setCustomCompletions(this.customCompletions);
    }
  },
  beforeUnmount() {
    // Sync final value to Python before destruction
    if (this.editor) {
      const element = mounted_app.elements[this.$props.id.slice(1)];
      if (element) element.props.value = this.editor.state.doc.toString();
    }
    clearTimeout(this._highlightTimer);
    clearTimeout(this._cursorTimer);
    clearTimeout(this._anchorTimer);
    if (this.editor) {
      this.editor.destroy();
      this.editor = null;
    }
  },
};
