from __future__ import annotations

import asyncio
import json

import pytest

from nicegui import Client, app, ui
from nicegui.testing import Screen


def test_prerender_with_run_javascript(screen: Screen, event_log: EventLog) -> None:
    app.on_connect(lambda client: event_log.append(f'connect: {client.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/answer', kind='prerender')

    @ui.page('/answer')
    async def answer() -> None:
        result = await ui.run_javascript('1 + 41')
        event_log.append(f'answer: {result}')

    screen.open('/')
    event_log.wait_for('connect: /')
    event_log.wait_for('connect: /answer')
    event_log.wait_for('answer: 42')


def test_prerender_with_client_connected(screen: Screen, event_log: EventLog) -> None:
    app.on_connect(lambda client: event_log.append(f'connect: {client.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/subpage', kind='prerender')

    @ui.page('/subpage')
    async def subpage() -> None:
        await ui.context.client.connected()
        event_log.append('subpage: connected')

    screen.open('/')
    event_log.wait_for('connect: /')
    event_log.wait_for('connect: /subpage')
    event_log.wait_for('subpage: connected')


def test_prerender_with_timer(screen: Screen, event_log: EventLog) -> None:
    app.on_connect(lambda client: event_log.append(f'connect: {client.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/timer', kind='prerender')

    @ui.page('/timer')
    async def timer() -> None:
        await ui.context.client.connected()
        ui.timer(0.1, lambda: event_log.append('timer: running'), once=True)

    screen.open('/')
    event_log.wait_for('connect: /')
    event_log.wait_for('connect: /timer')
    event_log.wait_for('timer: running')


def test_prerender_with_long_page_build(screen: Screen, event_log: EventLog) -> None:
    app.on_connect(lambda client: event_log.append(f'connect: {client.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/longbuild', kind='prerender')

    @ui.page('/longbuild', response_timeout=3)
    async def longbuild() -> None:
        await asyncio.sleep(2)
        event_log.append('longbuild: done')

    screen.open('/')
    event_log.wait_for('connect: /')
    event_log.wait_for('longbuild: done')
    event_log.wait_for('connect: /longbuild')
    assert event_log.items.index('longbuild: done') < event_log.items.index('connect: /longbuild')


def test_prefetch_connects_after_navigation(screen: Screen, event_log: EventLog) -> None:
    app.on_connect(lambda client: event_log.append(f'connect: {client.page.path}'))

    @ui.page('/')
    def root() -> None:
        add_speculation_rule('/answer', kind='prefetch')
        ui.link('answer', '/answer')

    @ui.page('/answer')
    async def answer() -> None:
        event_log.append('answer: called')
        result = await ui.run_javascript('41 + 1')
        event_log.append(f'answer: {result}')
        ui.label('all done')

    screen.open('/')
    event_log.wait_for('connect: /')
    screen.wait(1)
    assert event_log.items == ['answer: called', 'connect: /']

    screen.click('answer')
    event_log.wait_for('answer: 42')
    assert event_log.items == ['answer: called', 'connect: /', 'connect: /answer', 'answer: 42'], \
        'answer() should not re-evaluate despite small run_javascript timeout because in prefetch the page response timeout is used'
    screen.should_contain('all done')
    event_log.items.clear()

    screen.open('/')
    event_log.wait_for('answer: called')
    Client.prune_instances(client_age_threshold=0)
    assert event_log.items == ['answer: called', 'connect: /']

    screen.click('answer')
    event_log.wait_for('connect: /answer')
    event_log.wait_for('answer: 42')
    assert event_log.items == ['answer: called', 'connect: /', 'answer: called', 'connect: /answer', 'answer: 42'], \
        'answer() should re-evaluate after prefetch client was pruned'
    screen.should_contain('all done')


def add_speculation_rule(url: str, *, kind: str = 'prerender') -> None:
    rules = {kind: [{'source': 'list', 'urls': [url], 'eagerness': 'eager'}]}
    script = '<script type="speculationrules">' + json.dumps(rules) + '</script>'
    ui.add_head_html(script)


class EventLog:
    def __init__(self, screen: Screen) -> None:
        self.items: list[str] = []
        self._screen = screen

    def append(self, entry: str) -> None:
        self.items.append(entry)

    def wait_for(self, entry: str) -> None:
        try:
            self._screen.wait_for(lambda: entry in self.items)
        except AssertionError as e:
            raise AssertionError(f'{entry} not found in {self.items}') from e


@pytest.fixture(name='event_log')
def _event_log(screen: Screen) -> EventLog:
    return EventLog(screen)
