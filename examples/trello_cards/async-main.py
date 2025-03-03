#!/usr/bin/env python3
import asyncio
from dataclasses import dataclass
from functools import partial
from typing import Optional, Tuple

from nicegui import app, ui


@dataclass
class ToDo:
    title: str


@ui.page('/')
def main():
    def make_droppable_column(name: str) -> ui.column:
        col = ui.column().classes('bg-blue-grey-2 w-60 p-4 rounded shadow-2')
        with col:
            ui.label(name).classes('text-bold ml-1')
        col.on('dragover.prevent', partial(on_dragover, col))
        col.on('dragleave', partial(on_dragleave, col))
        col.on('drop', partial(on_drop, col, name))
        return col

    def make_draggable_card(todo: ToDo) -> ui.card:
        card = ui.card().props('draggable').classes('w-full cursor-pointer bg-grey-1')
        with card:
            ui.label(todo.title)
        card.on('dragstart', partial(on_dragstart, card, todo))
        return card

    def on_dragstart(card: ui.card, todo: ToDo) -> None:
        app.storage.tab['dragging-todo'] = (card, todo)

    def on_dragover(col: ui.column) -> None:
        col.classes(remove='bg-blue-grey-2', add='bg-blue-grey-3')

    def on_dragleave(col: ui.column) -> None:
        col.classes(remove='bg-blue-grey-3', add='bg-blue-grey-2')

    async def on_drop(tgt_col: ui.column, col_name: str) -> None:
        dragging: Optional[Tuple[ui.card, ToDo]] = app.storage.tab.get(
            'dragging-todo', None
        )
        if not dragging:
            return
        (card, todo) = dragging
        del app.storage.tab['dragging-todo']
        tgt_col.classes(remove='bg-blue-grey-3', add='bg-blue-grey-2')
        if not card.parent_slot:
            return
        src_col = card.parent_slot.parent
        if tgt_col == src_col:
            # no change, nothing to do
            return
        src_skel = ui.skeleton().classes('w-full')
        if False:
            # This might benefit from a new ui.column.replace(old_element, new_element)
            src_col.replace(card, src_skel)
        else:
            src_idx = card.parent_slot.children.index(card)
            src_skel.move(src_col, src_idx)
            card.parent_slot.children.remove(card)
        tgt_skel = ui.skeleton().classes('w-full')
        tgt_skel.move(tgt_col)

        await asyncio.sleep(1.0)

        src_col.remove(src_skel)
        if False:
            # This might benefit from a new ui.column.replace(old_element, new_element)
            tgt_col.replace(tgt_skel, card)
        else:
            tgt_idx = tgt_col.default_slot.children.index(tgt_skel)
            tgt_col.remove(tgt_skel)
            tgt_col.default_slot.children.insert(tgt_idx, card)
            card.parent_slot = tgt_col.default_slot
        ui.notify(f'"{todo.title}" is now in {col_name}')

    with ui.row():
        with make_droppable_column('Next'):
            make_draggable_card(ToDo('Provide Deployment'))
        with make_droppable_column('Doing'):
            make_draggable_card(ToDo('Improve Documentation'))
        with make_droppable_column('Done'):
            make_draggable_card(ToDo('Invent NiceGUI'))
            make_draggable_card(ToDo('Test in own Projects'))
            make_draggable_card(ToDo('Publish as Open Source'))
            make_draggable_card(ToDo('Release Native-Mode'))


ui.run()
