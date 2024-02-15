from typing import Any, Callable, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Checkbox(TextElement, ValueElement, DisableableElement):
    """A checkbox element.

    This element is based on Quasar's QCheckbox component.

    Args:
        text (str, optional): The label to display next to the checkbox. Defaults to ''.
        value (bool, optional): Whether the checkbox should be checked initially. Defaults to False.
        on_change (Callable[..., Any], optional): Callback to execute when the value changes. Defaults to None.

    Attributes:
        tag (str): The HTML tag for the checkbox element.

    Example:
        >>> checkbox = Checkbox(text='Enable', value=True, on_change=handle_checkbox_change)
        >>> checkbox.render()
        '<q-checkbox v-model="value" label="Enable" @change="handle_checkbox_change"></q-checkbox>'
    """

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Callable[..., Any]] = None) -> None:
        """Checkbox

        This element is based on Quasar's [QCheckbox ](https://quasar.dev/vue-components/checkbox) component.

        - text: the label to display next to the checkbox
        - value: whether it should be checked initially (default: `False`)
        - on_change: callback to execute when value changes
        """
        super().__init__(tag='q-checkbox', text=text, value=value, on_value_change=on_change)
