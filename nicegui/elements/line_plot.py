from typing import Any, Literal

from typing_extensions import Self

from .pyplot import Pyplot


class LinePlot(Pyplot):

    def __init__(self, *,
                 n: int = 1,
                 limit: int = 100,
                 update_every: int = 1,
                 close: bool = True,
                 **kwargs: Any,
                 ) -> None:
        """Line Plot

        Create a line plot using pyplot.
        The `push` method provides live updating when utilized in combination with `ui.timer`.

        :param n: number of lines
        :param limit: maximum number of datapoints per line (new points will displace the oldest)
        :param update_every: update plot only after pushing new data multiple times to save CPU and bandwidth
        :param close: whether the figure should be closed after exiting the context; set to `False` if you want to update it later (default: `True`)
        :param kwargs: arguments like `figsize` which should be passed to `pyplot.figure <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html>`_
        """
        super().__init__(close=close, **kwargs)

        self.x: list[float] = []
        self.Y: list[list[float]] = [[] for _ in range(n)]
        self.lines = [self.fig.gca().plot([], [])[0] for _ in range(n)]
        self.slice = slice(0 if limit is None else -limit, None)
        self.update_every = update_every
        self.push_counter = 0

    def with_legend(self, titles: list[str], **kwargs: Any):
        """Add a legend to the plot.

        :param titles: list of titles for the lines
        :param kwargs: additional arguments which should be passed to `pyplot.legend <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html>`_
        """
        self.fig.gca().legend(titles, **kwargs)
        self._convert_to_html()
        return self

    def push(self,
             x: list[float],
             Y: list[list[float]],
             *,
             x_limits: None | Literal['auto'] | tuple[float, float] = 'auto',
             y_limits: None | Literal['auto'] | tuple[float, float] = 'auto',
             ) -> None:
        """Push new data to the plot.

        :param x: list of x values
        :param Y: list of lists of y values (one list per line)
        :param x_limits: new x limits (tuple of floats, or "auto" to fit the data points, or ``None`` to leave unchanged, *added in version 2.10.0*)
        :param y_limits: new y limits (tuple of floats, or "auto" to fit the data points, or ``None`` to leave unchanged, *added in version 2.10.0*)
        """
        self.push_counter += 1

        self.x = [*self.x, *x][self.slice]
        for i in range(len(self.lines)):
            self.Y[i] = [*self.Y[i], *Y[i]][self.slice]

        if self.push_counter % self.update_every != 0:
            return

        for i, line in enumerate(self.lines):
            line.set_xdata(self.x)
            line.set_ydata(self.Y[i])

        if isinstance(x_limits, tuple):
            self.fig.gca().set_xlim(*x_limits)
        elif x_limits == 'auto':
            min_x = min(self.x)
            max_x = max(self.x)
            if min_x != max_x:
                pad_x = 0.01 * (max_x - min_x)
                self.fig.gca().set_xlim(min_x - pad_x, max_x + pad_x)

        if isinstance(y_limits, tuple):
            self.fig.gca().set_ylim(*y_limits)
        elif y_limits == 'auto':
            flat_y = [y_i for y in self.Y for y_i in y]
            min_y = min(flat_y)
            max_y = max(flat_y)
            if min_y != max_y:
                pad_y = 0.01 * (max_y - min_y)
                self.fig.gca().set_ylim(min_y - pad_y, max_y + pad_y)

        self._convert_to_html()

    def clear(self) -> Self:
        """Clear the line plot."""
        super().clear()
        self.x.clear()
        for y in self.Y:
            y.clear()
        for line in self.lines:
            line.set_data([], [])
        self._convert_to_html()
        return self
