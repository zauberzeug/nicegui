from collections.abc import Callable

from nicegui import ui
from nicegui.testing import User


async def test_page_title(user: User):
    @ui.page('/', title='My Page')
    def page():
        ui.label('Content')

    response = await user.http_client.get('/', headers={'Accept': 'text/markdown'})
    assert response.text.strip() == '# My Page\n\nContent'


async def test_html_response(user: User):
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/', headers={'Accept': 'text/html'})
    assert 'text/html' in response.headers['content-type']


async def test_label(user: User):
    await _assert_markdown(user, lambda: ui.label('Hello World'), 'Hello World')


async def test_markdown_element_passthrough(user: User):
    await _assert_markdown(user, lambda: ui.markdown('## Heading\n\n**Bold!**'), '## Heading\n\n**Bold!**')


async def test_link(user: User):
    await _assert_markdown(user, lambda: ui.link('NiceGUI', 'https://nicegui.io'), '[NiceGUI](https://nicegui.io)')


async def test_image(user: User):
    await _assert_markdown(user, lambda: ui.image('https://example.com/img.png'), '![](https://example.com/img.png)')


async def test_separator(user: User):
    await _assert_markdown(user, lambda: (ui.label('Above'), ui.separator(), ui.label('Below')), 'Above\n\n---\n\nBelow')


async def test_table(user: User):
    await _assert_markdown(user, lambda: ui.table(
        columns=[
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'age', 'label': 'Age', 'field': 'age'},
        ],
        rows=[
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25},
            {'name': 'a | b', 'age': 99},
        ],
    ), '| Name | Age |\n| --- | --- |\n| Alice | 30 |\n| Bob | 25 |\n| a \\| b | 99 |')


async def test_checkbox(user: User):
    await _assert_markdown(user, lambda: ui.checkbox('Accept terms', value=True), '- [x] Accept terms')
    await _assert_markdown(user, lambda: ui.checkbox('Subscribe', value=False), '- [ ] Subscribe')


async def test_button(user: User):
    await _assert_markdown(user, lambda: ui.button('Click me'), '[Button: Click me]')
    await _assert_markdown(user, lambda: ui.button('Click me', icon='thumb_up'), '[Button: Click me]')
    await _assert_markdown(user, lambda: ui.button(icon='face'), '[Button: icon:face]')
    await _assert_markdown(user, ui.button, '[Button]')


async def test_code_element(user: User):
    await _assert_markdown(user, lambda: ui.code('print("hello")', language='python'), '```python\nprint("hello")\n```')


async def test_input(user: User):
    await _assert_markdown(user, lambda: ui.input('Username', value='alice'), 'Username: alice')


async def test_expansion(user: User):
    def build(value: bool) -> None:
        with ui.expansion('Details', value=value):
            ui.label('Nested content')
    await _assert_markdown(user, lambda: build(True), '**Details**\n\nNested content')
    await _assert_markdown(user, lambda: build(False), '**Details**')


async def test_nested_containers(user: User):
    def build():
        with ui.card():
            with ui.row():
                ui.label('First')
                ui.label('Second')
    await _assert_markdown(user, build, 'First\n\nSecond')


async def test_no_accept_returns_html(user: User):
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/')
    assert 'text/html' in response.headers['content-type']


async def test_switch(user: User):
    await _assert_markdown(user, lambda: ui.switch('Dark mode', value=False), '- [ ] Dark mode')
    await _assert_markdown(user, lambda: ui.switch('Light mode', value=True), '- [x] Light mode')


async def test_number_input(user: User):
    await _assert_markdown(user, lambda: ui.number(value=30, label='Age'), 'Age: 30')
    await _assert_markdown(user, lambda: ui.number(value=42), '42')


async def test_textarea(user: User):
    await _assert_markdown(user, lambda: ui.textarea('Notes', value='some text'), 'Notes: some text')


async def test_chat_message(user: User):
    await _assert_markdown(user, lambda: ui.chat_message('Hello there!', name='Alice'), '**Alice**: Hello there!')


async def test_dialog(user: User):
    def build(value: bool) -> None:
        ui.label('Visible')
        with ui.dialog(value=value):
            ui.label('Nested content')
    await _assert_markdown(user, lambda: build(value=False), 'Visible')
    await _assert_markdown(user, lambda: build(value=True), 'Visible\n\nNested content')


async def test_context_menu(user: User):
    def build() -> None:
        with ui.label('Right-click me'):
            with ui.context_menu():
                ui.label('Nested content')
    await _assert_markdown(user, build, 'Right-click me')


async def test_invisible_elements(user: User):
    await _assert_markdown(user, ui.dark_mode, '')
    await _assert_markdown(user, ui.colors, '')
    await _assert_markdown(user, lambda: ui.slider(min=0, max=100, value=50), '')
    await _assert_markdown(user, lambda: ui.label('Hidden').set_visibility(False), '')


async def test_select(user: User):
    abc = ['A', 'B', 'C']
    xyz = {'X': 'x', 'Y': 'y', 'Z': 'z'}
    await _assert_markdown(user, lambda: ui.select(abc, value='B'), 'B')
    await _assert_markdown(user, lambda: ui.select(abc, value='B', label='Choice'), 'Choice: B')
    await _assert_markdown(user, lambda: ui.select(abc, value=['A', 'B', 'C'], multiple=True), 'A, B, C')
    await _assert_markdown(user, lambda: ui.select(xyz, value='Y'), 'y')
    await _assert_markdown(user, lambda: ui.select(xyz, value='Y', label='Letter'), 'Letter: y')
    await _assert_markdown(user, lambda: ui.select(xyz, value=['X', 'Y', 'Z'], multiple=True), 'x, y, z')


async def test_radio(user: User):
    await _assert_markdown(user, lambda: ui.radio(['X', 'Y', 'Z'], value='Y'), 'Y')


async def test_badge(user: User):
    await _assert_markdown(user, lambda: ui.badge('NEW'), 'NEW')


async def test_chip(user: User):
    await _assert_markdown(user, lambda: ui.chip('Tag'), 'Tag')


async def test_html(user: User):
    await _assert_markdown(user, lambda: ui.html('<b>Bold text</b>'), '<b>Bold text</b>')


async def test_menu(user: User):
    def build(value: bool) -> None:
        with ui.menu(value=value):
            ui.menu_item('Item 1')
            ui.menu_item('Item 2')
    await _assert_markdown(user, lambda: build(value=False), '')
    await _assert_markdown(user, lambda: build(value=True), 'Item 1\n\nItem 2')


async def test_notification(user: User):
    def build() -> None:
        ui.notification('Hello notification!')
        ui.label('Page content')
    await _assert_markdown(user, build, 'Page content\n\nHello notification!')


async def _assert_markdown(user: User, build: Callable, expected: str) -> None:
    @ui.page('/')
    def _():
        build()
    response = await user.http_client.get('/', headers={'Accept': 'text/markdown'})
    assert response.headers.get('X-NiceGUI-Content') == 'page'
    assert response.status_code == 200
    assert 'text/markdown' in response.headers['content-type']
    assert response.text.strip() == f'# NiceGUI\n\n{expected}'.strip()
