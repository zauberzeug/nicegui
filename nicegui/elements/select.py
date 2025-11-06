from copy import deepcopy
from typing import Any, Callable, Generic, Literal, Optional, Union, overload

from typing_extensions import TypeVar, TypeIs

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from ..helpers import add_docstring_from
from .choice_element import ChoiceElement, Option, OptionDict, T, P, to_option
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction

V = TypeVar('V', bound='Union[tuple[Option[Any, Any], ...], Optional[Option[Any, Any]]]')
VAL = TypeVar('VAL')


def are_all_primitive_type(values: Union[list[T], list[P]]) -> TypeIs[list[P]]:
    return all(isinstance(v, (str, int, float, bool)) for v in values)


@overload
def _convert_options(options: dict[VAL, P]) -> list[Option[P, VAL]]:
    ...

@overload
def _convert_options(options: list[T]) -> list[T]:
    ...   

@overload
def _convert_options(options: list[P]) -> list[Option[P, P]]:
    ...

def _convert_options(options: Union[dict[VAL, P], list[T], list[P]]) -> Union[list[Option[P, VAL]], list[T], list[Option[P, P]]]:
    if isinstance(options, dict):
        return [Option(v, k) for k, v in options.items()]
    if are_all_primitive_type(options):
        return [to_option(v) for v in options]
    return list(options)


class Select(
    LabelElement,
    ValidationElement[V],
    ChoiceElement[V, T],
    DisableableElement,
    Generic[V, T],
    component='select.js'
    ):

    def __init__(self,
                 options: Union[dict[VAL, P], list[T], list[P]], *,
                 label: str = '',
                 value: Union[list[T], list[P], list[VAL], Optional[T], Optional[VAL], Optional[P]] = None,
                 on_change: Optional[Union[
                    Handler[ValueChangeEventArguments[tuple[T, ...]]],
                    Handler[ValueChangeEventArguments[Optional[T]]],
                ]] = None,
                with_input: bool = False,
                new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None,
                multiple: bool = False,
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
        self.multiple = multiple
        self.new_value_mode = new_value_mode
        self.new_value_to_option: Optional[Callable[[str], Optional[T]]] = new_value_to_option
        if self.new_value_mode and self.new_value_to_option is None:
            raise ValueError(
                f"new_value_to_option not passed. You must provide a function for handling new values when new value mode is '{self.new_value_mode}'."
                )
        converted_options = _convert_options(options)
        value_to_option = {o.value: o for o in converted_options}
        if multiple and isinstance(value, list):
            super().__init__(
                label=label or None, options=converted_options, value=tuple(value_to_option[v] for v in value), on_change=on_change, validation=validation
                )
        else:
            super().__init__(label=label or None, options=converted_options, value=value_to_option[value] if value else None, on_change=on_change, validation=validation)
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

    def _invalid_values(self, value: V) -> tuple[Any, ...]:
        if value is None:
            return tuple()
        if isinstance(value, tuple):
            return tuple(set(o.value for o in value) - set(self._values))
        return tuple(set([value.value]) - set(self._values))

    @property
    def is_showing_popup(self) -> bool:
        """Whether the options popup is currently shown."""
        return self._is_showing_popup

    def _event_args_to_value(self, e: GenericEventArguments[Union[list[Union[OptionDict[Any, Any], str]], Optional[Union[OptionDict[Any, Any], str]]]]) -> Union[tuple[T, ...], Optional[T]]:
        if isinstance(e.args, list):
            if self.new_value_mode == 'add-unique':
                # handle issue #4896: eliminate duplicate arguments
                for arg1 in [a for a in e.args if isinstance(a, str)]:
                    for arg2 in [a for a in e.args if isinstance(a, dict)]:
                        if arg1 == arg2['value']:
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

    def _value_to_model_value(self, value: V) -> Any:
        if isinstance(value, tuple):
            return tuple(v for v in value if v.value in self._values)
        return value if value is not None and value.value in self._values else None

    def _handle_new_value(self, value: str) -> Optional[T]:
        assert self.new_value_to_option
        mode = self.new_value_mode
        new_option: Optional[T] = self.new_value_to_option(value)
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
    options: list[T], *, label: str = ..., value: list[T],
    on_change: Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    multiple: Literal[True] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[T]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[tuple[T, ...]], ValidationDict[tuple[T, ...]]]] = ...,
    ) -> Select[tuple[T, ...], T]:
    ...

