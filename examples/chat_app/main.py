#!/usr/bin/env python3
from nicegui import ui
from icecream import ic
messages = []


@ui.page('/')
def main():
    async def scroll_to_bottom() -> None:
        await ui.run_javascript(f'window.scrollTo(0, getElement({content.id}).clientHeight)', respond=False)

    async def send() -> None:
        messages.append(f'**{name.value}**: {message.value}')
        message.value = ''
        await scroll_to_bottom()

    ui.add_head_html('''
        <style> 
            a:link, a:visited {
                color: inherit !important;
                text-decoration: none;
                font-weight: 500;
            }
        </style>''')

    def update_messages():
        if len(messages) == message_count:
            return
        content.clear()
        with content:
            for message in messages:
                ui.markdown(message).classes('text-lg m-2')

    message_count = 0
    with ui.column().classes('w-full max-w-2xl mx-auto') as content:
        with ui.element('q-page-scroller').props('reverse position="top-right" :scroll-offset="0" :offset="[0, 18]'):
            ui.button().props('icon="keyboard_arrow_down" fab')
        with ui.footer().classes('bg-white text-black'), ui.column().classes('w-full  max-w-3xl mx-auto my-6'):
            with ui.row().classes('w-full no-wrap items-center'):
                name = ui.input(placeholder='name').props('rounded outlined autofocus input-class="ml-3"')
                message = ui.input().props('rounded outlined input-class="ml-3"') \
                    .classes('w-full self-center').on('keydown.enter', send)
            ui.markdown(
                'simple chat app built with [NiceGUI](https://nicegui.io)'
            ).classes('text-xs self-end mr-8 m-[-1em] text-primary')

    ui.timer(1, update_messages)


ui.run()
