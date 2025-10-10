from collections.abc import Generator, Iterator
from copy import deepcopy
from typing import (Any, Callable, Collection, Generic, Iterator,
                    Literal, Optional, Union, overload)

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import T, ChoiceElement, Option
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import (ValidationDict, ValidationElement,
                                        ValidationFunction)


class Select(LabelElement, ValidationElement, ChoiceElement[T], DisableableElement, Generic[T], component='select.js'):

    def __init__(self,
                 options: Union[list[T], T], *,
                 new_value_to_option: Callable[["Select[T]", str], T],
                 label: Optional[str] = None,
                 value: Union[list[T], Optional[T]] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 with_input: bool = False,
                 new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None,
                 multiple: bool = False,
                 clearable: bool = False,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 key_generator: Optional[Union[Callable[[T], Any], Iterator[T]]] = None,
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
        :param key_generator: a callback or iterator to generate a dictionary key for new values
        """
        self.multiple = multiple
        if multiple and isinstance(value, list):
            value = value[:]. # Note: avoid modifying the original list which could be the list of options (#3014)
        if multiple and value is None:
            value = []
        self.new_value_to_option = new_value_to_option
        super().__init__(label=label, options=options, value=value, on_change=on_change, validation=validation)
        if isinstance(key_generator, Generator):
            next(key_generator)  # prime the key generator, prepare it to receive the first value
        self.key_generator = key_generator
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

        self._is_showing_popup = False
        self.on('popup-show', lambda e: setattr(e.sender, '_is_showing_popup', True))
        self.on('popup-hide', lambda e: setattr(e.sender, '_is_showing_popup', False))

    @property
    def is_showing_popup(self) -> bool:
        """Whether the options popup is currently shown."""
        return self._is_showing_popup

    def _event_args_to_value(self, e: GenericEventArguments[Optional[Union[list[Union[Option[Any, Any], str]], Option[Any, Any]]]]) -> Any:
        # pylint: disable=too-many-nested-blocks
        if isinstance(e.args, dict) and not self.multiple:
            return e.args
        if isinstance(e.args, str) and not self.multiple:
            new_value = self._handle_new_value(self.new_value_to_option(self, e.args))
            return new_value if new_value in self._values else None
        if e.args is None:
            return None
        if self.multiple:
            args = [self._handle_new_value(self.new_value_to_option(self, a)) if isinstance(a, str) else a for a in e.args]
            if self._props.get('new-value-mode') == 'add-unique':
                args = list({o["value"]: o for o in args}.values())
                # ^ handle issue #4896: eliminate duplicate arguments
            return args

    def _handle_new_value(self, value: T) -> T:
        mode = self._props['new-value-mode']
        option = value
        if mode == 'add':
            self.options.append(option)
        elif mode == 'add-unique':
            if option["value"] not in [o["value"] for o in self.options]:
                self.options.append(option)
        elif mode == 'toggle':
            if option["value"] in [o["value"] for o in self.options]:
                self.options = [o for o in self.options if o["value"] != option["value"]]
            else:
                self.options.append(option)
        self._update_values_and_labels()
        return option
