import numpy as np
import pytest
from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen

CANVAS_SIZE = "(canvas => [canvas.width, canvas.height])(document.querySelector('.nicegui-uplot canvas'))"
CHART = "getElement(document.querySelector('.nicegui-uplot')).chart"
CHART_FITS = '''(() => {
    const host = document.querySelector('.nicegui-uplot').getBoundingClientRect();
    const chart = document.querySelector('.nicegui-uplot .uplot').getBoundingClientRect();
    return chart.right <= host.right + 1 && chart.bottom <= host.bottom + 1;
})()'''


def test_uplot(screen: Screen):
    @ui.page('/')
    def page():
        ui.uplot({'series': [{}, {'stroke': 'red'}]}, [[1, 2], [3, 4]])
        ui.uplot({'series': [{}, {'stroke': 'blue'}]}, [np.arange(3), np.array([1, 4, 9])])
        ui.uplot({}, [])

    screen.open('/')
    assert len(screen.find_all_by_tag('canvas')) == 3


def test_resize_to_element(screen: Screen):
    """The chart follows its element's size, also when changed options recreate it."""
    @ui.page('/')
    def page():
        # legend disabled so the canvas fills the host exactly (see test_chart_fits_in_box otherwise)
        options = {'series': [{}, {'stroke': 'red'}], 'legend': {'show': False}}
        plot = ui.uplot(options, [[0, 1], [1, 2]]).style('width: 400px; height: 200px')
        ui.button('Resize', on_click=lambda: plot.style('width: 600px; height: 300px'))
        ui.button('Restyle', on_click=lambda: plot.options['series'][1].update(stroke='blue'))

    screen.open('/')
    screen.wait_for_js(CANVAS_SIZE, [400, 200])

    screen.click('Resize')
    screen.wait_for_js(CANVAS_SIZE, [600, 300])

    screen.click('Restyle')
    screen.wait_for_js(f'{CHART}.series[1].stroke()', 'blue')
    assert screen.selenium.execute_script(f'return {CANVAS_SIZE}') == [600, 300], 'recreated chart keeps its size'


@pytest.mark.parametrize('mode', [1, 2])
def test_update_data_and_options(screen: Screen, mode: int):
    """Mode 2 (facets, e.g. for scatter plots) has no shared x values, so data[0] is None."""
    @ui.page('/')
    def page():
        options = {'mode': mode, 'scales': {'x': {'time': False}}, 'series': [{}, {'label': 'C', 'stroke': 'red'}]}
        data = [[0, 1], [2, 4]] if mode == 1 else [None, [[0, 1], [2, 4]]]
        plot = ui.uplot(options, data)

        def update_data():
            plot.data = [[0, 1, 2], [2, 4, 6]] if mode == 1 else [None, [[0, 1, 2], [2, 4, 6]]]
        ui.button('Update data', on_click=update_data)

        def update_options():
            plot.options['series'][1]['label'] = 'D'
        ui.button('Update options', on_click=update_options)

    screen.open('/')
    screen.wait_for_js("document.querySelector('.u-legend').innerText.includes('C')", True)

    screen.click('Update data')
    screen.wait_for_js(f'{CHART}.data[0].length' if mode == 1 else f'{CHART}.data[1][0].length', 3)

    screen.click('Update options')
    screen.wait_for_js("document.querySelector('.u-legend').innerText.includes('D')", True)


@pytest.mark.parametrize('case', ['title_padding_and_wrapping_legend', 'growing_legend'])
def test_chart_fits_in_box(screen: Screen, case: str):
    """The whole chart (title, plot and legend) must stay within its host box."""
    @ui.page('/')
    def page():
        if case == 'title_padding_and_wrapping_legend':
            colors = ['red', 'blue', 'green', 'orange', 'purple', 'teal', 'brown', 'magenta']
            with ui.element().style('width: 260px; height: 320px'):
                options: dict = {
                    'title': 'T',
                    'series': [{}] + [{'label': f'series-{i}', 'stroke': c} for i, c in enumerate(colors)],
                }
                data = [[0, 1, 2]] + [[i, i + 1, i + 2] for i in range(len(colors))]
                ui.uplot(options, data).classes('w-full h-full p-4 border')
        if case == 'growing_legend':
            with ui.element().style('width: 220px; height: 300px'):
                options = {'scales': {'x': {'time': False}},
                           'series': [{'label': 'x'}, {'label': 'alpha'}, {'label': 'beta'}]}
                ui.uplot(options, [[0, 1], [111111111111, 2], [333333333333, 4]]).classes('w-full h-full')

    screen.open('/')
    screen.wait_for_js(CHART_FITS, True)
    if case == 'growing_legend':  # the live legend shows wider values without resizing the host
        ActionChains(screen.selenium).move_to_element(screen.find_by_class('u-over')).perform()
        screen.wait(0.5)  # the legend grows without a signal to wait for
        assert screen.selenium.execute_script(f'return {CHART_FITS}')


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
    screen.wait_for_js(CANVAS_SIZE, [568, 168])


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

    x_range = f'(u => [u.scales[u.series[0].scale].min, u.scales[u.series[0].scale].max])({CHART})'
    n_points = f'{CHART}.data[0].length'
    full_range = [0, 11] if x_scale == 'ordinal' else [1000, 1110]
    zoom_range = [2, 5] if x_scale == 'ordinal' else [1020, 1050]

    screen.open('/')
    screen.wait_for_js(n_points, 11)
    screen.click('Update')
    screen.wait_for_js(n_points, 12)
    screen.wait_for_js(x_range, full_range)  # an update without zoom fits the new data

    screen.selenium.execute_script(
        f'(u => u.setScale(u.series[0].scale, {{min: {zoom_range[0]}, max: {zoom_range[1]}}}))({CHART})')
    screen.wait_for_js(x_range, zoom_range)
    screen.click('Update')
    screen.wait_for_js(n_points, 13)
    if keep_zoom:
        screen.wait_for_js(x_range, zoom_range)
    else:
        screen.wait_for_js(x_range, [full_range[0], full_range[1] + (1 if x_scale == 'ordinal' else 10)])


