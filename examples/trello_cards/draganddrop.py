from __future__ import annotations

from typing import Callable, Optional, Protocol

from nicegui import ui


class Item(Protocol):
    """
    Represents an item with a title.

    This protocol defines the structure of an item that has a title. It can be used as a base for defining classes that represent different types of items.

    Attributes:
        title (str): The title of the item.

    Example:
        class Task:
            def __init__(self, title):
                self.title = title

        task = Task("Finish project")
        print(task.title)  # Output: Finish project
    """
    title: str


dragged: Optional[card] = None


class column(ui.column):
    """
    Represents a column in a Trello-like board.

    Args:
        name (str): The name of the column.
        on_drop (Optional[Callable[[Item, str], None]]): A callback function that will be called when a card is dropped into the column.

    Attributes:
        name (str): The name of the column.

    Methods:
        highlight(): Highlights the column when a card is being dragged over it.
        unhighlight(): Removes the highlight from the column when a card is dragged away from it.
        move_card(): Moves the dragged card into the column and triggers the on_drop callback.

    Example:
        def on_drop_callback(item: Item, column_name: str) -> None:
            # Do something with the dropped card item and column name

        my_column = column("To Do", on_drop=on_drop_callback)
    """

    def __init__(self, name: str, on_drop: Optional[Callable[[Item, str], None]] = None) -> None:
        super().__init__()
        with self.classes('bg-blue-grey-2 w-60 p-4 rounded shadow-2'):
            ui.label(name).classes('text-bold ml-1')
        self.name = name
        self.on('dragover.prevent', self.highlight)
        self.on('dragleave', self.unhighlight)
        self.on('drop', self.move_card)
        self.on_drop = on_drop

    def highlight(self) -> None:
        """
        Highlights the column when a card is being dragged over it.
        """
        self.classes(remove='bg-blue-grey-2', add='bg-blue-grey-3')

    def unhighlight(self) -> None:
        """
        Removes the highlight from the column when a card is dragged away from it.
        """
        self.classes(remove='bg-blue-grey-3', add='bg-blue-grey-2')

    def move_card(self) -> None:
        """
        Moves the dragged card into the column and triggers the on_drop callback.
        """
        global dragged
        self.unhighlight()
        dragged.parent_slot.parent.remove(dragged)
        with self:
            card(dragged.item)
        self.on_drop(dragged.item, self.name)
        dragged = None


class card(ui.card):
    """
    Represents a draggable card in a Trello-like interface.

    Args:
        item (Item): The item associated with the card.

    Attributes:
        item (Item): The item associated with the card.

    """

    def __init__(self, item: Item) -> None:
        super().__init__()
        self.item = item
        with self.props('draggable').classes('w-full cursor-pointer bg-grey-1'):
            ui.label(item.title)
        self.on('dragstart', self.handle_dragstart)

    def handle_dragstart(self) -> None:
        """
        Event handler for the 'dragstart' event.

        Sets the global variable 'dragged' to the current card instance.

        """
        global dragged
        dragged = self
