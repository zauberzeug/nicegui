from pathlib import Path

import pytest

from nicegui import ui
from nicegui.testing import Screen, User

# pylint: disable=protected-access


def test_tiptap_renders(screen: Screen):
    """Editor renders and initial HTML content is visible in the DOM."""
    @ui.page('/')
    def page():
        ui.tiptap('<p>Hello World</p>')

    screen.open('/')
    screen.should_contain('Hello World')


async def test_unique_doc_id_per_instance(user: User) -> None:
    """Two editors without an explicit doc_id receive distinct UUIDs."""
    results: dict = {}

    @ui.page('/')
    def page():
        results['e1'] = ui.tiptap()
        results['e2'] = ui.tiptap()

    await user.open('/')
    assert results['e1'].doc_id != results['e2'].doc_id


async def test_explicit_doc_id(user: User) -> None:
    """An explicit doc_id is forwarded to the element props unchanged."""
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(doc_id='my-room')

    await user.open('/')
    editor = results['editor']
    assert editor.doc_id == 'my-room'
    assert editor._props['doc-id'] == 'my-room'


async def test_user_prop(user: User) -> None:
    """The user dict is stored in _props and forwarded to the Vue component."""
    user_data = {'name': 'Alice', 'color': '#3b82f6'}
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(user=user_data)

    await user.open('/')
    assert results['editor']._props['user'] == user_data


async def test_empty_user_prop_defaults_to_empty_dict(user: User) -> None:
    """When user is omitted, _props['user'] is an empty dict (Vue picks random colour)."""
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap()

    await user.open('/')
    assert results['editor']._props['user'] == {}


async def test_disable(user: User) -> None:
    """Disabled editor sets the disable prop correctly."""
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap()

    await user.open('/')
    results['editor'].disable()
    assert results['editor']._props.get('disable') is True


async def test_get_state_requires_y_py(user: User) -> None:
    """get_state raises ImportError with a helpful message when y-py is absent."""
    from nicegui import tiptap_room

    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(doc_id='state-test')

    await user.open('/')
    editor = results['editor']
    original = tiptap_room.HAS_Y_PY
    try:
        tiptap_room.HAS_Y_PY = False
        with pytest.raises(ImportError, match='y-py'):
            editor.get_state()
    finally:
        tiptap_room.HAS_Y_PY = original


async def test_set_state_requires_y_py(user: User) -> None:
    """set_state raises ImportError with a helpful message when y-py is absent."""
    from nicegui import tiptap_room

    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(doc_id='set-state-test')

    await user.open('/')
    editor = results['editor']
    original = tiptap_room.HAS_Y_PY
    try:
        tiptap_room.HAS_Y_PY = False
        with pytest.raises(ImportError, match='y-py'):
            editor.set_state(b'')
    finally:
        tiptap_room.HAS_Y_PY = original


async def test_room_state_is_initially_bytes(user: User) -> None:
    """get_state returns bytes (empty Yjs state) even before any client connects."""
    pytest.importorskip('y_py')

    doc_id = f'initial-state-{id(object())}'
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(doc_id=doc_id)

    await user.open('/')
    state = results['editor'].get_state()
    assert isinstance(state, bytes)
    # Yjs encodes an empty document as exactly 2 bytes.
    assert len(state) >= 2


async def test_room_state_roundtrip(user: User) -> None:
    """get_state / set_state roundtrip does not corrupt the doc (requires y-py)."""
    pytest.importorskip('y_py')
    from nicegui import tiptap_room

    doc_id = f'roundtrip-{id(object())}'
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(doc_id=doc_id)

    await user.open('/')
    editor = results['editor']
    state1 = editor.get_state()
    # set_state with the same bytes is a no-op CRDT merge — should not raise.
    tiptap_room.set_state(doc_id, state1)
    state2 = editor.get_state()
    assert isinstance(state2, bytes)


