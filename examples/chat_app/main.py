#!/usr/bin/env python3
import asyncio
from typing import List, Tuple

from nicegui import Client, ui

messages: List[Tuple[str, str]] = []
contents: List[ui.column] = []


async def update(content: ui.column) -> None:
    content.clear()
    with content:  # use the context of each client to update their ui
        for name, text in messages:
            ui.markdown(f'**{name or "someone"}:** {text}').classes('text-lg m-2')
        await ui.run_javascript(f'window.scrollTo(0, document.body.scrollHeight)', respond=False)


@ui.page('/')
async def main(client: Client):
    async def send() -> None:
        messages.append((name.value, text.value))
        text.value = ''
        await asyncio.gather(*[update(content) for content in contents])  # run updates concurrently

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')
    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            name = ui.input(placeholder='name').props('rounded outlined autofocus input-class=mx-3')
            text = ui.input(placeholder='message').props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')

    await client.connected()  # update(...) uses run_javascript which is only possible after connecting
    contents.append(ui.column().classes('w-full max-w-2xl mx-auto'))  # save ui context for updates
    await update(contents[-1])  # ensure all messages are shown after connecting


ui.run()
