from typing import Callable, Dict, Optional

from .input import Input


class Textarea(Input):

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Callable] = None,
                 validation: Dict[str, Callable] = {}) -> None:
        """Textarea

        This element is based on Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component.
        The ``type`` is set to ``textarea`` to create a multi-line text input.

        :param label: displayed name for the textarea
        :param placeholder: text to show if no value is entered
        :param value: the initial value of the field
        :param on_change: callback to execute when the input is confirmed by leaving the focus
        :param validation: dictionary of validation rules, e.g. ``{'Too short!': lambda value: len(value) < 3}``
        """
        super().__init__(label, placeholder=placeholder, value=value, on_change=on_change, validation=validation)
        self._props['type'] = 'textarea'