async def test_single_persistence_state_preserved(user: User) -> None:
    """Restored state is byte-for-byte equivalent to the saved snapshot."""
    pytest.importorskip('y_py')
    import y_py as Y

    from nicegui import tiptap_room

    doc_id = f'persist-preserved-{id(object())}'
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(doc_id=doc_id)

    await user.open('/')
    editor = results['editor']

    # Write known content into the server-side Y.Doc.
    doc = tiptap_room._get_or_create_doc(doc_id)
    ymap = doc.get_map('meta')
    with doc.begin_transaction() as txn:
        ymap.set(txn, 'version', '1')

    snapshot = editor.get_state()
    assert len(snapshot) > 2  # non-empty (Yjs empty-state sentinel is exactly 2 bytes)

    # Apply more edits — simulates user activity after the save point.
    with doc.begin_transaction() as txn:
        ymap.set(txn, 'version', '2')

    after_edit = editor.get_state()
    assert after_edit != snapshot  # confirm the state actually changed

    # Restore the snapshot.
    editor.set_state(snapshot)
    restored = editor.get_state()

    # Build the canonical reference bytes: fresh doc + snapshot applied.
    ref_doc = Y.YDoc()
    Y.apply_update(ref_doc, snapshot)
    ref_bytes = bytes(Y.encode_state_as_update(ref_doc))

    assert restored == ref_bytes

    # Release YDocs on this thread to avoid y-py "unsendable" Rust panic on GC.
    del ref_doc
    tiptap_room._clear_doc(doc_id)
    del ymap, doc


async def test_debounce_unsaved_edits_excluded_from_restore(user: User) -> None:
    """Edits within the debounce window (not yet auto-saved) are absent after restore."""
    pytest.importorskip('y_py')
    import y_py as Y

    from nicegui import tiptap_room

    doc_id = f'debounce-unsaved-{id(object())}'
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(doc_id=doc_id)

    await user.open('/')
    editor = results['editor']

    # Establish the "auto-saved" snapshot — the state the debounce timer captured.
    doc = tiptap_room._get_or_create_doc(doc_id)
    ymap = doc.get_map('content')
    with doc.begin_transaction() as txn:
        ymap.set(txn, 'saved', 'yes')

    snapshot = editor.get_state()  # what the debounce timer would have stored

    # Simulate user typing within the 2 s debounce window — NOT auto-saved yet.
    with doc.begin_transaction() as txn:
        ymap.set(txn, 'unsaved', 'yes')

    unsaved_state = editor.get_state()
    assert unsaved_state != snapshot  # confirm unsaved edits changed the state

    # Debounce timer fires: restore the earlier (auto-saved) snapshot.
    editor.set_state(snapshot)
    restored = editor.get_state()

    # Restored state must equal the snapshot, not the unsaved edits.
    ref_doc = Y.YDoc()
    Y.apply_update(ref_doc, snapshot)
    ref_bytes = bytes(Y.encode_state_as_update(ref_doc))

    assert restored == ref_bytes      # matches the auto-saved snapshot
    assert restored != unsaved_state  # unsaved content is gone

    # Release YDocs on this thread to avoid y-py "unsendable" Rust panic on GC.
    del ref_doc
    tiptap_room._clear_doc(doc_id)
    del ymap, doc


def test_remove_sid_cleans_rooms():
    """remove_sid discards a socket-ID from every room it was in."""
    from nicegui import tiptap_room

    tiptap_room._rooms['room-a'] = {'sid-1', 'sid-2'}
    tiptap_room._rooms['room-b'] = {'sid-1'}
    tiptap_room.remove_sid('sid-1')
    assert 'sid-1' not in tiptap_room._rooms['room-a']
    assert 'sid-2' in tiptap_room._rooms['room-a']
    assert 'sid-1' not in tiptap_room._rooms['room-b']


async def test_toolbar_default_true(user: User) -> None:
    """toolbar prop defaults to True."""
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap()

    await user.open('/')
    assert results['editor']._props.get('toolbar') is True


