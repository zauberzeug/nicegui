from nicegui import ui

from . import doc


@doc.demo(ui.matplotlib)
def main_demo() -> None:
    import numpy as np

    with ui.matplotlib(figsize=(3, 2)).figure as fig:
        x = np.linspace(0.0, 5.0)
        y = np.cos(2 * np.pi * x) * np.exp(-x)
        ax = fig.gca()
        ax.plot(x, y, '-')


doc.reference(ui.matplotlib)
