import time

import pytest
from selenium.webdriver import ActionChains
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


def test_collaboration_survives_socket_reconnect(screen: Screen):
    from pycrdt import Text  # pylint: disable=import-outside-toplevel

    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('reconnect-doc')

    screen.open('/')
    editor = screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content')
    editor.click()
    editor.send_keys('before ')
    screen.wait(0.5)
    screen.selenium.execute_script('window.socket.io.engine.close();')  # simulate a network blip
    screen.wait(2)  # Socket.IO auto-reconnects with a new sid; the client must re-join
    editor.send_keys('after')
    screen.wait(0.5)
    doc = yjs_room.get_doc('reconnect-doc')
    assert str(doc.get('codemirror', type=Text)) == 'before after'


def test_room_evicts_after_client_is_deleted(screen: Screen):
    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('evict-doc')

    @ui.page('/other')
    def other():
        ui.label('elsewhere')

    screen.open('/')
    screen.wait(0.5)
    assert 'evict-doc' in yjs_room._rooms  # pylint: disable=protected-access
    screen.open('/other')  # disconnects the editor's client, which is deleted after the reconnect timeout
    deadline = time.time() + 10
    while 'evict-doc' in yjs_room._rooms and time.time() < deadline:  # pylint: disable=protected-access
        screen.wait(0.5)
    assert 'evict-doc' not in yjs_room._rooms  # pylint: disable=protected-access


def test_async_access_check_denies_unauthorized_editor(screen: Screen):
    async def deny(_doc_id: str, _sid: str) -> bool:
        return False

    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('async-gated', access_check=deny).classes('blocked')
        ui.codemirror().with_crdt('async-open').classes('open')

    screen.open('/')
    blocked = screen.selenium.find_element(By.CSS_SELECTOR, '.blocked .cm-content')
    blocked.click()
    blocked.send_keys('should-not-sync')
    screen.wait(0.5)
    assert 'async-gated' not in yjs_room._rooms  # pylint: disable=protected-access


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


def test_line_anchors_survive_initial_sync(screen: Screen):
    from pycrdt import Text  # pylint: disable=import-outside-toplevel
    editor: ui.codemirror = None  # type: ignore[assignment]
    doc = yjs_room.get_doc('anchor-seed')
    doc['codemirror'] = Text()
    doc['codemirror'] += 'one\ntwo\nthree\nfour'

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(line_anchors={'mid': 3}).with_crdt('anchor-seed')

    screen.open('/')
    screen.wait_for(lambda: editor.line_anchors == {'mid': 3})


def test_line_tooltips_survive_initial_sync(screen: Screen):
    from pycrdt import Text  # pylint: disable=import-outside-toplevel
    doc = yjs_room.get_doc('tooltip-seed')
    doc['codemirror'] = Text()
    doc['codemirror'] += 'one\ntwo\nthree\nfour'

    @ui.page('/')
    def page():
        ui.codemirror(line_tooltips={3: 'seeded tooltip'}).with_crdt('tooltip-seed').classes('w-24')

    screen.open('/')
    screen.should_contain('three')  # arrives via yjs_init, after the tooltip was first applied
    ActionChains(screen.selenium).move_to_element(screen.find('three')).perform()
    screen.should_contain('seeded tooltip')


def test_line_anchors_are_applied_when_the_join_is_denied(screen: Screen):
    editor: ui.codemirror = None  # type: ignore[assignment]

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(line_anchors={'top': 1}).with_crdt('anchor-denied',
                                                                  access_check=lambda _doc_id, _sid: False)

    screen.open('/')
    screen.wait_for(lambda: editor.line_anchors == {'top': 1})


def test_line_anchors_are_applied_when_the_doc_id_is_not_a_string(screen: Screen):
    editor: ui.codemirror = None  # type: ignore[assignment]

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(line_anchors={'top': 1}).with_crdt(42)  # type: ignore[arg-type]

    screen.open('/')
    screen.wait_for(lambda: editor.line_anchors == {'top': 1})


def test_line_anchors_are_applied_when_the_access_check_raises(screen: Screen):
    editor: ui.codemirror = None  # type: ignore[assignment]

    def broken(_doc_id: str, _sid: str) -> bool:
        raise RuntimeError('access backend is down')

    @ui.page('/')
    def page():
        nonlocal editor
        editor = ui.codemirror(line_anchors={'top': 1}).with_crdt('anchor-broken', access_check=broken)

    screen.open('/')
    screen.wait_for(lambda: editor.line_anchors == {'top': 1})
    assert 'anchor-broken' not in yjs_room._rooms  # pylint: disable=protected-access
    screen.assert_py_logger('ERROR', 'access backend is down')
    screen.caplog.records.clear()  # a reconnect re-joins and raises again


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


