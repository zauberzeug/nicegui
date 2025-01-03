from nicegui import ElementFilter, ui

from . import doc


@doc.demo(ElementFilter)
def main_demo() -> None:
    from nicegui import ElementFilter

    with ui.card():
        ui.button('button A')
        ui.label('label A')

    with ui.card().mark('important'):
        ui.button('button B')
        ui.label('label B')

    ElementFilter(kind=ui.label).within(marker='important').classes('text-xl')


@doc.demo('Find all elements with text property', '''
    The `text` property is provided by a mixin called `TextElement`.
    If we filter by such a mixin, the ElementFilter itself will provide a typed iterable.
''')
def text_element() -> None:
    from nicegui import ElementFilter
    from nicegui.elements.mixins.text_element import TextElement

    with ui.card():
        ui.button('button')
        ui.icon('home')
        ui.label('label A')
        ui.label('label B')
        ui.html('HTML')

    # ui.label(', '.join(b.text for b in ElementFilter(kind=TextElement)))
    # END OF DEMO
    ui.label(', '.join(b.text for b in ElementFilter(kind=TextElement, local_scope=True)))


@doc.demo('Markers', '''
    Markers are a simple way to tag elements with a string which can be queried by an `ElementFilter`.
''')
def marker_demo() -> None:
    from nicegui import ElementFilter

    with ui.card().mark('red'):
        ui.label('label A')
    with ui.card().mark('strong'):
        ui.label('label B')
    with ui.card().mark('red strong'):
        ui.label('label C')

    # ElementFilter(marker='red').classes('bg-red-200')
    # ElementFilter(marker='strong').classes('text-bold')
    # ElementFilter(marker='red strong').classes('bg-red-600 text-white')
    # END OF DEMO
    ElementFilter(marker='red', local_scope=True).classes('bg-red-200')
    ElementFilter(marker='strong', local_scope=True).classes('text-bold')
    ElementFilter(marker='red strong', local_scope=True).classes('bg-red-600 text-white')


@doc.demo('Find elements on other pages', '''
    You can use the `app.clients` iterator to apply the element filter to all clients of a specific page.
''')
def multicasting():
    from nicegui import app
    import time

    @ui.page('/log')
    def page():
        ui.log()

    def log_time():
        for client in app.clients('/log'):
            with client:
                for log in ElementFilter(kind=ui.log):
                    log.push(f'{time.strftime("%H:%M:%S")}')

    ui.button('Log current time', on_click=log_time)
    ui.link('Open log', '/log', new_tab=True)


doc.reference(ElementFilter)
