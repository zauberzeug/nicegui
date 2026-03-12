from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.testing import Screen


def test_time_input(screen: Screen):
    @ui.page('/')
    def page():
        time_input = ui.time_input('Time')
        ui.label().bind_text_from(time_input, 'value', lambda value: f'time: {value}')

    screen.open('/')
    screen.should_contain('Time')
    element = screen.selenium.find_element(By.XPATH, '//*[@aria-label="Time"]')
    element.send_keys('12:00')
    screen.should_contain('time: 12:00')

    screen.click('schedule')
    screen.should_contain('AM')
    screen.should_contain('PM')
