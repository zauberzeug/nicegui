# This is a demo showing per-session (effectively per browser tab) user authentication w/o the need for cookies
# and with "safe logout" when the browser tab is closed.

from nicegui import ui
from nicegui.page import page
from nicegui import app
from nicegui.single_page import SinglePageRouter


@page('/', title="Welcome!")
def index():
    username = app.storage.session.get('username', '')
    if username == '':  # redirect to login page
        ui.navigate.to('/login')
        return
    ui.label(f'Welcome back {username}!').classes('text-2xl')
    ui.label('Dolor sit amet, consectetur adipiscing elit.').classes('text-lg')
    ui.link('About', '/about')
    ui.link('Logout', '/logout')


@page('/login', title="Login")
def login_page():
    def login():
        fake_pw_dict = {'user1': 'pw1',
                        'user2': 'pw2',
                        'user3': 'pw3'}

        if app.storage.session['username'] in fake_pw_dict and app.storage.session['password'] == fake_pw_dict[
            app.storage.session['username']]:
            ui.navigate.to("/")
            return True
        return False

    def handle_login():
        feedback.set_text('Login successful' if login() else 'Login failed')

    user = ui.input('Username').on('keydown.enter', handle_login)
    user.bind_value(app.storage.session, "username")
    password = ui.input('Password', password=True).on('keydown.enter', handle_login)
    password.bind_value(app.storage.session, "password")
    feedback = ui.label('')
    ui.button('Login', on_click=handle_login)
    ui.link('About', '/about')
    ui.html("<small>Psst... try user1/pw1, user2/pw2, user3/pw3</small>")


@page('/logout', title="Logout")
def logout():
    app.storage.session['username'] = ''
    app.storage.session['password'] = ''
    ui.label('You have been logged out').classes('text-2xl')
    ui.navigate.to('/login')


@page('/about', title="About")
def about():
    ui.label("A basic authentication with a persistent session connection")


sp = SinglePageRouter("/")  # setup a single page router at / (and all sub-paths)
ui.run(show=False)
