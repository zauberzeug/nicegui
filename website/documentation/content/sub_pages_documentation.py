from nicegui import ui

from . import doc


@doc.demo('Sub Pages', '''
    Sub pages provide url based navigation between different views.
    This allows you to easily build a single page application (SPA).
    The `ui.sub_pages` element itself functions as the container for the currently active sub page.
    You only need to provide the routes for each view builder function.
    NiceGUI takes care of replacing the content without triggering a full page reload when the url changes.
    The `ui.sub_pages` element can be used as a context manager to automatically navigate to the correct sub page when the context is entered or exited.
''')
def main_demo() -> None:
    from uuid import uuid4
    # @ui.page('/')
    # @ui.page('/{_:path}')
    # def index():
    #     ui.label(f'This id {str(uuid4())[:6]} changes only on reload')
    #     ui.separator()
    #     ui.sub_pages({'/': child, '/other': child2})
    location = 'section_pages_routing' if 'section_pages_routing' in ui.context.client.request.url.path else 'sub_pages'  # HIDE

    def child():
        ui.label('Main page content')
        # ui.link('Go to other page', '/other')
        ui.link('Go to other page', f'/documentation/{location}/other')  # HIDE

    def child2():
        ui.label('Another page content')
        # ui.link('Go to main page', '/')
        ui.link('Go to main page', f'/documentation/{location}')  # HIDE

    # END OF DEMO
    ui.label(f'This id {str(uuid4())[:6]} changes only on reload')
    ui.separator()
    ui.sub_pages({'/': child, '/other': child2}, root_path=f'/documentation/{location}')
