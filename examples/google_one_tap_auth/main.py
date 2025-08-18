#!/usr/bin/env python3
import time

import httpx
from fastapi import Form, HTTPException
from fastapi.responses import RedirectResponse

from nicegui import app, ui

# Get your Google Client ID from the Google Cloud Console.
# See https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid#get_your_google_api_client_id.
# For local development, you should add http://localhost:8080 to the authorized JavaScript origins.
# In production, you should add the domain of your website to the authorized JavaScript origins.
# Make sure you include <origin>/auth in "Authorized redirect URIs".
GOOGLE_CLIENT_ID = '...'


@ui.page('/')
def main_page() -> None:
    user_info = app.storage.user.get('user_info', {})
    if not _is_valid(user_info):
        ui.add_head_html('<script src="https://accounts.google.com/gsi/client" async defer></script>')
        ui.html(f'''
            <div id="g_id_onload"
                data-client_id="{GOOGLE_CLIENT_ID}"
                data-login_uri="http://localhost:8080/auth">
            </div>
        ''')
        ui.label('Sign in with Google One Tap')
        return

    ui.label(f'Welcome {user_info.get("name") or user_info.get("email", "")}!')
    ui.button('Logout', on_click=logout)


def logout() -> None:
    del app.storage.user['user_info']
    ui.navigate.to('/')


@app.post('/auth')
async def google_auth(credential: str = Form(...)) -> RedirectResponse:
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}')
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail='Invalid token')
    user_info = response.json()
    if not _is_valid(user_info):
        raise HTTPException(status_code=400, detail='Invalid token claims')
    app.storage.user['user_info'] = user_info
    return RedirectResponse('/', status_code=303)


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
