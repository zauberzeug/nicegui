#!/usr/bin/env python3
import website.api_docs_and_examples as api_docs_and_examples
from nicegui import ui


@ui.page('/')
async def index():
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    api_docs_and_examples.create_intro()


@ui.page('/reference')
def reference():
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1" />')
    api_docs_and_examples.create_full()


ui.run()
