import asyncio
import json

import pytest

from nicegui import app, ui
from nicegui.testing import Screen


class EventLog:
    def __init__(self, screen: Screen) -> None:
        self.items: list[str] = []
        self._screen = screen

    def append(self, entry: str) -> None:
        self.items.append(entry)

    def wait_for(self, entry: str) -> None:
        self._screen.wait_for(lambda: entry in self.items)


def test_prerender_with_run_javascript(screen: Screen, event_log: EventLog) -> None:
    app.on_connect(lambda c: event_log.append(f'connect:{c.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/test', kind='prerender')

    @ui.page('/test')
    async def test() -> None:
        result = await ui.run_javascript('1 + 41')
        event_log.append(f'js:{result}')

    screen.open('/')
    event_log.wait_for('connect:/test')
    event_log.wait_for('js:42')


def test_prerender_client_connected(screen: Screen, event_log: EventLog) -> None:
    app.on_connect(lambda c: event_log.append(f'connect:{c.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/connected', kind='prerender')

    @ui.page('/connected')
    async def connected() -> None:
        await ui.context.client.connected()
        event_log.append('connected')

    screen.open('/')
    event_log.wait_for('connect:/connected')
    event_log.wait_for('connected')


def test_prerender_timer(screen: Screen, event_log: EventLog) -> None:
    app.on_connect(lambda c: event_log.append(f'connect:{c.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/timer', kind='prerender')

    @ui.page('/timer')
    async def timer() -> None:
        await ui.context.client.connected()
        ui.timer(0.1, lambda: event_log.append('TIMER'), once=True)

    screen.open('/')
    event_log.wait_for('connect:/timer')
    event_log.wait_for('TIMER')


def test_prerender_long_page_build(screen: Screen, event_log: EventLog) -> None:

    app.on_connect(lambda c: event_log.append(f'connect:{c.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/longbuild', kind='prerender')

    @ui.page('/longbuild')
    async def longbuild() -> None:
        await asyncio.sleep(4)
        event_log.append('longbuild done')

    screen.open('/')
    event_log.wait_for('connect:/longbuild')
    event_log.wait_for('longbuild done')


def add_speculation_rule(url: str, *, kind: str = 'prerender', eagerness: str = 'eager') -> None:
    rules = {
        kind: [
            {
                'source': 'list',
                'urls': [url],
                'eagerness': eagerness,
            }
        ]
    }
    script = '<script type="speculationrules">' + json.dumps(rules) + '</script>'
    ui.add_head_html(script)


@pytest.fixture(name='event_log')
def _event_log(screen: Screen) -> EventLog:
    return EventLog(screen)
