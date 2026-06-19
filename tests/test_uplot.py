import numpy as np

from nicegui import ui
from nicegui.testing import Screen


def test_uplot(screen: Screen):
    @ui.page('/')
    def page():
        ui.uplot({'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}]}, [[1, 2], [3, 4]])
        x = np.arange(3)
        y = np.array([1, 4, 9])
        ui.uplot({'width': 400, 'height': 200, 'series': [{}, {'stroke': 'blue'}]}, [x, y])

    screen.open('/')
    assert len(screen.find_all_by_tag('canvas')) == 2


def test_resize_to_element(screen: Screen):
    @ui.page('/')
    def page():
        # legend disabled so the canvas fills the host exactly (see test_legend_fits_in_box otherwise)
        options = {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}], 'legend': {'show': False}}
        data = [[0, 1], [1, 2]]
        plot = ui.uplot(options, data).style('width: 400px; height: 200px')
        ui.button('Resize', on_click=lambda: plot.style('width: 600px; height: 300px'))

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == '400'
    assert canvas.get_attribute('height') == '200'

    screen.click('Resize')
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == '600'
    assert canvas.get_attribute('height') == '300'


def test_update_data_and_options(screen: Screen):
    @ui.page('/')
    def page():
        options = {'width': 400, 'height': 200, 'series': [{}, {'label': 'C', 'stroke': 'red'}]}
        data = [[0, 1], [2, 4]]
        plot = ui.uplot(options, data)

        def update():
            plot.data = [[0, 1, 2], [2, 4, 6]]
            plot.options['series'][1]['label'] = 'D'
        ui.button('Update', on_click=update)

    screen.open('/')
    legend = screen.find_by_tag('table')
    legend_html = legend.get_attribute('outerHTML')
    assert legend_html is not None and 'C' in legend_html

    screen.click('Update')
    legend = screen.find_by_tag('table')
    legend_html = legend.get_attribute('outerHTML')
    assert legend_html is not None and 'D' in legend_html


def test_custom_series_function(screen: Screen):
    @ui.page('/')
    def page():
        options = {
            'width': 400,
            'height': 200,
            'series': [
                {},
                {'stroke': 'red', 'label': 'F', ':value': '(self, v) => v == null ? "" : (v*2).toFixed(1)'},
            ],
            'legend': {'show': True},
        }
        data = [[0, 1], [2, 4]]
        ui.uplot(options, data)

    screen.open('/')
    legend = screen.find_by_tag('table')
    html = legend.get_attribute('outerHTML')
    assert html is not None and 'F' in html


def test_scale_mode_prop(screen: Screen):
    def register_page(prop):
        @ui.page(f'/{prop}')
        def _():
            options = {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}]}
            data = [[0, 1], [2, 4]]
            ui.uplot(options, data, scale_mode=prop)

    for prop in ['reset', 'preserve_zoom', 'preserve_all']:
        register_page(prop)

    for prop in ['reset', 'preserve_zoom', 'preserve_all']:
        screen.open(f'/{prop}')
        assert screen.find_by_tag('canvas')


def test_empty_data(screen: Screen):
    @ui.page('/')
    def page():
        options = {}
        data = []
        ui.uplot(options, data)

    screen.open('/')
    assert screen.find_by_tag('canvas')


def test_in_card(screen: Screen):
    @ui.page('/')
    def page():
        with ui.card().style('height: 200px; width: 600px'):
            # legend disabled so the canvas fills the card exactly (see test_legend_fits_in_box otherwise)
            options = {'series': [{}, {'stroke': 'red'}], 'legend': {'show': False}}
            data = [[0, 1], [2, 4]]
            ui.uplot(options, data).classes('w-full h-full')  # fill the card via the ResizeObserver

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('height') == '168'
    assert canvas.get_attribute('width') == '568'


def test_legend_fits_in_box(screen: Screen):
    @ui.page('/')
    def page():
        with ui.element().style('width: 400px; height: 300px'):
            options = {'width': 400, 'height': 300, 'title': 'T', 'series': [{}, {'label': 'a', 'stroke': 'red'}]}
            ui.uplot(options, [[0, 1], [2, 4]]).classes('w-full h-full')

    screen.open('/')
    screen.wait(0.5)  # let the chart reserve room for its title/legend on the next animation frame
    host_height = screen.selenium.execute_script("return document.querySelector('.nicegui-uplot').offsetHeight")
    chart_height = screen.selenium.execute_script("return document.querySelector('.nicegui-uplot .uplot').offsetHeight")
    # the whole chart (title + plot + legend) must stay within the host box instead of overflowing it
    assert chart_height <= host_height


