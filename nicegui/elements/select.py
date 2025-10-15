from collections.abc import Collection
from copy import deepcopy
from typing import Any, Callable, Literal, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement, T
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class Select(LabelElement, ValidationElement[tuple[T, ...]], ChoiceElement[T, Union[dict[str, Any], str, list[Union[dict[str, Any], str]]]], DisableableElement, component='select.js'):

    def __init__(self,
                 options: Collection[T], *,
                 label: Optional[str] = None,
                 selected: tuple[T, ...] = (),
                 on_change: Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]] = None,
                 with_input: bool = False,
                 new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None,
                 new_val_to_option: Optional[Callable[['Select[T]', str], T]] = None,
                 multiple: bool = False,
                 clearable: bool = False,
                 validation: Optional[Union[ValidationFunction[tuple[T, ...]], ValidationDict[tuple[T, ...]]]] = None,
                 ) -> None:
        """Dropdown Selection

        This element is based on Quasar's `QSelect <https://quasar.dev/vue-components/select>`_ component.

        The options can be specified as a list of values, or as a dictionary mapping values to labels.
        After manipulating the options, call `update()` to update the options in the UI.

        If `with_input` is True, an input field is shown to filter the options.

        If `new_value_mode` is not None, it implies `with_input=True` and the user can enter new values in the input field.
        See `Quasar's documentation <https://quasar.dev/vue-components/select#the-new-value-mode-prop>`_ for details.
        Note that this mode is ineffective when setting the `value` property programmatically.

        You can use the `validation` parameter to define a dictionary of validation rules,
        e.g. ``{'Too long!': lambda value: len(value) < 3}``.
        The key of the first rule that fails will be displayed as an error message.
        Alternatively, you can pass a callable that returns an optional error message.
        To disable the automatic validation on every value change, you can use the `without_auto_validation` method.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param label: the label to display above the selection
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param with_input: whether to show an input field to filter the options
        :param new_value_mode: handle new values from user input (default: None, i.e. no new values)
        :param multiple: whether to allow multiple selections
        :param clearable: whether to add a button to clear the selection
        :param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)
        """
        if not multiple and len(selected) > 1:
            raise ValueError(f'Too many values passed to selected. You passed {selected} and multiple is {multiple}.')
        self.multiple = multiple
        self.new_value_mode = new_value_mode
        super().__init__(label=label, options=options, value=selected, on_change=on_change, validation=validation)
        if self.new_value_mode is not None:
            self._props['new-value-mode'] = new_value_mode
            with_input = True
            assert new_val_to_option is not None, 'new_val_to_option must be passed when new_value_mode is not None.'
            self._new_val_to_option = new_val_to_option
        if with_input:
            self.original_options = deepcopy(options)
            self._props['use-input'] = True
            self._props['hide-selected'] = not multiple
            self._props['fill-input'] = True
            self._props['input-debounce'] = 0
        self._props['multiple'] = multiple
        self._props['clearable'] = clearable

        self._is_showing_popup = False
        self.on('popup-show', lambda e: setattr(e.sender, '_is_showing_popup', True))
        self.on('popup-hide', lambda e: setattr(e.sender, '_is_showing_popup', False))

    @property
    def is_showing_popup(self) -> bool:
        """Whether the options popup is currently shown."""
        return self._is_showing_popup

    def _event_args_to_value(self, e: GenericEventArguments[Union[dict[str, Any], str, list[Union[dict[str, Any], str]]]]) -> tuple[T, ...]:
        # pylint: disable=too-many-nested-blocks
        if isinstance(e.args, dict):
            return (self._index_to_option[e.args['id']],)
        if isinstance(e.args, str) and self.new_value_mode:
            new_value = self._handle_new_value(self._new_val_to_option(self, e.args))
            return (new_value,)
        else:
            args: list[T] = []
            for a in e.args:
                if isinstance(a, str) and self.new_value_mode:
                    args.append(self._handle_new_value(self._new_val_to_option(self, a)))
                elif isinstance(a, dict):
                    args.append(self._index_to_option[a['id']])
            if self.new_value_mode == 'add-unique':
                args = list({o.value: o for o in args}.values())
                # ^ handle issue #4896: eliminate duplicate arguments
            return tuple(args)

    def _handle_new_value(self, value: T) -> T:
        mode = self.new_value_mode
        if mode == 'add':
            self.options.append(value)
        elif mode == 'add-unique':
            if value.value not in [o.value for o in self.options]:
                self.options.append(value)
        elif mode == 'toggle':
            if value.value in [o.value for o in self.options]:
                self.options = [o for o in self.options if o.value != value.value]
            else:
                self.options.append(value)
        self._do_updates()
        return value

    def _value_to_model_value(self, value: tuple[T, ...]) -> tuple[T, ...]:
        return tuple(v for v in value if v in self.options)

    def _update_options(self) -> None:
        before_value = self.value
        self._props['options'] = self.options
        new_val = self._value_to_model_value(before_value)
        self.value = new_val
        self._props[self.VALUE_PROP] = new_val if self.multiple else (new_val[0] if len(new_val) > 0 else new_val)
