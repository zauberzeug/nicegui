from typing import Any, Callable, Optional

from nicegui.elements.mixins.value_element import ValueElement


class CodeMirror(ValueElement, component="codemirror.js"):
    VALUE_PROP = "value"

    def __init__(
        self,
        value: str = "",
        on_change: Optional[Callable[..., Any]] = None,
        language: str = "python",
        theme: str = "dracula",
    ) -> None:
        """CodeMirror

        CodeMirror is a versatile text editor implemented in JavaScript for the browser.
        """
        super().__init__(value=value, on_value_change=on_change)
        self._props["mode"] = language
        self._props["theme"] = theme
