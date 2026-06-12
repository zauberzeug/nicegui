from typing import Literal

import pytest

from nicegui import app, ui
from nicegui.testing import Screen


@pytest.mark.parametrize('unocss', [None, 'mini', 'wind3', 'wind4'])
def test_dynamic_classes(screen: Screen, unocss: Literal['mini', 'wind3', 'wind4'] | None):
    app.config.unocss = unocss

    @ui.page('/')
    def page():
        ui.table(rows=[]).add_slot('no-data', '<div class="text-red-500">Red slot</div>')

        label = ui.label('Label')
        ui.button('Make green', on_click=lambda: ui.run_javascript(f'{label.html_id}.classList.add("text-green-500")'))
        ui.button('Make yellow', on_click=lambda: label.classes('text-yellow-500'))
        ui.button('Create blue', on_click=lambda: ui.label('Blue Label').classes('text-blue-500'))

    screen.open('/')
    screen.wait_for(lambda: screen.find('Red slot').value_of_css_property('color') == 'oklch(0.637 0.237 25.331)')

    screen.click('Make green')
    screen.wait_for(lambda: screen.find('Label').value_of_css_property('color') == 'oklch(0.723 0.219 149.579)')

    screen.click('Make yellow')
    screen.wait_for(lambda: screen.find('Label').value_of_css_property('color') == 'oklch(0.795 0.184 86.047)')

    screen.click('Create blue')
    screen.wait_for(lambda: screen.find('Blue Label').value_of_css_property('color') == 'oklch(0.623 0.214 259.815)')
