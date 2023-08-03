import re
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Union

from ..events import GenericEventArguments
from .choice_element import ChoiceElement
from .mixins.disableable_element import DisableableElement


class Select(ChoiceElement, DisableableElement, component='select.js'):

    def __init__(self,
                 options: Union[List, Dict], *,
                 label: Optional[str] = None,
                 value: Any = None,
                 on_change: Optional[Callable[..., Any]] = None,
                 with_input: bool = False,
                 multiple: bool = False,
                 clearable: bool = False,
                 ) -> None:
        """Dropdown Selection

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param with_input: whether to show an input field to filter the options
        :param multiple: whether to allow multiple selections
        :param clearable: whether to add a button to clear the selection
        """
        self.multiple = multiple
        if multiple:
            if value is None:
                value = []
            elif not isinstance(value, list):
                value = [value]
        super().__init__(options=options, value=value, on_change=on_change)
        if label is not None:
            self._props['label'] = label
        if with_input:
            self.original_options = deepcopy(options)
            self._props['use-input'] = True
            self._props['hide-selected'] = not multiple
            self._props['fill-input'] = True
            self._props['input-debounce'] = 0
        self._props['multiple'] = multiple
        self._props['clearable'] = clearable

    def on_filter(self, e: GenericEventArguments) -> None:
        self.options = [
            option
            for option in self.original_options
            if not e.args or re.search(e.args, option, re.IGNORECASE)
        ]
        self.update()

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        if self.multiple:
            if e.args is None:
                return []
            else:
                return [self._values[arg['value']] for arg in e.args]
        else:
            if e.args is None:
                return None
            else:
                return self._values[e.args['value']]

    def _value_to_model_value(self, value: Any) -> Any:
        if self.multiple:
            result = []
            for item in value or []:
                try:
                    index = self._values.index(item)
                    result.append({'value': index, 'label': self._labels[index]})
                except ValueError:
                    pass
            return result
        else:
            try:
                index = self._values.index(value)
                return {'value': index, 'label': self._labels[index]}
            except ValueError:
                return None
