from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import SharedScreen


def test_time_input(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        time_input = ui.time_input('Time')
        ui.label().bind_text_from(time_input, 'value', lambda value: f'time: {value}')

    shared_screen.open('/')
    shared_screen.should_contain('Time')
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Time"]')
    element.send_keys('12:00')
    shared_screen.should_contain('time: 12:00')

    shared_screen.click('schedule')
    shared_screen.should_contain('AM')
    shared_screen.should_contain('PM')
