import * as CM from "nicegui-codemirror";

// Caller-supplied text is either sanitized HTML (via the setHTML polyfill) or plain text.
function setContent(dom, text, asHtml) {
  if (asHtml) dom.setHTML(text);
  else dom.textContent = text;
}

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
    setContent(span, this.text, this.html);
    return span;
  }
  ignoreEvent() {
    return false;
  }
}

// A RangeSet StateField whose ranges remap through document edits.
// Dispatching setEffect.of(ranges) replaces the whole set.
function defineRemappableRangeSet() {
  const setEffect = CM.StateEffect.define(); // value: list of ranges (replaces all)
  const field = CM.StateField.define({
    create() {
      return CM.RangeSet.empty;
    },
    update(set, tr) {
      set = set.map(tr.changes);
      for (const effect of tr.effects) {
        if (effect.is(setEffect)) set = CM.RangeSet.of(effect.value, true);
      }
      return set;
    },
  });
  return { setEffect, field };
}

// Line anchors: {id, line} pairs whose positions CM6 auto-remaps through edits. Each AnchorValue carries its id.
class AnchorValue extends CM.RangeValue {
  constructor(id) {
    super();
    this.id = id;
  }
  eq(other) {
    return this.id === other.id;
  }
}
const { setEffect: setAnchorsEffect, field: anchorField } = defineRemappableRangeSet();
const ANCHOR_DEBOUNCE_MS = 50;

function sameAnchorPositions(a, b) {
  const ids = Object.keys(a);
  return ids.length === Object.keys(b).length && ids.every((id) => a[id] === b[id]);
}

// Zero-width range so CM6's RangeSet.map() carries each tooltip through edits.
class TooltipValue extends CM.RangeValue {
  constructor(content) {
    super();
    this.content = content;
  }
}
const { setEffect: setTooltipsEffect, field: tooltipField } = defineRemappableRangeSet();

// Decorations live in a StateField (not a static facet) so `.map(tr.changes)` carries each
// range through document edits — a mark on "beta" follows the text, and the mark/replace
// inclusivity options actually affect how ranges grow at their edges. A new decoration list
// from the server replaces the whole set via setDecorationsEffect.
// Every decoration carries the spec it was declared with, so a client-side remount can rebuild
// the list from where the state field has since mapped each one.
const DECLARED_SPEC = Symbol("declared spec");

// A DecorationSet is a RangeSet: Decoration.none is RangeSet.empty and Decoration.set(v, true)
// is RangeSet.of(v, true), so the shared factory covers decorations as well.
// Providing them from a field (rather than a plugin) is what CM6 requires for block
// replace/widget decorations to work.
const { setEffect: setDecorationsEffect, field: decorationField } = defineRemappableRangeSet();

