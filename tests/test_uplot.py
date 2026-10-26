import numpy as np
import pytest
from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen


def test_uplot(screen: Screen):
    @ui.page('/')
    def page():
        ui.uplot({'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}]}, [[1, 2], [3, 4]])
        x = np.arange(3)
        y = np.array([1, 4, 9])
        ui.uplot({'width': 400, 'height': 200, 'series': [{}, {'stroke': 'blue'}]}, [x, y])
        ui.uplot({}, [])

    screen.open('/')
    assert len(screen.find_all_by_tag('canvas')) == 3


def test_resize_to_element(screen: Screen):
    @ui.page('/')
    def page():
        # legend disabled so the canvas fills the host exactly (see test_chart_fits_in_box otherwise)
        options = {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}], 'legend': {'show': False}}
        data = [[0, 1], [1, 2]]
        plot = ui.uplot(options, data).style('width: 400px; height: 200px')
        ui.button('Resize', on_click=lambda: plot.style('width: 600px; height: 300px'))

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == '400'
    assert canvas.get_attribute('height') == '200'

    screen.click('Resize')
    screen.wait(0.5)  # let the ResizeObserver and the next animation frame propagate the new size
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
    screen.wait(0.5)  # let the data/options update round-trip to the client
    legend = screen.find_by_tag('table')
    legend_html = legend.get_attribute('outerHTML')
    assert legend_html is not None and 'D' in legend_html


@pytest.mark.parametrize('case', ['title_and_padding', 'wrapping_legend', 'growing_legend'])
def test_chart_fits_in_box(screen: Screen, case: str):
    """The whole chart (title, plot and legend) must stay within its host box."""
    @ui.page('/')
    def page():
        if case == 'title_and_padding':
            with ui.element().style('width: 400px; height: 300px'):
                options = {'width': 400, 'height': 300, 'title': 'T', 'series': [{}, {'label': 'a', 'stroke': 'red'}]}
                ui.uplot(options, [[0, 1], [2, 4]]).classes('w-full h-full p-4 border')
        if case == 'wrapping_legend':
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
        if case == 'growing_legend':
            with ui.element().style('width: 220px; height: 300px'):
                options = {'width': 220, 'height': 300, 'scales': {'x': {'time': False}},
                           'series': [{'label': 'x'}, {'label': 'alpha'}, {'label': 'beta'}]}
                ui.uplot(options, [[0, 1], [111111111111, 2], [333333333333, 4]]).classes('w-full h-full')

    screen.open('/')
    screen.wait(0.5)
    if case == 'growing_legend':  # the live legend shows wider values without resizing the host
        ActionChains(screen.selenium).move_to_element(screen.find_by_class('u-over')).perform()
        screen.wait(0.5)
    host_right, host_bottom, chart_right, chart_bottom = screen.selenium.execute_script('''
        const host = document.querySelector('.nicegui-uplot').getBoundingClientRect();
        const chart = document.querySelector('.nicegui-uplot .uplot').getBoundingClientRect();
        return [host.right, host.bottom, chart.right, chart.bottom];
    ''')
    assert chart_right <= host_right + 1
    assert chart_bottom <= host_bottom + 1


def test_resize_after_reveal(screen: Screen):
    """A chart created in a hidden container without width/height in its options must fill its box once revealed."""
    @ui.page('/')
    def page():
        with ui.expansion() as expansion:
            with ui.card().style('height: 200px; width: 600px'):
                options = {'series': [{}, {'stroke': 'red'}], 'legend': {'show': False}}
                ui.uplot(options, [[0, 1], [2, 4]]).classes('w-full h-full')
        ui.button('Open', on_click=expansion.open)

    screen.open('/')
    screen.click('Open')
    screen.wait(0.5)
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('width') == '568'
    assert canvas.get_attribute('height') == '168'


