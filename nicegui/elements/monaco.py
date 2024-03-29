from pathlib import Path
from typing import Optional

from nicegui import ui
from nicegui.element import Element


class Monaco(Element, component="monaco.js", ):
    def __init__(self, language: Optional[str], theme: str, value: str, minimap: bool):
        """Monaco

        
        Monaco code editor. See https://microsoft.github.io/monaco-editor/

        :param language: Language identifier (e.g. 'python')
        :param theme: Theme identifier (e.g. 'vs-dark')
        :param value: Initial value
        :param minimap: Show minimap
        

        
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib' / 'monaco-editor' / 'vs' / 'editor')

        self._props['language'] = language
        self._props['theme'] = theme
        self._props['value'] = value
        self._props['minimap'] = minimap