// Python addresses the document by str index (one per code point), CodeMirror by UTF-16 code unit.
// The two only differ once the document contains a character outside the Basic Multilingual Plane.
function documentOffsets(doc) {
  const text = doc.toString();
  let length = text.length; // in Python str indices
  let toUnit = (index) => index;
  let toIndex = (unit) => unit;
  if (/[\uD800-\uDBFF]/.test(text)) {
    const units = []; // units[i] = UTF-16 offset of the i-th code point
    let unit = 0;
    for (const character of text) {
      units.push(unit);
      unit += character.length;
    }
    units.push(unit); // an offset may address the end of the document
    length = units.length - 1;
    toUnit = (index) => units[Math.max(0, Math.min(index, units.length - 1))];
    toIndex = (unit) => {
      let low = 0;
      let high = units.length - 1;
      while (low < high) {
        const middle = (low + high + 1) >> 1;
        if (units[middle] <= unit) low = middle;
        else high = middle - 1;
      }
      return low;
    };
  }
  return {
    length,
    toUtf16(spec) {
      if (spec.kind === "mark" || spec.kind === "replace")
        return { ...spec, from: toUnit(spec.from), to: toUnit(spec.to) };
      if (spec.kind === "widget") return { ...spec, position: toUnit(spec.position) };
      return spec;
    },
    toPython(spec, from, to) {
      if (spec.kind === "line") return { ...spec, line: doc.lineAt(from).number };
      if (spec.kind === "widget") return { ...spec, position: toIndex(from) };
      return { ...spec, from: toIndex(from), to: toIndex(to) };
    },
  };
}

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
    lineAnchors: Object,
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
    decorations() {
      // Applied from setEditorValueFromProps, after a value sent in the same update has landed;
      // watchers run before nicegui.js calls the update method, so specs declared for the new
      // value would otherwise be built against the old document.
      this._decorationsPending = true;
    },
    lineAnchors(newAnchors) {
      this.applyLineAnchors(newAnchors);
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
      if (element) {
        element.props.value = this.editor.state.doc.toString();
        // A client-side remount (e.g. a v-if container) re-applies these props against the restored
        // document, so they have to describe where the anchors are now, not where they were declared.
        if (element.props["line-anchors"]) element.props["line-anchors"] = this.currentAnchorPositions();
        if (element.props.decorations?.length) element.props.decorations = this.currentDecorationSpecs();
      }
    }
    clearTimeout(this._anchorTimer);
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
      if (this._decorationsPending) {
        this._decorationsPending = false;
        this.setDecorations(this.decorations);
      }
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
      // The server marks `decorations` as a preserved prop on unrelated updates, so this only runs on a
      // deliberate write, which re-applies every spec at its declared offset, as line anchors do.
      if (!this.editor) return;
      const offsets = documentOffsets(this.editor.state.doc);
      const all = [];
      for (const spec of decorations || []) {
        if (!this._fitsDocument(spec, offsets.length)) continue;
        const dec = this._createDecoration(offsets.toUtf16(spec), spec);
        if (dec) all.push(dec);
      }
      this.editor.dispatch({ effects: setDecorationsEffect.of(all) });
    },
    // The specs as declared, with their offsets moved to where the state field has mapped each decoration.
    // A decoration that vanished with its text is left out.
    currentDecorationSpecs() {
      const offsets = documentOffsets(this.editor.state.doc);
      const specs = [];
      for (const cursor = this.editor.state.field(decorationField).iter(); cursor.value; cursor.next()) {
        const declared = cursor.value.spec[DECLARED_SPEC];
        if (declared) specs.push(offsets.toPython(declared, cursor.from, cursor.to));
      }
      return specs;
    },
    // An offset past the end of the document is warned-and-skipped, like a line past the last one,
    // rather than clamped: a spec computed from a longer value than the browser holds by now would
    // otherwise land silently at the end. `length` counts Python str indices, as the spec does.
    _fitsDocument(spec, length) {
      if (spec.kind === "line") return true;
      const end = spec.kind === "widget" ? spec.position : spec.to;
      if (end <= length) return true;
      const where = spec.kind === "widget" ? `position ${spec.position}` : `range ${spec.from}..${spec.to}`;
      logAndEmit("warning", `decorations: ${spec.kind} ${where} is past the end of the document (length ${length})`);
      return false;
    },
    _createDecoration(spec, declared) {
      const doc = this.editor.state.doc;
      // The server refuses structurally broken specs before they get here; only what depends on the
      // document is checked. Such specs are warned-and-skipped (returning null) rather than thrown,
      // so one unusable entry never voids the rest of the batch.
      if (spec.kind === "mark") {
        const { from, to } = spec;
        if (from === to) {
          // CodeMirror rejects zero-length mark ranges.
          logAndEmit("warning", `decorations: mark range is empty (from=${declared.from}, to=${declared.to})`);
          return null;
        }
        // Only the documented fields reach CodeMirror; stray keys in a user spec are dropped, not forwarded.
        const markSpec = { [DECLARED_SPEC]: declared };
        if (spec.class) markSpec.class = spec.class;
        if (spec.attributes) markSpec.attributes = spec.attributes;
        if (spec.inclusiveStart !== undefined) markSpec.inclusiveStart = spec.inclusiveStart;
        if (spec.inclusiveEnd !== undefined) markSpec.inclusiveEnd = spec.inclusiveEnd;
        return CM.Decoration.mark(markSpec).range(from, to);
      }
      if (spec.kind === "line") {
        if (spec.line > doc.lines) {
          logAndEmit("warning", `decorations: line ${spec.line} out of range [1, ${doc.lines}]`);
          return null;
        }
        const lineSpec = { [DECLARED_SPEC]: declared };
        if (spec.class) lineSpec.class = spec.class;
        if (spec.attributes) lineSpec.attributes = spec.attributes;
        return CM.Decoration.line(lineSpec).range(doc.line(spec.line).from);
      }
      if (spec.kind === "replace") {
        const { from, to } = spec;
        // CodeMirror rejects an empty replace range unless it is inclusive, which `block` implies.
        if (from === to && !(spec.inclusive ?? !!spec.block)) {
          logAndEmit("warning", `decorations: replace range is empty (from=${declared.from}, to=${declared.to})`);
          return null;
        }
        const replaceSpec = { [DECLARED_SPEC]: declared };
        if (spec.inclusive !== undefined) replaceSpec.inclusive = spec.inclusive;
        if (spec.block) replaceSpec.block = true;
        if (spec.text !== undefined)
          replaceSpec.widget = new TextWidget(spec.text, spec.class, this.decorationTextHtml);
        return CM.Decoration.replace(replaceSpec).range(from, to);
      }
      if (spec.kind === "widget") {
        return CM.Decoration.widget({
          [DECLARED_SPEC]: declared,
          widget: new TextWidget(spec.text, spec.class, this.decorationTextHtml),
          side: spec.side ?? 1,
        }).range(spec.position);
      }
      return null;
    },
    async applyLineAnchors(anchors) {
      // The server marks `line-anchors` as a preserved prop on unrelated updates, so the watcher
      // only fires on a deliberate (re)assignment — re-applying from the declared lines is then intended,
      // snapping anchors back to their declared positions (and restoring any dropped by a delete-across).
      if (!this.editor) await this.editorPromise;
      const doc = this.editor.state.doc;
      const ranges = [];
      for (const [id, line] of Object.entries(anchors || {})) {
        if (line >= 1 && line <= doc.lines) {
          const pos = doc.line(line).from;
          ranges.push(new AnchorValue(id).range(pos, pos));
        } else {
          logAndEmit(
            "warning",
            `line_anchors: anchor ${JSON.stringify(id)} on line ${line} out of range [1, ${doc.lines}]`,
          );
        }
      }
      this.editor.dispatch({ effects: setAnchorsEffect.of(ranges) });
      // The dispatch re-armed the debounced tracker; the immediate emit below supersedes that echo.
      clearTimeout(this._anchorTimer);
      this.emitAnchorPositions({ force: true });
    },
    currentAnchorPositions() {
      const state = this.editor.state;
      const field = state.field(anchorField);
      const doc = state.doc;
      const positions = {};
      const cursor = field.iter();
      while (cursor.value) {
        positions[cursor.value.id] = doc.lineAt(cursor.from).number;
        cursor.next();
      }
      return positions;
    },
    // A deliberate apply forces the emit: the server treats it as the confirmation that its declared
    // anchors have landed, even when they happen to sit where the live ones already were.
    emitAnchorPositions({ force = false } = {}) {
      if (!this.editor) return;
      const positions = this.currentAnchorPositions();
      if (!force && this._lastAnchors && sameAnchorPositions(this._lastAnchors, positions)) return;
      this._lastAnchors = positions;
      this.$emit("anchor-positions", { anchors: positions });
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

      // The debounce coalesces bursts (paste, multi-cursor insert) so high-latency
      // connections do not see one event per keystroke. The fire-time callback reads live
      // editor state via emitAnchorPositions(), so a stale timer that survives a clear or
      // re-set transaction will see the up-to-date field rather than its scheduling-time snapshot.
      const anchorTracker = CM.ViewPlugin.fromClass(
        class {
          update(update) {
            if (!update.docChanged) return;
            // Skip only when there is nothing to report before and after — checking just the end state
            // would swallow the last anchor's removal (1 -> 0), leaving the Python mirror stale.
            if (update.state.field(anchorField).size === 0 && update.startState.field(anchorField).size === 0) return;
            clearTimeout(self._anchorTimer);
            self._anchorTimer = setTimeout(() => self.emitAnchorPositions(), ANCHOR_DEBOUNCE_MS);
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
            setContent(dom, content, renderHtml);
            return { dom };
          },
        };
      });

      const extensions = [
        CM.basicSetup,
        changeSender,
        anchorTracker,
        anchorField,
        tooltipField,
        decorationField,
        CM.EditorView.decorations.from(decorationField),
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
    if (this.lineAnchors && Object.keys(this.lineAnchors).length > 0) {
      this.applyLineAnchors(this.lineAnchors);
    }
    this.setLineTooltips(this.lineTooltips);
    this.validateUserKeymap();
  },
};
