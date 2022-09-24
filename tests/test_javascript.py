from datetime import datetime

from nicegui import ui

from .user import User


def test_executing_javascript(user: User):
    async def set_title():
        await ui.run_javascript('document.title = "A New Title"')
    ui.button('change title', on_click=set_title)

    user.open('/')
    user.selenium.title == 'NiceGUI'
    user.click('change title')
    user.selenium.title == 'A New Title'
    user.selenium.title != 'NiceGUI'


def test_retrieving_content_from_javascript(user: User):
    async def write_time():
        response = await ui.await_javascript('Date.now()')
        ui.label(f'Browser time: {response}')

    ui.button('write time', on_click=write_time)

    user.open('/')
    user.click('write time')
    label = user.find('Browser time').text
    jstime = datetime.fromtimestamp(int(label.split(': ')[1])/1000)
    assert abs((datetime.now() - jstime).total_seconds()) < 1, f'{jstime} should be close to now'
