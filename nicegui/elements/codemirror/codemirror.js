import * as CM from "nicegui-codemirror";
import { Awareness, applyAwarenessUpdate, encodeAwarenessUpdate, yCollab } from "nicegui-codemirror";
import * as Y from "yjs";

// Origin tag for Yjs updates applied locally from a remote source; used to suppress
// the echo back to the server which would otherwise cause an infinite update storm.
const YJS_REMOTE = "yjs-remote";

// Per-page registry of shared Y.Doc / Awareness state, keyed by doc_id. Multiple
// ui.codemirror instances in the same browser tab with the same doc_id share one
// Y.Doc — their yCollab extensions all subscribe to the same Y.Text, so in-tab
// edits propagate locally via Yjs observers (no server round-trip needed; the
// server's broadcast deliberately skips the originator sid for cross-tab clients).
const yjsRooms = new Map();

// Engine.IO rejects incoming messages above ~1 MB, so updates larger than this are
// split into parts which the receiver reassembles (see yjs_room.py, incl. the parts cap).
const YJS_CHUNK_BYTES = 500 * 1024;
const YJS_MAX_CHUNKS = 256;

function emitChunked(event, docId, update) {
  if (update.length <= YJS_CHUNK_BYTES) {
    window.socket.emit(event, { doc_id: docId, update });
    return;
  }
  const parts = Math.ceil(update.length / YJS_CHUNK_BYTES);
  if (parts > YJS_MAX_CHUNKS) {
    console.error(`Yjs update of ${update.length} bytes exceeds the ${YJS_MAX_CHUNKS * YJS_CHUNK_BYTES}-byte transfer limit; not sent.`);
    return;
  }
  for (let i = 0; i < parts; i++) {
    const chunk = update.subarray(i * YJS_CHUNK_BYTES, (i + 1) * YJS_CHUNK_BYTES);
    window.socket.emit(event, { doc_id: docId, update: chunk, part: i, parts });
  }
}

