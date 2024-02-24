from nicegui import ui

from . import doc


@doc.demo(ui.html)
def main_demo() -> None:
    ui.html('This is <strong>HTML</strong>.')


@doc.demo('Producing in-line elements', '''
    Use the `tag` parameter to produce something other than a div.
''')
def demo_inline() -> None:
    ui.html('This is rendered as a paragraph.', tag='p')


doc.reference(ui.html)