@overload
def select(
    options: list[T], *, label: str = ..., value: Optional[T] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[T]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    multiple: Literal[False] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[T]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[Optional[T]], ValidationDict[Optional[T]]]] = ...,
    ) -> Select[Optional[T], T]:
    ...

@overload
def select(
    options: list[P], *, label: str = ..., value: list[P],
    on_change: Optional[Handler[ValueChangeEventArguments[tuple[Option[P, P], ...]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    multiple: Literal[True] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[Option[P, P]]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[tuple[Option[P, P], ...]], ValidationDict[tuple[Option[P, P], ...]]]] = ...,
    ) -> Select[tuple[Option[P, P], ...], Option[P, P]]:
    ...

@overload
def select(
    options: list[P], *, label: str = ..., value: Optional[P] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[Option[P, P]]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    multiple: Literal[False] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[Option[P, P]]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[Optional[Option[P, P]]], ValidationDict[Optional[Option[P, P]]]]] = ...,
    ) -> Select[Optional[Option[P, P]], Option[P, P]]:
    ...

@overload
def select(
    options: list[P], *, label: str = ..., value: Literal[None] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[Option[P, P]]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    multiple: Literal[False] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[Option[P, P]]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[Optional[Option[P, P]]], ValidationDict[Optional[Option[P, P]]]]] = ...,
    ) -> Select[Optional[Option[P, P]], Option[P, P]]:
    ...

@overload
def select(
    options: dict[VAL, P], *, label: str = ..., value: Optional[VAL] = ...,
    on_change: Optional[Handler[ValueChangeEventArguments[Optional[Option[P, VAL]]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    multiple: Literal[False] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[Option[P, VAL]]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[Optional[Option[P, VAL]]], ValidationDict[Optional[Option[P, VAL]]]]] = ...,
    ) -> Select[Optional[Option[P, VAL]], Option[P, VAL]]:
    ...

@overload
def select(
    options: dict[VAL, P], *, label: str = ..., value: list[VAL],
    on_change: Optional[Handler[ValueChangeEventArguments[tuple[Option[P, VAL], ...]]]] = ...,
    with_input: bool = ...,
    new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = ...,
    multiple: Literal[True] = ...,
    new_value_to_option: Optional[Callable[[str], Optional[Option[P, VAL]]]] = ...,
    clearable: bool = ...,
    validation: Optional[Union[ValidationFunction[tuple[Option[P, VAL], ...]], ValidationDict[tuple[Option[P, VAL], ...]]]] = ...,
    ) -> Select[tuple[Option[P, VAL], ...], Option[P, VAL]]:
    ...

# pylint: disable=missing-function-docstring
@add_docstring_from(Select.__init__)
def select(
        options: Union[dict[VAL, P], list[T], list[P]], *,
        label: str = '',
        value: Union[list[T], Optional[T], list[VAL], list[P], Optional[VAL]] = None,
        on_change: Union[
            Optional[Handler[ValueChangeEventArguments[tuple[T, ...]]]],
            Optional[Handler[ValueChangeEventArguments[Optional[T]]]],
        ] = None,
        with_input: bool = False,
        new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None,
        multiple: bool = False,
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
            Select[Optional[Option[P, VAL]], Option[P, VAL]],
            Select[tuple[Option[P, VAL], ...], Option[P, VAL]]
        ]:
    return Select(
        options=options, label=label, value=value, on_change=on_change,
        with_input=with_input, new_value_mode=new_value_mode, multiple=multiple, 
        new_value_to_option=new_value_to_option,
        clearable=clearable, validation=validation
    )