function reassemble(buffers, event, data, apply) {
  const update = new Uint8Array(data.update);
  if (data.parts === undefined) return apply(update);
  if (!buffers[event] || buffers[event].parts !== data.parts) {
    buffers[event] = { parts: data.parts, chunks: new Map() }; // new transfer supersedes any stale one
  }
  const { chunks } = buffers[event];
  chunks.set(data.part, update);
  if (chunks.size < data.parts) return;
  delete buffers[event];
  const ordered = Array.from({ length: data.parts }, (_, i) => chunks.get(i));
  const joined = new Uint8Array(ordered.reduce((total, chunk) => total + chunk.length, 0));
  let offset = 0;
  for (const chunk of ordered) {
    joined.set(chunk, offset);
    offset += chunk.length;
  }
  apply(joined);
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
    crdtDocId: { type: String, default: null },
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
    if (this.crdtDocId) {
      this._teardownCrdt();
      return;
    }
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
      // When collaboration is on, Yjs owns the document state; the `value` prop is no
      // longer the source of truth.
      if (this.crdtDocId) return;
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
        // In CRDT mode yjs owns the doc and emits via its own update channel; skip changeSender.
        ...(this.crdtDocId ? [yCollab(this.ytext, this.awareness)] : [changeSender]),
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
        CM.EditorView.theme({
          "&": { height: "100%" },
          ".cm-scroller": { overflow: "auto" },
        }),
      ];

      if (this.highlightWhitespace) extensions.push([CM.highlightWhitespace()]);

      return extensions;
    },
    _setupCrdt() {
      const docId = this.crdtDocId;
      let room = yjsRooms.get(docId);
      if (!room) {
        const ydoc = new Y.Doc();
        const awareness = new Awareness(ydoc);
        room = { ydoc, awareness, refs: 0, handlers: null, rx: {} };
        yjsRooms.set(docId, room);

        room.handlers = {
          onInit: (data) => {
            if (data.doc_id !== docId) return;
            reassemble(room.rx, "yjs_init", data, (update) => {
              if (update.length > 0) Y.applyUpdate(ydoc, update, YJS_REMOTE);
              // Send back whatever the server is missing (edits made while disconnected);
              // an empty diff encodes as 2 bytes.
              const serverStateVector = update.length > 0 ? Y.encodeStateVectorFromUpdate(update) : undefined;
              const diff = Y.encodeStateAsUpdate(ydoc, serverStateVector);
              if (diff.length > 2) emitChunked("yjs_update", docId, diff);
            });
          },
          onSocketConnect: () => {
            // A transient reconnect mints a new server-side sid; re-join to restore
            // room membership (the server replies with yjs_init, which resyncs both ways).
            window.socket.emit("yjs_join", { doc_id: docId });
          },
          onUpdate: (data) => {
            if (data.doc_id !== docId) return;
            reassemble(room.rx, "yjs_update", data, (update) => Y.applyUpdate(ydoc, update, YJS_REMOTE));
          },
          onAwareness: (data) => {
            if (data.doc_id !== docId) return;
            applyAwarenessUpdate(awareness, new Uint8Array(data.update), YJS_REMOTE);
          },
          onDocUpdate: (update, origin) => {
            if (origin === YJS_REMOTE) return;
            emitChunked("yjs_update", docId, update);
          },
          onAwarenessUpdate: ({ added, updated, removed }, origin) => {
            if (origin === YJS_REMOTE) return;
            const update = encodeAwarenessUpdate(awareness, added.concat(updated, removed));
            window.socket.emit("yjs_awareness", { doc_id: docId, update });
          },
        };

        // window.socket only exists after NiceGUI's handshake, which races with this
        // mount hook on first load; defer registration until the socket is ready.
        const wireSocket = () => {
          window.socket.on("yjs_init", room.handlers.onInit);
          window.socket.on("yjs_update", room.handlers.onUpdate);
          window.socket.on("yjs_awareness", room.handlers.onAwareness);
          window.socket.on("connect", room.handlers.onSocketConnect);
          ydoc.on("update", room.handlers.onDocUpdate);
          awareness.on("update", room.handlers.onAwarenessUpdate);
          window.socket.emit("yjs_join", { doc_id: docId });
        };
        const tryWire = () => {
          if (room.cancelled) return;
          if (window.socket && window.did_handshake) wireSocket();
          else setTimeout(tryWire, 10);
        };
        tryWire();
      }
      room.refs++;
      this.ydoc = room.ydoc;
      this.ytext = room.ydoc.getText("codemirror");
      this.awareness = room.awareness;
    },
    _teardownCrdt() {
      const docId = this.crdtDocId;
      const room = yjsRooms.get(docId);
      if (!room) return;
      room.refs--;
      if (room.refs > 0) return;
      room.cancelled = true;
      if (window.socket) {
        window.socket.emit("yjs_leave", { doc_id: docId });
        window.socket.off("yjs_init", room.handlers.onInit);
        window.socket.off("yjs_update", room.handlers.onUpdate);
        window.socket.off("yjs_awareness", room.handlers.onAwareness);
        window.socket.off("connect", room.handlers.onSocketConnect);
      }
      room.ydoc.off("update", room.handlers.onDocUpdate);
      room.awareness.off("update", room.handlers.onAwarenessUpdate);
      room.awareness.destroy();
      room.ydoc.destroy();
      yjsRooms.delete(docId);
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

    if (this.crdtDocId) this._setupCrdt();

    const extensions = this.setupExtensions();

    this.editor = new CM.EditorView({
      // In CRDT mode the y-codemirror binding seeds the editor from ytext on its own.
      doc: this.crdtDocId ? this.ytext.toString() : this.value,
      extensions: extensions,
      parent: this.$el,
    });

    this.resolveEditor(this.editor);

    this.setLanguage(this.language);
    this.setTheme(this.theme);
    this.setDisabled(this.disable);
    this.setLineWrapping(this.lineWrapping);
    this.setLineTooltips(this.lineTooltips);
    this.validateUserKeymap();
  },
};
