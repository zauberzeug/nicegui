from collections.abc import Iterable
from copy import deepcopy
from typing import Any, Callable, Generic, Literal, Optional, Union, overload

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import VAL, ChoiceElement, Option, OptionDict, P, T, to_option
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class Select(
    LabelElement,
    ValidationElement[VAL],
    ChoiceElement[VAL, T],
    DisableableElement,
    Generic[VAL, T],
    component='select.js'
    ):

    def __init__(self,
                 options: Union[Iterable[T], Iterable[P]], *,
                 label: str = '',
                 value: Union[tuple[T, ...], Optional[T], tuple[P, ...], Optional[P], Optional[Option[P, P]], tuple[Option[P, P], ...]] = None,
                 on_change: Optional[Union[
                    Handler[ValueChangeEventArguments[tuple[T, ...]]],
                    Handler[ValueChangeEventArguments[Optional[T]]],
                ]] = None,
                with_input: bool = False,
                new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None,
                new_value_to_option: Optional[Callable[[str], Optional[T]]] = None,
                clearable: bool = False,
                validation: Union[
                    Optional[Union[ValidationFunction[tuple[T, ...]], ValidationDict[tuple[T, ...]]]],
                    Optional[Union[ValidationFunction[Optional[T]], ValidationDict[Optional[T]]]],
                ] = None
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
        self.multiple = isinstance(value, tuple)
        self.new_value_mode = new_value_mode
        self.new_value_to_option: Optional[Callable[[str], Optional[T]]] = new_value_to_option
        if isinstance(value, tuple) and all(isinstance(v, (str, int, float, bool)) for v in value):
            value = tuple(to_option(v) for v in value)
        if isinstance(value, (str, int, float, bool)):
            value = to_option(value)
        if all(isinstance(v, (str, int, float, bool)) for v in options):
            super().__init__(label=label or None, options=[to_option(v) for v in options], value=value, on_change=on_change, validation=validation)
        else:
            super().__init__(label=label or None, options=options, value=value, on_change=on_change, validation=validation)
        if new_value_mode is not None:
            self._props['new-value-mode'] = new_value_mode
            with_input = True
        if with_input:
            self.original_options = deepcopy(self.options)
            self._props['use-input'] = True
            self._props['hide-selected'] = not self.multiple
            self._props['fill-input'] = True
            self._props['input-debounce'] = 0
        self._props['multiple'] = self.multiple
        self._props['clearable'] = clearable

        self._is_showing_popup = False
        self.on('popup-show', lambda e: setattr(e.sender, '_is_showing_popup', True))
        self.on('popup-hide', lambda e: setattr(e.sender, '_is_showing_popup', False))

    @property
    def is_showing_popup(self) -> bool:
        """Whether the options popup is currently shown."""
        return self._is_showing_popup

    def _event_args_to_value(self, e: GenericEventArguments[Union[list[Union[OptionDict[Any, Any], str]], Optional[Union[OptionDict[Any, Any], str]]]]) -> Union[tuple[T, ...], Optional[T]]:
        print('e.args =', e.args)
        if isinstance(e.args, list):
            if self.new_value_mode == 'add-unique':
                # handle issue #4896: eliminate duplicate arguments
                for arg1 in [a for a in e.args if isinstance(a, str)]:
                    for arg2 in [a for a in e.args if isinstance(a, dict)]:
                        if arg1 == arg2['label']:
                            e.args.remove(arg1)
                            break
            args = [self._id_to_option[arg['id']] if isinstance(arg, dict) else self._handle_new_value(arg) for arg in e.args]
            args_without_nones = [v for v in args if v is not None]
            return tuple(arg for arg in args_without_nones if arg.value in self._values)
        else:  # noqa: PLR5501
            if e.args is None:
                return None
            else:  # noqa: PLR5501
                if isinstance(e.args, str):
                    new_value = self._handle_new_value(e.args)
                    return new_value if new_value and new_value.value in self._values else None
                else:
                    return self._id_to_option[e.args['id']]

    def _value_to_model_value(self, value: VAL) -> Any:
        if isinstance(value, tuple):
            return tuple(v for v in value if v.value in self._values)
        return value if value is not None and value.value in self._values else None

    def _handle_new_value(self, value: str) -> Optional[T]:
        assert self.new_value_to_option
        mode = self.new_value_mode
        new_option: Optional[T] = self.new_value_to_option(value)
        print('new_option =', new_option)
        if mode == 'add' and new_option:
            self.options.append(new_option)
        elif mode == 'add-unique' and new_option:
            if new_option.value not in [o.value for o in self.options]:
                self.options.append(new_option)
        elif mode == 'toggle' and new_option:
            if new_option.value in [o.value for o in self.options]:
                self.options.remove(new_option)
            else:
                self.options.append(new_option)
        self._update_values_and_labels()
        return new_option

@overload
def select(
    options: Iterable[T], *, label: str = ..., value: tuple[T, ...],
    on_change: Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[T]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[tuple[T, ...]], ValidationDict[tuple[T, ...]]]] = ...,
    ) -> Select[tuple[T, ...], T]:
    ...


@overload
def select(
    options: Iterable[T], *, label: str = ..., value: Literal[None] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[T]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[tuple[T, ...]], ValidationDict[tuple[T, ...]]]] = ...,
    ) -> Select[Optional[T], T]:
    ...


@overload
def select(
    options: Iterable[P], *, label: str = ..., value: tuple[P, ...],
    on_change: Optional[Handler[ValueChangeEventArguments[tuple[Option[P, P], ...]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[Option[P, P]]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[tuple[Option[P, P], ...]], ValidationDict[tuple[Option[P, P], ...]]]] = ...,
    ) -> Select[tuple[Option[P, P], ...], Option[P, P]]:
    ...


@overload
def select(
    options: Iterable[P], *, label: str = ..., value: Optional[P] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[Option[P, P]]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[Option[P, P]]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[Optional[Option[P, P]]], ValidationDict[Optional[Option[P, P]]]]] = ...,
    ) -> Select[Optional[Option[P, P]], Option[P, P]]:
    ...

def select(
        options: Union[Iterable[T], Iterable[P]], *,
        label: str = '',
        value: Union[
            tuple[T, ...],
            tuple[P, ...],
            Optional[T],
            Optional[P]
        ] = None,
        on_change: Union[
            Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]],
            Optional[Handler[ValueChangeEventArguments[Optional[T]]]],
        ] = None,
        with_input: bool = False,
        new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None,
        new_value_to_option: Optional[Callable[[str], Optional[T]]] = None,
        clearable: bool = False,
        validation: Union[
            Optional[Union[ValidationFunction[tuple[T, ...]], ValidationDict[tuple[T, ...]]]],
            Optional[Union[ValidationFunction[Optional[T]], ValidationDict[Optional[T]]]],
        ] = None,
        ) -> Union[
            Select[tuple[T, ...], T],
            Select[Optional[T], T],
            Select[Optional[Option[P, P]], Option[P, P]],
            Select[tuple[Option[P, P], ...], Option[P, P]],
        ]:
    return Select(
        options=options, label=label, value=value, on_change=on_change,
        with_input=with_input, new_value_mode=new_value_mode, new_value_to_option=new_value_to_option,
        clearable=clearable, validation=validation
    )
