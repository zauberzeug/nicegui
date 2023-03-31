from typing import Callable, Optional

from .mixins.value_element import ValueElement


class Splitter(ValueElement):
    def __init__(self, *,
                 horizontal: Optional[bool] = False,
                 reverse: Optional[bool] = False,
                 limits: Optional[list] = [0, 100],
                 value: Optional[float] = 50,
                 on_change: Optional[Callable] = None) -> None:
        """Splitter

        :param horizontal: Allows the splitter to split its two panels horizontally, instead of vertically
        :param limits: An array of two values representing the minimum and maximum split size of the two panels
        :param value: Size of the first panel (or second if using reverse)
        :param reverse: Apply the model size to the second panel (by default it applies to the first)
        :param on_change: callback which is invoked when the user releases the splitter

        This element is based on Quasar's `Splitter <https://quasar.dev/vue-components/splitter>`_ component.

        There are four slots which can contain content:

            - before - Content of the panel on left/top of the splitter
            - after - Content of the panel on right/bottom of the splitter
            - default - Default slot in the devland unslotted content of the component; Suggestion: ui.tooltip, ui.menu
            - separator - Content to be placed inside the separator; By default it is centered

            Warning: The use of the **before** and **after** slots is required.

        """
        super().__init__(tag='q-splitter', value=value, on_value_change=on_change, throttle=0.05)
        self._props['horizontal'] = horizontal
        self._props['limits'] = limits
        self._props['reverse'] = reverse
