#!/usr/bin/env python3
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
from nicegui import ui

image_urls = [
    'https://picsum.photos/300/300?1',
    'https://picsum.photos/300/300?2',
    'https://picsum.photos/300/300?3',
]

avatar_urls = [
    'https://robohash.org/1?bgset=bg1',
    'https://robohash.org/2?bgset=bg2',
    'https://robohash.org/3?bgset=bg3',
]

messages: List[Tuple[str, str, str, str]] = []

@ui.refreshable
async def chat_messages(own_id: str) -> None:
    for user_id, avatar, text, stamp in messages:
        ui.chat_message(text=text, stamp=stamp, avatar=avatar, sent=own_id == user_id)
    await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)

def send() -> None:
    stamp = datetime.utcnow().strftime('%X')
    messages.append((user_id, avatar, text.value, stamp))
    text.value = ''
    chat_messages.refresh()

avatar_index = 0
def switch_icon():
    global avatar_index
    avatar_index = (avatar_index + 1) % len(avatar_urls)
    avatar_image.url = avatar_urls[avatar_index]

def on_avatar_click():
    switch_icon()
    left_drawer.toggle()

user_id = str(uuid4())
avatar = avatar_urls[avatar_index]

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    with ui.column().classes('w-full'):
        with ui.row().classes('w-full no-wrap items-center'):
            avatar_image = ui.avatar(avatar).on('click', on_avatar_click)
            text = ui.input(placeholder='message').on('keydown.enter', send).props('rounded outlined input-class=mx-3').classes('flex-grow')

        with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
            ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)').classes('text-xs self-end mr-8 m-[-1em] text-primary')
            chat_messages(user_id)

# Continue with the rest of your application...
# The rest of your code...



tabs = {}

def switch_tab(value):
    tabs['panels'].value = value

tab_bar = ui.tabs()

with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tab_bar, value='A').classes('w-full') as panels:
    tabs['panels'] = panels

    with ui.tab_panel('A') as tabA:
        ui.label('Content of A').classes('text-center')
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[0]).classes('w-full h-full')
                ui.button(on_click=lambda: switch_tab('C'), icon='arrow_back').classes('absolute top-1/2 left-2')
                ui.button(on_click=lambda: switch_tab('B'), icon='arrow_forward').classes('absolute top-1/2 right-2')

    with ui.tab_panel('B') as tabB:
        ui.label('Content of B').classes('text-center')
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[1]).classes('w-full h-full')
                ui.button(on_click=lambda: switch_tab('C'), icon='arrow_forward').classes('absolute top-1/2 right-2')
                ui.button(on_click=lambda: switch_tab('A'), icon='arrow_back').classes('absolute top-1/2 left-2')

    with ui.tab_panel('C') as tabC:
        ui.label('Content of C').classes('text-center')
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[2]).classes('w-full h-full')
                ui.button(on_click=lambda: switch_tab('A'), icon='arrow_forward').classes('absolute top-1/2 right-2')
                ui.button(on_click=lambda: switch_tab('B'), icon='arrow_back').classes('absolute top-1/2 left-2')

with ui.row():
    for i, url in enumerate(image_urls):
        with ui.card().classes('m-4 p-4 shadow-lg relative').style('width: 300px'):
            ui.image(url).classes('w-full h-full')
            ui.label(f"Image {i+1}").classes('mt-2')
            with ui.row().classes('justify-between mt-2'):
                ui.button(on_click=lambda i=i: print(f"Image {i+1} liked"), icon='thumb_up').classes('fab')
                ui.button(on_click=lambda i=i: print(f"Image {i+1} disliked"), icon='thumb_down').classes('fab')
                ui.button(on_click=lambda: left_drawer.toggle(), icon='info').classes('fab')

ui.run()
