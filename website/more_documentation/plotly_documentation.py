from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    import plotly.graph_objects as go

    fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    ui.plotly(fig).classes('w-full h-40')


def more() -> None:
    @text_demo('Plot updates', '''
        This demo shows how to update the plot in real time.
        Click the button to add a new trace to the plot.
        To send the new plot to the browser, make sure to explicitly call `plot.update()` or `ui.update(plot)`.
    ''')
    def plot_updates():
        import numpy as np
        import plotly.graph_objects as go

        fig = go.Figure()
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        plot = ui.plotly(fig).classes('w-full h-40')

        def add_trace():
            fig.add_trace(go.Scatter(x=np.arange(10), y=np.random.randn(10)))
            plot.update()

        ui.button('Add trace', on_click=add_trace)
