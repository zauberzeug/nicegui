from nicegui import ui

from . import doc


@doc.demo(ui.color_picker)
def main_demo() -> None:
    with ui.button(icon='colorize') as button:
        ui.color_picker(on_pick=lambda e: button.classes(f'bg-[{e.color}]'))


@doc.demo('Customize the Color Picker', '''
    You can customize the color picker via props, classes and style attributes.
    Because the QColor component is nested inside a menu, you can't use the `props` method directly,
    but via the `q_color` attribute.
''')
def color_picker_props() -> None:
    with ui.button(icon='palette'):
        picker = ui.color_picker(on_pick=lambda e: ui.notify(f'You chose {e.color}'))
        picker.q_color.props('default-view=palette no-header no-footer')


doc.reference(ui.color_picker)
