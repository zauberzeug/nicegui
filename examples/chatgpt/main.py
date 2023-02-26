#!/usr/bin/env python3
import json
import logging

import aiofiles
from icecream import ic
from revChatGPT.V1 import AsyncChatbot

from nicegui import app, ui


@ui.page('/')
async def main_page() -> None:

    async def apply_config() -> None:
        async with aiofiles.open('.chatgpt_config.json', 'w') as file:
            await file.write(json.dumps({'access_token': token_input.value, 'paid': paid_checkbox.value}))
        ui.open('/')

    async def ask() -> None:
        async for data in chatbot.ask(prompt.value):
            messages.set_content(data["message"])

    with ui.column().classes('w-full max-w-3xl mx-auto'):
        try:
            async with aiofiles.open('.chatgpt_config.json', 'r') as file:
                chatbot = AsyncChatbot(config=json.loads(await file.read()))
            await chatbot.get_conversations()  # NOTE: this is just to check if the token is valid
            messages = ui.markdown().classes('h-full mb-auto')
            with ui.footer().classes('bg-white text-black'), ui.column().classes('w-full  max-w-3xl mx-auto my-6'):
                prompt = ui.input().props('rounded outlined autofocus input-class="ml-3"') \
                    .classes('w-full self-center').on('keydown.enter', ask)
                ui.markdown('[ChatGPT](https://chat.openai.com/chat) interface by [NiceGUI](https://nicegui.io)')\
                    .classes('text-xs self-end mr-8 m-[-1em]')
        except Exception:
            logging.exception('error')
            with ui.row():
                paid_checkbox = ui.checkbox('paid')
                token_input = ui.input('Access Token').on('keydown.enter', apply_config)
                ui.markdown(
                    'copy & paste from [session json](https://chat.openai.com/api/auth/session){:target="_blank"}')
            ui.button('Apply', on_click=apply_config)

ui.run()
