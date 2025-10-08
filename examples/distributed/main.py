#!/usr/bin/env python3
import random
import socket

from nicegui import Event, context, ui

reaction_event = Event[str]()


@ui.page('/')
def index():
    ui.add_css('''@keyframes float-up { to { transform: translateY(-500px) scale(1.5); opacity: 0; }  }''')

    with ui.column().classes('items-center justify-center h-screen w-screen gap-8'):
        ui.label(f'This is instance {socket.gethostname()}').classes('text-3xl font-bold')
        ui.label('Click an emoji - watch it appear on all instances (open multiple tabs)!').classes('text-gray-600')

        emojis = ['🎉', '❤️', '👍', '😂', '🔥', '✨', '🚀', '👏']
        with ui.row().classes('gap-4'):
            for emoji in emojis:
                ui.button(emoji, on_click=lambda e=emoji: reaction_event.emit(e)).props('flat size=lg')

    def show_reaction(emoji: str):
        left = random.randint(10, 90)
        with context.client.layout:
            floating = ui.html(emoji, sanitize=False).classes('fixed text-5xl pointer-events-none z-[9999]')
            floating.style(f'animation: float-up 3s ease-out forwards; left: {left}%; bottom: 100px')
            ui.timer(3.0, floating.delete, once=True)

    reaction_event.subscribe(show_reaction)


ui.run(distributed=True)
