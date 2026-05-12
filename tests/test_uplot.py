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


def test_update_width_and_height(screen: Screen):
    @ui.page('/')
    def page():
        options = {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}]}
        data = [[0, 1], [1, 2]]
        plot = ui.uplot(options, data)

        def resize():
            plot.options['width'] = 600
            plot.options['height'] = 300
        ui.button('Resize', on_click=resize)

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
            options = {'series': [{}, {'stroke': 'red'}]}
            data = [[0, 1], [2, 4]]
            ui.uplot(options, data)

    screen.open('/')
    canvas = screen.find_by_tag('canvas')
    assert canvas.get_attribute('height') == '168'
    assert canvas.get_attribute('width') == '568'


def test_create_dynamically(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('Create', on_click=lambda: ui.uplot(
            {'width': 400, 'height': 200, 'series': [{}, {'stroke': 'red'}]}, [[0, 1], [1, 2]]))

    screen.open('/')
    screen.click('Create')
    assert screen.find_by_tag('canvas')
