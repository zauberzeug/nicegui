export * from "codemirror";
export * from "@codemirror/view";
export * from "@codemirror/state";
export * from "@codemirror/commands";
export * from "@codemirror/language";
export * from "@codemirror/language-data";
export * from "@codemirror/theme-one-dark";
export * as themes from "@uiw/codemirror-themes-all";

// CRDT layer — opt-in via `ui.codemirror(...).with_crdt(doc_id)`. Bundled here so
// y-codemirror.next sees the same `@codemirror/state` instance as the editor;
// splitting them across rollup passes triggers "multiple instances of @codemirror/state"
// at runtime. yjs core is external and shared via NiceGUI's _yjs_bundle ESM module.
export { yCollab } from "y-codemirror.next";
export {
  Awareness,
  applyAwarenessUpdate,
  encodeAwarenessUpdate,
} from "y-protocols/awareness";
