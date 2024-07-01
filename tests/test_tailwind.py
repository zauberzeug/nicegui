from nicegui import Tailwind, ui
from nicegui.testing import SeleniumScreen


def test_tailwind_builder(screen: SeleniumScreen):
    ui.label('A').tailwind('bg-red-500', 'text-white')

    screen.open('/')
    assert screen.find('A').get_attribute('class') == 'bg-red-500 text-white'


def test_tailwind_call(screen: SeleniumScreen):
    ui.label('A').tailwind('bg-red-500 text-white')

    screen.open('/')
    assert screen.find('A').get_attribute('class') == 'bg-red-500 text-white'


def test_tailwind_apply(screen: SeleniumScreen):
    style = Tailwind().background_color('red-500').text_color('white')

    ui.label('A').tailwind(style)
    b = ui.label('B')
    style.apply(b)

    screen.open('/')
    assert screen.find('A').get_attribute('class') == 'bg-red-500 text-white'
    assert screen.find('B').get_attribute('class') == 'bg-red-500 text-white'


def test_empty_values(nicegui_reset_globals):
    label = ui.label('A')
    label.tailwind.border_width('')
    assert 'border' in label._classes
