#!/usr/bin/env python3
import trello

from nicegui import ui

with ui.row():
    with trello.column('Next'):
        trello.card('Improve Documentation')
        trello.card('Simplify Layouting')
        trello.card('Provide Deployment')
    with trello.column('Doing'):
        trello.card('Release Standalone-Mode')
    with trello.column('Done'):
        trello.card('Invent NiceGUI')
        trello.card('Test in own Projects')
        trello.card('Publish as Open Source')

ui.run(standalone=True)
