from nicegui import ui

from . import doc


@doc.demo(ui.expansion)
def main_demo() -> None:
    with ui.expansion('Expand!', icon='work').classes('w-full'):
        ui.label('inside the expansion')


@doc.demo('Expansion with Custom Header', '''
    Instead of setting a plain-text title, you can fill the expansion header with UI elements by adding them to the "header" slot.
''')
def expansion_with_custom_header():
    with ui.expansion() as expansion:
        with expansion.add_slot('header'):
            ui.image('https://nicegui.io/logo.png').classes('w-16')
        ui.label('What a nice GUI!')


@doc.demo('Expansion with Custom Caption', '''
    A caption, or sub-label, can be added below the title.
''')
def expansion_with_caption():
    with ui.expansion('Expand!', caption='Expansion Caption').classes('w-full'):
        ui.label('inside the expansion')


@doc.demo('Expansion with Grouping', '''
    An expansion group can be defined to enable coordinated open/close states a.k.a. "accordion mode".
''')
def expansion_with_grouping():
    with ui.expansion(text='Expand One!', group='group'):
        ui.label('inside expansion one')
    with ui.expansion(text='Expand Two!', group='group'):
        ui.label('inside expansion two')
    with ui.expansion(text='Expand Three!', group='group'):
        ui.label('inside expansion three')


doc.reference(ui.expansion)