def test_stale_tail_chunks_do_not_corrupt_next_transfer(screen: Screen):
    from pycrdt import Doc, Text  # pylint: disable=import-outside-toplevel

    def update_for(content: str) -> bytes:
        doc = Doc()
        doc['codemirror'] = text = Text()
        text += content
        return doc.get_update()

    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('stale-tail')

    screen.open('/')
    screen.wait(0.5)
    # A client joining mid-relay only receives the tail of a chunked update; the next transfer must not reuse it.
    stale, fresh = update_for('stale ' * 20), update_for('fresh content')

    def thirds(update: bytes) -> list[list[int]]:
        return [list(update[i * len(update) // 3:(i + 1) * len(update) // 3]) for i in range(3)]

    screen.selenium.execute_script('''
        const [stale, fresh] = arguments;
        const deliver = (update, part) => window.socket.onevent({
            data: ['yjs_update', { doc_id: 'stale-tail', update, part, parts: 3 }],
        });
        deliver(stale[1], 1);
        deliver(stale[2], 2);
        fresh.forEach((update, part) => deliver(update, part));
    ''', thirds(stale), thirds(fresh))
    screen.wait(0.5)
    assert screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content').text == 'fresh content'


def test_offline_edits_survive_page_reload(screen: Screen):
    screen.allowed_js_errors.append('ERR_INTERNET_DISCONNECTED')

    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('offline-reload')

    def set_offline(offline: bool) -> None:
        screen.selenium.execute_cdp_cmd('Network.enable', {})
        screen.selenium.execute_cdp_cmd('Network.emulateNetworkConditions', {
            'offline': offline, 'latency': 0, 'downloadThroughput': -1, 'uploadThroughput': -1})

    def content() -> str:
        return screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content').text

    screen.open('/')
    window_a = screen.selenium.current_window_handle
    editor = screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content')
    editor.click()
    editor.send_keys('keep-me DELETE-ME')
    screen.wait(0.5)

    screen.selenium.switch_to.new_window('window')  # a second, online client
    window_b = screen.selenium.current_window_handle
    screen.open('/')
    screen.wait(1)
    assert content() == 'keep-me DELETE-ME'

    screen.selenium.switch_to.window(window_a)
    set_offline(True)
    screen.selenium.execute_script('window.socket.io.engine.close();')
    screen.selenium.execute_script('window.marker = 1')
    editor.send_keys(' offline-edit')

    screen.selenium.switch_to.window(window_b)
    screen.selenium.execute_script('''
        const view = document.querySelector('.cm-content').cmView.view;
        view.dispatch({changes: {from: 8, to: 17}});
        view.dispatch({changes: {from: view.state.doc.length, insert: ' b-edit'}});''')
    assert content() == 'keep-me  b-edit'

    screen.wait(5)  # longer than reconnect_timeout=3: the server forgets client A and its page reloads
    screen.selenium.switch_to.window(window_a)
    set_offline(False)
    deadline = time.time() + 15
    while time.time() < deadline and screen.selenium.execute_script('return window.marker') is not None:
        screen.wait(0.5)
    screen.wait(2)
    assert screen.selenium.execute_script('return window.marker') is None, 'page should have reloaded'
    expected = content()
    assert expected.count('offline-edit') == 1 and expected.count('b-edit') == 1
    assert 'DELETE-ME' not in expected and expected.startswith('keep-me')
    screen.selenium.switch_to.window(window_b)
    assert content() == expected


def test_edit_dropped_on_a_connected_socket_survives_page_reload(screen: Screen):
    screen.allowed_js_errors.append('ERR_INTERNET_DISCONNECTED')

    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('dropped-edit')

    def content() -> str:
        return screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content').text

    screen.open('/')
    window_a = screen.selenium.current_window_handle
    editor = screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content')
    editor.click()
    editor.send_keys('start')
    screen.wait(0.5)

    # half-open connection: the socket still reports connected, but the update never reaches the server
    screen.selenium.execute_script('window.socket.io.engine.write = () => {}; window.marker = 1')
    editor.send_keys(' dropped-edit')
    assert screen.selenium.execute_script('return window.socket.connected') is True
    screen.selenium.execute_cdp_cmd('Network.enable', {})
    screen.selenium.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': True, 'latency': 0, 'downloadThroughput': -1, 'uploadThroughput': -1})
    screen.selenium.execute_script('window.socket.io.engine.close();')
    screen.wait(5)  # longer than reconnect_timeout=3: the server forgets the client and its page reloads
    screen.selenium.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False, 'latency': 0, 'downloadThroughput': -1, 'uploadThroughput': -1})
    deadline = time.time() + 15
    while time.time() < deadline and screen.selenium.execute_script('return window.marker') is not None:
        screen.wait(0.5)
    screen.wait(2)
    assert screen.selenium.execute_script('return window.marker') is None, 'page should have reloaded'
    assert content() == 'start dropped-edit'

    screen.selenium.switch_to.new_window('window')  # a second client deletes the restored text
    window_b = screen.selenium.current_window_handle
    screen.open('/')
    screen.wait(1)
    assert content() == 'start dropped-edit'
    screen.selenium.execute_script(
        "document.querySelector('.cm-content').cmView.view.dispatch({changes: {from: 5, to: 18}});")
    screen.wait(1)

    screen.selenium.switch_to.window(window_a)
    screen.selenium.execute_script('location.reload()')  # a clean tab stores its state on unload again
    screen.wait(3)
    assert content() == 'start'
    screen.selenium.switch_to.window(window_b)
    assert content() == 'start'


def _seed(doc_id: str, text: str) -> None:
    from pycrdt import Text  # pylint: disable=import-outside-toplevel
    doc = yjs_room.get_doc(doc_id)
    if 'codemirror' not in doc.keys():
        doc['codemirror'] = Text()
        doc['codemirror'] += text


def _outage_until_room_is_dropped(screen: Screen, doc_id: str) -> None:
    """Take the tab offline for longer than reconnect_timeout and prove the server dropped the room."""
    screen.selenium.execute_cdp_cmd('Network.enable', {})
    screen.selenium.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': True, 'latency': 0, 'downloadThroughput': -1, 'uploadThroughput': -1})
    screen.selenium.execute_script('window.socket.io.engine.close();')
    deadline = time.time() + 15
    while doc_id in yjs_room._rooms and time.time() < deadline:  # pylint: disable=protected-access
        screen.wait(0.5)
    assert doc_id not in yjs_room._rooms, 'room should have been dropped'  # pylint: disable=protected-access


def _come_back_online_and_wait_for_reload(screen: Screen) -> None:
    screen.selenium.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False, 'latency': 0, 'downloadThroughput': -1, 'uploadThroughput': -1})
    deadline = time.time() + 15
    while time.time() < deadline and screen.selenium.execute_script('return window.marker') is not None:
        screen.wait(0.5)
    screen.wait(2)
    assert screen.selenium.execute_script('return window.marker') is None, 'page should have reloaded'


