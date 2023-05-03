#!/usr/bin/env python3
import os
from datetime import datetime
from typing import List, Tuple

from langchain.llms import OpenAI

from nicegui import Client, ui

os.environ['OPENAI_API_KEY'] = 'not-set'

llm = OpenAI(model_name='gpt-3.5-turbo')

messages: List[Tuple[str, str, str]] = []


@ui.refreshable
async def chat_messages() -> None:
    for name, text, stamp in messages:
        ui.chat_message(text=text,
                        name=name,
                        stamp=stamp,
                        avatar=f'https://robohash.org/{name or "You"}?bgset=bg2',
                        sent=name == "You")
    await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)


@ui.page('/')
async def main(client: Client):
    async def send() -> None:
        stamp = datetime.utcnow().strftime('%X')
        message = text.value
        messages.append(('You', text.value, stamp))
        messages.append(('Bot', 'Thinking...', stamp))
        text.value = ""
        chat_messages.refresh()

        await query(message)
        await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)

    async def query(user_message: str) -> None:
        response = await llm.agenerate([user_message])

        # replace last message ('Thinking....') with response
        messages[-1] = ('Bot', response.generations[0][0].text, datetime.now().strftime('%H:%M'))
        chat_messages.refresh()

        await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')
    await client.connected()

    # chatbox
    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        await chat_messages()

    # footer
    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            _placeholder = 'message' if os.environ['OPENAI_API_KEY'] != 'not-set' else \
                'please provide your OPENAI key in the Python script first!'
            text = ui.input(placeholder=_placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')

ui.run(title='Chat with GPT-3 (example)')
