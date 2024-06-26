from typing import Any, Callable, Dict, Optional, Union

from .input import Input


class Textarea(Input, component='input.js'):

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Callable[..., Any]] = None,
                 validation: Optional[Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]] = None,
                 ) -> None:
        """Textarea

        This element is based on Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component.
        The ``type`` is set to ``textarea`` to create a multi-line text input.

        You can use the `validation` parameter to define a dictionary of validation rules,
        e.g. ``{'Too long!': lambda value: len(value) < 3}``.
        The key of the first rule that fails will be displayed as an error message.
        Alternatively, you can pass a callable that returns an optional error message.
        To disable the automatic validation on every value change, you can use the `without_auto_validation` method.

        :param label: displayed name for the textarea
        :param placeholder: text to show if no value is entered
        :param value: the initial value of the field
        :param on_change: callback to execute when the value changes
        :param validation: dictionary of validation rules or a callable that returns an optional error message
        """
        super().__init__(label, placeholder=placeholder, value=value, on_change=on_change, validation=validation)
        self._props['type'] = 'textarea'
