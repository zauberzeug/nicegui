from nicegui import ui
from nicegui.testing import Screen


def test_removable_chip(screen: Screen):
    chip = ui.chip('Chip', removable=True)

    screen.open('/')
    screen.should_contain('Chip')

    chip.set_value(False)
    screen.wait(0.5)
    screen.should_not_contain('Chip')


def test_selectable_chip(screen: Screen):
    chip = ui.chip('Chip', selectable=True)
    ui.label().bind_text_from(chip, 'selected', lambda s: f'Selected: {s}')

    screen.open('/')
    screen.should_contain('Selected: False')

    screen.click('Chip')
    screen.should_contain('Selected: True')

    screen.click('Chip')
    screen.should_contain('Selected: False')
