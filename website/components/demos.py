import random
import time

from nicegui import ui

from .shared import browser_window, code_window, section, section_heading


def create() -> None:
    """Create the demos section with tab-based interactive demos."""
    with section('demos'):
        section_heading('demos', 'See it in action.',
                        "Interactive examples that showcase NiceGUI's power and flexibility.")

        with ui.column().classes('w-full mo-reveal'):
            with ui.tabs().classes('mo-demo-tabs-bar').props('no-caps') as tabs:
                spa_tab = ui.tab('Single Page App')
                reactive_tab = ui.tab('Reactive UI')
                events_tab = ui.tab('Custom Events')

            with ui.tab_panels(tabs, value=spa_tab).classes('w-full'):
                with ui.tab_panel(spa_tab).classes('p-0'):
                    _spa_demo()
                with ui.tab_panel(reactive_tab).classes('p-0'):
                    _reactive_demo()
                with ui.tab_panel(events_tab).classes('p-0'):
                    _event_demo()


def _demo_playground() -> ui.element:
    """Return a two-column playground container (code left, browser right)."""
    return ui.element('div').classes('mo-demo-playground')


def _spa_demo() -> None:
    with _demo_playground():
        code_window('main.py', 'description', (
            '<span class="kw">from</span> nicegui <span class="kw">import</span> ui\n'
            '\n'
            '<span class="kw">with</span> ui.sub_pages(<span class="str">\'/\'</span>):\n'
            '    <span class="kw">with</span> ui.page(<span class="str">\'/\'</span>):\n'
            '        ui.label(<span class="str">\'Home\'</span>)\n'
            '        ui.link(<span class="str">\'Go to about\'</span>, <span class="str">\'/about\'</span>)\n'
            '\n'
            '    <span class="kw">with</span> ui.page(<span class="str">\'/about\'</span>):\n'
            '        ui.label(<span class="str">\'About page\'</span>)\n'
            '        ui.link(<span class="str">\'Go home\'</span>, <span class="str">\'/\'</span>)\n'
            '\n'
            'ui.run()'
        ))
        with browser_window():
            with ui.column().classes('mo-browser-content'):
                ui.label('Home').classes('text-xl font-medium mb-3')
                ui.link('Go to about \u2192', '#').style('color: var(--mo-brand-blue)')


def _reactive_demo() -> None:
    with _demo_playground():
        code_window('main.py', 'description', (
            '<span class="kw">from</span> nicegui <span class="kw">import</span> ui\n'
            '\n'
            'user_input = ui.input(value=<span class="str">\'Hello\'</span>)\n'
            'ui.label().bind_text_from(\n'
            '    user_input, <span class="str">\'value\'</span>, reverse\n'
            ')\n'
            '\n'
            '<span class="kw">def</span> <span class="fn">reverse</span>(text: str) -> str:\n'
            '    <span class="kw">return</span> text[::-<span class="num">1</span>]\n'
            '\n'
            'ui.run()'
        ))
        with browser_window():
            with ui.column().classes('mo-browser-content'):
                user_input = ui.input(value='Hello').classes('w-full')
                result = ui.label('olleH').classes('text-lg mt-2')
                user_input.on('update:model-value', lambda e: result.set_text(e.args[::-1]))


def _event_demo() -> None:
    with _demo_playground():
        code_window('main.py', 'description', (
            '<span class="kw">from</span> nicegui <span class="kw">import</span> Event, app, ui\n'
            '\n'
            'sensor = Event[float]()\n'
            '\n'
            '<span class="op">@</span>app.post(<span class="str">\'/sensor\'</span>)\n'
            '<span class="kw">def</span> <span class="fn">sensor_webhook</span>(temperature: float):\n'
            '    sensor.emit(temperature)\n'
            '\n'
            'chart = ui.echart({...})\n'
            '\n'
            '<span class="kw">def</span> <span class="fn">update_chart</span>(temperature: float):\n'
            '    data = chart.options[<span class="str">\'series\'</span>][<span class="num">0</span>]'
            '[<span class="str">\'data\'</span>]\n'
            '    data.append([time.time(), temperature])\n'
            '\n'
            'sensor.subscribe(update_chart)\n'
            'ui.run()'
        ))
        with browser_window():
            with ui.column().classes('mo-browser-content'):
                chart = ui.echart({
                    'xAxis': {'type': 'time', 'axisLabel': {'hideOverlap': True}},
                    'yAxis': {'type': 'value', 'min': 'dataMin'},
                    'series': [{'type': 'line', 'data': [], 'smooth': True}],
                }).classes('w-full h-48')
                data = chart.options['series'][0]['data']
                data.append([time.time() * 1000, 24.0])

                def add_point() -> None:
                    d = chart.options['series'][0]['data']
                    d.append([time.time() * 1000, round(d[-1][1] + (random.random() - 0.5), 1)])
                    if len(d) > 10:
                        d.pop(0)
                    chart.update()
                ui.timer(1.5, add_point)