def test_redraw_when_keeping_scales(screen: Screen):
    """Data updates must redraw the canvas even when the scales are kept (uPlot's setData(data, false) does not)."""
    @ui.page('/')
    def page():
        options = {'scales': {'x': {'time': False}}, 'series': [{}, {'stroke': 'red'}]}
        plot = ui.uplot(options, [[0, 1, 2], [0, 1, 2]])
        ui.button('Update', on_click=lambda: setattr(plot, 'data', [[0, 1, 2], [2, 1, 0]]))

    def canvas_image() -> str:
        return screen.selenium.execute_script('return document.querySelector(".nicegui-uplot canvas").toDataURL();')

    screen.open('/')
    screen.wait_for_js(f'{CHART}.data[0].length', 3)
    # zoom in, so the update keeps the scales
    screen.selenium.execute_script(f"{CHART}.setScale('x', {{min: 0.5, max: 1.5}})")
    screen.wait_for_js(f'{CHART}.scales.x.min', 0.5)
    image_before = canvas_image()
    screen.click('Update')
    screen.wait_for(lambda: canvas_image() != image_before)  # the canvas shows the new data


def test_delete_without_error(screen: Screen):
    """Deleting the chart removes its canvas without errors."""
    @ui.page('/')
    def page():
        options = {'series': [{}, {'stroke': 'red'}]}
        plot = ui.uplot(options, [[0, 1], [2, 4]])
        ui.button('Delete', on_click=plot.delete)

    screen.open('/')
    assert screen.find_by_tag('canvas')
    screen.click('Delete')
    screen.wait_for_js("document.querySelector('canvas') === null", True)


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
    screen.wait_for_js(f'{CANVAS_SIZE}[0]', 500)
    size_before = screen.selenium.execute_script(f'return {CANVAS_SIZE}')
    assert size_before[1] > 0

    screen.click('Update')
    screen.wait_for_js(f'{CHART}.data[0].length', 3)
    screen.wait(0.2)  # give a size change the chance to happen
    assert screen.selenium.execute_script(f'return {CANVAS_SIZE}') == size_before


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
    # the legend table is moved out of the uPlot root into the external target
    screen.wait_for_js("document.querySelector('.legend-target table') !== null", True)
    assert screen.selenium.execute_script("return document.querySelector('.nicegui-uplot .uplot table') === null")
    # with the legend gone (and no title), there is no chrome to reserve, so the canvas fills the whole card
    screen.wait_for_js(CANVAS_SIZE, [568, 168])


def test_dark_mode(screen: Screen):
    """Axis labels follow the page's text color, also when the dark mode is toggled."""
    @ui.page('/')
    def page():
        dark = ui.dark_mode(True)
        ui.uplot({'scales': {'x': {'time': False}}, 'series': [{}, {'stroke': 'red'}]}, [[0, 1, 2], [1, 3, 2]])
        ui.button('Light', on_click=dark.disable)

    def mostly_light() -> bool:
        return screen.selenium.execute_script('''
            const canvas = document.querySelector('.nicegui-uplot canvas');
            if (!canvas) return false;
            const data = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data;
            let white = 0, black = 0;
            for (let i = 0; i < data.length; i += 4) {
                if (data[i + 3] < 200) continue;
                if (data[i] > 200 && data[i + 1] > 200 && data[i + 2] > 200) white++;
                if (data[i] < 60 && data[i + 1] < 60 && data[i + 2] < 60) black++;
            }
            return white > black;
        ''')

    screen.open('/')
    screen.wait_for(mostly_light)  # axis labels are light in dark mode

    screen.click('Light')
    screen.wait_for(lambda: not mostly_light())  # axis labels are dark in light mode
