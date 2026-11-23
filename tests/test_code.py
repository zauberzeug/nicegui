from nicegui import ui
from nicegui.testing import Screen


def test_code(screen: Screen):
    @ui.page('/')
    def page():
        ui.code('x = 42')

    screen.open('/')
    assert screen.find_by_class('n').text == 'x'
    assert screen.find_by_class('o').text == '='
    assert screen.find_by_class('mi').text == '42'


def test_embedded_code_fences(screen: Screen):
    content = '```python\nprint(42)\n```\n**After**'
    updated_content = content.replace('```', '````')

    @ui.page('/')
    def page():
        code = ui.code(content, language='markdown')
        ui.button('Update', on_click=lambda: code.set_content(updated_content))

    screen.open('/')
    assert screen.find_by_tag('code').text == content

    screen.click('Update')
    screen.wait_for(lambda: screen.find_by_tag('code').text == updated_content)
