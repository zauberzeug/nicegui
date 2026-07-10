import pytest
from selenium.webdriver.common.by import By

from nicegui import ui, yjs_room
from nicegui.testing import Screen

pytest.importorskip('pycrdt')


def test_two_editors_share_state(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror(language='Python').with_crdt('shared').classes('editor-a')
        ui.codemirror(language='Python').with_crdt('shared').classes('editor-b')

    screen.open('/')
    editor_a = screen.selenium.find_element(By.CSS_SELECTOR, '.editor-a .cm-content')
    editor_a.click()
    editor_a.send_keys('hello world')
    screen.wait(0.5)
    editor_b = screen.selenium.find_element(By.CSS_SELECTOR, '.editor-b .cm-content')
    assert 'hello world' in editor_b.text


def test_seeded_room_propagates_to_first_client(screen: Screen):
    from pycrdt import Text  # pylint: disable=import-outside-toplevel
    doc = yjs_room.get_doc('seed-test')
    doc['codemirror'] = Text()
    doc['codemirror'] += 'preseeded content'

    @ui.page('/')
    def page():
        ui.codemirror(language='Markdown').with_crdt('seed-test')

    screen.open('/')
    screen.wait(0.5)
    screen.should_contain('preseeded content')


def test_large_update_from_client_is_chunked(screen: Screen):
    from pycrdt import Text  # pylint: disable=import-outside-toplevel
    big_text = ('x' * 100 + '\n') * 15_000  # ~1.5 MB, above Engine.IO's 1 MB receive limit

    @ui.page('/')
    def page():
        editor = ui.codemirror().with_crdt('big-paste')
        ui.button('paste', on_click=lambda: editor.run_method('setEditorValue', big_text))

    screen.open('/')
    screen.wait(0.5)
    screen.click('paste')
    screen.wait(3)
    doc = yjs_room.get_doc('big-paste')
    assert str(doc.get('codemirror', type=Text)) == big_text


def test_large_seeded_state_is_chunked_to_client(screen: Screen):
    from pycrdt import Text  # pylint: disable=import-outside-toplevel
    big_text = ('y' * 100 + '\n') * 15_000  # ~1.5 MB, sent to the client in chunks
    doc = yjs_room.get_doc('big-seed')
    doc['codemirror'] = Text()
    doc['codemirror'] += big_text

    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('big-seed')

    screen.open('/')
    screen.wait(3)
    content = screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content')
    assert 'yyyy' in content.text


def test_access_check_denies_unauthorized_editor(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('gated', access_check=lambda _doc_id, _sid: False).classes('blocked')
        ui.codemirror().with_crdt('shared-open').classes('open')

    screen.open('/')
    blocked = screen.selenium.find_element(By.CSS_SELECTOR, '.blocked .cm-content')
    blocked.click()
    blocked.send_keys('should-not-sync')
    screen.wait(0.5)
    open_editor = screen.selenium.find_element(By.CSS_SELECTOR, '.open .cm-content')
    assert 'should-not-sync' not in open_editor.text
