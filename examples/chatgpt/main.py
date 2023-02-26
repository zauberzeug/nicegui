#!/usr/bin/env python3
import asyncio
import json
import logging

import aiofiles
from revChatGPT.V1 import AsyncChatbot

from nicegui import ui


@ui.page('/')
async def main_page() -> None:

    async def scroll_to_bottom() -> None:
        await ui.run_javascript(f'window.scrollTo(0, getElement({content.id}).clientHeight)', respond=False)

    async def apply_config() -> None:
        async with aiofiles.open('.chatgpt_config.json', 'w') as file:
            await file.write(json.dumps({'access_token': token_input.value, 'paid': paid_checkbox.value}))
        ui.open('/')

    async def ask() -> None:
        question = prompt.value
        prompt.value = ''
        await scroll_to_bottom()
        with content:
            ui.label(question).classes('text-bold text-lg')
            response = ui.markdown().classes('text-lg')
            async for data in chatbot.ask(question):
                response.set_content(data["message"])
                await scroll_to_bottom()

    with ui.column().classes('w-full max-w-3xl mx-auto') as content:
        with ui.element('q-page-scroller').props('reverse position="top-right" :scroll-offset="0" :offset="[0, 18]'):
            ui.button().props('icon="keyboard_arrow_down" fab')
        try:
            async with aiofiles.open('.chatgpt_config.json', 'r') as file:
                chatbot = AsyncChatbot(config=json.loads(await file.read()))
            await chatbot.get_conversations()  # NOTE: this is just to check if the token is valid
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
