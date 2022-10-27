import asyncio

from nicegui import ui

from .screen import Screen


class Counter:
    value = 0

    def increment(self):
        self.value += 1


def test_timer(screen: Screen):
    counter = Counter()
    ui.timer(0.1, counter.increment)

    assert counter.value == 0, 'count is initially zero'
    screen.wait(0.5)
    assert counter.value == 0, 'timer is not running'

    screen.start_server()
    screen.wait(0.5)
    assert counter.value > 0, 'timer is running after starting the server'


def test_timer_on_private_page(screen: Screen):
    counter = Counter()

    @ui.page('/')
    def page():
        ui.timer(0.1, counter.increment)

    assert counter.value == 0, 'count is initially zero'
    screen.start_server()
    screen.wait(0.5)
    assert counter.value == 0, 'timer is not running even after starting the server'

    screen.open('/')
    screen.wait(0.5)
    assert counter.value > 0, 'timer is running after opening the page'

    screen.close()
    count = counter.value
    screen.wait(0.5)
    assert counter.value == count, 'timer is not running anymore after closing the page'
