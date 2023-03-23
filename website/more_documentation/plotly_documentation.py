from nicegui import ui


def main_demo() -> None:
    import plotly.graph_objects as go

    fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    ui.plotly(fig).classes('w-full h-40')
