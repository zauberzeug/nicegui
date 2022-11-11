from typing import Optional

import justpy as jp

from ..binding import BindableProperty, BindValueMixin
from .element import Element


class LinearProgress(Element, BindValueMixin):
    value = BindableProperty()

    def __init__(self, value: float = 0.0, *, size: Optional[str] = None, show_value: bool = True) -> None:
        """Linear Progress

        A linear progress bar wrapping Quasar's
        `QLinearProgress <https://v1.quasar.dev/vue-components/linear-progress>`_ component.

        :param value: the initial value of the field (from 0.0 to 1.0)
        :param size: the height of the progress bar (default: "20px" with value label and "4px" without)
        :param show_value: whether to show a value label in the center (default: `True`)
        """
        view = jp.QLinearProgress(value=value, temp=False)
        view.prop_list.append('size')
        view.size = size if size is not None else '20px' if show_value else '4px'
        super().__init__(view)

        self.value = value
        self.bind_value_to(self.view, 'value')

        if show_value:
            label = jp.Div(text='', classes='absolute-center text-sm text-white', temp=False)
            label.add_page(self.page)
            self.view.add(label)
            self.bind_value_to(label, 'text')


class CircularProgress(Element, BindValueMixin):
    value = BindableProperty()

    def __init__(self, value: float = 0.0, *,
                 min: float = 0.0, max: float = 1.0, size: str = 'xl', show_value: bool = True) -> None:
        """Circular Progress

        A circular progress bar wrapping Quasar's
        `QCircularProgress <https://v1.quasar.dev/vue-components/circular-progress>`_.

        :param value: the initial value of the field
        :param size: the size of the progress circle (default: "xl")
        :param show_value: whether to show a value label in the center (default: `True`)
        """
        view = jp.QCircularProgress(value=value, min=min, max=max, size=size, show_value=show_value,
                                    color='primary', track_color='grey-4', temp=False)
        view.prop_list.append('instant-feedback')
        super().__init__(view)

        self.value = value
        self.bind_value_to(self.view, 'value')