@pytest.mark.parametrize('keep_zoom, x_scale', [
    (True, 'numeric'),
    (True, 'ordinal'),
    (False, 'numeric'),
])
def test_zoom_on_update(screen: Screen, keep_zoom: bool, x_scale: str):
    """Data updates refit the x scale, except for a manual zoom with keep_zoom=True."""
    @ui.page('/')
    def page():
        # the ordinal case also uses a custom x scale key; the ":value" function must not recreate the chart
        key = 't' if x_scale == 'ordinal' else 'x'
        options = {
            'scales': {key: {'time': False, 'distr': 2 if x_scale == 'ordinal' else 1}},
            'axes': [{'scale': key}, {}],
            'series': [{'scale': key}, {'stroke': 'red', ':value': '(self, v) => v'}],
        }
        plot = ui.uplot(options, [[1000 + 10 * i for i in range(11)], list(range(11))], keep_zoom=keep_zoom)

        def update():
            n = len(plot.data[0]) + 1
            plot.data = [[1000 + 10 * i for i in range(n)], list(range(n))]
        ui.button('Update', on_click=update)

    def x_range() -> list:
        return screen.selenium.execute_script('''
            const u = getElement(document.querySelector('.nicegui-uplot')).chart;
            const scale = u.scales[u.series[0].scale];
            return [scale.min, scale.max];
        ''')

    full_range = [0, 11] if x_scale == 'ordinal' else [1000, 1110]
    zoom_range = [2, 5] if x_scale == 'ordinal' else [1020, 1050]

    screen.open('/')
    screen.wait(0.3)
    screen.click('Update')
    screen.wait(0.3)
    assert x_range() == full_range, 'an update without zoom should fit the new data'

    screen.selenium.execute_script(f'''
        const u = getElement(document.querySelector('.nicegui-uplot')).chart;
        u.setScale(u.series[0].scale, {{min: {zoom_range[0]}, max: {zoom_range[1]}}});
    ''')
    screen.wait(0.3)
    assert x_range() == zoom_range
    screen.click('Update')
    screen.wait(0.3)
    if keep_zoom:
        assert x_range() == zoom_range, 'keep_zoom should keep the manual zoom'
    else:
        assert x_range() == [full_range[0], full_range[1] + (1 if x_scale == 'ordinal' else 10)], \
            'keep_zoom=False should fit the new data'


def test_redraw_when_keeping_scales(screen: Screen):
    """Data updates must redraw the canvas even when the scales are kept (uPlot's setData(data, false) does not)."""
    @ui.page('/')
    def page():
        options = {'width': 400, 'height': 200, 'scales': {'x': {'time': False}}, 'series': [{}, {'stroke': 'red'}]}
        plot = ui.uplot(options, [[0, 1, 2], [0, 1, 2]])
        ui.button('Update', on_click=lambda: setattr(plot, 'data', [[0, 1, 2], [2, 1, 0]]))

    def canvas_image() -> str:
        return screen.selenium.execute_script('return document.querySelector(".nicegui-uplot canvas").toDataURL();')

    screen.open('/')
    screen.wait(0.3)
    screen.selenium.execute_script('''
        getElement(document.querySelector('.nicegui-uplot')).chart.setScale('x', {min: 0.5, max: 1.5});
    ''')  # zoom in, so the update keeps the scales
    screen.wait(0.3)
    image_before = canvas_image()
    screen.click('Update')
    screen.wait(0.3)
    assert canvas_image() != image_before, 'the canvas should show the new data'


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
    screen.wait(0.8)  # allow the resize observer to settle
    # with no box to fit into, the plot must keep the configured height instead of absorbing the chrome
    assert screen.find_by_tag('canvas').get_attribute('height') == '200'
    height_1 = screen.selenium.execute_script("return document.querySelector('.nicegui-uplot').offsetHeight")
    screen.wait(1.0)
    height_2 = screen.selenium.execute_script("return document.querySelector('.nicegui-uplot').offsetHeight")
    assert height_1 == height_2, f'host height should stay constant once settled: {height_1} -> {height_2}'
    assert 0 < height_2 < 600, f'host should stay content-sized: {height_2}'


def test_dark_mode(screen: Screen):
    """Axis labels follow the page's text color, also when the dark mode is toggled."""
    @ui.page('/')
    def page():
        dark = ui.dark_mode(True)
        ui.uplot({'scales': {'x': {'time': False}}, 'series': [{}, {'stroke': 'red'}]}, [[0, 1, 2], [1, 3, 2]])
        ui.button('Light', on_click=dark.disable)

    def count_white_and_black_pixels() -> list[int]:
        return screen.selenium.execute_script('''
            const canvas = document.querySelector('.nicegui-uplot canvas');
            const data = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data;
            let white = 0, black = 0;
            for (let i = 0; i < data.length; i += 4) {
                if (data[i + 3] < 200) continue;
                if (data[i] > 200 && data[i + 1] > 200 && data[i + 2] > 200) white++;
                if (data[i] < 60 && data[i + 1] < 60 && data[i + 2] < 60) black++;
            }
            return [white, black];
        ''')

    screen.open('/')
    screen.wait(0.5)
    white, black = count_white_and_black_pixels()
    assert white > black, 'axis labels should be light in dark mode'

    screen.click('Light')
    screen.wait(0.5)
    white, black = count_white_and_black_pixels()
    assert black > white, 'axis labels should be dark in light mode'
