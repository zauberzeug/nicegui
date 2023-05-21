from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    with ui.column():
        ui.label('label 1')
        ui.label('label 2')
        ui.label('label 3')


def more() -> None:
    @text_demo('Masonry or Pinterest-Style Layout', '''
        To create a masonry/pinterest layout, the normal ui.column can not be used.
        But it can be archived with a few Tailwind CSS classes.
    ''')
    def masonry() -> None:
        from random import choice, randint

        with ui.element('div').classes('columns-3 w-full gap-2'):
            for i in range(0, 9):
                height = f'h-{choice([8, 12, 14, 16, 20])}'
                color = f'bg-sky-{randint(1,5)}00'
                classes = f'w-full mb-2 {height} {color} break-inside-avoid'
                with ui.element('div').classes(classes):
                    ui.label(f'Content #{i+1}')
