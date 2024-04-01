from nicegui import ui
from nicegui.page import page
from nicegui import app


@page('/')
def index():
    def increment():
        data = app.storage.user
        counter = data['counter'] = data.get('counter', 0) + 1
        button.text = f'Hello {counter} times!'

    ui.label("This data is unique per user")
    ui.html('<br>')
    button = ui.button('Hello, World!').on_click(increment)
    ui.link('Go to perClient', '/perClient')


@page('/perClient')
def per_client():
    def increment():
        data = app.storage.client
        counter = data['counter'] = data.get('counter', 0) + 1
        button.text = f'Hello {counter} times!'

    ui.label("This data is unique per browser tab - like in Streamlit")
    ui.html('<br>')
    button = ui.button('Hello, World!').on_click(increment)
    ui.link('Go to per user', '/')
    ui.link('Open in new tab', '/perClient', new_tab=True)


ui.run(storage_secret='my_secret')
