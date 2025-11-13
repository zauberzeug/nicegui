from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen, User


def test_date_input(screen: Screen):
    @ui.page('/')
    def page():
        date_input = ui.date_input('Date')
        ui.label().bind_text_from(date_input, 'value', lambda value: f'date: {value}')

    screen.open('/')
    screen.should_contain('Date')
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Date"]')
    element.send_keys('2025-01-01')
    screen.should_contain('date: 2025-01-01')

    screen.click('edit_calendar')
    screen.should_contain('Sat')
    screen.should_contain('Jan 1')


@pytest.mark.parametrize('range_input', [False, True])
async def test_date_conversion(user: User, range_input: bool):
    date_input = None

    @ui.page('/')
    def page():
        nonlocal date_input
        date_input = ui.date_input('Date', range_input=range_input)

    await user.open('/')
    await user.should_see('Date')

    pairs: list[tuple[str | None, str | dict[str, str] | None]] = [
        ('2025-01-01', '2025-01-01'),
        ('foo', 'foo'),
        ('', ''),
        (None, None),
    ]
    if range_input:
        pairs.append(('2025-01-01 - 2025-01-02', {'from': '2025-01-01', 'to': '2025-01-02'}))

    assert isinstance(date_input, ui.date_input)
    for input_value, picker_value in pairs:
        date_input.value = input_value
        assert date_input.picker.value == picker_value

        date_input.picker.value = picker_value
        assert date_input.value == input_value
