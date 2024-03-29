from typing import Optional

from nicegui import ui
from nicegui.element import Element


class Monaco(Element, component="monaco.js"):
    def __init__(self, language: Optional[str], theme: str, value: str, minimap: bool):
        super().__init__()
        self._props['language'] = language
        self._props['theme'] = theme
        self._props['value'] = value
        self._props['minimap'] = minimap

        
