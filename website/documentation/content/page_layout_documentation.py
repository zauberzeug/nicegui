from nicegui import ui

from . import doc


@doc.demo('Page Layout', '''
    With `ui.header`, `ui.footer`, `ui.left_drawer` and `ui.right_drawer` you can add additional layout elements to a page.
    The `fixed` argument controls whether the element should scroll or stay fixed on the screen.
    The `top_corner` and `bottom_corner` arguments indicate whether a drawer should expand to the top or bottom of the page.
    See <https://quasar.dev/layout/header-and-footer> and <https://quasar.dev/layout/drawer> for more information about possible props.
    With `ui.page_sticky` you can place an element "sticky" on the screen.
    See <https://quasar.dev/layout/page-sticky> for more information.
''')
def page_layout_demo():
    @ui.page('/page_layout')
    def page_layout():
        ui.label('CONTENT')
        [ui.label(f'Line {i}') for i in range(100)]
        with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
            ui.label('HEADER')
            ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
            ui.label('LEFT DRAWER')
        with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
            ui.label('RIGHT DRAWER')
        with ui.footer().style('background-color: #3874c8'):
            ui.label('FOOTER')

    ui.link('show page with fancy layout', page_layout)


doc.reference(ui.header, title='Reference for ui.header')
doc.reference(ui.left_drawer, title='Reference for ui.left_drawer')
doc.reference(ui.right_drawer, title='Reference for ui.right_drawer')
doc.reference(ui.footer, title='Reference for ui.footer')
doc.reference(ui.page_sticky, title='Reference for ui.page_sticky')
