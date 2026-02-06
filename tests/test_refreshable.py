import asyncio

from nicegui import ui
from nicegui.testing import SharedScreen


def test_refreshable(shared_screen: SharedScreen) -> None:
    numbers = []

    @ui.refreshable
    def number_ui() -> None:
        ui.label('[' + ', '.join(str(n) for n in sorted(numbers)) + ']')

    @ui.page('/')
    def page():
        number_ui()
        ui.button('Refresh', on_click=number_ui.refresh)

    shared_screen.open('/')
    shared_screen.should_contain('[]')

    numbers.append(1)
    shared_screen.click('Refresh')
    shared_screen.should_contain('[1]')

    numbers.append(2)
    shared_screen.click('Refresh')
    shared_screen.should_contain('[1, 2]')

    numbers.clear()
    shared_screen.click('Refresh')
    shared_screen.should_contain('[]')


def test_async_refreshable(shared_screen: SharedScreen) -> None:
    numbers = []

    @ui.refreshable
    async def number_ui() -> None:
        await asyncio.sleep(0.1)
        ui.label('[' + ', '.join(str(n) for n in sorted(numbers)) + ']')

    @ui.page('/')
    async def index():
        with ui.column():  # this is necessary to reproduce bug #863
            await number_ui()
        ui.button('Refresh', on_click=number_ui.refresh)

    shared_screen.open('/')
    shared_screen.should_contain('[]')

    numbers.append(1)
    shared_screen.click('Refresh')
    shared_screen.should_contain('[1]')
    shared_screen.should_not_contain('[]')  # ensure bug #863 is fixed

    numbers.append(2)
    shared_screen.click('Refresh')
    shared_screen.should_contain('[1, 2]')
    shared_screen.should_not_contain('[]')

    numbers.clear()
    shared_screen.click('Refresh')
    shared_screen.should_contain('[]')


def test_multiple_targets(shared_screen: SharedScreen) -> None:
    count = 0

    class MyClass:

        def __init__(self, name: str) -> None:
            self.name = name
            self.state = 1

        @ui.refreshable_method
        def create_ui(self) -> None:
            nonlocal count
            count += 1
            ui.label(f'{self.name} = {self.state} ({count})')
            ui.button(f'increment {self.name}', on_click=self.increment)

        def increment(self) -> None:
            self.state += 1
            self.create_ui.refresh()

    @ui.page('/')
    def page():
        a = MyClass('A')
        a.create_ui()

        b = MyClass('B')
        b.create_ui()

    shared_screen.open('/')
    shared_screen.should_contain('A = 1 (1)')
    shared_screen.should_contain('B = 1 (2)')

    shared_screen.click('increment A')
    shared_screen.should_contain('A = 2 (3)')
    shared_screen.should_contain('B = 1 (2)')

    shared_screen.click('increment B')
    shared_screen.should_contain('A = 2 (3)')
    shared_screen.should_contain('B = 2 (4)')


def test_refresh_with_arguments(shared_screen: SharedScreen):
    count = 0

    @ui.refreshable
    def some_ui(value: int):
        nonlocal count
        count += 1
        ui.label(f'{count=}, {value=}')

    @ui.page('/')
    def page():
        some_ui(0)
        ui.button('refresh', on_click=some_ui.refresh)
        ui.button('refresh()', on_click=lambda: some_ui.refresh())  # pylint: disable=unnecessary-lambda
        ui.button('refresh(1)', on_click=lambda: some_ui.refresh(1))
        ui.button('refresh(2)', on_click=lambda: some_ui.refresh(2))
        ui.button('refresh(value=3)', on_click=lambda: some_ui.refresh(value=3))

    shared_screen.open('/')
    shared_screen.should_contain('count=1, value=0')

    shared_screen.click('refresh')
    shared_screen.should_contain('count=2, value=0')

    shared_screen.click('refresh()')
    shared_screen.should_contain('count=3, value=0')

    shared_screen.click('refresh(1)')
    shared_screen.should_contain('count=4, value=1')

    shared_screen.click('refresh(2)')
    shared_screen.should_contain('count=5, value=2')

    shared_screen.click('refresh(value=3)')
    shared_screen.wait(0.5)
    shared_screen.assert_py_logger(
        'ERROR', "'value' needs to be consistently passed to some_ui() either as positional or as keyword argument")


