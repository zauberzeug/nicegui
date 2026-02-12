from nicegui import ui

from .. import doc
from . import (
    card_documentation,
    column_documentation,
    grid_documentation,
    list_documentation,
    row_documentation,
)

doc.title('Containers')


@doc.demo('Auto-context', '''
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


doc.intro(card_documentation)
doc.intro(column_documentation)
doc.intro(row_documentation)
doc.intro(grid_documentation)
doc.intro(list_documentation)


@doc.demo('Clear Containers', '''
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
