import * as RTE from 'nicegui-tiptap';
import { loadResource } from '../../static/utils/resources.js';

// Button definitions — keyed by the IDs the Python API exposes.
// Regular buttons: active is spread args for editor.isActive(); null = no active state.
//                  cmdAttrs is the extra argument for commands that need one (e.g. heading level).
// Dropdown buttons: type='dropdown', items is an array of {label, cmd, cmdAttrs?, active}.
//                  The button label reflects the currently active item.
const BUTTONS = {
  bold:         { icon: 'format_bold',             tooltip: 'Bold',            cmd: 'toggleBold',        active: ['bold'] },
  italic:       { icon: 'format_italic',            tooltip: 'Italic',          cmd: 'toggleItalic',      active: ['italic'] },
  underline:    { icon: 'format_underline',         tooltip: 'Underline',       cmd: 'toggleUnderline',   active: ['underline'] },
  strike:       { icon: 'strikethrough_s',          tooltip: 'Strikethrough',   cmd: 'toggleStrike',      active: ['strike'] },
  code:         { icon: 'code',                     tooltip: 'Inline code',     cmd: 'toggleCode',        active: ['code'] },
  // Individual heading buttons (available for custom toolbars).
  h1:           { label: 'H1',                      tooltip: 'Heading 1',       cmd: 'toggleHeading',     cmdAttrs: {level: 1}, active: ['heading', {level: 1}] },
  h2:           { label: 'H2',                      tooltip: 'Heading 2',       cmd: 'toggleHeading',     cmdAttrs: {level: 2}, active: ['heading', {level: 2}] },
  h3:           { label: 'H3',                      tooltip: 'Heading 3',       cmd: 'toggleHeading',     cmdAttrs: {level: 3}, active: ['heading', {level: 3}] },
  // Heading dropdown — shows the active level as its label.
  heading: {
    type: 'dropdown',
    tooltip: 'Heading',
    items: [
      { label: 'Normal',    cmd: 'setParagraph',  active: null },
      { label: 'Heading 1', cmd: 'toggleHeading', cmdAttrs: {level: 1}, active: ['heading', {level: 1}] },
      { label: 'Heading 2', cmd: 'toggleHeading', cmdAttrs: {level: 2}, active: ['heading', {level: 2}] },
      { label: 'Heading 3', cmd: 'toggleHeading', cmdAttrs: {level: 3}, active: ['heading', {level: 3}] },
    ],
  },
  bullet_list:  { icon: 'format_list_bulleted',     tooltip: 'Bullet list',     cmd: 'toggleBulletList',  active: ['bulletList'] },
  ordered_list: { icon: 'format_list_numbered',     tooltip: 'Ordered list',    cmd: 'toggleOrderedList', active: ['orderedList'] },
  blockquote:   { icon: 'format_quote',             tooltip: 'Blockquote',      cmd: 'toggleBlockquote',  active: ['blockquote'] },
  code_block:   { icon: 'integration_instructions', tooltip: 'Code block',      cmd: 'toggleCodeBlock',   active: ['codeBlock'] },
  table:        { icon: 'table_chart',              tooltip: 'Insert table',    cmd: 'insertTable',       cmdAttrs: {rows: 3, cols: 3, withHeaderRow: true}, active: null },
  undo:         { icon: 'undo',                     tooltip: 'Undo',            cmd: 'undo',              active: null },
  redo:         { icon: 'redo',                     tooltip: 'Redo',            cmd: 'redo',              active: null },
  hr:           { icon: 'horizontal_rule',          tooltip: 'Horizontal rule', cmd: 'setHorizontalRule', active: null },
};

const DEFAULT_TOOLBAR = [
  ['bold', 'italic', 'underline', 'strike', 'code'],
  ['heading'],
  ['bullet_list', 'ordered_list'],
  ['blockquote', 'code_block'],
  ['undo', 'redo'],
];

