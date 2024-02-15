from typing import Any, Callable, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Expansion(TextElement, ValueElement, DisableableElement):
    """
    Represents an expandable container based on Quasar's QExpansionItem component.

    Args:
        text (str): The title text of the expansion.
        caption (str, optional): The optional caption (or sub-label) text. Defaults to None.
        icon (str, optional): The optional icon. Defaults to None.
        group (str, optional): The optional group name for coordinated open/close state within the group, also known as "accordion mode". Defaults to None.
        value (bool, optional): Whether the expansion should be opened on creation. Defaults to False.
        on_value_change (callable, optional): The callback to execute when the value changes. Defaults to None.

    Attributes:
        tag (str): The HTML tag for the expansion item.
        value (bool): Whether the expansion is currently open or closed.
        _props (dict): The dictionary of additional properties for the expansion item.
        _classes (list): The list of additional CSS classes for the expansion item.

    Methods:
        open(): Opens the expansion.
        close(): Closes the expansion.
        _text_to_model_text(text: str): Converts the given text to the model text.

    Example:
        # Create an expansion with a title and a caption
        expansion = Expansion(text='My Expansion', caption='Expand me!')

        # Open the expansion
        expansion.open()

        # Close the expansion
        expansion.close()
    """

    def __init__(self,
                 text: str = '', *,
                 caption: Optional[str] = None,
                 icon: Optional[str] = None,
                 group: Optional[str] = None,
                 value: bool = False,
                 on_value_change: Optional[Callable[..., Any]] = None
                 ) -> None:
        """Expansion Element

        Provides an expandable container based on Quasar's QExpansionItem component.

        Args:
            text (str): The title text of the expansion.
            caption (str, optional): The optional caption (or sub-label) text. Defaults to None.
            icon (str, optional): The optional icon. Defaults to None.
            group (str, optional): The optional group name for coordinated open/close state within the group, also known as "accordion mode". Defaults to None.
            value (bool, optional): Whether the expansion should be opened on creation. Defaults to False.
            on_value_change (callable, optional): The callback to execute when the value changes. Defaults to None.
        """
        super().__init__(tag='q-expansion-item', text=text, value=value, on_value_change=on_value_change)
        if caption is not None:
            self._props['caption'] = caption
        if group is not None:
            self._props['group'] = group
        self._props['icon'] = icon
        self._classes.append('nicegui-expansion')

    def open(self) -> None:
            """
            Open the expansion.

            This method sets the value of the expansion to True, indicating that it should be open.
            The expansion can be used to display additional content or options to the user.

            Usage:
                expansion = Expansion()
                expansion.open()

            Returns:
                None
            """
            self.value = True

    def close(self) -> None:
            """Close the expansion.

            This method sets the value of the expansion to False, effectively closing it.

            Usage:
                expansion.close()

            Returns:
                None
            """
            self.value = False

    def _text_to_model_text(self, text: str) -> None:
            """
            Converts the given text to the model text.

            Parameters:
                text (str): The text to be converted.

            Returns:
                None

            Description:
                This method is responsible for converting the given text to the model text.
                It updates the 'label' property of the element with the provided text.

            Usage:
                Call this method to update the label of the element with the desired text.
            """
            self._props['label'] = text