def test_create_dynamically(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('Create', on_click=lambda: ui.uplot(
            {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}]}, [[0, 1], [1, 2]]))

    screen.open('/')
    screen.click('Create')
    assert screen.find_by_tag('canvas')


def _x_scale(screen: Screen) -> list:
    """Read the live uPlot x-scale [min, max] via the NiceGUI client's getElement() seam."""
    return screen.selenium.execute_script(
        'const u = getElement(parseInt(document.querySelector(".nicegui-uplot").id.slice(1)))._chart;'
        'return [u.scales.x.min, u.scales.x.max];')


def test_resize_after_reveal(screen: Screen):
    """A chart created in a hidden (zero-size) container must fill its box once revealed."""
    @ui.page('/')
    def page():
        with ui.expansion() as expansion:
            with ui.card().style('height: 200px; width: 600px'):
                options = {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}], 'legend': {'show': False}}
                ui.uplot(options, [[0, 1], [2, 4]]).classes('w-full h-full')
        ui.button('Open', on_click=expansion.open)

    screen.open('/')
    screen.click('Open')
    screen.wait(0.5)
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == '568'
    assert canvas.get_attribute('height') == '168'


def test_preserve_zoom_keeps_zoom_on_update(screen: Screen):
    """scale_mode='preserve_zoom' keeps a manual zoom across a data update; 'reset' recomputes it."""
    @ui.page('/{mode}')
    def page(mode: str):
        options = {'width': 400, 'height': 200, 'scales': {'x': {'time': False}}, 'series': [{}, {'stroke': 'red'}]}
        plot = ui.uplot(options, [list(range(11)), list(range(11))], scale_mode=mode)

        def update():
            plot.data = [list(range(12)), list(range(12))]
        ui.button('Update', on_click=update)

    def zoom_to_2_5():
        screen.selenium.execute_script(
            'getElement(parseInt(document.querySelector(".nicegui-uplot").id.slice(1)))'
            '._chart.setScale("x", {min: 2, max: 5});')

    screen.open('/preserve_zoom')
    screen.wait(0.3)
    zoom_to_2_5()
    assert _x_scale(screen) == [2, 5]
    screen.click('Update')
    screen.wait(0.3)
    assert _x_scale(screen) == [2, 5], 'preserve_zoom should keep the manual zoom after a data update'

    screen.open('/reset')
    screen.wait(0.3)
    zoom_to_2_5()
    screen.click('Update')
    screen.wait(0.3)
    min_x, max_x = _x_scale(screen)
    assert (min_x, max_x) != (2, 5), 'reset should recompute the scale'
    assert max_x >= 11, 'reset should fit the new full data range'


def test_recreate_preserves_container_size(screen: Screen):
    """Changing a series stroke recreates the chart; it must stay sized to its container, not options."""
    @ui.page('/')
    def page():
        with ui.card().style('height: 200px; width: 600px'):
            options = {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}], 'legend': {'show': False}}
            plot = ui.uplot(options, [[0, 1], [2, 4]]).classes('w-full h-full')

        def restyle():
            plot.options = {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'blue'}], 'legend': {'show': False}}
        ui.button('Restyle', on_click=restyle)

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == '568'
    assert canvas.get_attribute('height') == '168'

    screen.click('Restyle')
    screen.wait(0.3)
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == '568', 'recreated chart must keep its container width'
    assert canvas.get_attribute('height') == '168', 'recreated chart must keep its container height'


def test_delete_without_error(screen: Screen):
    """Deleting the chart must disconnect the ResizeObserver and not raise on either side."""
    @ui.page('/')
    def page():
        options = {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}]}
        plot = ui.uplot(options, [[0, 1], [2, 4]])
        ui.button('Delete', on_click=plot.delete)

    screen.open('/')
    assert screen.find_by_tag('canvas')
    screen.click('Delete')
    screen.wait(0.3)
    assert not screen.find_all_by_tag('canvas')
    js_errors = [log['message'] for log in screen.selenium.get_log('browser')
                 if log['level'] == 'SEVERE' and 'favicon' not in log['message']]
    assert not js_errors, js_errors
    assert not screen.caplog.records


