from nicegui import ui

from . import doc


@doc.demo(ui.tooltip)
def tooltips_demo():
    with ui.button(icon='thumb_up'):
        ui.tooltip('I like this').classes('bg-green')


@doc.demo('Tooltip method', '''
    Instead of nesting a tooltip element inside another element, you can also use the `tooltip` method.

    Note that with this method you cannot apply additional properties (props) or styling directly to the tooltip.
    If you need custom styling or properties, nest a `ui.tooltip` element instead.
''')
def tooltip_method_demo():
    ui.label('Tooltips...').tooltip('...are shown on mouse over')


@doc.demo('Tooltip with HTML', '''
    You can use HTML in tooltips by nesting a `ui.html` element.
''')
def tooltip_html_demo():
    with ui.label('HTML...'):
        with ui.tooltip():
            ui.html('<b>b</b>, <em>em</em>, <u>u</u>, <s>s</s>', sanitize=False)


@doc.demo('Tooltip with other content', '''
    Other elements like `ui.images` can also be nested inside a tooltip.
''')
def tooltip_with_other_content():
    with ui.label('Mountains...'):
        with ui.tooltip().classes('bg-transparent'):
            ui.image('https://picsum.photos/id/377/640/360').classes('w-64')


@doc.demo('Tooltip on HTML and Markdown', '''
    Some elements like `ui.html` and `ui.markdown` do not support nested elements.
    In this case, you can nest such elements inside a container element with a tooltip.
''')
def tooltip_on_html_and_markdown():
    with ui.element().tooltip('...with a tooltip!'):
        ui.html('This is <u>HTML</u>...', sanitize=False)


@doc.demo('Tooltip for the upload element', '''
    Components like `ui.upload` do not support tooltips directly.
    You can wrap them in a `ui.element` to add tooltips and props.
''')
def simple_upload_with_tooltip_demo():
    with ui.element():
        ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.file.name}')).classes('w-72')
        ui.tooltip('Upload files').props('delay=1000 transition-show=rotate')


doc.reference(ui.tooltip)
