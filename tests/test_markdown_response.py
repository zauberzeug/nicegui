from nicegui import ui
from nicegui.testing import User

MARKDOWN_ACCEPT = {'Accept': 'text/markdown'}


async def test_label(user: User):
    @ui.page('/')
    def page():
        ui.label('Hello World')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert response.status_code == 200
    assert 'text/markdown' in response.headers['content-type']
    assert 'Hello World' in response.text


async def test_page_title(user: User):
    @ui.page('/', title='My Page')
    def page():
        ui.label('Content')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert response.text.startswith('# My Page')
    assert 'Content' in response.text


async def test_markdown_element_passthrough(user: User):
    @ui.page('/')
    def page():
        ui.markdown('## Hello\n\nThis is **bold** text.')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '## Hello' in response.text
    assert '**bold**' in response.text


async def test_link(user: User):
    @ui.page('/')
    def page():
        ui.link('NiceGUI', 'https://nicegui.io')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '[NiceGUI](https://nicegui.io)' in response.text


async def test_image(user: User):
    @ui.page('/')
    def page():
        ui.image('https://example.com/image.png')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '![](https://example.com/image.png)' in response.text


async def test_separator(user: User):
    @ui.page('/')
    def page():
        ui.label('Above')
        ui.separator()
        ui.label('Below')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '---' in response.text
    assert 'Above' in response.text
    assert 'Below' in response.text


async def test_table(user: User):
    @ui.page('/')
    def page():
        ui.table(
            columns=[
                {'name': 'name', 'label': 'Name', 'field': 'name'},
                {'name': 'age', 'label': 'Age', 'field': 'age'},
            ],
            rows=[
                {'name': 'Alice', 'age': 30},
                {'name': 'Bob', 'age': 25},
                {'name': 'a | b', 'age': 99},
            ],
        )

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '| Name | Age |' in response.text
    assert '| Alice | 30 |' in response.text
    assert '| Bob | 25 |' in response.text
    assert r'| a \| b | 99 |' in response.text


async def test_checkbox(user: User):
    @ui.page('/')
    def page():
        ui.checkbox('Accept terms', value=True)
        ui.checkbox('Subscribe', value=False)

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '- [x] Accept terms' in response.text
    assert '- [ ] Subscribe' in response.text


async def test_button(user: User):
    @ui.page('/')
    def page():
        ui.button('Click me')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '[Button: Click me]' in response.text


async def test_code_element(user: User):
    @ui.page('/')
    def page():
        ui.code('print("hello")', language='python')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '```python' in response.text
    assert 'print("hello")' in response.text
    assert '```' in response.text


async def test_input(user: User):
    @ui.page('/')
    def page():
        ui.input('Username', value='alice')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Username: alice' in response.text


async def test_expansion(user: User):
    @ui.page('/')
    def page():
        with ui.expansion('Details'):
            ui.label('Hidden content')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '**Details**' in response.text
    assert 'Hidden content' in response.text


async def test_nested_containers(user: User):
    @ui.page('/')
    def page():
        with ui.card():
            with ui.row():
                ui.label('First')
                ui.label('Second')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'First' in response.text
    assert 'Second' in response.text


async def test_html_accept_returns_html(user: User):
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/', headers={'Accept': 'text/html'})
    assert 'text/html' in response.headers['content-type']


async def test_no_accept_returns_html(user: User):
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/')
    assert 'text/html' in response.headers['content-type']


async def test_switch(user: User):
    @ui.page('/')
    def page():
        ui.switch('Dark mode', value=True)

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '- [x] Dark mode' in response.text


async def test_number_input(user: User):
    @ui.page('/')
    def page():
        ui.number('Age', value=25)

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Age: 25' in response.text


async def test_textarea(user: User):
    @ui.page('/')
    def page():
        ui.textarea('Notes', value='some text')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Notes: some text' in response.text


async def test_chat_message(user: User):
    @ui.page('/')
    def page():
        ui.chat_message('Hello there!', name='Alice')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '**Alice**' in response.text
    assert 'Hello there!' in response.text


