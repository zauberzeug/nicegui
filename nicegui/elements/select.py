import re
from copy import deepcopy
from typing import Any, Callable, Dict, List, Literal, Optional, Union

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
                 new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None,
                 multiple: bool = False,
                 clearable: bool = False,
                 ) -> None:
        """Dropdown Selection

        This element is based on Quasar's `QSelect <https://quasar.dev/vue-components/select>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        If `with_input` is True, an input field is shown to filter the options.

        If `new_value_mode` is not None, it implies `with_input=True` and the user can enter new values in the input field.
        See `Quasar's documentation <https://quasar.dev/vue-components/select#the-new-value-mode-prop>`_ for details.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param with_input: whether to show an input field to filter the options
        :param new_value_mode: handle new values from user input (default: None, i.e. no new values)
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
        if new_value_mode is not None:
            self._props['new-value-mode'] = new_value_mode
            with_input = True
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
        # pylint: disable=no-else-return
        if self.multiple:
            if e.args is None:
                return []
            else:
                out = []
                for arg in e.args:
                    if isinstance(arg, str):
                        self._handle_new_value(arg)
                        out.append(self._values[len(self.options) - 1])
                    else:
                        out.append(self._values[arg['value']])
                return out
        else:
            if e.args is None:
                return None
            else:
                if isinstance(e.args, str):
                    self._handle_new_value(e.args)
                    return self._values[len(self.options) - 1]
                else:
                    return self._values[e.args['value']]

    def _value_to_model_value(self, value: Any) -> Any:
        # pylint: disable=no-else-return
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

    def _handle_new_value(self, value: str) -> None:
        # TODO: handle add-unique and toggle
        if isinstance(self.options, list):
            self.options.append(value)
            # NOTE: self._labels and self._values are updated via self.options since they share the same references
        else:
            self.options[value] = value
            self._labels.append(value)
            self._values.append(value)