def test_update_in_flex_container(screen: Screen):
    """A data update inside a vertical flex box must not disturb the chart's size."""
    @ui.page('/')
    def page():
        with ui.column().style('height: 300px; width: 500px'):
            options = {'series': [{}, {'stroke': 'red'}], 'legend': {'show': False}}
            plot = ui.uplot(options, [[0, 1], [2, 4]]).classes('w-full').style('flex: 1 1 0; min-height: 0')

        def update():
            plot.data = [[0, 1, 2], [2, 4, 6]]
        ui.button('Update', on_click=update)

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    width_before = canvas.get_attribute('width')
    height_before = canvas.get_attribute('height')
    assert width_before == '500'
    assert int(height_before or '0') > 0

    screen.click('Update')
    screen.wait(0.3)
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == width_before
    assert canvas.get_attribute('height') == height_before


def test_wrapping_legend_fits_in_box(screen: Screen):
    """With many series in a narrow box the legend wraps to several rows; the whole chart must still fit."""
    @ui.page('/')
    def page():
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'teal', 'brown', 'magenta']
        with ui.element().style('width: 260px; height: 320px'):
            options = {
                'width': 260,
                'height': 320,
                'title': 'wrap',
                'series': [{}] + [{'label': f'series-{i}', 'stroke': c} for i, c in enumerate(colors)],
            }
            data = [[0, 1, 2]] + [[i, i + 1, i + 2] for i in range(len(colors))]
            ui.uplot(options, data).classes('w-full h-full')

    screen.open('/')
    screen.wait(0.6)  # let the wrapped legend settle and the chart reserve room on the next frame
    host_height = screen.selenium.execute_script("return document.querySelector('.nicegui-uplot').offsetHeight")
    chart_height = screen.selenium.execute_script("return document.querySelector('.nicegui-uplot .uplot').offsetHeight")
    assert chart_height <= host_height


def test_legend_mounted_externally(screen: Screen):
    """uPlot's legend.mount relocates the legend; our resize logic then gives the whole box to the canvas."""
    @ui.page('/')
    def page():
        ui.element().classes('legend-target')
        with ui.card().style('height: 200px; width: 600px'):
            options = {
                'series': [{}, {'label': 'y', 'stroke': 'red'}],
                'legend': {':mount': '(self, el) => document.querySelector(".legend-target").appendChild(el)'},
            }
            ui.uplot(options, [[0, 1], [2, 4]]).classes('w-full h-full')

    screen.open('/')
    screen.wait(0.5)
    # the legend table is moved out of the uPlot root into the external target
    assert screen.selenium.execute_script("return document.querySelector('.legend-target table') !== null")
    assert screen.selenium.execute_script("return document.querySelector('.nicegui-uplot .uplot table') === null")
    # with the legend gone (and no title), there is no chrome to reserve, so the canvas fills the whole card
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == '568'
    assert canvas.get_attribute('height') == '168'


def test_content_sized_host_does_not_grow(screen: Screen):
    """A content-sized host must converge, not grow on every ResizeObserver cycle (the feedback loop)."""
    @ui.page('/')
    def page():
        options = {'width': 400, 'height': 200, 'title': 'T', 'series': [{}, {'label': 'y', 'stroke': 'red'}]}
        # height:auto makes the host content-sized — the configuration that could feed the observer loop
        ui.uplot(options, [[0, 1, 2], [3, 4, 5]]).style('width: 400px; height: auto')

    screen.open('/')
    screen.wait(0.8)  # allow the chrome re-measure and observer to settle
    height_1 = screen.selenium.execute_script("return document.querySelector('.nicegui-uplot').offsetHeight")
    screen.wait(1.0)
    height_2 = screen.selenium.execute_script("return document.querySelector('.nicegui-uplot').offsetHeight")
    assert height_1 == height_2, f'host kept resizing: {height_1} -> {height_2}'
    assert 0 < height_2 < 600, f'host grew unexpectedly: {height_2}'
