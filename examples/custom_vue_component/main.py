#!/usr/bin/env python3
from counter import Counter

from nicegui import ui

ui.markdown('''
#### Try the new click counter!

Click to increment its value.
''')
with ui.card():
    counter = Counter('Clicks', on_change=lambda e: ui.notify(f'The value changed to {e.args}.'))


ui.button('Reset', on_click=counter.reset).props('small outline')

ui.run()
