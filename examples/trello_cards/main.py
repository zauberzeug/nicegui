#!/usr/bin/env python3
import draganddrop as dnd

from nicegui import ui


def on_drop(card: dnd.card, location: str):
    ui.notify(f'"{card.text}" is now in {location}')


with ui.row():
    with dnd.column('Next', on_drop=lambda card: on_drop(card, 'Next')):
        dnd.card('Improve Documentation')
        dnd.card('Simplify Layouting')
        dnd.card('Provide Deployment')
    with dnd.column('Doing', on_drop=lambda card: on_drop(card, 'Doing')):
        dnd.card('Release Standalone-Mode')
    with dnd.column('Done', on_drop=lambda card: on_drop(card, 'Done')):
        dnd.card('Invent NiceGUI')
        dnd.card('Test in own Projects')
        dnd.card('Publish as Open Source')

ui.run()
