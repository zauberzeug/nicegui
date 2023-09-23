from nicegui import ui
from nicegui.events import ValueChangeEventArguments

## Basics

def _show_ui(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    msg = f'element name= {name}, value= {event.value}'
    ui.notify(msg)
    print(msg)

with ui.row():
    ui.label('Hello NiceGui !')
    ui.icon('thumb_up')

ui.markdown('This is **Markdown**.')
ui.html('Welcome to <strong>NiceGui</strong>.')
ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui', new_tab=True)

with ui.row():
    ui.label('CSS').style('color: #888; font-weight: bold')
    ui.label('Tailwind').classes('font-serif')
    ui.label('Quasar').classes('q-ml-xl')

ui.button('Welcome', on_click=lambda: ui.notify('Welcome to NiceGui'))

## Common UI Elements

ui.button('Button', on_click=lambda: ui.notify('Button is clicked'))

with ui.row():
    ui.checkbox('Checkbox', on_change=_show_ui)
    ui.switch('Switch', on_change=_show_ui)
ui.radio(['A', 'B', 'C'], value='A', on_change=_show_ui).props('inline')

with ui.row():
    ui.input('Text input', on_change=_show_ui)
    ui.select(['One', 'Two'], value='One', on_change=_show_ui)
ui.link('Find more at NiceGui Docs ...', 'https://nicegui.io/documentation', new_tab=True).classes('mt-8')

## Value Binding

class Demo:
    def __init__(self):
        self.number = 1

demo = Demo()
v = ui.checkbox('visible', value=True)
with ui.column().bind_visibility_from(v, 'value'):
    ui.slider(min=1, max=3, on_change=_show_ui).bind_value(demo, 'number')
    ui.toggle({1: 'A', 2: 'B', 3: 'C'}, on_change=_show_ui).bind_value(demo, 'number')
    ui.number(min=1, max=3, on_change=_show_ui).bind_value(demo, 'number')


ui.run()