from collections.abc import Callable, Generator, Iterable, Iterator
from contextlib import suppress
from copy import deepcopy
from typing import Any, Generic, Literal, cast, overload

from ..defaults import DEFAULT_PROP, DEFAULT_PROPS, resolve_defaults
from ..events import GenericEventArguments, Handler, ValueChangeEventArguments, ValueT
from .choice_element import ChoiceElement, OptionT
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction

NewValueMode = Literal['add', 'add-unique', 'toggle']


class Select(LabelElement, ValidationElement[ValueT], ChoiceElement[OptionT, ValueT], DisableableElement,
             Generic[OptionT, ValueT], component='select.js'):

    @overload
    def __init__(self: 'Select[OptionT, list[OptionT]]',
                 options: list[OptionT] | dict[OptionT, Any], *,
                 label: str | None = ...,
                 value: OptionT | list[OptionT] | None = ...,
                 on_change: Handler[ValueChangeEventArguments[list[OptionT]]] | None = ...,
                 with_input: bool = ...,
                 new_value_mode: NewValueMode | None = ...,
                 multiple: Literal[True],
                 clearable: bool = ...,
                 validation: ValidationFunction | ValidationDict | None = ...,
                 key_generator: Callable[[Any], Any] | Iterator[Any] | None = ...,
                 option_label: Callable[[OptionT], Any] | None = ...,
                 ) -> None: ...

    @overload
    def __init__(self: 'Select[OptionT, OptionT | None]',
                 options: list[OptionT] | dict[OptionT, Any], *,
                 label: str | None = ...,
                 value: OptionT | None = ...,
                 on_change: Handler[ValueChangeEventArguments[OptionT | None]] | None = ...,
                 with_input: bool = ...,
                 new_value_mode: NewValueMode | None = ...,
                 multiple: Literal[False] = ...,
                 clearable: bool = ...,
                 validation: ValidationFunction | ValidationDict | None = ...,
                 key_generator: Callable[[Any], Any] | Iterator[Any] | None = ...,
                 option_label: Callable[[OptionT], Any] | None = ...,
                 ) -> None: ...

    @overload
    def __init__(self: 'Select[OptionT, Any]',
                 options: list[OptionT] | dict[OptionT, Any], *,
                 label: str | None = ...,
                 value: OptionT | list[OptionT] | None = ...,
                 on_change: Handler[ValueChangeEventArguments[Any]] | None = ...,
                 with_input: bool = ...,
                 new_value_mode: NewValueMode | None = ...,
                 multiple: bool = ...,
                 clearable: bool = ...,
                 validation: ValidationFunction | ValidationDict | None = ...,
                 key_generator: Callable[[Any], Any] | Iterator[Any] | None = ...,
                 option_label: Callable[[OptionT], Any] | None = ...,
                 ) -> None: ...

    @resolve_defaults
    def __init__(self,
                 options: list[OptionT] | dict[OptionT, Any], *,
                 label: str | None = DEFAULT_PROP | None,
                 value: Any = DEFAULT_PROPS['model-value'] | None,
                 on_change: Handler[ValueChangeEventArguments[Any]] | None = None,
                 with_input: bool = False,
                 new_value_mode: NewValueMode | None = DEFAULT_PROP | None,
                 multiple: bool = DEFAULT_PROP | False,
                 clearable: bool = DEFAULT_PROP | False,
                 validation: ValidationFunction | ValidationDict | None = None,
                 key_generator: Callable[[Any], Any] | Iterator[Any] | None = None,
                 option_label: Callable[[OptionT], Any] | None = None,
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

        Options are not limited to scalars: a list may hold dataclasses or dictionaries,
        in which case `value` is the selected option itself.
        Pass `option_label` to say how such an option should be labelled.
        A rich option's own fields are sent to the client and are available as ``props.opt.<key>`` in slots,
        except for the reserved keys "value" and "label".

        The element is generic in its option type, so type checkers infer the argument of `option_label`
        as well as the type of `value` from the options:
        ``ui.select(people, option_label=lambda person: person.name).value`` is a ``Person | None``,
        and a ``list[Person]`` when `multiple` is True.

        :param options: a list ['value1', ...] or dictionary `{'value1':'label1', ...}` specifying the options
        :param label: the label to display above the selection
        :param value: the initial value
        :param on_change: callback to execute when selection changes
        :param with_input: whether to show an input field to filter the options
        :param new_value_mode: handle new values from user input (default: None, i.e. no new values)
        :param multiple: whether to allow multiple selections
        :param clearable: whether to add a button to clear the selection
        :param validation: dictionary of validation rules or a callable that returns an optional error message (default: None for no validation)
        :param key_generator: a callback or iterator to generate a dictionary key for new values
        :param option_label: a callback mapping an option to the label shown for it (default: None, i.e. the option itself)
        """
        self.multiple = multiple
        if multiple:
            if value is None:
                value = []
            elif not isinstance(value, list):
                value = [value]
            else:
                value = value[:]  # avoid modifying the original list which could be the list of options (#3014)
        super().__init__(label=label, options=options, value=value, on_change=on_change, validation=validation,
                         option_label=option_label)
        if isinstance(key_generator, Generator):
            next(key_generator)  # prime the key generator, prepare it to receive the first value
        self.key_generator = key_generator
        if new_value_mode is not None:
            if isinstance(options, dict) and new_value_mode == 'add' and key_generator is None:
                raise ValueError('new_value_mode "add" is not supported for dict options without key_generator')
            self._props['new-value-mode'] = new_value_mode
            with_input = True
        if with_input:
            self.original_options = deepcopy(options)
            self._props['use-input'] = True
            self._props.set_bool('hide-selected', not multiple)
            self._props['fill-input'] = True
            self._props['input-debounce'] = 0
            self._props['for'] = self.html_id  # keep html_id on the input so tooltips/ui.query can anchor (#6114)
        self._props.set_bool('multiple', multiple)
        self._props.set_bool('clearable', clearable)

        self._is_showing_popup = False
        self.on('popup-show', lambda e: setattr(e.sender, '_is_showing_popup', True))
        self.on('popup-hide', lambda e: setattr(e.sender, '_is_showing_popup', False))

    @property
    def is_showing_popup(self) -> bool:
        """Whether the options popup is currently shown."""
        return self._is_showing_popup

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        # pylint: disable=too-many-nested-blocks
        if self.multiple:
            if e.args is None:
                return []
            else:
                if self._props.get('new-value-mode') == 'add-unique':
                    # handle issue #4896: eliminate duplicate arguments
                    for arg1 in [a for a in e.args if isinstance(a, str)]:
                        for arg2 in [a for a in e.args if isinstance(a, dict)]:
                            if arg1 == arg2['label']:
                                e.args.remove(arg1)
                                break
                args = [self._values[arg['value']] if isinstance(arg, dict) else arg for arg in e.args]
                for arg in e.args:
                    if isinstance(arg, str):
                        self._handle_new_value(arg)
                return [arg for arg in args if arg in self._values]
        else:  # noqa: PLR5501
            if e.args is None:
                return None
            else:  # noqa: PLR5501
                if isinstance(e.args, str):
                    new_value = self._handle_new_value(e.args)
                    return new_value if new_value in self._values else None
                else:
                    return self._values[e.args['value']]

    def _value_to_model_value(self, value: Any) -> Any:
        # pylint: disable=no-else-return
        if self.multiple:
            result = []
            for item in value or []:
                with suppress(ValueError):
                    result.append(self._option_dict(self._values.index(item)))
            return result
        else:
            try:
                return self._option_dict(self._values.index(value))
            except ValueError:
                return None

    def _generate_key(self, value: str) -> Any:
        if isinstance(self.key_generator, Generator):
            return self.key_generator.send(value)
        if isinstance(self.key_generator, Iterable):
            return next(self.key_generator)
        if callable(self.key_generator):
            return self.key_generator(value)
        return value

    def _handle_new_value(self, value: str) -> Any:
        mode = self._props['new-value-mode']
        # NOTE: new values entered by the user are strings, so they widen the option type beyond OptionT
        options = cast('list[Any] | dict[Any, Any]', self.options)
        if isinstance(options, list):
            if mode == 'add':
                options.append(value)
            elif mode == 'add-unique':
                if value not in options:
                    options.append(value)
            elif mode == 'toggle':
                if value in options:
                    options.remove(value)
                else:
                    options.append(value)
            # self._labels and self._values are updated via self.options since they share the same references
            return value
        else:
            key = value
            if mode == 'add':
                key = self._generate_key(value)
                options[key] = value
            elif mode == 'add-unique':
                if value not in options.values():
                    key = self._generate_key(value)
                    options[key] = value
            elif mode == 'toggle':
                if value in options:
                    options.pop(value)
                else:
                    key = self._generate_key(value)
                    options.update({key: value})
            self._update_values_and_labels()
            return key
