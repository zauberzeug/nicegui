import threading
from time import sleep

from nicegui import globals, ui


async def test_title(selenium):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('hello world')
    # start new thread
    thread = threading.Thread(target=ui.run, kwargs={'port': 3392, 'show': False, 'reload': False})
    thread.start()
    sleep(2)
    selenium.get('http://localhost:3392')
    assert "My Custom Title" in selenium.title
    print(globals)
    globals.server.should_exit = True
    thread.join()
