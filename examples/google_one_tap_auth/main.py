#!/usr/bin/env python3
import os

import httpx
from dotenv import load_dotenv
from fastapi import Form, HTTPException
from fastapi.responses import RedirectResponse

from nicegui import app, ui

# Get your Google Client ID from the Google Cloud Console and pass it as an environment variable (or write it to an .env file)
# For local development, you should add http://localhost:8080 to the authorized javascript origins
# In production, you should add the domain of your website to the authorized javascript origins
# see https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid#get_your_google_api_client_id
load_dotenv()
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
assert GOOGLE_CLIENT_ID, 'Please set the GOOGLE_CLIENT_ID environment variable'


@ui.page('/')
def main_page():
    user_data = app.storage.user.get('user_data', None)
    if not user_data:
        ui.add_head_html('<script src="https://accounts.google.com/gsi/client" async defer></script>')
        ui.html(f'''
            <div id="g_id_onload"
                data-client_id="{GOOGLE_CLIENT_ID}"
                data-login_uri="http://localhost:8080/auth">
            </div>''')
        ui.label('Sign in with Google One Tap')
    else:
        ui.label(f'Welcome {user_data["name"]}!')
        ui.button('Logout', on_click=logout)


def logout():
    del app.storage.user['user_data']
    ui.navigate.to('/')


@app.post('/auth')
async def google_auth(credential: str = Form(...)):
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}')
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail='Invalid token')
    app.storage.user['user_data'] = response.json()
    return RedirectResponse('/', status_code=303)

ui.run(storage_secret='here you should pick a random secret string for your app')
