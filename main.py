from nice_gui import ui
from icecream import ic


ui.label('Hello, Nice GUI!')

ui.button('BUTTON', on_click=lambda _: ui.label('Nice!'))
