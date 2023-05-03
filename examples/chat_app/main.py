#!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple

from nicegui import Client, ui

messages: List[Tuple[str, str]] = []


@ui.refreshable
async def chat_messages(name_input: ui.input) -> None:
    for name, text, stamp in messages:
        ui.chat_message(text=text,
                        name=name,
                        stamp=stamp,
                        avatar=f'https://robohash.org/{name or "anonymous"}?bgset=bg2',
                        sent=name == name_input.value)
    await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)


@ui.page('/')
async def main(client: Client):
    def send() -> None:
        stamp = datetime.utcnow().strftime('%X')
        messages.append((name.value, text.value, stamp))
        text.value = ''
        chat_messages.refresh()

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')
    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            name = ui.input(placeholder='name').props('rounded outlined autofocus input-class=mx-3')
            text = ui.input(placeholder='message').props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')

    await client.connected()  # chat_messages(...) uses run_javascript which is only possible after connecting
    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        await chat_messages(name_input=name)

ui.run()
