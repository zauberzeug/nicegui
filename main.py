from nice_gui import NiceGui
from icecream import ic

ui = NiceGui()

ui.label('Hello, Nice GUI!')

ui.button('BUTTON', on_click=lambda _: ui.label('Nice!'))

app = ui.app