#!/usr/bin/env python3
import logging
import time
from typing import Optional

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request
from starlette.responses import RedirectResponse

from nicegui import app, ui

# Get the credentials from the Google Cloud Console.
# See https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid#get_your_google_api_client_id.
# For local development, you should add http://localhost:8080 to the authorized JavaScript origins.
# In production, you should add the domain of your website to the authorized JavaScript origins.
# Make sure you include <origin>/auth in "Authorized redirect URIs".
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


@ui.page('/')
async def main(request: Request) -> Optional[RedirectResponse]:
    user_info = app.storage.user.get('user_info', {})
    if not _is_valid(user_info):
        app.storage.user.pop('user_info', None)
        return await oauth.google.authorize_redirect(request, request.url_for('google_oauth'))

    ui.label(f'Welcome {user_info.get("name") or user_info.get("email", "")}!')
    ui.button('Logout', on_click=logout)
    return None


def logout() -> None:
    del app.storage.user['user_info']
    ui.navigate.to('/')


@app.get('/auth')
async def google_oauth(request: Request) -> RedirectResponse:
    try:
        user_info = (await oauth.google.authorize_access_token(request)).get('userinfo', {})
        if _is_valid(user_info):
            app.storage.user['user_info'] = user_info
    except (OAuthError, Exception):
        logging.exception('could not authorize access token')
    return RedirectResponse('/')


def _is_valid(user_info: dict) -> bool:
    try:
        return all([
            int(user_info.get('exp', 0)) > int(time.time()),
            user_info.get('aud') == GOOGLE_CLIENT_ID,
            user_info.get('iss') in {'https://accounts.google.com', 'accounts.google.com'},
            str(user_info.get('email_verified')).lower() == 'true',
        ])
    except Exception:
        return False


ui.run(
    host='localhost',  # NOTE: this ensures that you can run the app locally, accessing via http://127.0.0.1:8080 is not supported by Google OAuth2
    storage_secret='random secret goes here',
)
