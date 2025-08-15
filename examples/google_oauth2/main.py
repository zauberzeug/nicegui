#!/usr/bin/env python3
from typing import Optional

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui

# Get the credentials from the Google Cloud Console
# https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid#get_your_google_api_client_id
# make sure you include <origin>/auth in "Authorized redirect URIs"
GOOGLE_CLIENT_ID = '...'
GOOGLE_CLIENT_SECRET = '...'

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={'scope': 'openid email profile'},
)


@app.get('/auth')
async def google_oauth(request: Request) -> RedirectResponse:
    try:
        user_data = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f'OAuth error: {e}')
        return RedirectResponse('/')  # or return an error page/message
    app.storage.user['user_data'] = user_data
    return RedirectResponse('/')


def logout() -> None:
    del app.storage.user['user_data']
    ui.navigate.to('/')


@ui.page('/')
async def main(request: Request) -> Optional[RedirectResponse]:
    user_data = app.storage.user.get('user_data', None)
    if user_data:
        ui.label(f'Welcome {user_data.get("userinfo", {}).get("name", "")}!')
        ui.button('Logout', on_click=logout)
        return None
    else:
        url = request.url_for('google_oauth')
        return await oauth.google.authorize_redirect(request, url)

ui.run(host='localhost', storage_secret='random secret goes here')
