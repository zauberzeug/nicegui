from nicegui import ui

ui.label('Hello NiceGUI!')
ui.button('BUTTON', on_click=lambda: ui.notify('Welcome to NiceGui'))

ui.run()