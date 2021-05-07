from nice_gui import ui
from icecream import ic


ui.label('Hello, Nice GUI!')

with ui.column() as col:
    col.button('BUTTON', on_click=lambda _: col.label('Nice!'))
