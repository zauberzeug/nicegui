from nice_gui import ui
from icecream import ic


ui.label('Hello, Nice GUI!')

with ui.column():
    ui.button('BUTTON 1', on_click=lambda _: ui.label('Nice!'))
    ui.button('BUTTON 2', on_click=lambda _: ui.label('GUI!'))
    
