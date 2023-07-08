#!/usr/bin/env python3
from nicegui import Client, app, background_tasks, events, globals, ui
from nicegui.element import Element
from nicegui.elements import markdown
from nicegui.elements.mixins.text_element import TextElement
from nicegui.nicegui import Element
from nicegui.page import page


ui.joystick()

# ui.mermaid('''
# graph LR;
#     A --> B;
#     A --> C;
# ''')

ui.button('plotly', on_click=lambda: ui.plotly())
ui.button('pyplot', on_click=lambda: ui.pyplot())

ui.label('test')
ui.run(favicon='🚀', storage_secret='secret')
# ui.run(favicon='🚀', storage_secret='secret', on_air='falkos-token')
