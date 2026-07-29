from collections import namedtuple

from nicegui import ui
from nicegui.testing import Screen

ColorCase = namedtuple('ColorCase', ['label', 'color', 'result'])

COLOR_CASES = [
    ColorCase('Quasar Red-5',     'red-5',   'rgba(239, 83, 80, 1)'),
    ColorCase('Tailwind Red-500', 'red-500', 'oklch(0.637 0.237 25.331)'),
    ColorCase('CSS Red',          '#ff0000', 'rgba(255, 0, 0, 1)'),
]


def test_add_action(screen: Screen):
    clicked: list[str] = []

    @ui.page('/')
    def page():
        n = ui.notification('Decide', timeout=None)
        n.add_action(lambda: clicked.append('yes'), text='Yes', icon='check')
        n.add_action(lambda: clicked.append('maybe'), text='Maybe')
        n.add_action(lambda: clicked.append('no'), text='No')

    screen.open('/')
    screen.should_contain('Yes')
    screen.should_contain('check')
    screen.click('Maybe')
    screen.wait(0.5)
    assert clicked == ['maybe']
    screen.should_not_contain('Decide')


def test_no_dismiss(screen: Screen):
    clicked: list[str] = []

    @ui.page('/')
    def page():
        n = ui.notification('Decide', timeout=None)
        n.add_action(lambda: clicked.append('stay'), text='Stay', no_dismiss=True)

    screen.open('/')
    screen.click('Stay')
    screen.wait(0.5)
    assert clicked == ['stay']
    screen.should_contain('Decide')


def test_add_action_after_render(screen: Screen):
    # see https://github.com/zauberzeug/nicegui/pull/4819
    clicked: list[str] = []

    @ui.page('/')
    def page():
        n = ui.notification('Decide', timeout=None)
        ui.button('Add', on_click=lambda: n.add_action(lambda: clicked.append('late'), text='Late'))

    screen.open('/')
    screen.click('Add')
    screen.wait(0.5)
    assert len(screen.find_all_by_class('q-notification')) == 1
    screen.click('Late')
    screen.wait(0.5)
    assert clicked == ['late']


def test_action_colors(screen: Screen):
    @ui.page('/')
    def page():
        n = ui.notification('Decide', timeout=None)
        for case in COLOR_CASES:
            n.add_action(lambda: None, text=case.label, color=case.color)
        n.add_action(lambda: None, text='Bold class', color='red-500', **{'class': 'font-bold'})
        n.add_action(lambda: None, text='Bold style', color='#ff0000', style='font-weight: bold')

    screen.open('/')
    for case in COLOR_CASES:
        assert screen.find(case.label).value_of_css_property('color') == case.result
    assert screen.find('Bold class').value_of_css_property('color') == 'oklch(0.637 0.237 25.331)'
    assert screen.find('Bold class').value_of_css_property('font-weight') == '700'
    assert screen.find('Bold style').value_of_css_property('color') == 'rgba(255, 0, 0, 1)'
    assert screen.find('Bold style').value_of_css_property('font-weight') == '700'
