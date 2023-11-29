from nicegui import ui

from . import doc


@doc.demo(ui.pyplot)
def main_demo() -> None:
    import numpy as np
    from matplotlib import pyplot as plt

    with ui.pyplot(figsize=(3, 2)):
        x = np.linspace(0.0, 5.0)
        y = np.cos(2 * np.pi * x) * np.exp(-x)
        plt.plot(x, y, '-')


doc.reference(ui.pyplot)
