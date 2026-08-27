import asyncio
from collections import namedtuple

from nicegui import background_tasks, ui
from nicegui.testing import Screen, User

ColorCase = namedtuple('ColorCase', ['label', 'color', 'result'])

COLOR_CASES = [
    ColorCase('Quasar Red-5',     'red-5',   'rgba(239, 83, 80, 1)'),
    ColorCase('Tailwind Red-500', 'red-500', 'oklch(0.637 0.237 25.331)'),
    ColorCase('CSS Red',          '#ff0000', 'rgba(255, 0, 0, 1)'),
    ColorCase('CSS Cyan',         '#00ffff', 'rgba(0, 255, 255, 1)'),
]


def test_colors_via_color_parameter(screen: Screen):
    @ui.page('/')
    def page():
        ui.button()
        ui.button(color=None)
        for case in COLOR_CASES:
            ui.button(color=case.color)

    screen.open('/')
    assert screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'
    assert screen.find_all_by_tag('button')[1].value_of_css_property('background-color') == 'rgba(0, 0, 0, 0)'
    for i, case in enumerate(COLOR_CASES, start=2):
        assert screen.find_all_by_tag('button')[i].value_of_css_property('background-color') == case.result


def test_colors_via_setter(screen: Screen):
    @ui.page('/')
    def page():
        button = ui.button()
        button.bind_background_color_to(ui.label(), 'text', forward=lambda c: f'Button color: {c}')
        for case in COLOR_CASES:
            ui.button(f'Choose {case.label}', on_click=lambda c=case.color: button.set_background_color(c))

    screen.open('/')
    screen.should_contain('Button color: primary')
    assert screen.find_by_tag('button').value_of_css_property('background-color') == 'rgba(88, 152, 212, 1)'

    for case in COLOR_CASES:
        screen.click(f'Choose {case.label}')
        screen.should_contain(f'Button color: {case.color}')
        assert screen.find_by_tag('button').value_of_css_property('background-color') == case.result


def test_colors_via_binding(screen: Screen):
    @ui.page('/')
    def page():
        display = ui.label()
        button = ui.button()
        button.bind_background_color_to(display, 'text', forward=lambda c: f'Button color: {c}')
        toggle = ui.toggle({case.color: f'Choose {case.label}' for case in COLOR_CASES}, value=COLOR_CASES[0].color)
        button.bind_background_color_from(toggle, 'value')

    screen.open('/')
    screen.should_contain(f'Button color: {COLOR_CASES[0].color}')
    assert screen.find_by_tag('button').value_of_css_property('background-color') == COLOR_CASES[0].result

    for case in COLOR_CASES:
        screen.click(f'Choose {case.label}')
        screen.should_contain(f'Button color: {case.color}')
        assert screen.find_by_tag('button').value_of_css_property('background-color') == case.result


def test_enable_disable(screen: Screen):
    events = []

    @ui.page('/')
    def page():
        b = ui.button('Button', on_click=lambda: events.append(1))
        ui.button('Enable', on_click=b.enable)
        ui.button('Disable', on_click=b.disable)

    screen.open('/')
    screen.click('Button')
    assert events == [1]

    screen.click('Disable')
    screen.click('Button')
    assert events == [1]

    screen.click('Enable')
    screen.wait_for(screen.find_by_tag('button').is_enabled)
    screen.click('Button')
    assert events == [1, 1]


async def test_clicked_is_cancelled_when_client_is_deleted(user: User):
    """The task awaiting a button click must be cancelled when the client is deleted, e.g. after a disconnect."""
    results = []

    @ui.page('/')
    def page():
        button = ui.button('Click me')

        async def wait_for_click() -> None:
            await button.clicked()
            results.append('clicked')  # must not run: the button was never clicked

        ui.button('Wait', on_click=wait_for_click)

    client = await user.open('/')
    user.find('Wait').click()
    await asyncio.sleep(0.1)  # let the handler start awaiting the click
    client.delete()
    await asyncio.sleep(0.1)  # let the cancellation take effect
    assert not results, 'code after clicked() must not run for a click that never happened'
    assert not any('wait_for_click' in task.get_name() for task in background_tasks.running_tasks), \
        'the awaiting task should be cancelled, not leaked'


async def test_clicked_is_cancelled_when_button_is_deleted(user: User):
    """The task awaiting a button click must be cancelled when the button itself is removed from the page."""
    results = []

    @ui.page('/')
    def page():
        with ui.card() as card:
            button = ui.button('Click me')

        async def wait_for_click() -> None:
            await button.clicked()
            results.append('clicked')  # must not run: the button was never clicked

        ui.button('Wait', on_click=wait_for_click)
        ui.button('Clear', on_click=card.clear)

    await user.open('/')
    user.find('Wait').click()
    await asyncio.sleep(0.1)  # let the handler start awaiting the click
    user.find('Clear').click()
    await asyncio.sleep(0.1)  # let the cancellation take effect
    assert not results, 'code after clicked() must not run for a click that never happened'
    assert not any('wait_for_click' in task.get_name() for task in background_tasks.running_tasks), \
        'the awaiting task should be cancelled, not leaked'


async def test_awaiting_an_already_deleted_button_is_cancelled(user: User):
    """Awaiting a button which has already been deleted must cancel immediately instead of waiting forever."""
    results = []

    @ui.page('/')
    def page():
        button = ui.button('Click me')
        button.delete()

        async def wait_for_click() -> None:
            await button.clicked()
            results.append('clicked')  # must not run: the button was never clicked

        ui.button('Wait', on_click=wait_for_click)

    await user.open('/')
    user.find('Wait').click()
    await asyncio.sleep(0.1)  # let the cancellation take effect
    assert not results, 'code after clicked() must not run for a click that never happened'
    assert not any('wait_for_click' in task.get_name() for task in background_tasks.running_tasks), \
        'the awaiting task should be cancelled, not leaked'


async def test_click_that_deletes_the_button_is_still_delivered(user: User):
    """A real click must resume the awaiting task even if an async click handler deletes the button."""
    results = []

    @ui.page('/')
    def page():
        with ui.card() as card:
            async def clear() -> None:
                card.clear()
            button = ui.button('Click me', on_click=clear)

        async def wait_for_click() -> None:
            await button.clicked()
            results.append('clicked')

        ui.button('Wait', on_click=wait_for_click)

    await user.open('/')
    user.find('Wait').click()
    await asyncio.sleep(0.1)  # let the handler start awaiting the click
    user.find('Click me').click()
    await asyncio.sleep(0.1)  # let the async on_click handler delete the button
    assert results == ['clicked'], 'a real click must not be swallowed by the deletion it triggers'
