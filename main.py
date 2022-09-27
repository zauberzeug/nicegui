#!/usr/bin/env python3
import re

import docutils.core

import api_docs_and_examples
from nicegui import ui
from traffic_tracking import TrafficChard as traffic_chart


@ui.page('/', on_page_ready=api_docs_and_examples.create)
async def index():
    # add docutils css to webpage
    ui.add_head_html(docutils.core.publish_parts('', writer_name='html')['stylesheet'])
    # avoid display:block for PyPI/Docker/GitHub badges
    ui.add_head_html('<style>p a img {display: inline; vertical-align: baseline}</style>')

    ui.html(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-fork-ribbon-css/0.2.3/gh-fork-ribbon.min.css" />'
        '<style>.github-fork-ribbon:before { background-color: #999; }</style>'
        '<a class="github-fork-ribbon" href="https://github.com/zauberzeug/nicegui" data-ribbon="Fork me on GitHub" title="Fork me on GitHub">Fork me on GitHub</a>'
    )

    with ui.row().classes('flex w-full'):
        with open('README.md', 'r') as file:
            content = file.read()
            content = re.sub(r'(?m)^\<img.*\n?', '', content)
            ui.markdown(content).classes('w-6/12')

        with ui.column().classes('w-5/12 flex-center'):
            width = 450

            with ui.card(), ui.row().style(f'width:{width}px'):
                with ui.column():
                    ui.button('Click me!', on_click=lambda: output.set_text('Click'))
                    ui.checkbox('Check me!', on_change=lambda e: output.set_text('Checked' if e.value else 'Unchecked'))
                    ui.switch('Switch me!', on_change=lambda e: output.set_text(
                        'Switched' if e.value else 'Unswitched'))
                    ui.input('Text', value='abc', on_change=lambda e: output.set_text(e.value))
                    ui.number('Number', value=3.1415927, format='%.2f', on_change=lambda e: output.set_text(e.value))

                with ui.column():
                    ui.slider(min=0, max=100, value=50, step=0.1, on_change=lambda e: output.set_text(e.value))
                    ui.radio(['A', 'B', 'C'], value='A', on_change=lambda e: output.set_text(e.value)).props('inline')
                    ui.toggle(['1', '2', '3'], value='1', on_change=lambda e: output.set_text(e.value)).classes('mx-auto')
                    ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1,
                              on_change=lambda e: output.set_text(e.value)).classes('mx-auto')

                with ui.column().classes('w-24'):
                    ui.label('Output:')
                    output = ui.label('').classes('text-bold')

            with ui.row().style('margin-top: 40px'):
                traffic_chart().style(f'width:{width}px;height:250px')

ui.run()
