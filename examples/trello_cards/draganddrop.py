from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from nicegui import ui


class Item(Protocol):
    title: str


dragged: card | None = None
drop_target: card | None = None


class column(ui.column):

    def __init__(self, name: str, on_drop: Callable[[Item, str], None] | None = None) -> None:
        super().__init__()
        with self.classes('bg-blue-grey-2 w-60 p-4 rounded shadow-2'):
            ui.label(name).classes('text-bold ml-1')
        self.name = name
        self.on('dragover.prevent', self.highlight)
        self.on('dragleave', self.unhighlight)
        self.on('drop', self.move_card)
        self.on_drop = on_drop

    def highlight(self) -> None:
        self.classes(remove='bg-blue-grey-2', add='bg-blue-grey-3')

    def unhighlight(self) -> None:
        self.classes(remove='bg-blue-grey-3', add='bg-blue-grey-2')

    def move_card(self) -> None:
        global dragged, drop_target  # pylint: disable=global-statement # noqa: PLW0603
        self.unhighlight()
        if dragged is None:
            return
        # Determine insertion index based on the card being hovered over
        target_index = -1
        if drop_target is not None and drop_target.parent_slot is not None:
            if drop_target.parent_slot.parent is self:
                target_index = self.default_slot.children.index(drop_target)
        dragged.move(target_container=self, target_index=target_index)
        if self.on_drop:
            self.on_drop(dragged.item, self.name)
        dragged = None
        drop_target = None


class card(ui.card):

    def __init__(self, item: Item) -> None:
        super().__init__()
        self.item = item
        with self.props('draggable').classes('w-full cursor-pointer bg-grey-1'):
            ui.label(item.title)
        self.on('dragstart', self.handle_dragstart)
        self.on('dragover.prevent', self.handle_dragover)

    def handle_dragstart(self) -> None:
        global dragged  # pylint: disable=global-statement # noqa: PLW0603
        dragged = self

    def handle_dragover(self) -> None:
        global drop_target  # pylint: disable=global-statement # noqa: PLW0603
        drop_target = self