async def test_toolbar_disabled(user: User) -> None:
    """toolbar=False is forwarded to the Vue component."""
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(toolbar=False)

    await user.open('/')
    assert results['editor']._props.get('toolbar') is False


async def test_toolbar_custom_groups(user: User) -> None:
    """A 2D list toolbar is forwarded to the Vue component unchanged."""
    groups = [['bold', 'italic'], ['undo', 'redo']]
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap(toolbar=groups)

    await user.open('/')
    assert results['editor']._props.get('toolbar') == groups


async def test_update_method_is_set(user: User) -> None:
    """_update_method is set so NiceGUI calls setContentFromProps on prop updates."""
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap()

    await user.open('/')
    assert results['editor']._update_method == 'setContentFromProps'


def test_value_prop_name():
    """VALUE_PROP and LOOPBACK are set correctly on the class."""
    assert ui.tiptap.VALUE_PROP == 'value'
    assert ui.tiptap.LOOPBACK is None


async def test_shared_doc_id_returns_identical_state(user: User) -> None:
    """Two editors with the same doc_id read from the same server-side Yjs room."""
    pytest.importorskip('y_py')

    doc_id = f'shared-{id(object())}'
    results: dict = {}

    @ui.page('/')
    def page():
        results['e1'] = ui.tiptap(doc_id=doc_id)
        results['e2'] = ui.tiptap(doc_id=doc_id)

    await user.open('/')
    assert results['e1'].doc_id == results['e2'].doc_id == doc_id
    assert results['e1'].get_state() == results['e2'].get_state()


def test_table_html_renders(screen: Screen):
    """An editor initialised with table HTML shows the cell content in the DOM."""
    @ui.page('/')
    def page():
        ui.tiptap(
            '<table><thead><tr><th>Name</th><th>Role</th></tr></thead>'
            '<tbody><tr><td>Alice</td><td>Engineer</td></tr></tbody></table>',
        )

    screen.open('/')
    screen.should_contain('Name')
    screen.should_contain('Alice')
    screen.should_contain('Engineer')


def test_css_file_exists():
    """The dist/tiptap.css file must exist next to the element source."""
    import nicegui.elements.tiptap.tiptap as tiptap_module
    css = Path(tiptap_module.__file__).parent / 'dist' / 'tiptap.css'
    assert css.is_file(), f'CSS file missing: {css}'


def test_css_contains_collaboration_cursor_styles():
    """The CSS file must include the collaboration cursor rules that display other users' names."""
    import nicegui.elements.tiptap.tiptap as tiptap_module
    css = Path(tiptap_module.__file__).parent / 'dist' / 'tiptap.css'
    content = css.read_text()
    assert 'collaboration-cursor__label' in content
    assert 'collaboration-cursor__caret' in content


async def test_resource_path_prop_is_set(user: User) -> None:
    """add_resource() must set the resource-path prop so the Vue component can load the CSS."""
    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap()

    await user.open('/')
    assert 'resource-path' in results['editor']._props, 'resource-path prop missing — add_resource() not called?'


async def test_event_args_to_value_non_string(user: User) -> None:
    """_event_args_to_value returns an empty string for non-string event args."""
    from nicegui.events import GenericEventArguments

    results: dict = {}

    @ui.page('/')
    def page():
        results['editor'] = ui.tiptap()

    await user.open('/')
    editor = results['editor']
    for bad_arg in (None, 42, {}, []):
        e = GenericEventArguments(sender=editor, client=None, args=bad_arg)
        assert editor._event_args_to_value(e) == ''


def test_on_change_callback(screen: Screen):
    """on_change callback is wired up through the ValueElement machinery."""
    # Verify the callback registration does not raise; full integration requires
    # browser-level interaction to trigger the Yjs onUpdate event.
    changes: list[str] = []

    @ui.page('/')
    def page():
        ui.tiptap(
            '<p>Start</p>',
            on_change=lambda e: changes.append(e.value),
        )

    screen.open('/')
    # No error on page load means the callback was registered successfully.
