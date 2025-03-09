import os

from authlib.integrations.starlette_client import OAuth, OAuthError
from dotenv import load_dotenv
from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui

# Get the credentials from the Google Cloud Console
# https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid#get_your_google_api_client_id
# and pass them as environment variables (or write it to an .env file)
load_dotenv()
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

oauth = OAuth()

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={'scope': 'openid email profile', },
)


@app.get('/auth')
async def google_oauth(request: Request):
    try:
        user_data = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f'OAuth error: {e}')
        return RedirectResponse('/')  # or return an error page/message
    app.storage.user['user_data'] = user_data
    return RedirectResponse('/')


def logout():
    del app.storage.user['user_data']
    ui.navigate.to('/')


@ui.page('/')
async def main(request: Request):

    user_data = app.storage.user.get('user_data', None)
    if user_data:
        ui.label(f'Welcome {user_data.get('userinfo', {}).get('name', '')}!')
        ui.button('Logout', on_click=logout)
    else:
        url = request.url_for('google_oauth')
        if url.hostname != 'localhost':  # NOTE this ensures we use the localhost URL configured in Google Console
            return RedirectResponse(next(app.urls))
        return await oauth.google.authorize_redirect(request, url)

ui.run(storage_secret='random secret goes here')
