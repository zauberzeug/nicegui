from nicegui import ui
from nicegui.testing import Screen


def test_xterm_in_unopened_tab(screen: Screen) -> None:
    @ui.page('/')
    def page():
        with ui.tabs() as tabs:
            ui.tab('One')
            ui.tab('Two')
        with ui.tab_panels(tabs, value='One'):
            with ui.tab_panel('One'):
                ui.label('First tab')
            with ui.tab_panel('Two'):
                with ui.keep_alive():
                    terminal = ui.xterm()
        ui.button('Write', on_click=lambda: terminal.write('Hello, Terminal!'))

    screen.open('/')
    screen.click('Write')
    screen.click('Two')
    screen.should_contain('Hello, Terminal!')


def test_aggrid_get_client_data_in_closed_dialog(screen: Screen) -> None:
    data: list = []

    @ui.page('/')
    def page():
        with ui.dialog() as dialog:
            with ui.keep_alive():
                grid = ui.aggrid({'columnDefs': [{'field': 'name'}], 'rowData': [{'name': 'Alice'}, {'name': 'Bob'}]})

        @ui.button('Read').on_click
        async def _():
            data[:] = await grid.get_client_data()

        ui.button('Open', on_click=dialog.open)

    screen.open('/')
    screen.click('Read')  # without keep_alive this would silently return [] until the dialog has been opened
    screen.wait_for(lambda: data == [{'name': 'Alice'}, {'name': 'Bob'}])


def test_visible_children_render_in_place(screen: Screen) -> None:
    @ui.page('/')
    def page():
        with ui.card().classes('card'):
            with ui.keep_alive():
                ui.label('Inside keep_alive')

    screen.open('/')
    screen.should_contain('Inside keep_alive')
    assert 'Inside keep_alive' in screen.find_by_css('.card').text


def test_deletion_cleans_up_host(screen: Screen) -> None:
    wrapper: ui.keep_alive | None = None

    @ui.page('/')
    def page():
        nonlocal wrapper
        with ui.card() as card:
            with ui.keep_alive() as wrapper:
                ui.label('Inside keep_alive')
        ui.button('Drop', on_click=card.delete)

    screen.open('/')
    screen.should_contain('Inside keep_alive')
    assert wrapper is not None

    screen.click('Drop')
    screen.wait_for(lambda: wrapper.is_deleted)
    screen.wait_for(lambda: wrapper._host.is_deleted)  # pylint: disable=protected-access


def test_xterm_in_unopened_menu(screen: Screen) -> None:
    @ui.page('/')
    def page():
        with ui.button('Menu'):
            with ui.menu():
                with ui.keep_alive():
                    terminal = ui.xterm()
        ui.button('Write', on_click=lambda: terminal.write('Hello, Menu!'))

    screen.open('/')
    screen.click('Write')
    screen.click('Menu')
    screen.should_contain('Hello, Menu!')


def test_nested_keep_alive(screen: Screen) -> None:
    @ui.page('/')
    def page():
        with ui.tabs() as tabs:
            ui.tab('One')
            ui.tab('Two')
        with ui.tab_panels(tabs, value='One'):
            with ui.tab_panel('One'):
                ui.label('First tab')
            with ui.tab_panel('Two'):
                with ui.keep_alive():
                    with ui.dialog() as dialog, ui.card():
                        with ui.keep_alive():
                            terminal = ui.xterm()
                        ui.button('Close', on_click=dialog.close)
                    ui.button('Open dialog', on_click=dialog.open)
        ui.button('Write', on_click=lambda: terminal.write('Hello, Nested!'))

    screen.open('/')
    screen.click('Write')  # neither the tab panel nor the dialog have ever been opened
    screen.click('Two')
    screen.click('Open dialog')
    screen.should_contain('Hello, Nested!')


def test_inside_sub_pages_cleans_up_on_navigation(screen: Screen) -> None:
    @ui.page('/')
    @ui.page('/other')
    def index():
        ui.sub_pages({'/': home, '/other': other})

    def home():
        with ui.keep_alive():
            ui.label('Inside keep_alive')
        ui.link('Go to other', '/other')
        ui.label(f'element count: {len(ui.context.client.elements)}')

    def other():
        ui.link('Back home', '/')

    screen.open('/')
    screen.should_contain('Inside keep_alive')
    initial = screen.find('element count:').text

    screen.click('Go to other')
    screen.click('Back home')
    screen.should_contain('Inside keep_alive')
    screen.should_contain(initial)  # no orphaned host from first visit
