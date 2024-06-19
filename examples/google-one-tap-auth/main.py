#!/usr/bin/env python3
import os

import httpx
from dotenv import load_dotenv
from fastapi import Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from nicegui import Client, app, core, ui

# Get your Google Client ID from the Google Cloud Console
# https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid#get_your_google_api_client_id
# and pass it as an environment variable (or write it to an .env file)
load_dotenv()
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']


@ui.page('/')
def main_page(request: Request):
    assert request.url.hostname
    assert core.air
    assert core.air.remote_url
    if 'on-air.io' not in request.url.hostname:
        return RedirectResponse(core.air.remote_url)
    ui.add_head_html('<script src="https://accounts.google.com/gsi/client" async defer></script>')
    ui.html(f'''
        <div id="g_id_onload"
            data-client_id="{GOOGLE_CLIENT_ID}"
            data-login_uri="{core.air.remote_url}auth/google">
        </div>''')
    ui.button('Click', on_click=lambda: ui.run_javascript('fail()'))


@app.post('/auth/google')
async def google_auth(request: Request, credential: str = Form(...)):
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}')
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail='Invalid token')
    user_data = response.json()
    with Client(ui.page('')) as nicegui_client:
        ui.label(f'Welcome {user_data["name"]}!')
    return nicegui_client.build_response(request, 404)

# NOTE we use NiceGUI On Air (https://nicegui.io/documentation/section_configuration_deployment#nicegui_on_air)
# to make the local server available to google one-tap auth
# if you deploy your app on a server, you can remove the whole On Air part
ui.run(on_air=True, storage_secret='THIS_NEEDS_TO_BE_CHANGED')