def test_seeded_room_dropped_during_outage_is_not_duplicated_by_reload(screen: Screen):
    screen.allowed_js_errors.append('ERR_INTERNET_DISCONNECTED')

    @ui.page('/')
    def page():
        _seed('seeded-gap', 'seed')
        ui.codemirror().with_crdt('seeded-gap')

    def content() -> str:
        return screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content').text

    screen.open('/')
    screen.wait(1)
    assert content() == 'seed'
    editor = screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content')
    editor.click()
    editor.send_keys(' typed')
    screen.wait(0.5)
    assert content() == 'seed typed'
    screen.selenium.execute_script('window.marker = 1')
    _outage_until_room_is_dropped(screen, 'seeded-gap')
    _come_back_online_and_wait_for_reload(screen)
    assert content() == 'seed'  # the server rebuilt the room from the seed; replaying the old copy would double it


def test_room_reseeded_by_the_server_during_outage_is_not_duplicated_by_reload(screen: Screen):
    screen.allowed_js_errors.append('ERR_INTERNET_DISCONNECTED')

    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('server-changed')

    def content() -> str:
        return screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content').text

    screen.open('/')
    editor = screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content')
    editor.click()
    editor.send_keys('start dropped-edit')
    screen.wait(0.5)
    screen.selenium.execute_script('window.marker = 1')
    _outage_until_room_is_dropped(screen, 'server-changed')
    _seed('server-changed', 'server-new')  # the application re-creates the room with different content
    _come_back_online_and_wait_for_reload(screen)
    assert content() == 'server-new'


def test_stored_copy_is_not_applied_again_by_later_reloads(screen: Screen):
    screen.allowed_js_errors.append('ERR_INTERNET_DISCONNECTED')

    @ui.page('/')
    def page():
        ui.codemirror().with_crdt('two-reloads')

    def content() -> str:
        return screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content').text

    screen.open('/')
    editor = screen.selenium.find_element(By.CSS_SELECTOR, '.cm-content')
    editor.click()
    editor.send_keys('start dropped-edit')
    screen.wait(0.5)
    screen.selenium.execute_script('window.marker = 1')
    _outage_until_room_is_dropped(screen, 'two-reloads')
    _come_back_online_and_wait_for_reload(screen)
    assert content() == 'start dropped-edit'
    for _ in range(2):
        screen.selenium.execute_script('location.reload()')
        screen.wait(3)
        assert content() == 'start dropped-edit'
