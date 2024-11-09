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


@doc.demo('Local updates', '''
    The content on a page is private to the client and has its own local element context. 
    If you have a global background process, like a websocket-based chat handler or a notification system, and you want 
    to send updates to pages instead of the global context, you need to filter for each client connected to that page.

    Here, you can use the `app.client(path="/some-path")` iterator to return all applicable clients and use their 
    context to apply updates.
''')
def local_updates():
    import time
    import asyncio
    from nicegui import ui, app, ElementFilter

    @ui.page("/time")
    def make_page():
        ui.label("Current time")
        ui.label(time.strftime('%H:%M:%S')).mark('clock')

    async def run_clock():
        """Background activity to update the label value every second."""

        def update_clock():
            # Apply updates to clients currently connected to `/time`
            for client in app.clients("/time"):
                # Enter the client content context to look-up elements by their mark and apply the update.
                # If you try to update this element without the client.content the element filter will not be able
                # to find it, since the element is local to the page context.
                with client.content:
                    for element in ElementFilter(kind=ui.label, marker='clock'):
                        element.text = time.strftime('%H:%M:%S')

        while True:
            update_clock()
            await asyncio.sleep(1)

    app.on_startup(run_clock)
    ui.run()


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


doc.reference(ElementFilter)
