import random
from typing import Callable

from nicegui import ui

from ..style import subheading
from .content.sub_pages_documentation import FakeSubPages
from .demo import demo


def create_intro() -> None:
    @_main_page_demo('Single Page App', '''
        Build applications with fast client-side routing using [`ui.sub_pages`](/documentation/sub_pages) and a `root` function as single entry point.
        For each visitor, the `root` function is executed and generates the interface.
        [`ui.link`](/documentation/link) and [`ui.navigate`](/documentation/navigate) can be used to navigate to other sub pages.

        If you do not want a Single Page App, you can also use [`@ui.page('/your/path')`](/documentation/page) to define standalone content available at a specific path.
    ''')
    def spa_demo():
        def root():
            # ui.link.default_classes('no-underline text-white')
            # with ui.header():
            #     ui.link('Home', '/')
            #     ui.link('About', '/about')
            # ui.sub_pages({
            #     '/': home_page,
            #     '/about': about_page,
            # })
            ui.context.slot_stack[-1].parent.classes(remove='p-4')  # HIDE
            sub_pages = FakeSubPages({'/': home_page, '/about': about_page}).classes('mx-4')  # HIDE
            with ui.row().classes('bg-primary w-full p-4'):  # HIDE
                sub_pages.link('Home', '/').classes('no-underline text-white')  # HIDE
                sub_pages.link('About', '/about').classes('no-underline text-white')  # HIDE
            sub_pages.init()  # HIDE

        def home_page():
            ui.label('Home page').classes('text-2xl')

        def about_page():
            ui.label('About page').classes('text-2xl')

        return root

    @_main_page_demo('Reactive Transformations', '''
        Create real-time interfaces with automatic updates.
        Type and watch text flow in both directions.
        When input changes, the [binding](/documentation/section_binding_properties) transforms the text with a custom python function and updates the label.
    ''')
    def binding_demo():
        def root():
            with ui.column():
                user_input = ui.input(value='Hello')
                ui.label().bind_text_from(user_input, 'value', reverse)

        def reverse(text: str) -> str:
            return text[::-1]

        return root

    @_main_page_demo('Event System', '''
        Use an [Event](/documentation/event) to trigger actions and pass data.
        Here we have an IoT temperature sensor submitting its readings to a [FastAPI endpoint](/documentation/section_pages_routing#api_responses) with path `/sensor`.
        If a new value arrives, it emits an event for the chart to be updated.
    ''')
    def event_system_demo():
        from datetime import datetime

        from nicegui import Event, app, ui

        sensor = Event[float]()

        # @app.get('/sensor')
        def sensor_webhook(temperature: float):
            sensor.emit(temperature)

        def root():
            chart = ui.echart({
                'xAxis': {'type': 'time', 'axisLabel': {'hideOverlap': True}},
                'yAxis': {'type': 'value', 'min': 'dataMin'},
                'series': [{'type': 'line', 'data': [], 'smooth': True}],
            })
            data = chart.options['series'][0]['data']

            def update_chart(temperature: float):
                data.append([datetime.now().timestamp() * 1000, temperature])
                if len(data) > 10:
                    data.pop(0)

            sensor.subscribe(update_chart)
            #
            # END OF DEMO

            data.append([datetime.now().timestamp() * 1000, 24.0])
            ui.timer(1.0, lambda: update_chart(round(data[-1][1] + (random.random() - 0.5), 1)), immediate=False)
        app  # noqa: B018 to avoid unused import warning

        return root


def _main_page_demo(title: str, explanation: str) -> Callable:
    def decorator(f: Callable) -> Callable:
        subheading(title)
        ui.markdown(explanation).classes('bold-links arrow-links')
        return demo(f)
    return decorator
