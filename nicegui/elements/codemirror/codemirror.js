import * as CM from "nicegui-codemirror";

// Line anchors: named sets of {id, line} pairs that CM6 RangeSet auto-remaps
// through document edits. Each AnchorValue carries its id + setName so a single
// shared StateField can hold multiple independently-managed sets.

class AnchorValue extends CM.RangeValue {
  constructor(id, setName) {
    super();
    this.id = id;
    this.setName = setName;
  }
  // Required by RangeValue for RangeSet diffing.
  eq(other) { return this.id === other.id && this.setName === other.setName; }
}

const setAnchorsEffect = CM.StateEffect.define();    // value: {setName, ranges}
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
          if (cursor.value.setName !== effect.value) {
            keep.push(cursor.value.range(cursor.from, cursor.to));
          }
          cursor.next();
        }
        return CM.RangeSet.of(keep, true);
      }
      if (effect.is(setAnchorsEffect)) {
        const { setName, ranges } = effect.value;
        const keep = [];
        const cursor = set.iter();
        while (cursor.value) {
          if (cursor.value.setName !== setName) {
            keep.push(cursor.value.range(cursor.from, cursor.to));
          }
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
    clearTimeout(this._anchorTimer);
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
    async setLineAnchors(anchors, setName) {
      if (!this.editor) await this.editorPromise;
      const doc = this.editor.state.doc;
      const ranges = [];
      for (const a of anchors) {
        const lineNum = Math.max(1, Math.min(a.line, doc.lines));
        const pos = doc.line(lineNum).from;
        ranges.push(new AnchorValue(a.id, setName).range(pos, pos));
      }
      this.editor.dispatch({ effects: setAnchorsEffect.of({ setName, ranges }) });
      this.emitAnchorPositions();
    },
    async clearLineAnchors(setName) {
      if (!this.editor) await this.editorPromise;
      clearTimeout(this._anchorTimer);
      this._anchorTimer = null;
      this.editor.dispatch({ effects: clearAnchorsEffect.of(setName ?? null) });
      this.emitAnchorPositions();
    },
    // Snapshot the current anchor field and emit a full {set_name: {id: line}} mirror.
    // Reads live editor state so callers don't need to capture anything.
    emitAnchorPositions() {
      if (!this.editor) return;
      const state = this.editor.state;
      const field = state.field(anchorField);
      const doc = state.doc;
      const sets = {};
      const cursor = field.iter();
      while (cursor.value) {
        const sn = cursor.value.setName;
        if (!sets[sn]) sets[sn] = {};
        sets[sn][cursor.value.id] = doc.lineAt(cursor.from).number;
        cursor.next();
      }
      this.$emit("anchor-positions", { anchors: sets });
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

      // Re-emit anchor positions when the document changes and at least one anchor exists.
      // The 50 ms debounce coalesces bursts (paste, multi-cursor insert) so high-latency
      // connections do not see one event per keystroke. The fire-time callback reads live
      // editor state via emitAnchorPositions(), so a stale timer that survives a clear or
      // re-set transaction will see the up-to-date field rather than its scheduling-time snapshot.
      const anchorTracker = CM.ViewPlugin.fromClass(
        class {
          update(update) {
            if (!update.docChanged) return;
            if (update.state.field(anchorField).size === 0) return;
            if (self._anchorTimer) clearTimeout(self._anchorTimer);
            self._anchorTimer = setTimeout(() => {
              self._anchorTimer = null;
              self.emitAnchorPositions();
            }, 50);
          }
        },
      );

      const extensions = [
        CM.basicSetup,
        changeSender,
        anchorTracker,
        anchorField,
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
