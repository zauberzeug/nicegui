import plotly.express as px
import plotly.graph_objects as go

from nicegui import ui

from .screen import Screen


def test_plotly(screen: Screen):
    fig = px.scatter(x=[1, 2, 3], y=[1, 2, 3], title='Test')
    plot = ui.plotly(fig)

    ui.button('Add trace', on_click=lambda: (
        fig.add_trace(go.Scatter(x=[0, 1, 2], y=[2, 1, 0], name='New trace')),
        plot.update()
    ))

    screen.open('/')
    screen.should_contain('Test')

    screen.click('Add trace')
    screen.should_contain('New trace')