async def test_dialog_closed(user: User):
    """Closed dialog should not render children."""
    @ui.page('/')
    def page():
        with ui.dialog():
            ui.label('Secret content')
        ui.label('Visible')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Visible' in response.text
    assert 'Secret' not in response.text


async def test_dialog_open(user: User):
    """Open dialog should render children."""
    @ui.page('/')
    def page():
        with ui.dialog(value=True):
            ui.label('Dialog content')
        ui.label('Visible')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Dialog content' in response.text
    assert 'Visible' in response.text


async def test_context_menu_skipped(user: User):
    @ui.page('/')
    def page():
        with ui.label('Right-click me'):
            with ui.context_menu():
                ui.menu_item('Option 1')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Right-click me' in response.text
    assert 'Option 1' not in response.text


async def test_non_visual_elements_skipped(user: User):
    """Non-visual elements (dark_mode, colors, etc.) produce no output by default."""
    @ui.page('/')
    def page():
        ui.dark_mode(False)
        ui.colors(primary='red')
        ui.label('Content')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Content' in response.text
    assert 'red' not in response.text


async def test_invisible_elements_excluded(user: User):
    """Elements with visible=False produce no markdown output."""
    @ui.page('/')
    def page():
        ui.label('Visible')
        ui.label('Hidden').set_visibility(False)

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Visible' in response.text
    assert 'Hidden' not in response.text


async def test_select_with_label(user: User):
    @ui.page('/')
    def page():
        ui.select(['A', 'B', 'C'], label='Choice', value='B')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Choice' in response.text
    assert 'B' in response.text


async def test_select_without_label(user: User):
    @ui.page('/')
    def page():
        ui.select(['A', 'B', 'C'], value='B')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'B' in response.text


async def test_radio(user: User):
    @ui.page('/')
    def page():
        ui.radio(['X', 'Y', 'Z'], value='Y')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Y' in response.text


async def test_slider_skipped(user: User):
    """Slider has no markdown representation."""
    @ui.page('/')
    def page():
        ui.slider(min=0, max=100, value=50)
        ui.label('After slider')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'After slider' in response.text
    assert '50' not in response.text


async def test_number_without_label(user: User):
    @ui.page('/')
    def page():
        ui.number(value=42)

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '42' in response.text


async def test_badge(user: User):
    @ui.page('/')
    def page():
        ui.badge('NEW')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'NEW' in response.text


async def test_chip(user: User):
    @ui.page('/')
    def page():
        ui.chip('Tag')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Tag' in response.text


async def test_html_element(user: User):
    @ui.page('/')
    def page():
        ui.html('<b>Bold text</b>')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '<b>Bold text</b>' in response.text


async def test_menu_closed(user: User):
    """Closed menu should not render children."""
    @ui.page('/')
    def page():
        with ui.button('Menu button'):
            with ui.menu():
                ui.menu_item('Item 1')
        ui.label('Visible')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Visible' in response.text
    assert 'Item 1' not in response.text


async def test_menu_open(user: User):
    """Open menu should render children."""
    @ui.page('/')
    def page():
        with ui.column():
            with ui.menu(value=True):
                ui.menu_item('Item 1')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Item 1' in response.text


async def test_notification(user: User):
    """Notification should render its message."""
    @ui.page('/')
    def page():
        ui.notification('Hello notification!')
        ui.label('Page content')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert 'Hello notification!' in response.text
    assert 'Page content' in response.text


async def test_button_icon_only(user: User):
    """Icon-only button should show icon name."""
    @ui.page('/')
    def page():
        ui.button(icon='thumb_up')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert '[Button: icon:thumb_up]' in response.text


async def test_x_nicegui_content_header(user: User):
    """Markdown response should include X-NiceGUI-Content header."""
    @ui.page('/')
    def page():
        ui.label('Hello')

    response = await user.http_client.get('/', headers=MARKDOWN_ACCEPT)
    assert response.headers.get('X-NiceGUI-Content') == 'page'
