import json

from nicegui import ui
from nicegui.testing import Screen


def test_prerender_with_run_javascript(screen: Screen) -> None:
    @ui.page('/')
    def root() -> None:
        add_speculation_prerender('/test')
        ui.link('test', '/test')

    @ui.page('/test')
    async def test() -> None:
        result = await ui.run_javascript('1 + 41')
        ui.label(result)

    screen.open('/')
    screen.wait(0.5)
    screen.click('test')
    screen.should_contain('42')
    screen.should_not_contain('500:')


def test_prerender_client_connected(screen: Screen) -> None:
    @ui.page('/')
    def root() -> None:
        add_speculation_prerender('/connected')
        ui.link('connected', '/connected')

    @ui.page('/connected')
    async def connected() -> None:
        await ui.context.client.connected()
        ui.label('connected')

    screen.open('/')
    screen.wait(0.5)
    screen.click('connected')
    screen.should_contain('connected')


def test_prerender_timer(screen: Screen) -> None:
    @ui.page('/')
    def root() -> None:
        add_speculation_prerender('/timer')
        ui.link('timer', '/timer')

    @ui.page('/timer')
    def timer() -> None:
        ui.label('page')
        ui.timer(0.1, lambda: ui.label('TIMER'), once=True)

    screen.open('/')
    screen.wait(0.5)
    screen.click('timer')
    screen.should_contain('TIMER')


def test_prerender_long_page_build(screen: Screen) -> None:
    import asyncio

    @ui.page('/')
    def root() -> None:
        add_speculation_prerender('/longbuild')
        ui.link('longbuild', '/longbuild')

    @ui.page('/longbuild')
    async def longbuild() -> None:
        await asyncio.sleep(4)
        ui.label('after longbuild')

    screen.open('/')
    screen.wait(0.5)
    screen.click('longbuild')
    screen.should_contain('after longbuild')
    screen.should_not_contain('500:')


def add_speculation_prerender(url: str, *, eagerness: str = 'eager') -> None:
    rules = {
        'prerender': [
            {
                'source': 'list',
                'urls': [url],
                'eagerness': eagerness,
            }
        ]
    }
    script = '<script type="speculationrules">' + json.dumps(rules) + '</script>'
    ui.add_head_html(script)
