from collections import namedtuple

from nicegui import ui
from nicegui.testing import SharedScreen

ColorCase = namedtuple('ColorCase', ['label', 'color', 'result'])

COLOR_CASES = [
    ColorCase('Quasar Red-5',     'red-5',   'rgba(239, 83, 80, 1)'),
    ColorCase('Tailwind Red-500', 'red-500', 'oklch(0.637 0.237 25.331)'),
    ColorCase('CSS Red',          '#ff0000', 'rgba(255, 0, 0, 1)'),
    ColorCase('CSS Cyan',         '#00ffff', 'rgba(0, 255, 255, 1)'),
]


def test_colors_via_color_parameter(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button()
        ui.button(color=None)
        for case in COLOR_CASES:
            ui.button(color=case.color)

    shared_screen.open('/')
    assert shared_screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'
    assert shared_screen.find_all_by_tag('button')[1].value_of_css_property('background-color') == 'rgba(0, 0, 0, 0)'
    for i, case in enumerate(COLOR_CASES, start=2):
        assert shared_screen.find_all_by_tag('button')[i].value_of_css_property('background-color') == case.result


def test_colors_via_setter(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        button = ui.button()
        button.bind_background_color_to(ui.label(), 'text', forward=lambda c: f'Button color: {c}')
        for case in COLOR_CASES:
            ui.button(f'Choose {case.label}', on_click=lambda c=case.color: button.set_background_color(c))

    shared_screen.open('/')
    shared_screen.should_contain('Button color: primary')
    assert shared_screen.find_by_tag('button').value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'

    for case in COLOR_CASES:
        shared_screen.click(f'Choose {case.label}')
        shared_screen.should_contain(f'Button color: {case.color}')
        assert shared_screen.find_by_tag('button').value_of_css_property('background-color') == case.result


def test_colors_via_binding(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        display = ui.label()
        button = ui.button()
        button.bind_background_color_to(display, 'text', forward=lambda c: f'Button color: {c}')
        toggle = ui.toggle({case.color: f'Choose {case.label}' for case in COLOR_CASES}, value=COLOR_CASES[0].color)
        button.bind_background_color_from(toggle, 'value')

    shared_screen.open('/')
    shared_screen.should_contain(f'Button color: {COLOR_CASES[0].color}')
    assert shared_screen.find_by_tag('button').value_of_css_property('background-color') == COLOR_CASES[0].result

    for case in COLOR_CASES:
        shared_screen.click(f'Choose {case.label}')
        shared_screen.should_contain(f'Button color: {case.color}')
        assert shared_screen.find_by_tag('button').value_of_css_property('background-color') == case.result


def test_enable_disable(shared_screen: SharedScreen):
    events = []

    @ui.page('/')
    def page():
        b = ui.button('Button', on_click=lambda: events.append(1))
        ui.button('Enable', on_click=b.enable)
        ui.button('Disable', on_click=b.disable)

    shared_screen.open('/')
    shared_screen.click('Button')
    assert events == [1]

    shared_screen.click('Disable')
    shared_screen.click('Button')
    assert events == [1]

    shared_screen.click('Enable')
    shared_screen.click('Button')
    assert events == [1, 1]
