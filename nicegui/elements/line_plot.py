from typing import List
from .plot import Plot

class LinePlot(Plot):

    def __init__(self, n: int = 1, limit: int = 100, close: bool = True):

        super().__init__(close)

        self.x = []
        self.Y = [[] for _ in range(n)]
        self.lines = [self.fig.gca().plot([], [])[0] for _ in range(n)]
        self.slice = slice(0 if limit is None else -limit, None)

    def with_legend(self, titles: List[str], **kwargs):

        self.fig.gca().legend(titles, **kwargs)
        self.view.set_figure(self.fig)
        return self

    def push(self, x: List[float], Y: List[List[float]]):

        self.x = [*self.x, *x][self.slice]
        for i in range(len(self.lines)):
            self.Y[i] = [*self.Y[i], *Y[i]][self.slice]
            self.lines[i].set_xdata(self.x)
            self.lines[i].set_ydata(self.Y[i])
        flat_y = [y_i for y in self.Y for y_i in y]
        self.fig.gca().set_xlim(min(self.x), max(self.x))
        self.fig.gca().set_ylim(min(flat_y), max(flat_y))
        self.view.set_figure(self.fig)