export default {
  template: `
    <div style="display:flex;flex-direction:column;">
      <div v-if="toolbarGroups.length"
           class="row no-wrap items-center q-pa-xs nicegui-tiptap-toolbar">
        <template v-for="(group, gi) in toolbarGroups" :key="gi">
          <q-separator v-if="gi > 0" vertical class="q-mx-xs" />
          <q-btn-group flat>
            <template v-for="btnId in group" :key="btnId">
              <q-btn-dropdown v-if="getBtn(btnId).type === 'dropdown'"
                              dense flat no-icon-animation
                              :label="getDropdownLabel(btnId)"
                              @mousedown.prevent>
                <q-list dense>
                  <q-item v-for="item in getBtn(btnId).items" :key="item.label"
                          clickable v-close-popup
                          :active="isDropdownItemActive(item)"
                          active-class="text-primary"
                          @click="execDropdownItem(item)">
                    <q-item-section>{{ item.label }}</q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
              <q-btn v-else
                     dense flat
                     :icon="getBtn(btnId).icon || undefined"
                     :color="isActive(btnId) ? 'primary' : undefined"
                     @mousedown.prevent @click="execBtn(btnId)">
                {{ getBtn(btnId).label || '' }}
                <q-tooltip>{{ getBtn(btnId).tooltip }}</q-tooltip>
              </q-btn>
            </template>
          </q-btn-group>
        </template>
      </div>
      <div v-if="isInTable" class="row no-wrap items-center q-pa-xs nicegui-tiptap-table-toolbar">
        <q-btn-dropdown dense flat no-icon-animation no-caps icon="border_all" label="Edit table" @mousedown.prevent>
          <q-list dense>
            <q-item-label header class="text-caption q-pb-none">Rows</q-item-label>
            <q-item clickable v-close-popup @click="execTableCmd('addRowBefore')">
              <q-item-section avatar><q-icon name="keyboard_arrow_up" /></q-item-section>
              <q-item-section>Add row above</q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="execTableCmd('addRowAfter')">
              <q-item-section avatar><q-icon name="keyboard_arrow_down" /></q-item-section>
              <q-item-section>Add row below</q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="execTableCmd('deleteRow')">
              <q-item-section avatar><q-icon name="delete_outline" color="negative" /></q-item-section>
              <q-item-section class="text-negative">Delete row</q-item-section>
            </q-item>
            <q-separator />
            <q-item-label header class="text-caption q-pb-none">Columns</q-item-label>
            <q-item clickable v-close-popup @click="execTableCmd('addColumnBefore')">
              <q-item-section avatar><q-icon name="keyboard_arrow_left" /></q-item-section>
              <q-item-section>Add column left</q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="execTableCmd('addColumnAfter')">
              <q-item-section avatar><q-icon name="keyboard_arrow_right" /></q-item-section>
              <q-item-section>Add column right</q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="execTableCmd('deleteColumn')">
              <q-item-section avatar><q-icon name="delete_outline" color="negative" /></q-item-section>
              <q-item-section class="text-negative">Delete column</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup @click="execTableCmd('deleteTable')">
              <q-item-section avatar><q-icon name="grid_off" color="negative" /></q-item-section>
              <q-item-section class="text-negative">Delete table</q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
      <div ref="editorEl" style="flex:1;min-height:0;overflow-y:auto;"></div>
    </div>
  `,
  props: {
    value: String,
    docId: String,
    user: Object,
    disable: Boolean,
    toolbar: [Boolean, Array],
    resourcePath: String,
    id: String,
  },
  data() {
    return {
      // Bump on every Tiptap transaction so toolbar active-state bindings re-evaluate.
      editorUpdated: 0,
      // Allows methods called by the server before mount to await the editor.
      editorPromise: new Promise((resolve) => {
        this.resolveEditor = resolve;
      }),
    };
  },
  computed: {
    // Resolve toolbar prop to a 2D array of button-ID groups (or [] when hidden).
    toolbarGroups() {
      if (!this.toolbar) return [];
      return Array.isArray(this.toolbar) ? this.toolbar : DEFAULT_TOOLBAR;
    },
    // True when the cursor is inside a table — drives the table context toolbar.
    isInTable() {
      void this.editorUpdated;
      return this.editor ? this.editor.isActive('table') : false;
    },
  },
  watch: {
    disable(newVal) {
      if (this.editor) this.editor.setEditable(!newVal);
    },
  },
  methods: {
    // Called by NiceGUI via _update_method when Python sets .value.
    setContentFromProps() {
      if (!this.editor) return;
      if (this.editor.getHTML() === this.value) return;
      this._applyingServerContent = true;
      this.editor.commands.setContent(this.value || '', false);
      this._applyingServerContent = false;
    },
    getHTML() {
      return this.editor ? this.editor.getHTML() : '';
    },
    // Look up a button definition by ID; returns {} for unknown IDs.
    getBtn(id) {
      return BUTTONS[id] || {};
    },
    // Returns whether the given button's format is active at the current selection.
    // Accessing this.editorUpdated registers it as a reactive dependency so the
    // toolbar re-renders after every Tiptap transaction.
    isActive(id) {
      void this.editorUpdated;
      const btn = BUTTONS[id];
      if (!btn || !btn.active || !this.editor) return false;
      return this.editor.isActive(...btn.active);
    },
    // Execute the command for a toolbar button.
    execBtn(id) {
      const btn = BUTTONS[id];
      if (!btn || !this.editor) return;
      const chain = this.editor.chain().focus();
      (btn.cmdAttrs ? chain[btn.cmd](btn.cmdAttrs) : chain[btn.cmd]()).run();
    },
    // Returns the label for a dropdown button reflecting the currently active item.
    getDropdownLabel(id) {
      void this.editorUpdated;
      const btn = BUTTONS[id];
      if (!btn || !btn.items) return '';
      if (!this.editor) return btn.items[0]?.label || '';
      const active = btn.items.find((item) => item.active && this.editor.isActive(...item.active));
      return active ? active.label : btn.items[0].label;
    },
    // Returns true when the given dropdown item matches the current editor state.
    isDropdownItemActive(item) {
      void this.editorUpdated;
      if (!item.active || !this.editor) return false;
      return this.editor.isActive(...item.active);
    },
    // Execute a table structural command (addRowBefore, deleteColumn, etc.).
    execTableCmd(cmd) {
      if (!this.editor) return;
      this.editor.chain().focus()[cmd]().run();
    },
    // Full document reset triggered by a server-side set_state() call.
    // A plain CRDT merge cannot restore deleted content (deletions are permanent),
    // so we recreate the Y.Doc and the Tiptap editor from scratch.
    async _resetToState(updateBytes) {
      this.awareness.destroy();
      this.editor.destroy();

      // Fresh Yjs document populated with the restored state.
      this.ydoc = new RTE.Y.Doc();
      this.awareness = new RTE.Awareness(this.ydoc);
      RTE.Y.applyUpdate(this.ydoc, updateBytes, 'server');

      // Re-bind outbound listeners to the new ydoc / awareness instances.
      this.ydoc.on('update', (update, origin) => {
        if (origin === 'server') return;
        if (!window.socket) return;
        window.socket.emit('yjs_update', {
          client_id: window.clientId,
          doc_id: this.docId,
          update: Array.from(update),
        });
      });
      this.awareness.on('update', ({ added, updated, removed }) => {
        if (!window.socket) return;
        const changed = [...added, ...updated, ...removed];
        const encoded = RTE.encodeAwarenessUpdate(this.awareness, changed);
        window.socket.emit('yjs_awareness', {
          client_id: window.clientId,
          doc_id: this.docId,
          awareness: Array.from(encoded),
        });
      });

      // Update the inbound awareness handler to reference the new awareness object.
      this._onYjsAwareness = (data) => {
        if (data.doc_id !== this.docId) return;
        RTE.applyAwarenessUpdate(this.awareness, new Uint8Array(data.awareness), 'server');
      };
      window.socket.off('yjs_awareness', this._onYjsAwareness);
      window.socket.on('yjs_awareness', this._onYjsAwareness);

      // Recreate the Tiptap editor bound to the new ydoc.
      await this.$nextTick();
      const userInfo = this.user?.name ? this.user : {
        name: 'Anonymous',
        color: '#' + Math.floor(Math.random() * 0xffffff).toString(16).padStart(6, '0'),
      };
      this.editor = new RTE.Editor({
        element: this.$refs.editorEl,
        editable: !this.disable,
        extensions: [
          RTE.StarterKit.configure({ history: false }),
          RTE.Underline,
          RTE.Collaboration.configure({ document: this.ydoc }),
          RTE.CollaborationCursor.configure({
            provider: { awareness: this.awareness },
            user: userInfo,
          }),
          RTE.Image,
          RTE.Table.configure({ resizable: true }),
          RTE.TableRow,
          RTE.TableCell,
          RTE.TableHeader,
        ],
        onUpdate: ({ editor }) => {
          if (!this._applyingServerContent) this.$emit('update:value', editor.getHTML());
        },
        onTransaction: () => { this.editorUpdated += 1; },
      });
    },
    // Execute the command for a dropdown menu item.
    execDropdownItem(item) {
      if (!this.editor) return;
      const chain = this.editor.chain().focus();
      (item.cmdAttrs ? chain[item.cmd](item.cmdAttrs) : chain[item.cmd]()).run();
    },
  },
  async mounted() {
    this.$nextTick().then(() =>
      loadResource(window.path_prefix + `${this.resourcePath}/tiptap.css`),
    );

    // Flag used to suppress echoing server-applied content back to the server.
    this._applyingServerContent = false;

    // --- Yjs document and awareness ---
    this.ydoc = new RTE.Y.Doc();
    this.awareness = new RTE.Awareness(this.ydoc);

    // --- Outbound: doc updates → server ---
    // window.socket is set inside the root Vue app's mounted() hook, which runs
    // AFTER child component mounted() hooks in Vue 3. We access window.socket
    // lazily inside callbacks so it is always resolved at call time.
    this.ydoc.on('update', (update, origin) => {
      // 'server' origin means we applied an inbound relay — do not echo it back.
      if (origin === 'server') return;
      if (!window.socket) return;
      window.socket.emit('yjs_update', {
        client_id: window.clientId,
        doc_id: this.docId,
        update: Array.from(update),
      });
    });

    // --- Outbound: awareness (cursor positions) → server ---
    this.awareness.on('update', ({ added, updated, removed }) => {
      if (!window.socket) return;
      const changed = [...added, ...updated, ...removed];
      const encoded = RTE.encodeAwarenessUpdate(this.awareness, changed);
      window.socket.emit('yjs_awareness', {
        client_id: window.clientId,
        doc_id: this.docId,
        awareness: Array.from(encoded),
      });
    });

    // --- Inbound handlers (named references for later .off() cleanup) ---
    this._onYjsUpdate = (data) => {
      if (data.doc_id !== this.docId) return;
      RTE.Y.applyUpdate(this.ydoc, new Uint8Array(data.update), 'server');
    };
    this._onYjsAwareness = (data) => {
      if (data.doc_id !== this.docId) return;
      RTE.applyAwarenessUpdate(this.awareness, new Uint8Array(data.awareness), 'server');
    };
    this._onYjsInit = (data) => {
      if (data.doc_id !== this.docId) return;
      RTE.Y.applyUpdate(this.ydoc, new Uint8Array(data.update), 'server');
    };
    this._onYjsReset = (data) => {
      if (data.doc_id !== this.docId) return;
      this._resetToState(new Uint8Array(data.update));
    };

    // Register inbound listeners once the socket is ready.
    // We poll with nextTick until window.socket is available (set by root Vue mounted()).
    const registerSocketListeners = async () => {
      while (!window.socket) {
        await new Promise((resolve) => setTimeout(resolve, 10));
      }
      window.socket.on('yjs_update', this._onYjsUpdate);
      window.socket.on('yjs_awareness', this._onYjsAwareness);
      window.socket.on('yjs_init', this._onYjsInit);
      window.socket.on('yjs_reset', this._onYjsReset);
      // Join the room — server replies with yjs_init if the doc has existing state.
      window.socket.emit('yjs_join', { client_id: window.clientId, doc_id: this.docId });
    };
    registerSocketListeners();

    // --- User identity for collaboration cursors ---
    const userInfo =
      this.user && this.user.name
        ? this.user
        : {
            name: 'Anonymous',
            color:
              '#' +
              Math.floor(Math.random() * 0xffffff)
                .toString(16)
                .padStart(6, '0'),
          };

    // --- Create Tiptap editor ---
    this.editor = new RTE.Editor({
      element: this.$refs.editorEl,
      editable: !this.disable,
      extensions: [
        // history: false is mandatory — Yjs/y-prosemirror provides its own undo stack.
        RTE.StarterKit.configure({ history: false }),
        RTE.Underline,
        RTE.Collaboration.configure({ document: this.ydoc }),
        // CollaborationCursor only requires provider.awareness — our Awareness object satisfies this.
        RTE.CollaborationCursor.configure({
          provider: { awareness: this.awareness },
          user: userInfo,
        }),
        RTE.Image,
        RTE.Table.configure({ resizable: true }),
        RTE.TableRow,
        RTE.TableCell,
        RTE.TableHeader,
      ],
      onUpdate: ({ editor }) => {
        if (!this._applyingServerContent) {
          this.$emit('update:value', editor.getHTML());
        }
      },
      // Bump editorUpdated on every transaction so toolbar active-state re-evaluates.
      onTransaction: () => {
        this.editorUpdated += 1;
      },
    });

    // Apply any initial HTML value passed from Python.
    if (this.value) this.setContentFromProps();

    this.resolveEditor(this.editor);
  },
  beforeUnmount() {
    // Sync final HTML back to the server element state (mirrors codemirror.js pattern).
    const element = mounted_app.elements[this.$props.id.slice(1)];
    if (element) element.props.value = this.getHTML();

    if (window.socket) {
      window.socket.emit('yjs_leave', { client_id: window.clientId, doc_id: this.docId });
      window.socket.off('yjs_update', this._onYjsUpdate);
      window.socket.off('yjs_awareness', this._onYjsAwareness);
      window.socket.off('yjs_init', this._onYjsInit);
      window.socket.off('yjs_reset', this._onYjsReset);
    }

    if (this.awareness) this.awareness.destroy();
    if (this.editor) this.editor.destroy();
  },
};
