from nicegui import ui

from . import doc

@doc.demo(ui.tiptap)
def main_demo() -> None:
    ui.tiptap('<p>Hello, <strong>world!</strong></p>').classes('h-full w-full border')


@doc.demo('Custom toolbar', '''
Use ``ui.tiptap.Toolbar(buttons=[[...], [...]])`` to define custom button groups.
Each inner list becomes a button group with a separator between groups.
Use ``toolbar=None`` to hide the toolbar.
''')
def toolbar_demo() -> None:
    ui.tiptap('<p>Minimal toolbar</p>', toolbar=ui.tiptap.Toolbar(buttons=[
        ['bold', 'italic', 'underline'],
        ['bullet_list', 'ordered_list'],
        ['undo', 'redo'],
    ])).classes('h-full w-full border')


@doc.demo('Available toolbar buttons', '''
Every button has a string ID that you use when building a custom toolbar.
The editor below shows all of them at once.

**Inline formatting** — ``bold``, ``italic``, ``underline``, ``strike``, ``code``

**Headings** — ``heading`` (dropdown: Normal / H1 / H2 / H3), or individual buttons ``h1``, ``h2``, ``h3``

**Lists** — ``bullet_list``, ``ordered_list``

**Blocks** — ``blockquote``, ``code_block``, ``table``, ``hr``

**History** — ``undo``, ``redo``
''')
def all_buttons_demo() -> None:
    ui.tiptap('<p>Try every button above.</p>', toolbar=ui.tiptap.Toolbar(buttons=[
        ['bold', 'italic', 'underline', 'strike', 'code'],
        ['heading', 'h1', 'h2', 'h3'],
        ['bullet_list', 'ordered_list'],
        ['blockquote', 'code_block'],
        ['table', 'hr'],
        ['undo', 'redo'],
    ])).classes('h-full w-full border')


@doc.demo('Collaborative editing', '''
Two or more clients sharing the same ``doc_id`` edit the same document
in real time without any external server.
Open this demo in two browser tabs to see collaboration in action.
''')
def collab_demo() -> None:
    ui.label('Open a second tab and start typing, changes appear instantly.').classes('text-sm text-gray-500')
    ui.tiptap('', doc_id='shared-room').classes('h-full w-full border')


@doc.demo('Collaborative tables', '''
The editor supports multi-column tables with a header row out of the box.
Use the ``table`` toolbar button to insert a new 3×3 table, or supply
initial HTML with a ``<table>`` element.
Clicking inside a table reveals an *Edit table* dropdown for adding or
removing rows and columns, or deleting the whole table.
Tab / Shift-Tab navigates between cells; cell content supports all inline
formatting (bold, italic, etc.).
''')
def table_demo() -> None:
    ui.tiptap(
        '<table>'
        '<thead><tr><th>Name</th><th>Role</th><th>Status</th></tr></thead>'
        '<tbody>'
        '<tr><td>Alice</td><td>Engineer</td><td>Active</td></tr>'
        '<tr><td>Bob</td><td>Designer</td><td>On leave</td></tr>'
        '</tbody>'
        '</table>',
        toolbar=ui.tiptap.Toolbar(buttons=[['bold', 'italic'], ['table'], ['undo', 'redo']]),
        doc_id='shared-table'
    ).classes('h-full w-full border')


@doc.demo('Named users with colored cursors', '''
Pass a ``user`` dict with a ``name`` and ``color`` to show collaborators\'
cursor positions and names inside the editor.
''')
def user_demo() -> None:
    def join_room(name: str, color: str) -> None:
        ui.tiptap('', doc_id='named-room', user={'name': name, 'color': color}).classes('h-full w-full border')

    with ui.row():
        name = ui.input('Input your name', value='')
        color = ui.color_input('Select your color')
    ui.button('join room').on_click(lambda: join_room(name.value, color.value))


# NOTE The states requires the ``pycrdt`` package: ``pip install pycrdt``
@doc.demo('Persistence with get_state / set_state', '''
``get_state()`` returns raw Yjs binary bytes that can be stored in any database
(e.g. MongoDB, Redis, or a file).  ``set_state()`` restores and broadcasts the
state to all connected clients.
''')
def persistence_demo() -> None:
    saved: dict = {}
    editor = ui.tiptap('<p>Editable content</p>', doc_id='persist-demo').classes('h-full w-full border')

    def save():
        saved['data'] = editor.get_state()
        ui.notify('State saved!')

    def restore():
        if 'data' in saved:
            editor.set_state(saved['data'])
            ui.notify('State restored!')
        else:
            ui.notify('Nothing saved yet.', type='warning')

    with ui.row():
        ui.button('Save', on_click=save)
        ui.button('Restore', on_click=restore)


@doc.demo('Multi-user persistence strategy', '''
When multiple clients share a ``doc_id``, always read state **server-side** via
``get_state()`` — never collect HTML from individual clients.
The server maintains one Yjs document per ``doc_id`` that merges every client\'s edits
in real time, so a single call always returns the complete state regardless of how many
users are connected.

The recommended save strategy is to **debounce writes on change**: cancel the previous
timer on each edit and write to the database only after a quiet period.
Ten concurrent users still produce at most one database write per interval.

``set_state()`` is a **hard reset** — every connected client recreates its Yjs document
from the snapshot, discarding edits made after that point.
The typical use case is pre-populating a room from the database before users connect.
If the room is already active, all clients will lose unsaved changes, so warn users first.
''')
def multi_user_persistence_demo() -> None:
    import asyncio
    from nicegui import background_tasks

    db: dict[str, bytes] = {}
    _pending: dict[str, asyncio.Task] = {}
    status = ui.label('No changes yet.').classes('text-sm text-gray-500')

    async def _deferred_save(doc_id: str) -> None:
        await asyncio.sleep(2)
        db[doc_id] = editor.get_state()
        status.set_text(f'Auto-saved ({len(db[doc_id])} bytes).')

    def on_change(_) -> None:
        doc_id = editor.doc_id
        if task := _pending.get(doc_id):
            task.cancel()
        _pending[doc_id] = background_tasks.create(
            _deferred_save(doc_id), name=f'save_{doc_id}',
        )
        status.set_text('Unsaved changes…')

    editor = ui.tiptap(
        '<p>Edit here — auto-saved 2 s after you stop typing.</p>',
        doc_id='persist-multi',
        on_change=on_change,
    ).classes('h-full w-full border')

    def restore() -> None:
        data = db.get(editor.doc_id)
        if data:
            editor.set_state(data)
            status.set_text('Restored.')
        else:
            ui.notify('Nothing saved yet.', type='warning')

    ui.button('Restore last save', on_click=restore)


doc.reference(ui.tiptap)
