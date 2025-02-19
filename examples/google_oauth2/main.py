from nicegui import ui, app
from fastapi import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
import dotenv

app.add_middleware(SessionMiddleware,
                     secret_key="random secret goes here",
                     session_cookie="my_session",
                     https_only=False)


dotenv.load_dotenv()
import os

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    client_kwargs={
        'scope': 'openid email profile',
        'redirect_uri': 'http://localhost:8000/auth'
    },
    authorize_state="random secret goes here"  
)


@ui.page("/")
def main(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse("/welcome")
    with ui.link(target=f"/login"):
        ui.label("Click me to login")

@ui.page("/welcome")
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse("/")
    ui.label(f"Welcome {user.get('info', {}).get('userinfo', {}).get('name', '')}!")
    with ui.link(target="/logout"):
        ui.label("Logout")

@ui.page("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@ui.page("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f"OAuth error: {e}")
        return RedirectResponse("/")  # or return an error page/message
    app.storage.user['info'] = token
    request.session['user'] = app.storage.user
    return RedirectResponse("/welcome")


@ui.page("/logout")
def logout(request: Request):
    request.session.pop('user', None)

    return RedirectResponse("/")


ui.run(port=8001, storage_secret="random secret goes here")