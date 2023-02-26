#!/usr/bin/env python3
import logging

import aiofiles
from revChatGPT.V1 import AsyncChatbot
from starlette.middleware.sessions import SessionMiddleware

from nicegui import app, ui

app.add_middleware(SessionMiddleware, secret_key='some_random_string')  # use your own secret key here


@ui.page('/')
async def main_page() -> None:

    async def save_access_token() -> None:
        async with aiofiles.open('.access_token.txt', 'w') as file:
            await file.write(token_input.value)
        ui.open('/')

    async def ask() -> None:
        async for data in chatbot.ask(prompt.value):
            messages.set_content(data["message"])

    try:
        async with aiofiles.open('.access_token.txt', 'r') as file:
            access_token = await file.read()
        chatbot = AsyncChatbot(config={'access_token': access_token, 'paid': True})
        await chatbot.get_conversations()  # NOTE: this is just to check if the token is valid
        messages = ui.markdown()
        prompt = ui.input('promt').on('keydown.enter', ask)
    except Exception:
        logging.exception('error')
        token_input = ui.input('Access Token').on('keydown.enter', save_access_token)
        ui.markdown('copy & paste from <https://chat.openai.com/api/auth/session>')

ui.run()
