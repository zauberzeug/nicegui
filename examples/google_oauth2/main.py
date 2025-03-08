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
    user_data = app.storage.user.get('user_data', None)
    if user_data:
        ui.label(f'Welcome {user_data.get('userinfo', {}).get('name', '')}!')
        ui.link('Logout', target='/logout')
    else:
        ui.link('Click me to login', target='/login')


@ui.page('/login')
async def login(request: Request):
    url = request.url_for('google_oauth')
    return await oauth.google.authorize_redirect(request, url)


@app.get('/auth')
async def google_oauth(request: Request):
    try:
        user_data = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f'OAuth error: {e}')
        return RedirectResponse('/')  # or return an error page/message
    app.storage.user['user_data'] = user_data
    return RedirectResponse('/')


@ui.page('/logout')
def logout(request: Request):
    request.session.pop('user', None)

    return RedirectResponse('/')


ui.run(port=8080, storage_secret='random secret goes here')
