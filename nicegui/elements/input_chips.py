import re
from typing import Any, Literal, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction
from .mixins.value_element import ValueElement


class InputChips(LabelElement, ValidationElement, ValueElement, DisableableElement, component='input_chips.js'):

    def __init__(self,
                 value: Any = None,
                 *,
                 label: Optional[str] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 new_value_mode: Literal['add', 'add-unique', 'toggle'] = 'toggle',
                 clearable: bool = False,
                 use_delimiter: bool = False,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        """Dropdown Selection

        This element is based on Quasar's `QSelect <https://quasar.dev/vue-components/select>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        You can use the `validation` parameter to define a dictionary of validation rules,
        e.g. ``{'Too long!': lambda value: len(value) < 3}``.
        The key of the first rule that fails will be displayed as an error message.
        Alternatively, you can pass a callable that returns an optional error message.
        To disable the automatic validation on every value change, you can use the `without_auto_validation` method.

        :param value: the initial value
        :param label: the label to display above the selection
        :param on_change: callback to execute when selection changes
        :param new_value_mode: handle new values from user input (default: toggle)
        :param clearable: whether to add a button to clear the selection
        :param use_delimiter: whether Separate multiple values by [,;|、،]
        :param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)
        """
        if value is None:
            value = []
        elif not isinstance(value, list):
            value = [value]
        else:
            value = value[:]  # NOTE: avoid modifying the original list which could be the list of options (#3014)
        super().__init__(label=label, value=value, on_value_change=on_change, validation=validation)

        self._props['new-value-mode'] = new_value_mode

        self.use_delimiter = use_delimiter

        self._props['use-input'] = True
        self._props['hide-selected'] = False
        self._props['fill-input'] = True
        self._props['input-debounce'] = 0
        self._props['multiple'] = True
        self._props['hide-dropdown-icon'] = True
        self._props['clearable'] = clearable

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        if e.args is None:
            return []
        else:
            new_value = next((arg for arg in e.args if isinstance(arg, str)), None)
            split_args = []
            if new_value is not None:
                split_args = [value.strip() for value in re.split(r'[,;|]+', new_value) if len(value)> 0] if self.use_delimiter else [new_value]

            args = [arg['label'] for arg in e.args if isinstance(arg, dict)]
            mode = self._props['new-value-mode']


            for value in split_args:
                if mode == 'add':
                    args.append(value)
                elif mode == 'add-unique':
                    if value not in args:
                        args.append(value)
                elif mode == 'toggle':
                    if value in args:
                        args.remove(value)
                    else:
                        args.append(value)
            return args


    def _value_to_model_value(self, value: Any) -> Any:
        return [{'value': ind, 'label': val} for ind, val in enumerate(value or [])]
