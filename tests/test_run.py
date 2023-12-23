import time

from nicegui import app, run, ui

from .screen import Screen


def test_io_bound(screen: Screen):
    def delayed_hello():
        time.sleep(1)
        ui.label('hello')

    switch = ui.switch('test interaction')
    app.on_startup(run.io_bound(delayed_hello))

    screen.open('/')
    screen.wait(0.1)
    screen.should_not_contain('hello')
    t = time.time()
    screen.click('test interaction')
    assert switch.value is True
    assert time.time() < t + 0.5, 'interacting with the switch should happen fast'
    screen.wait(1)
    screen.should_contain('hello')


def test_storage_inside_io_bound(screen: Screen):
    @ui.page('/')
    async def index():
        def count():
            app.storage.user['count'] = app.storage.user.get('count', 0) + 1
            ui.label(f'count is {app.storage.user["count"]}')
        await run.io_bound(count)

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    screen.should_contain('count is 1')
