from __future__ import annotations

from typing import Optional

from nicegui import ui


class column(ui.column):

    def __init__(self, name: str) -> None:
        super().__init__()
        with self.classes('bg-gray-200 w-60 p-4 rounded shadow-2'):
            ui.label(name).classes('text-bold')
        self.on('dragover.prevent', self.highlight)
        self.on('dragleave', self.unhighlight)
        self.on('drop', self.move_card)

    def highlight(self) -> None:
        self.classes(add='bg-gray-400')

    def unhighlight(self) -> None:
        self.classes(remove='bg-gray-400')

    def move_card(self) -> None:
        self.unhighlight()
        card.dragged.parent_slot.parent.remove(card.dragged)
        with self:
            card(card.dragged.text)


class card(ui.card):
    dragged: Optional[card] = None

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        with self.props('draggable').classes('w-full cursor-pointer'):
            ui.label(self.text)
        self.on('dragstart', self.handle_dragstart)

    def handle_dragstart(self) -> None:
        card.dragged = self
