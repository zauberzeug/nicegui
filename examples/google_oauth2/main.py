from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui

GOOGLE_CLIENT_ID = 'your google client id'
GOOGLE_CLIENT_SECRET = 'your google client secret'

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid email profile',
        'redirect_uri': 'http://localhost:8080/auth'
    },
    authorize_state='random secret goes here'
)


@ui.page('/')
def main(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse('/welcome')
    with ui.link(target='/login'):
        ui.label('Click me to login')


@ui.page('/welcome')
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    ui.label(f'Welcome {user.get('info', {}).get('userinfo', {}).get('name', '')}!')
    with ui.link(target='/logout'):
        ui.label('Logout')


@ui.page('/login')
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@ui.page('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f'OAuth error: {e}')
        return RedirectResponse('/')  # or return an error page/message
    app.storage.user['info'] = token
    request.session['user'] = app.storage.user
    return RedirectResponse('/welcome')


@ui.page('/logout')
def logout(request: Request):
    request.session.pop('user', None)

    return RedirectResponse('/')


ui.run(port=8080, storage_secret='random secret goes here')
