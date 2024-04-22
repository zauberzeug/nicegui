from pathlib import Path
from typing import Any, Callable, List, Optional

from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement


class CodeMirror(ValueElement, DisableableElement, component='codemirror.js'):
    VALUE_PROP = 'value'
    LOOPBACK = None

    def __init__(
        self,
        value: str = '',
        *,
        on_change: Optional[Callable[..., Any]] = None,
        language: str = 'Python',
        theme: str = 'basicDark',
        indent: str = ' ' * 4,
        line_wrapping: bool = False,
        highlight_whitespace: bool = False,
        min_height: str = '',
        max_height: str = '',
        fixed_height: str = '',
    ) -> None:
        """CodeMirror

        An element to create a code editor using `CodeMirror <https://codemirror.net/>`_.

        It supports syntax highlighting for over 140 languages, more than 30 themes, line numbers, code folding, (limited) auto-completion, and more.

        Supported languages and themes:
            - Languages: A list of supported languages can be found in the `@codemirror/language-data <https://github.com/codemirror/language-data/blob/main/src/language-data.ts>`_ package.
            - Themes: A list can be found in the `@uiw/codemirror-themes-all <https://github.com/uiwjs/react-codemirror/tree/master/themes/all>`_ package.

        At runtime, the methods `supported_languages` and `supported_themes` can be used to get supported languages and themes.

        :param value: initial value of the editor (default: "")
        :param on_change: callback to be executed when the value changes (default: `None`)
        :param language: initial language of the editor. Case-insensitive (default: "Python")
        :param theme: initial theme of the editor (default: "basicDark")
        :param indent: string to use for indentation. Can be any string consisting entirely of the same whitespace character. (default: "    ")
        :param line_wrapping: whether to wrap lines (default: `False`)
        :param highlight_whitespace: whether to highlight whitespace (default: `False`)
        :param min_height: minimum height of the editor. Can be any valid CSS height value (default: "")
        :param max_height: maximum height of the editor. Can be any valid CSS height value (default: "")
        :param fixed_height: fixed height of the editor. If set, min/max height are ignored (default: "")
        """

        super().__init__(value=value, on_value_change=on_change)
        self.add_resource(Path(__file__).parent / 'lib' / 'codemirror')

        self._props['language'] = language
        self._props['theme'] = theme
        self._props['indent'] = indent
        self._props['lineWrapping'] = line_wrapping
        self._props['highlightWhitespace'] = highlight_whitespace
        self._props['minHeight'] = min_height
        self._props['maxHeight'] = max_height
        self._props['fixedHeight'] = fixed_height

    @property
    def theme(self) -> str:
        """The current theme of the editor."""
        return self._props['theme']

    def set_theme(self, theme: str) -> None:
        """Sets the theme of the editor."""
        self._props['theme'] = theme
        self.update()

    @property
    def language(self) -> str:
        """The current language of the editor."""
        return self._props['language']

    def set_language(self, language: str) -> None:
        """Sets the language of the editor (case-insensitive)."""
        self._props['language'] = language
        self.update()

    async def supported_languages(self, *, timeout: float = 10) -> List[str]:
        """Get the list of supported languages."""
        await self.client.connected()
        values = await self.run_method('get_languages', timeout=timeout)
        return sorted(values)

    async def supported_themes(self, *, timeout: float = 10) -> List[str]:
        """Get the list of supported themes."""
        await self.client.connected()
        values = await self.run_method('get_themes', timeout=timeout)
        return sorted(values)
