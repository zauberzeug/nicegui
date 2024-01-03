from nicegui import ui
from nicegui.testing import Screen


def test_add_head_html(screen: Screen) -> None:
    ui.add_head_html(r'<style>.my-label {background: rgb(0, 0, 255)}</style>')
    ui.label('Label').classes('my-label')
    ui.button('Green', on_click=lambda: ui.add_head_html(r'<style>.my-label {background: rgb(0, 255, 0)}</style>'))

    screen.open('/')
    assert screen.find('Label').value_of_css_property('background-color') == 'rgba(0, 0, 255, 1)'

    screen.click('Green')
    screen.wait(0.5)
    assert screen.find('Label').value_of_css_property('background-color') == 'rgba(0, 255, 0, 1)'
