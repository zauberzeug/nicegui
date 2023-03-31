#!/usr/bin/env python3
from nicegui import ui

messages = []


@ui.page('/')
def main():
    def send() -> None:
        messages.append((name.value, text.value))
        text.value = ''

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')

    content = ui.column().classes('w-full max-w-2xl mx-auto')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            name = ui.input(placeholder='name').props('rounded outlined autofocus input-class=mx-3')
            text = ui.input(placeholder='message').props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')

    async def update_messages() -> None:
        if len(messages) != len(content.default_slot.children):
            content.clear()
            with content:
                for name, text in messages:
                    ui.markdown(f'**{name or "someone"}:** {text}').classes('text-lg m-2')
            await ui.run_javascript(f'window.scrollTo(0, document.body.scrollHeight)', respond=False)
    ui.timer(0.1, update_messages)


ui.run()
