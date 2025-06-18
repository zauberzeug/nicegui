from typing import Any, Dict, List, Optional, Union

from nicegui.elements.mixins.value_element import ValueElement
from nicegui.events import Handler, ValueChangeEventArguments


class ButtonToggle(ValueElement):

    def __init__(
        self,
        options: Union[List[str], List[Dict[str, Any]]],
        *,
        value: Optional[str] = None,
        on_change: Optional[Handler[ValueChangeEventArguments]] = None,
        **kwargs,
    ) -> None:
        """Button Toggle

        A button toggle group component that maintains a selected value.
        This element is based on Quasar's `QBtnToggle <https://quasar.dev/vue-components/button-toggle>`_ component.

        Args:
            options: List of options. Can be strings or dicts with 'label' and 'value' keys
            value: Initial selected value (default: None)
            on_change: Callback function that receives the new value when changed
            **kwargs: Additional props to pass to the underlying q-btn-toggle
        """
        # Process options to ensure they have the right format
        processed_options = []
        for option in options:
            if isinstance(option, str):
                processed_options.append({'label': option, 'value': option})
            elif isinstance(option, dict):
                if 'label' in option and 'value' in option:
                    processed_options.append(option)
                else:
                    # If missing label or value, use the option as both
                    label = option.get('label', str(option.get('value', option)))
                    value_key = option.get('value', label)
                    processed_options.append({'label': label, 'value': value_key})
            else:
                # Convert other types to string
                str_option = str(option)
                processed_options.append({'label': str_option, 'value': str_option})

        super().__init__(tag='q-btn-toggle', value=value, on_value_change=on_change)
        self._props['options'] = processed_options
        self._props.update(kwargs)
