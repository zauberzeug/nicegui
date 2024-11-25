from nicegui import ui

from . import doc


@doc.demo(ui.html)
def main_demo() -> None:
    ui.html('This is <strong>HTML</strong>.')


@doc.demo('Producing in-line elements', '''
    Use the `tag` parameter to produce something other than a div.
''')
def demo_inline() -> None:
    ui.html('This is <u>emphasized</u>.', tag='em')


@doc.demo('Other HTML Elements', '''
    There is also an `html` module that allows you to insert other HTML elements like `<span>`, `<div>`, `<p>`, etc.
    It is equivalent to using the `ui.element` method with the `tag` argument.

    Like with any other element, you can add classes, style, props, tooltips and events.
    One convenience is that the keyword arguments are automatically added to the element's `props` dictionary.
''')
def other_html_elements():
    from nicegui import html, ui

    with html.section().style('font-size: 120%'):
        html.strong('This is bold.') \
            .classes('cursor-pointer') \
            .on('click', lambda: ui.notify('Bold!'))
        html.hr()
        html.em('This is italic.').tooltip('Nice!')
        with ui.row():
            html.img().props('src=https://placehold.co/60')
            html.img(src='https://placehold.co/60')


doc.reference(ui.html)
