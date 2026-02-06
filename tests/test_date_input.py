import pytest
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import SharedScreen, User


def test_date_input(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        date_input = ui.date_input('Date')
        ui.label().bind_text_from(date_input, 'value', lambda value: f'date: {value}')

    shared_screen.open('/')
    shared_screen.should_contain('Date')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Date"]')
    element.send_keys('2025-01-01')
    shared_screen.should_contain('date: 2025-01-01')

    shared_screen.click('edit_calendar')
    shared_screen.should_contain('Sat')
    shared_screen.should_contain('Jan 1')


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
