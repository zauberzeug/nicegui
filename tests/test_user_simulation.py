from typing import Callable, Dict

import pytest
from fastapi.responses import PlainTextResponse

from nicegui import app, ui
from nicegui.testing import User

# pylint: disable=missing-function-docstring


async def test_auto_index_page(user: User) -> None:
    ui.label('Main page')

    await user.open('/')
    await user.should_see('Main page')


async def test_multiple_pages(create_user: Callable[[], User]) -> None:
    @ui.page('/')
    def index():
        ui.label('Main page')

    @ui.page('/other')
    def other():
        ui.label('Other page')

    userA = create_user()
    userB = create_user()

    await userA.open('/')
    await userA.should_see('Main page')
    await userA.should_not_see('Other page')

    await userB.open('/other')
    await userB.should_see('Other page')
    await userB.should_not_see('Main page')


async def test_source_element(user: User) -> None:
    @ui.page('/')
    def index():
        ui.image('https://via.placeholder.com/150')

    await user.open('/')
    await user.should_see('placeholder.com')


async def test_button_click(user: User) -> None:
    @ui.page('/')
    def index():
        ui.button('click me', on_click=lambda: ui.label('clicked'))

    await user.open('/')
    user.find('click me').click()
    await user.should_see('clicked')


async def test_assertion_raised_when_no_nicegui_page_is_returned(user: User) -> None:
    @app.get('/plain')
    def index() -> PlainTextResponse:
        return PlainTextResponse('Hello')

    with pytest.raises(ValueError):
        await user.open('/plain')


async def test_assertion_raised_when_element_not_found(user: User) -> None:
    @ui.page('/')
    def index():
        ui.label('Hello')

    await user.open('/')
    with pytest.raises(AssertionError):
        await user.should_see('World')


@pytest.mark.parametrize('storage_builder', [lambda: app.storage.browser, lambda: app.storage.user])
async def test_storage(user: User, storage_builder: Callable[[], Dict]) -> None:
    @ui.page('/')
    def page():
        storage = storage_builder()
        storage['count'] = storage.get('count', 0) + 1
        ui.label().bind_text_from(storage, 'count')

    await user.open('/')
    await user.should_see('1')

    await user.open('/')
    await user.should_see('2')


async def test_navigation(user: User) -> None:
    @ui.page('/')
    def page():
        ui.label('Main page')
        ui.button('go to other', on_click=lambda: ui.navigate.to('/other'))
        ui.button('forward', on_click=ui.navigate.forward)

    @ui.page('/other')
    def other():
        ui.label('Other page')
        ui.button('back', on_click=ui.navigate.back)

    await user.open('/')
    await user.should_see('Main page')
    user.find('go to other').click()
    await user.should_see('Other page')
    user.find('back').click()
    await user.should_see('Main page')
    user.find('forward').click()
    await user.should_see('Other page')


async def test_reload(user: User) -> None:
    @ui.page('/')
    def page():
        ui.input('test input')
        ui.button('reload', on_click=ui.navigate.reload)

    await user.open('/')
    await user.should_not_see('Hello')
    user.find('test input').type('Hello')
    await user.should_see('Hello')
    user.find('reload').click()
    await user.should_not_see('Hello')


async def test_notification(user: User) -> None:
    @ui.page('/')
    def page():
        ui.button('notify', on_click=lambda: ui.notify('Hello'))

    await user.open('/')
    user.find('notify').click()
    await user.should_see('Hello')


async def test_checkbox(user: User) -> None:
    checkbox = ui.checkbox('my checkbox', on_change=lambda e: ui.notify(f'Changed: {e.value}'))
    ui.label().bind_text_from(checkbox, 'value', lambda v: 'enabled' if v else 'disabled')

    await user.open('/')
    await user.should_see('disabled')
    user.find('checkbox').click()
    await user.should_see('enabled')
    await user.should_see('Changed: True')
    user.find('checkbox').click()
    await user.should_see('disabled')
    await user.should_see('Changed: False')


async def test_should_not_see(user: User) -> None:
    @ui.page('/')
    def page():
        ui.label('Hello')

    await user.open('/')
    await user.should_not_see('World')
    await user.should_see('Hello')


async def test_should_not_see_notification(user: User) -> None:
    @ui.page('/')
    def page():
        ui.button('Notify', on_click=lambda: ui.notification('Hello'))

    await user.open('/')
    await user.should_not_see('Hello')
    user.find('Notify').click()
    await user.should_see('Hello')
    with pytest.raises(AssertionError):
        await user.should_not_see('Hello')
    user.find('Hello').trigger('dismiss')
    await user.should_not_see('Hello')


async def test_trigger_event(user: User) -> None:
    @ui.page('/')
    def page():
        ui.input().on('keydown.enter', lambda: ui.notify('Enter pressed'))

    await user.open('/')
    user.find(ui.input).trigger('keydown.enter')
    await user.should_see('Enter pressed')


async def test_click_link(user: User) -> None:
    @ui.page('/')
    def page():
        ui.link('go to other', '/other')

    @ui.page('/other')
    def other():
        ui.label('Other page')

    await user.open('/')
    user.find('go to other').click()
    await user.should_see('Other page')


async def test_kind_content_marker_combinations(user: User) -> None:
    @ui.page('/')
    def page():
        ui.label('One')
        ui.button('Two')
        ui.button('Three').mark('three')

    await user.open('/')
    await user.should_see(content='One')
    await user.should_see(kind=ui.button)
    await user.should_see(kind=ui.button, content='Two')
    with pytest.raises(AssertionError):
        await user.should_see(kind=ui.button, content='One')
    await user.should_see(marker='three')
    await user.should_see(kind=ui.button, marker='three')
    with pytest.raises(AssertionError):
        await user.should_see(marker='three', content='One')


async def test_page_to_string_output_used_in_error_messages(user: User) -> None:
    @ui.page('/')
    def page():
        ui.label('Hello').mark('first')
        with ui.row():
            with ui.column():
                ui.button('World').mark('second')
                ui.icon('thumbs-up').mark('third')
        ui.avatar('star')
        ui.input('some input', placeholder='type here', value='typed')
        ui.markdown('''## Markdown
                    - A
                    - B
                    - C
                    ''')
        with ui.card().tight():
            ui.image('https://via.placeholder.com/150')

    await user.open('/')
    output = str(user.current_layout)
    assert output == '''
q-layout
 q-page-container
  q-page
   div
    Label [markers=first, text=Hello]
    Row
     Column
      Button [markers=second, label=World]
      Icon [markers=third, name=thumbs-up]
    Avatar [icon=star]
    Input [value=typed, label=some input, placeholder=type here, type=text]
    Markdown [content=## Markdown...]
    Card
     Image [src=https://via.placehol...]
'''.strip()
