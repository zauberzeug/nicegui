#!/usr/bin/env python3
from nicegui import ui

from counter import Counter

ui.markdown('''
#### Try the new click counter!

Click to increment its value.
''')
with ui.card():
    counter = Counter('Clicks', on_change=lambda value: message.set_text(f'The value changed to {value}.'))


ui.button('Reset', on_click=lambda: counter.reset()).props('small outline')

message = ui.label()

ui.run()
