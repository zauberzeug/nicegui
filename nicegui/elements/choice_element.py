from typing import Any, Callable, Dict, List, Optional, Union

from .mixins.value_element import ValueElement


class ChoiceElement(ValueElement):

    def __init__(self, *,
                 tag: str,
                 options: Union[List, Dict],
                 value: Any,
                 on_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        self.options = options
        self._values: List[str] = []
        self._labels: List[str] = []
        self._update_values_and_labels()
        super().__init__(tag=tag, value=value, on_value_change=on_change)
        self._update_options()

    def _update_values_and_labels(self) -> None:
        self._values = self.options if isinstance(self.options, list) else list(self.options.keys())
        self._labels = self.options if isinstance(self.options, list) else list(self.options.values())

    def _update_options(self) -> None:
        self._props['options'] = [{'value': index, 'label': option} for index, option in enumerate(self._labels)]

    def update(self) -> None:
        self._update_values_and_labels()
        self._update_options()
        super().update()
