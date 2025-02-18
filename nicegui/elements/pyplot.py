from __future__ import annotations

import asyncio
import io
import os
from typing import Any

from typing_extensions import Self

from .. import background_tasks, optional_features
from ..client import Client
from ..element import Element

try:
    if os.environ.get('MATPLOTLIB', 'true').lower() == 'true':
        import matplotlib.figure
        import matplotlib.pyplot as plt
        optional_features.register('matplotlib')

        class MatplotlibFigure(matplotlib.figure.Figure):

            def __init__(self, element: Matplotlib, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                self.element = element

            def __enter__(self) -> Self:
                return self

            def __exit__(self, *_) -> None:
                self.element.update()

except ImportError:
    pass


class Pyplot(Element, default_classes='nicegui-pyplot'):

    def __init__(self, *, close: bool = True, **kwargs: Any) -> None:
        """Pyplot Context

        Create a context to configure a `Matplotlib <https://matplotlib.org/>`_ plot.

        :param close: whether the figure should be closed after exiting the context; set to `False` if you want to update it later (default: `True`)
        :param kwargs: arguments like `figsize` which should be passed to `pyplot.figure <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html>`_
        """
        if not optional_features.has('matplotlib'):
            raise ImportError('Matplotlib is not installed. Please run "pip install matplotlib".')

        super().__init__('div')
        self.close = close
        self.fig = plt.figure(**kwargs)  # pylint: disable=possibly-used-before-assignment
        self._convert_to_html()

        if not self.client.shared:
            background_tasks.create(self._auto_close(), name='auto-close plot figure')

    def _convert_to_html(self) -> None:
        with io.StringIO() as output:
            self.fig.savefig(output, format='svg')
            self._props['innerHTML'] = output.getvalue()

    def __enter__(self) -> Self:
        plt.figure(self.fig)
        return self

    def __exit__(self, *_) -> None:
        self._convert_to_html()
        if self.close:
            plt.close(self.fig)
        self.update()

    async def _auto_close(self) -> None:
        while self.client.id in Client.instances:
            await asyncio.sleep(1.0)
        plt.close(self.fig)


class Matplotlib(Element):

    def __init__(self, **kwargs: Any) -> None:
        """Matplotlib

        Create a `Matplotlib <https://matplotlib.org/>`_ element rendering a Matplotlib figure.
        The figure is automatically updated when leaving the figure context.

        :param kwargs: arguments like `figsize` which should be passed to `matplotlib.figure.Figure <https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure>`_
        """
        if not optional_features.has('matplotlib'):
            raise ImportError('Matplotlib is not installed. Please run "pip install matplotlib".')

        super().__init__('div')
        self.figure = MatplotlibFigure(self, **kwargs)
        self._convert_to_html()

    def _convert_to_html(self) -> None:
        with io.StringIO() as output:
            self.figure.savefig(output, format='svg')
            self._props['innerHTML'] = output.getvalue()

    def update(self) -> None:
        self._convert_to_html()
        return super().update()
