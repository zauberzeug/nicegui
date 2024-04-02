# This is a demo showing per-session (effectively per browser tab) user authentication w/o the need for cookies
# and with "safe logout" when the browser tab is closed.
# TODO Note that due to loosing the WS connection between page changes and thus the "session" this demo does not work
# yet.

from nicegui import ui
from nicegui.page import page
from nicegui import app
from nicegui.single_page import SinglePageRouter


def login():
    fake_pw_dict = {'user1': 'pw1',
                    'user2': 'pw2',
                    'user3': 'pw3'}

    if app.storage.session['username'] in fake_pw_dict and app.storage.session['password'] == fake_pw_dict[
            app.storage.session['username']]:
        ui.navigate.to("/secret_content")
        return True
    return False


@page('/')
def index():
    def handle_login():
        feedback.set_text('Login successful' if login() else 'Login failed')

    user = ui.input('Username').on('keydown.enter', handle_login)
    user.bind_value(app.storage.session, "username")
    password = ui.input('Password', password=True).on('keydown.enter', handle_login)
    password.bind_value(app.storage.session, "password")
    feedback = ui.label('')
    ui.button('Login', on_click=handle_login)
    ui.link('Logout', '/secret_content')  # TODO remove me


@page('/secret_content', title='Secret Content')
def secret_content():
    ui.label(f'This is secret content, welcome {app.storage.session.get("username", "unknown user")}!')


if __name__ in {"__main__", "__mp_main__"}:
    sp = SinglePageRouter("/")
    ui.run(show=False)
