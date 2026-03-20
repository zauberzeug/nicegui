import random

from nicegui import ui

from .. import design as d
from ..documentation.content.sub_pages_documentation import FakeSubPages
from ..documentation.demo import demo
from .shared import section, section_heading


def create() -> None:
    """Create the demos section with tab-based interactive demos."""
    with section('demos'):
        section_heading('demos', 'See it in action.',
                        "Interactive examples that showcase NiceGUI's power and flexibility.")

        with ui.column().classes('w-full reveal'):
            tab_classes = (
                '[&_.q-focus-helper]:hidden'
                f' {d.TEXT_MUTED}'
                f' hover:text-[{d._TEXT_SECONDARY_LIGHT}] dark:hover:text-[{d._TEXT_SECONDARY_DARK}]'
                f' [&.q-tab--active]:!text-[{d.BLUE}]'
            )
            with ui.tabs().classes(f'w-full {d.BORDER_B}').props('no-caps align=left') as tabs:
                spa_tab = ui.tab('Single Page App').classes(tab_classes)
                reactive_tab = ui.tab('Reactive UI').classes(tab_classes)
                events_tab = ui.tab('Custom Events').classes(tab_classes)

            with ui.tab_panels(tabs, value=spa_tab).classes('w-full bg-transparent'):
                with ui.tab_panel(spa_tab).classes('p-0'):
                    _spa_demo()
                with ui.tab_panel(reactive_tab).classes('p-0'):
                    _reactive_demo()
                with ui.tab_panel(events_tab).classes('p-0'):
                    _event_demo()


def _demo_playground() -> ui.element:
    """Return a two-column playground container (code left, browser right)."""
    return ui.element().classes('grid grid-cols-2 gap-6 items-stretch w-full max-lg:grid-cols-1')


def _spa_demo() -> None:
    @demo
    def spa_demo():
        sub_pages = None  # HIDE

        def root():
            # ui.sub_pages({
            #     '/': table_page,
            #     '/map/{lat}/{lon}': map_page,
            # }).classes('w-full')
            nonlocal sub_pages  # HIDE
            sub_pages = FakeSubPages({'/': table_page, '/map/{lat}/{lon}': map_page}).classes('w-full')  # HIDE
            sub_pages.init()  # HIDE

        def table_page():
            ui.table(rows=[
                {'name': 'New York', 'lat': 40.7119, 'lon': -74.0027},
                {'name': 'London', 'lat': 51.5074, 'lon': -0.1278},
                {'name': 'Tokyo', 'lat': 35.6863, 'lon': 139.7722},
            ]).props('flat bordered') \
                .on('row-click',  # HIDE
                    lambda e: sub_pages._render('/map/{lat}/{lon}', lat=e.args[1]['lat'], lon=e.args[1]['lon']))  # HIDE
            #     .on('row-click', lambda e: ui.navigate.to(f'/map/{e.args[1]["lat"]}/{e.args[1]["lon"]}'))

        def map_page(lat: float, lon: float):
            ui.leaflet(center=(lat, lon), zoom=10)
            # ui.link('Back to table', '/')
            sub_pages.link('Back to table', '/')  # HIDE

        return root


def _reactive_demo() -> None:
    @demo
    def reactive_demo():
        def root():
            user_input = ui.input(value='Hello')
            ui.label().bind_text_from(user_input, 'value', reverse)

        def reverse(text: str) -> str:
            return text[::-1]

        return root


def _event_demo() -> None:
    @demo
    def event_demo():
        import time

        from nicegui import Event, app

        sensor = Event[float]()

        # @app.post('/sensor')
        def sensor_webhook(temperature: float):
            sensor.emit(temperature)

        def root():
            chart = ui.echart({
                'xAxis': {'type': 'time', 'axisLabel': {'hideOverlap': True}},
                'yAxis': {'type': 'value', 'min': 'dataMin'},
                'series': [{'type': 'line', 'data': [], 'smooth': True}],
            })

            def update_chart(temperature: float):
                data = chart.options['series'][0]['data']
                data.append([time.time(), temperature])
                if len(data) > 10:
                    data.pop(0)

            sensor.subscribe(update_chart)
            # END OF DEMO

            data = chart.options['series'][0]['data']
            data.append([time.time(), 24.0])
            ui.timer(1.0, lambda: update_chart(round(data[-1][1] + (random.random() - 0.5), 1)), immediate=False)
        app  # noqa: B018 to avoid unused import warning

        return root
