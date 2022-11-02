from .float_element import FloatElement
from .quasarcommponents import QLinearProgressExtended, QCircularProgressExtended
from ..auto_context import ContextMixin


class LinearProgress(FloatElement, ContextMixin):

    def __init__(self, *, value: float = 0.0, target_object=None, target_name=None, **kwargs):
        """LinearProgress

        An element to create a linear progress bar wrapping
        `Linear Progress <https://v1.quasar.dev/vue-components/linear-progress>`_ component.

        :param value: the initial value of the field (ratio 0.0 - 1.0)
        :param target_object: the object to data bind to
        :param target_name: the field name of the data bound object
        """
        view = QLinearProgressExtended(color='primary', size='1.4rem', value=value, temp=False)
        super().__init__(view, value=value, on_change=None, **kwargs)
        if target_object and target_name:
            self.bind_value_from(target_object=target_object, target_name=target_name)


class CircularProgress(FloatElement, ContextMixin):

    def __init__(self, *, value: float = 0.0, target_object=None, target_name=None, show_value: bool = True,
                 **kwargs):
        """CircularProgress

        An element to create a linear progress bar wrapping
        `Circular Progress <https://v1.quasar.dev/vue-components/circular-progress>`_ component.

        :param value: the initial value of the field (ratio 0.0 - 1.0)
        :param target_object: the object to data bind to
        :param target_name: the field name of the data bound object
        """
        value = self._convert_ratio(value)
        view = QCircularProgressExtended(color='primary', value=value, temp=False,
                                         track_color='grey-4',
                                         center_color='transparent',
                                         size='xl', show_value=show_value)
        super().__init__(view, value=value, on_change=None, **kwargs)
        if target_object and target_name:
            self.bind_value_from(target_object=target_object, target_name=target_name)

    @property
    def value(self):
        val = getattr(self, '_value')
        return val

    @value.setter
    def value(self, value):
        val = self._convert_ratio(value=value)
        setattr(self, '_value', val)

    def _convert_ratio(self, value: float) -> float:
        return round(value * 100, 2) if 0.0 <= value <= 1.0 else float(value)
