from nicegui import ui
from selenium.webdriver.common.by import By


async def test_title(server, selenium):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('some content')
    server.start()
    selenium.get(server.base_url)
    assert 'My Custom Title' in selenium.title


async def test_route_with_custom_path(server, selenium):
    @ui.page('/test_route')
    def page():
        ui.label('page with custom path')
    server.start()
    selenium.get(server.base_url + '/test_route')
    element = selenium.find_element(By.XPATH, '//*[contains(text(),"custom path")]')
    assert element.text == 'page with custom path'
