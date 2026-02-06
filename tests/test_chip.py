from nicegui import ui
from nicegui.testing import SharedScreen


def test_removable_chip(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        chip = ui.chip('Chip', removable=True)
        ui.button('Set value to False', on_click=lambda: chip.set_value(False))

    shared_screen.open('/')
    shared_screen.should_contain('Chip')

    shared_screen.click('Set value to False')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Chip')


def test_selectable_chip(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        chip = ui.chip('Chip', selectable=True)
        ui.label().bind_text_from(chip, 'selected', lambda s: f'Selected: {s}')

    shared_screen.open('/')
    shared_screen.should_contain('Selected: False')

    shared_screen.click('Chip')
    shared_screen.should_contain('Selected: True')

    shared_screen.click('Chip')
    shared_screen.should_contain('Selected: False')
