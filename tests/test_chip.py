from nicegui import ui
from nicegui.testing import Screen, User


def test_removable_chip(screen: Screen):
    @ui.page('/')
    def page():
        chip = ui.chip('Chip', removable=True)
        ui.button('Set value to False', on_click=lambda: chip.set_value(False))

    screen.open('/')
    screen.should_contain('Chip')

    screen.click('Set value to False')
    screen.wait(0.5)
    screen.should_not_contain('Chip')


def test_selectable_chip(screen: Screen):
    @ui.page('/')
    def page():
        chip = ui.chip('Chip', selectable=True)
        ui.label().bind_text_from(chip, 'selected', lambda s: f'Selected: {s}')

    screen.open('/')
    screen.should_contain('Selected: False')

    screen.click('Chip')
    screen.should_contain('Selected: True')

    screen.click('Chip')
    screen.should_contain('Selected: False')


async def test_selectable_chip_props(user: User):
    chips: list[ui.chip] = []

    @ui.page('/')
    def page():
        chips.append(ui.chip('x', selectable=True))

    await user.open('/')
    assert 'selected' in chips[0]._props
    assert 'selectable' not in chips[0]._props
