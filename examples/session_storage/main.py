# This is a demo showing per-session (effectively per browser tab) user authentication w/o the need for cookies
# and with "safe logout" when the browser tab is closed.
from pydantic import BaseModel, Field

from nicegui import ui
from nicegui.page import page
from nicegui import app
from nicegui.single_page import SinglePageRouter


class UserData(BaseModel):  # Example for per-session user data
    username: str = Field('', description='The username')
    password: str = Field('', description='The password')
    logged_in: bool = Field(False, description='Whether the user is logged in')

    def log_out(self):  # Clears the user data, e.g. after logout
        self.username = ''
        self.password = ''
        self.logged_in: bool = False

    @staticmethod
    def get_current() -> "UserData":  # Returns the UserData instance for the current session ("browser tab")
        return app.storage.session["userData"]


def login() -> bool:  # Fake login function. Evaluate the user data updates the logged_in flag on success
    fake_pw_dict = {'user1': 'pw1',
                    'user2': 'pw2',
                    'user3': 'pw3'}
    user_data = UserData.get_current()
    if user_data.username in fake_pw_dict and user_data.password == fake_pw_dict[user_data.username]:
        user_data.logged_in = True
        user_data.password = ''  # Clear the password
        ui.navigate.to(index_page)
        return True
    return False


@page('/', title="Welcome!")
def index_page():
    user_data = UserData.get_current()
    if not user_data.logged_in:  # redirect to login page
        ui.navigate.to('/login')
        return
    ui.label(f'Welcome back {user_data.username}!').classes('text-2xl')
    ui.label('Dolor sit amet, consectetur adipiscing elit.').classes('text-lg')
    ui.link('About', about_page)
    ui.link('Logout', logout_page)


@page('/login', title="Login")
def login_page():
    def handle_login():
        feedback.set_text('Login successful' if login() else 'Login failed')

    user_data = UserData.get_current()
    user = ui.input('Username').on('keydown.enter', handle_login)
    user.bind_value(user_data, 'username')
    password = ui.input('Password', password=True).on('keydown.enter', handle_login)
    password.bind_value(user_data, 'password')
    feedback = ui.label('')
    ui.button('Login', on_click=handle_login)
    ui.link('About', about_page)
    ui.html("<small>Psst... try user1/pw1, user2/pw2, user3/pw3</small>")


@page('/logout', title="Logout")
def logout_page():
    UserData.get_current().log_out()
    ui.label('You have been logged out').classes('text-2xl')
    ui.navigate.to(login_page)


@page('/about', title="About")
def about_page():
    ui.label("A basic authentication with a persistent session connection")


def setup_new_session():  # Initialize the user data for a new session
    app.storage.session["userData"] = UserData()


# setups a single page router at / (and all sub-paths)
sp = SinglePageRouter("/", on_session_created=setup_new_session)
sp.setup_page_routes()

ui.run()
