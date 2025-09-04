import asyncio

from nicegui import ui
from nicegui.testing import Screen


def test_refreshable(screen: Screen) -> None:
    numbers = []

    @ui.refreshable
    def number_ui() -> None:
        ui.label('[' + ', '.join(str(n) for n in sorted(numbers)) + ']')

    @ui.page('/')
    def page():
        number_ui()
        ui.button('Refresh', on_click=number_ui.refresh)

    screen.open('/')
    screen.should_contain('[]')

    numbers.append(1)
    screen.click('Refresh')
    screen.should_contain('[1]')

    numbers.append(2)
    screen.click('Refresh')
    screen.should_contain('[1, 2]')

    numbers.clear()
    screen.click('Refresh')
    screen.should_contain('[]')


def test_async_refreshable(screen: Screen) -> None:
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

    screen.open('/')
    screen.should_contain('[]')

    numbers.append(1)
    screen.click('Refresh')
    screen.should_contain('[1]')
    screen.should_not_contain('[]')  # ensure bug #863 is fixed

    numbers.append(2)
    screen.click('Refresh')
    screen.should_contain('[1, 2]')
    screen.should_not_contain('[]')

    numbers.clear()
    screen.click('Refresh')
    screen.should_contain('[]')


def test_multiple_targets(screen: Screen) -> None:
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

    screen.open('/')
    screen.should_contain('A = 1 (1)')
    screen.should_contain('B = 1 (2)')

    screen.click('increment A')
    screen.should_contain('A = 2 (3)')
    screen.should_contain('B = 1 (2)')

    screen.click('increment B')
    screen.should_contain('A = 2 (3)')
    screen.should_contain('B = 2 (4)')


def test_refresh_with_arguments(screen: Screen):
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

    screen.open('/')
    screen.should_contain('count=1, value=0')

    screen.click('refresh')
    screen.should_contain('count=2, value=0')

    screen.click('refresh()')
    screen.should_contain('count=3, value=0')

    screen.click('refresh(1)')
    screen.should_contain('count=4, value=1')

    screen.click('refresh(2)')
    screen.should_contain('count=5, value=2')

    screen.click('refresh(value=3)')
    screen.wait(0.5)
    screen.assert_py_logger(
        'ERROR', "'value' needs to be consistently passed to some_ui() either as positional or as keyword argument")


def test_refresh_deleted_element(screen: Screen):
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

    screen.open('/')
    screen.should_contain('some text')

    screen.click('Clear')
    screen.click('Refresh')


def test_refresh_with_function_reference(screen: Screen):
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

    screen.open('/')
    screen.should_contain('Refreshing A (0)')
    screen.should_contain('Refreshing B (0)')
    screen.click('A')
    screen.should_contain('Refreshing A (1)')
    screen.click('B')
    screen.should_contain('Refreshing B (1)')


def test_refreshable_with_state(screen: Screen):
    @ui.refreshable
    def counter(title: str):
        count, set_count = ui.state(0)
        ui.label(f'{title}: {count}')
        ui.button(f'Increment {title}', on_click=lambda: set_count(count + 1))

    @ui.page('/')
    def page():
        counter('A')
        counter('B')

    screen.open('/')
    screen.should_contain('A: 0')
    screen.should_contain('B: 0')

    screen.click('Increment A')
    screen.wait(0.5)
    screen.should_contain('A: 1')
    screen.should_contain('B: 0')

    screen.click('Increment B')
    screen.wait(0.5)
    screen.should_contain('A: 1')
    screen.should_contain('B: 1')


def test_refreshable_with_return_value(screen: Screen):
    @ui.refreshable
    def number_ui() -> int:
        ui.label('42')
        return 42

    @ui.page('/')
    def page():
        answer = number_ui()
        assert answer == 42

    screen.open('/')
    screen.should_contain('42')
