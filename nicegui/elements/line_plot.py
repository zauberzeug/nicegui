from typing import Any, List

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

        self.x: List[float] = []
        self.Y: List[List[float]] = [[] for _ in range(n)]
        self.lines = [self.fig.gca().plot([], [])[0] for _ in range(n)]
        self.slice = slice(0 if limit is None else -limit, None)
        self.update_every = update_every
        self.push_counter = 0

    def with_legend(self, titles: List[str], **kwargs: Any):
        """Add a legend to the plot.

        :param titles: list of titles for the lines
        :param kwargs: additional arguments which should be passed to `pyplot.legend <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html>`_
        """
        self.fig.gca().legend(titles, **kwargs)
        self._convert_to_html()
        return self

    def push(self, x: List[float], Y: List[List[float]]) -> None:
        """Push new data to the plot.

        :param x: list of x values
        :param Y: list of lists of y values (one list per line)
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

        flat_y = [y_i for y in self.Y for y_i in y]
        min_x = min(self.x)
        max_x = max(self.x)
        min_y = min(flat_y)
        max_y = max(flat_y)
        pad_x = 0.01 * (max_x - min_x)
        pad_y = 0.01 * (max_y - min_y)
        self.fig.gca().set_xlim(min_x - pad_x, max_x + pad_x)
        self.fig.gca().set_ylim(min_y - pad_y, max_y + pad_y)
        self._convert_to_html()
        self.update()

    def clear(self) -> None:
        """Clear the line plot."""
        super().clear()
        self.x.clear()
        for y in self.Y:
            y.clear()
        for line in self.lines:
            line.set_data([], [])
        self._convert_to_html()
        self.update()
