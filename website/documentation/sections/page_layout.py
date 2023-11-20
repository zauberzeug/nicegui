from nicegui import ui

from ..tools import load_demo, text_demo

name = 'page_layout'
title = 'Page Layout'
description = '''
    This section covers fundamental techniques as well as several elements to structure your UI.
'''


def content() -> None:
    @text_demo('Auto-context', '''
        In order to allow writing intuitive UI descriptions, NiceGUI automatically tracks the context in which elements are created.
        This means that there is no explicit `parent` parameter.
        Instead the parent context is defined using a `with` statement.
        It is also passed to event handlers and timers.

        In the demo, the label "Card content" is added to the card.
        And because the `ui.button` is also added to the card, the label "Click!" will also be created in this context.
        The label "Tick!", which is added once after one second, is also added to the card.

        This design decision allows for easily creating modular components that keep working after moving them around in the UI.
        For example, you can move label and button somewhere else, maybe wrap them in another container, and the code will still work.
    ''')
    def auto_context_demo():
        with ui.card():
            ui.label('Card content')
            ui.button('Add label', on_click=lambda: ui.label('Click!'))
            ui.timer(1.0, lambda: ui.label('Tick!'), once=True)

    load_demo(ui.card)
    load_demo(ui.column)
    load_demo(ui.row)
    load_demo(ui.grid)

    @text_demo('Clear Containers', '''
        To remove all elements from a row, column or card container, use can call
        ```py
        container.clear()
        ```

        Alternatively, you can remove individual elements by calling
        
        - `container.remove(element: Element)`,
        - `container.remove(index: int)`, or
        - `element.delete()`.
    ''')
    def clear_containers_demo():
        container = ui.row()

        def add_face():
            with container:
                ui.icon('face')
        add_face()

        ui.button('Add', on_click=add_face)
        ui.button('Remove', on_click=lambda: container.remove(0) if list(container) else None)
        ui.button('Clear', on_click=container.clear)

    load_demo(ui.expansion)
    load_demo(ui.scroll_area)
    load_demo(ui.separator)
    load_demo(ui.splitter)
    load_demo('tabs')
    load_demo(ui.stepper)
    load_demo(ui.timeline)
    load_demo(ui.carousel)
    load_demo(ui.pagination)
    load_demo(ui.menu)
    load_demo(ui.context_menu)

    @text_demo('Tooltips', '''
        Simply call the `tooltip(text:str)` method on UI elements to provide a tooltip.

        For more artistic control you can nest tooltip elements and apply props, classes and styles.
    ''')
    def tooltips_demo():
        ui.label('Tooltips...').tooltip('...are shown on mouse over')
        with ui.button(icon='thumb_up'):
            ui.tooltip('I like this').classes('bg-green')

    load_demo(ui.notify)
    load_demo(ui.dialog)
