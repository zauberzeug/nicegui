// Tiptap core
export { Editor } from '@tiptap/core';

// Tiptap extensions
export { StarterKit } from '@tiptap/starter-kit';
export { Collaboration } from '@tiptap/extension-collaboration';
export { CollaborationCursor } from '@tiptap/extension-collaboration-cursor';
export { Image } from '@tiptap/extension-image';
export { Underline } from '@tiptap/extension-underline';
export { Table } from '@tiptap/extension-table';
export { TableRow } from '@tiptap/extension-table-row';
export { TableCell } from '@tiptap/extension-table-cell';
export { TableHeader } from '@tiptap/extension-table-header';

// Yjs CRDT — exported as namespace so component can use Y.Doc, Y.applyUpdate, etc.
export * as Y from 'yjs';

// Yjs awareness protocol for collaborative cursors
export { Awareness, encodeAwarenessUpdate, applyAwarenessUpdate } from 'y-protocols/awareness';
