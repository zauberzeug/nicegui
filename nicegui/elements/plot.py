import io

import matplotlib.pyplot as plt

from ..element import Element


class Plot(Element):

    def __init__(self, *, close: bool = True, **kwargs) -> None:
        """Plot Context

        Create a context to configure a `Matplotlib <https://matplotlib.org/>`_ plot.

        :param close: whether the figure should be closed after exiting the context; set to `False` if you want to update it later (default: `True`)
        :param kwargs: arguments like `figsize` which should be passed to `pyplot.figure <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html>`_
        """
        super().__init__('div')
        self.close = close
        self.fig = plt.figure(**kwargs)
        self._convert_to_html()

    def _convert_to_html(self) -> None:
        with io.StringIO() as output:
            self.fig.savefig(output, format='svg')
            self._props['innerHTML'] = output.getvalue()

    def __enter__(self):
        plt.figure(self.fig)
        return self

    def __exit__(self, *_):
        self._convert_to_html()
        if self.close:
            plt.close(self.fig)
        self.update()
