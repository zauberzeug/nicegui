#!/usr/bin/env python3
import re

import markdown2

import api_docs_and_examples
import traffic_tracking
from nicegui import ui
from nicegui.elements.markdown import Markdown

with open('README.md') as f:
    content = f.read()
    content = re.sub(r'(?m)^\<img.*\n?', '', content)
    # change absolute link on GitHub to relative link
    content = content.replace('(https://nicegui.io/reference)', '(reference)')
    README = Markdown.apply_tailwind(markdown2.markdown(content, extras=['fenced-code-blocks']))


async def go_to_anchor() -> None:
    # NOTE because the docs are added after initial page load, we need to manually trigger the jump to the anchor
    await ui.run_javascript('''
        parts = document.URL.split("#");
        console.log(parts);
        if (parts.length > 1) {
            console.log(window.location);
            window.location = parts[0] + "reference#" + parts[1];
            console.log(window.location);
        }
    ''')


@ui.page('/', on_connect=traffic_tracking.on_connect, on_page_ready=go_to_anchor)
async def index():
    # avoid display:block for PyPI/Docker/GitHub badges
    ui.add_head_html('<style>p a img {display: inline; vertical-align: baseline}</style>')

    ui.html(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-fork-ribbon-css/0.2.3/gh-fork-ribbon.min.css" />'
        '<style>.github-fork-ribbon:before { background-color: #999; }</style>'
        '<a class="github-fork-ribbon" href="https://github.com/zauberzeug/nicegui" data-ribbon="Fork me on GitHub" title="Fork me on GitHub">Fork me on GitHub</a>'
    )

    installation_start = README.find('<h2 class="text-4xl mb-3 mt-5">Installation</h2>')
    documentation_start = README.find('The API reference is hosted at')
    assert installation_start >= 0
    assert documentation_start >= 0

    with ui.row().classes('flex w-full'):
        ui.html(README[:installation_start]).classes('w-6/12')

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
                traffic_tracking.chart().style(f'width:{width}px;height:250px')

    ui.html(README[installation_start:documentation_start])

    api_docs_and_examples.create_intro()
    with ui.row().style('background-color: #e8f0fa; width: 100%; margin: 1em 0; padding: 1em 1em 0.5em 1em; font-size: large'):
        ui.markdown('See the [API reference](/reference) for many more interactive examples!')

    ui.html(README[documentation_start:])


@ui.page('/reference')
def reference():
    api_docs_and_examples.create_full()


ui.run()
