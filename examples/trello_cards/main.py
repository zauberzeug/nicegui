#!/usr/bin/env python3
import draganddrop as dnd

from nicegui import ui

with ui.row():
    with dnd.column('Next'):
        dnd.card('Improve Documentation')
        dnd.card('Simplify Layouting')
        dnd.card('Provide Deployment')
    with dnd.column('Doing'):
        dnd.card('Release Standalone-Mode')
    with dnd.column('Done'):
        dnd.card('Invent NiceGUI')
        dnd.card('Test in own Projects')
        dnd.card('Publish as Open Source')

ui.run(standalone=True)
