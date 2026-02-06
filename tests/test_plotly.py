import numpy as np
import plotly.graph_objects as go

from nicegui import ui
from nicegui.testing import SharedScreen


def test_plotly(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name='Trace 1'))
        fig.update_layout(title='Test Figure')
        plot = ui.plotly(fig)

        ui.button('Add trace', on_click=lambda: (
            # test NumPy array support for value arrays
            fig.add_trace(go.Scatter(x=np.array([0, 1, 2]), y=np.array([2, 1, 0]), name='Trace 2')),
            plot.update()
        ))

    shared_screen.open('/')
    shared_screen.should_contain('Test Figure')

    shared_screen.click('Add trace')
    shared_screen.should_contain('Trace 1')
    shared_screen.should_contain('Trace 2')


def test_replace_plotly(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.plotly(go.Figure(go.Scatter(x=[1], y=[1], text=['A'], mode='text')))

        def replace():
            with container.clear():
                ui.plotly(go.Figure(go.Scatter(x=[1], y=[1], text=['B'], mode='text')))
        ui.button('Replace', on_click=replace)

    shared_screen.open('/')
    assert shared_screen.find_by_tag('text').text == 'A'

    shared_screen.click('Replace')
    shared_screen.wait(0.5)
    assert shared_screen.find_by_tag('text').text == 'B'


def test_create_dynamically(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('Create', on_click=lambda: ui.plotly(go.Figure(go.Scatter(x=[], y=[]))))

    shared_screen.open('/')
    shared_screen.click('Create')
    assert shared_screen.find_by_tag('svg')
