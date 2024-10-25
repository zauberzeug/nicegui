from . import (
    chat_message_documentation,
    doc,
    element_documentation,
    html_documentation,
    label_documentation,
    link_documentation,
    markdown_documentation,
    mermaid_documentation,
    restructured_text_documentation,
)

doc.title('*Text* Elements')

doc.intro(label_documentation)
doc.intro(link_documentation)
doc.intro(chat_message_documentation)
doc.intro(element_documentation)
doc.intro(markdown_documentation)
doc.intro(restructured_text_documentation)
doc.intro(mermaid_documentation)
doc.intro(html_documentation)


@doc.demo('Other HTML Elements', '''
    There is an `html` module that allows you to insert other HTML elements like `<span>`, `<div>`, `<p>`, etc.
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
