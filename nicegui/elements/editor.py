from typing import Any, Callable, Optional

from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Editor(ValueElement, DisableableElement):
    """
    A WYSIWYG editor based on Quasar's QEditor.

    The `Editor` class provides a rich text editor component that allows users to input and format text using a WYSIWYG (What You See Is What You Get) interface. It is based on Quasar's QEditor component.

    Usage:
    ```python
    editor = Editor(
        placeholder="Enter your text here",
        value="",
        on_change=my_callback_function
    )
    ```

    Parameters:
    - `placeholder` (Optional[str]): The placeholder text to be displayed when the editor is empty.
    - `value` (str): The initial value of the editor, represented as HTML code.
    - `on_change` (Optional[Callable[..., Any]]): A callback function to be invoked when the value of the editor changes.

    Attributes:
    - `tag` (str): The HTML tag used to render the editor component.
    - `value` (str): The current value of the editor, represented as HTML code.
    - `on_value_change` (Optional[Callable[..., Any]]): The callback function to be invoked when the value of the editor changes.
    - `_classes` (List[str]): The CSS classes applied to the editor component.
    - `_props` (Dict[str, Any]): Additional properties of the editor component.

    Example:
    ```python
    def handle_editor_change(new_value):
        print("Editor value changed:", new_value)

    editor = Editor(
        placeholder="Enter your text here",
        value="<p>Hello, world!</p>",
        on_change=handle_editor_change
    )
    ```

    Note:
    The `Editor` class inherits from the `ValueElement` and `DisableableElement` classes, which provide common functionality for elements with a value and disable state.
    """
    def __init__(self,
                 *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Callable[..., Any]] = None,
                 ) -> None:
        """Editor
        A WYSIWYG editor based on [Quasar's QEditor](https://quasar.dev/vue-components/editor).
        The value is a string containing the formatted text as HTML code.
        Args:
            
            - value: initial value
            - on_change: callback to be invoked when the value changes
        """
        super().__init__(tag='q-editor', value=value, on_value_change=on_change)
        self._classes.append('nicegui-editor')
        if placeholder is not None:
            self._props['placeholder'] = placeholder
