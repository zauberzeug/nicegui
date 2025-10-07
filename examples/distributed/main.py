#!/usr/bin/env python3
import random
import socket

from nicegui import Event, ui

reaction_event = Event[str]()


@ui.page('/')
def index():
    ui.add_head_html('''
        <style>
            .emoji-float {
                position: fixed;
                font-size: 3rem;
                pointer-events: none;
                animation: float-up 3s ease-out forwards;
                z-index: 9999;
            }
            @keyframes float-up {
                0% {
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translateY(-500px) scale(1.5);
                    opacity: 0;
                }
            }
        </style>
    ''')

    with ui.column().classes('items-center justify-center h-screen w-screen gap-8'):
        ui.label(f'This is instance {socket.gethostname()}').classes('text-3xl font-bold')
        ui.label('Click an emoji - watch it appear on all instances (open multiple tabs)!').classes('text-gray-600')

        emojis = ['🎉', '❤️', '👍', '😂', '🔥', '✨', '🚀', '👏']
        with ui.row().classes('gap-4'):
            for emoji in emojis:
                ui.button(emoji, on_click=lambda e=emoji: reaction_event.emit(e)).props('flat size=lg')

    def show_reaction(emoji: str):
        left = random.randint(10, 90)
        ui.run_javascript(f'''
            const div = document.createElement('div');
            div.className = 'emoji-float';
            div.textContent = '{emoji}';
            div.style.left = '{left}%';
            div.style.bottom = '100px';
            document.body.appendChild(div);
            setTimeout(() => div.remove(), 3000);
        ''')

    reaction_event.subscribe(show_reaction)


ui.run(distributed=True, title='Distributed Events')
