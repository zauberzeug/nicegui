import re
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Union, Literal

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
                 new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None
                 ) -> None:
        """Dropdown Selection

        This element is based on Quasar's `QSelect <https://quasar.dev/vue-components/select>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param with_input: whether to show an input field to filter the options
        :param multiple: whether to allow multiple selections
        :param clearable: whether to add a button to clear the selection
        :param new_value_mode: processing new values from user input, see `<https://quasar.dev/vue-components/select#create-new-values>`_.
        Is only applied if `with_input == True`.
        Be careful when using with `options` being a `dict`: if an existing key matches the new value, the existing value is overwritten.
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
            if new_value_mode is not None:
                self._props['new_value_mode'] = new_value_mode
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
                        if isinstance(self.options, list):
                            self.options.append(arg)
                        else:  # self.options is a dict
                            self.options[arg] = arg
                        self.update()
                        out.append(self._values[len(self.options) - 1])
                    else:
                        out.append(self._values[arg['value']])
                return out
        else:
            if e.args is None:
                return None
            else:
                if isinstance(e.args, str):
                    if isinstance(self.options, list):
                        self.options.append(e.args)
                    else:  # self.options is a dict
                        self.options[e.args] = e.args
                    self.update()
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
