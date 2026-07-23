#!/usr/bin/env python3
"""Two-browser collaborative code editor.

Open the served URL in two browser windows (or share it with a colleague). Edits in
one window propagate to the other in real time via Yjs + pycrdt, with live cursor and
selection awareness.

Requires the ``[crdt]`` extra::

    pip install "nicegui[crdt]"
"""
from nicegui import ui

DOC_ID = 'shared-demo'  # treat as a soft secret; replace with a per-document UUID in a real app.


@ui.page('/')
def index() -> None:
    ui.label('Collaborative code editor').classes('text-xl font-bold')
    ui.label(f'All sessions on this page share document "{DOC_ID}".').classes('text-sm text-gray-600')
    ui.codemirror(language='Python', line_wrapping=True).with_crdt(DOC_ID).classes('w-full h-96')


ui.run()