def test_refresh_deleted_element(shared_screen: SharedScreen):
    @ui.refreshable
    def some_ui():
        ui.label('some text')

    @ui.page('/')
    def page():
        with ui.card() as card:
            some_ui()

        ui.button('Refresh', on_click=some_ui.refresh)
        ui.button('Clear', on_click=card.clear)

        some_ui()

    shared_screen.open('/')
    shared_screen.should_contain('some text')

    shared_screen.click('Clear')
    shared_screen.click('Refresh')


def test_refresh_with_function_reference(shared_screen: SharedScreen):
    # https://github.com/zauberzeug/nicegui/issues/1283
    class Test:

        def __init__(self, name):
            self.name = name
            self.count = 0
            self.ui()

        @ui.refreshable_method
        def ui(self):
            ui.notify(f'Refreshing {self.name} ({self.count})')
            self.count += 1
            ui.button(self.name, on_click=self.ui.refresh)

    @ui.page('/')
    def page():
        Test('A')
        Test('B')

    shared_screen.open('/')
    shared_screen.should_contain('Refreshing A (0)')
    shared_screen.should_contain('Refreshing B (0)')
    shared_screen.click('A')
    shared_screen.should_contain('Refreshing A (1)')
    shared_screen.click('B')
    shared_screen.should_contain('Refreshing B (1)')


def test_refreshable_with_state(shared_screen: SharedScreen):
    @ui.refreshable
    def counter(title: str):
        count, set_count = ui.state(0)
        ui.label(f'{title}: {count}')
        ui.button(f'Increment {title}', on_click=lambda: set_count(count + 1))

    @ui.page('/')
    def page():
        counter('A')
        counter('B')

    shared_screen.open('/')
    shared_screen.should_contain('A: 0')
    shared_screen.should_contain('B: 0')

    shared_screen.click('Increment A')
    shared_screen.wait(0.5)
    shared_screen.should_contain('A: 1')
    shared_screen.should_contain('B: 0')

    shared_screen.click('Increment B')
    shared_screen.wait(0.5)
    shared_screen.should_contain('A: 1')
    shared_screen.should_contain('B: 1')


def test_refreshable_with_return_value(shared_screen: SharedScreen):
    @ui.refreshable
    def number_ui() -> int:
        ui.label('42')
        return 42

    @ui.page('/')
    def page():
        answer = number_ui()
        assert answer == 42

    shared_screen.open('/')
    shared_screen.should_contain('42')


def test_awaitable_refresh(shared_screen: SharedScreen):
    events = []

    @ui.refreshable
    async def content(number: int):
        events.append('refresh started')
        await asyncio.sleep(0.5)
        ui.label(f'1 / {number} = {1 / number}')
        events.append('refresh finished')

    async def update(number: int):
        events.append('update started')
        try:
            await content.refresh(number)
        except ZeroDivisionError:
            events.append('refresh failed')
            ui.label('error handled')
        events.append('update finished')

    @ui.page('/')
    async def page():
        await content(1)
        ui.button('Try 2', on_click=lambda: update(2))
        ui.button('Try 0', on_click=lambda: update(0))

    shared_screen.open('/')
    shared_screen.should_contain('1 / 1 = 1.0')
    assert events == ['refresh started', 'refresh finished']

    events.clear()
    shared_screen.click('Try 2')
    shared_screen.should_contain('1 / 2 = 0.5')
    assert events == ['update started', 'refresh started', 'refresh finished', 'update finished']

    events.clear()
    shared_screen.click('Try 0')
    shared_screen.should_contain('error handled')
    assert events == ['update started', 'refresh started', 'refresh failed', 'update finished']
