import csv
from io import BytesIO
from typing import Callable, Dict, Type, Union

import pytest
from fastapi import UploadFile
from fastapi.datastructures import Headers
from fastapi.responses import PlainTextResponse

from nicegui import app, events, ui
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


async def test_multi_user_navigation(create_user: Callable[[], User]) -> None:
    @ui.page('/')
    def page():
        ui.label('Main page')
        ui.button('go to other', on_click=lambda: ui.navigate.to('/other'))
        ui.button('forward', on_click=ui.navigate.forward)

    @ui.page('/other')
    def other():
        ui.label('Other page')
        ui.button('back', on_click=ui.navigate.back)

    userA = create_user()
    userB = create_user()

    await userA.open('/')
    await userA.should_see('Main page')

    await userB.open('/')
    await userB.should_see('Main page')

    userA.find('go to other').click()
    await userA.should_see('Other page')
    await userB.should_see('Main page')

    userA.find('back').click()
    await userA.should_see('Main page')
    await userB.should_see('Main page')

    userA.find('forward').click()
    await userA.should_see('Other page')
    await userB.should_see('Main page')


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


@pytest.mark.parametrize('kind', [ui.checkbox, ui.switch])
async def test_checkbox_and_switch(user: User, kind: Type) -> None:
    element = kind('my element', on_change=lambda e: ui.notify(f'Changed: {e.value}'))
    ui.label().bind_text_from(element, 'value', lambda v: 'enabled' if v else 'disabled')

    await user.open('/')
    await user.should_see('disabled')

    user.find('element').click()
    await user.should_see('enabled')
    await user.should_see('Changed: True')

    user.find('element').click()
    await user.should_see('disabled')
    await user.should_see('Changed: False')


@pytest.mark.parametrize('kind', [ui.input, ui.editor, ui.codemirror])
async def test_input(user: User, kind: Type) -> None:
    element = kind(on_change=lambda e: ui.notify(f'Changed: {e.value}'))
    ui.label().bind_text_from(element, 'value', lambda v: f'Value: {v}')

    await user.open('/')
    await user.should_see('Value: ')

    user.find(kind).type('Hello')
    await user.should_see('Value: Hello')
    await user.should_see('Changed: Hello')

    user.find(kind).type(' World')
    await user.should_see('Value: Hello World')
    await user.should_see('Changed: Hello World')

    user.find(kind).clear()
    user.find(kind).type('Test')
    await user.should_see('Value: Test')
    await user.should_see('Changed: Test')


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


async def test_combined_filter_parameters(user: User) -> None:
    ui.input(placeholder='x', value='y')

    await user.open('/')
    await user.should_see('x')
    await user.should_see('y')
    await user.should_not_see('x y')


async def test_typing(user: User) -> None:
    @ui.page('/')
    def page():
        ui.label('Hello!')
        ui.button('World!')

    await user.open('/')
    # NOTE we have not yet found a way to test the typing suggestions automatically
    # to test, hover over the variable and verify that your IDE inferres the correct type
    _ = user.find(kind=ui.label).elements  # Set[ui.label]
    _ = user.find(ui.label).elements  # Set[ui.label]
    _ = user.find('World').elements  # Set[ui.element]
    _ = user.find('Hello').elements  # Set[ui.element]
    _ = user.find('!').elements  # Set[ui.element]


async def test_select(user: User) -> None:
    ui.select(options=['A', 'B', 'C'], on_change=lambda e: ui.notify(f'Value: {e.value}'))

    await user.open('/')
    await user.should_not_see('A')
    await user.should_not_see('B')
    await user.should_not_see('C')
    user.find(ui.select).click()
    await user.should_see('B')
    await user.should_see('C')
    user.find('A').click()
    await user.should_see('Value: A')
    await user.should_see('A')
    await user.should_not_see('B')
    await user.should_not_see('C')


async def test_upload_table(user: User) -> None:
    def receive_file(e: events.UploadEventArguments) -> None:
        reader = csv.DictReader(e.content.read().decode('utf-8').splitlines())
        ui.table(columns=[{'name': h, 'label': h.capitalize(), 'field': h} for h in reader.fieldnames or []],
                 rows=list(reader))
    ui.upload(on_upload=receive_file)

    await user.open('/')
    upload = user.find(ui.upload).elements.pop()
    headers = Headers(raw=[(b'content-type', b'text/csv')])
    upload.handle_uploads([UploadFile(BytesIO(b'name,age\nAlice,30\nBob,28'), headers=headers)])

    table = user.find(ui.table).elements.pop()
    assert table.columns == [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    assert table.rows == [
        {'name': 'Alice', 'age': '30'},
        {'name': 'Bob', 'age': '28'},
    ]


@pytest.mark.parametrize('data', ['/data', b'Hello'])
async def test_download_file(user: User, data: Union[str, bytes]) -> None:
    @app.get('/data')
    def get_data() -> PlainTextResponse:
        return PlainTextResponse('Hello')

    @ui.page('/')
    def page():
        ui.button('Download', on_click=lambda: ui.download(data))

    await user.open('/')
    assert len(user.download.http_responses) == 0
    user.find('Download').click()
    response = await user.download.next()
    assert len(user.download.http_responses) == 1
    assert response.status_code == 200
    assert response.text == 'Hello'


async def test_validation(user: User) -> None:
    ui.input('Number', validation={'Not a number': lambda value: value.isnumeric()})

    await user.open('/')
    await user.should_not_see('Not a number')
    user.find(ui.input).type('some invalid entry')
    await user.should_see('Not a number')


async def test_trigger_autocomplete(user: User) -> None:
    ui.input(label='fruit', autocomplete=['apple', 'banana', 'cherry'])

    await user.open('/')
    await user.should_not_see('apple')
    user.find('fruit').type('a').trigger('keydown.tab')
    await user.should_see('apple')


async def test_seeing_invisible_elements(user: User) -> None:
    visible_label = ui.label('Visible')
    hidden_label = ui.label('Hidden')
    hidden_label.visible = False

    await user.open('/')
    with pytest.raises(AssertionError):
        await user.should_see('Hidden')
    with pytest.raises(AssertionError):
        await user.should_not_see('Visible')

    visible_label.visible = False
    hidden_label.visible = True
    await user.should_see('Hidden')
    await user.should_not_see('Visible')


async def test_finding_invisible_elements(user: User) -> None:
    button = ui.button('click me', on_click=lambda: ui.label('clicked'))
    button.visible = False

    await user.open('/')
    with pytest.raises(AssertionError):
        user.find('click me').click()

    button.visible = True
    user.find('click me').click()
    await user.should_see('clicked')


async def test_page_to_string_output_for_invisible_elements(user: User) -> None:
    ui.label('Visible')
    ui.label('Hidden').set_visibility(False)

    await user.open('/')
    output = str(user.current_layout)
    assert output == '''
q-layout
 q-page-container
  q-page
   div
    Label [text=Visible]
    Label [text=Hidden, visible=False]
'''.strip()

async def test_typing_to_disabled_element(user: User) -> None:
    initial_value = 'Hello first'
    given_new_input = 'Hello second'
    target = ui.input(value=initial_value)
    target.disable()

    await user.open('/')
    user.find(initial_value).type(given_new_input)

    assert target.value == initial_value
    await user.should_see(initial_value)
    await user.should_not_see(given_new_input)
