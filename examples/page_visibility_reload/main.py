#!/usr/bin/env python3
from pagevisibility import AutoReloader
from nicegui import ui

ui.markdown('''
#### Emit from javascript to python using visibility of page!

Try to change tab or minimize the browser window...

Notice how we can call a python function from javascript using $emit()...
''')
autoreloader = AutoReloader('Not needed, just javascript...', on_change=lambda msg: ui.notify(
    f'The value changed to {msg["args"]}.'))

ui.run(port=1234)
