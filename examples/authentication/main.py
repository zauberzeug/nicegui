
import starlette
from nicegui import ui

from session_info import SessionInfo

session_infos = SessionInfo()


def build_content(username: str) -> None:
    with ui.row().classes('flex justify-center w-full mt-20'):
        ui.label(f'Hello {username}!').classes('text-2xl')


def build_login_form() -> None:
    def on_login(username: str, password: str, socket: starlette.websockets.WebSocket):
        session_id = socket.cookies['jp_token'].split('.')[0]
        if (username == 'user1' and password == 'pass1') or (username == 'user2' and password == 'pass2'):
            session_infos[session_id] = {'authenticated': True, 'user': username}
            ui.open('/', socket)

    with ui.row().classes('flex justify-center w-full mt-20'):
        with ui.card():
            username = ui.input('User Name')
            password = ui.input('Password').classes('w-full').props('type=password')
            ui.button('Log in', on_click=lambda e: on_login(username.value, password.value, e.socket))


@ui.page('/')
def main_page(request: starlette.requests.Request):
    if session_infos[request.session_id].get('authenticated', False):
        build_content(session_infos[request.session_id]["user"])
    else:
        build_login_form()


ui.run()
