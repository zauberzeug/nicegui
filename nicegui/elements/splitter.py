from typing import Callable, Optional, Tuple

from .mixins.value_element import ValueElement


class Splitter(ValueElement):
    def __init__(self, *,
                 horizontal: Optional[bool] = False,
                 reverse: Optional[bool] = False,
                 limits: Optional[Tuple[float, float]] = (0, 100),
                 value: Optional[float] = 50,
                 on_change: Optional[Callable] = None) -> None:
        """Splitter

        This element is based on Quasar's `Splitter <https://quasar.dev/vue-components/splitter>`_ component.

        It provides three additional slots: `before`, `after`, and `separator`.
        They can be used to place other elements inside.

        :param horizontal: Whether to split horizontally instead of vertically
        :param limits: Two numbers representing the minimum and maximum split size of the two panels
        :param value: Size of the first panel (or second if using reverse)
        :param reverse: Whether to apply the model size to the second panel instead of the first
        :param on_change: callback which is invoked when the user releases the splitter
        """
        super().__init__(tag='q-splitter', value=value, on_value_change=on_change, throttle=0.05)
        self._props['horizontal'] = horizontal
        self._props['limits'] = limits
        self._props['reverse'] = reverse

        self.before = self.add_slot('before')
        self.after = self.add_slot('after')
        self.separator = self.add_slot('separator')
