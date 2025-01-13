from nicegui import events, ui

from . import doc


@doc.demo(ui.line_plot)
def main_demo() -> None:
    import math
    from datetime import datetime

    line_plot = ui.line_plot(n=2, limit=20, figsize=(3, 2), update_every=5) \
        .with_legend(['sin', 'cos'], loc='upper center', ncol=2)

    def update_line_plot() -> None:
        now = datetime.now()
        x = now.timestamp()
        y1 = math.sin(x)
        y2 = math.cos(x)
        line_plot.push([now], [[y1], [y2]])

    line_updates = ui.timer(0.1, update_line_plot, active=False)
    line_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')

    # END OF DEMO
    def handle_change(e: events.GenericEventArguments) -> None:
        def turn_off() -> None:
            line_checkbox.set_value(False)
            ui.notify('Turning off that line plot to save resources on our live demo server. 😎')
        line_checkbox.value = e.args
        if line_checkbox.value:
            ui.timer(10.0, turn_off, once=True)
    line_checkbox.on('update:model-value', handle_change, args=[None])


@doc.demo('Setting Custom Limits',
          """
        By default, the x and y limits are calculated and changed based on new data points.
        You can disable this behovior by passing `x_limits = None` and/or `y_limits = None` to `push`.
        You can also have the push method set custom limits by passing a tuple of `(min, max)` to `x_limits`/`y_limits`.
""")
def lims_demo() -> None:
    import math
    from datetime import datetime
    import matplotlib.pyplot as plt

    line_plot = ui.line_plot(n=1, limit=20, figsize=(3, 2), update_every=5) \
        .with_legend(['sin'], loc='upper center', ncol=1)

    with line_plot:
        plt.ylim([0, 1])

    def update_line_plot() -> None:
        now = datetime.now()
        x = now.timestamp()
        y1 = math.sin(x)
        line_plot.push([now], [[y1]], y_limits=None)
        ## or to set the limits here
        line_plot.push([now], [[y1]], y_limits=(-1,1))

    line_updates = ui.timer(0.1, update_line_plot, active=False)
    line_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')

    # END OF DEMO
    def handle_change(e: events.GenericEventArguments) -> None:
        def turn_off() -> None:
            line_checkbox.set_value(False)
            ui.notify('Turning off that line plot to save resources on our live demo server. 😎')
        line_checkbox.value = e.args
        if line_checkbox.value:
            ui.timer(10.0, turn_off, once=True)
    line_checkbox.on('update:model-value', handle_change, args=[None])


doc.reference(ui.line_plot)
