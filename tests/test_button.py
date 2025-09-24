import pytest

from nicegui import ui
from nicegui.testing import Screen


@pytest.mark.parametrize('extra_classes', ['', '!bg-[#00ffff]'])
def test_quasar_colors(screen: Screen, extra_classes: str):
    b1 = b2 = b3 = b4 = b5 = None

    @ui.page('/')
    def page():
        nonlocal b1, b2, b3, b4, b5
        b1 = ui.button().classes(extra_classes)
        b2 = ui.button(color=None).classes(extra_classes)
        b3 = ui.button(color='red-5').classes(extra_classes)
        b4 = ui.button(color='red-500').classes(extra_classes)
        b5 = ui.button(color='#ff0000').classes(extra_classes)

    screen.open('/')

    if extra_classes == '!bg-[#00ffff]':
        expected = ['rgba(0, 255, 255, 1)'] * 5
    else:
        expected = [
            'rgba(88, 152, 212, 1)',
            'rgba(0, 0, 0, 0)',
            'rgba(239, 83, 80, 1)',
            'oklch(0.637 0.237 25.331)',
            'rgba(255, 0, 0, 1)',
        ]

    for b, exp in zip((b1, b2, b3, b4, b5), expected):
        assert screen.find_element(b).value_of_css_property('background-color') == exp


def test_enable_disable(screen: Screen):
    events = []

    @ui.page('/')
    def page():
        b = ui.button('Button', on_click=lambda: events.append(1))
        ui.button('Enable', on_click=b.enable)
        ui.button('Disable', on_click=b.disable)

    screen.open('/')
    screen.click('Button')
    assert events == [1]

    screen.click('Disable')
    screen.click('Button')
    assert events == [1]

    screen.click('Enable')
    screen.click('Button')
    assert events == [1, 1]
