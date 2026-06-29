from __future__ import annotations

from itertools import accumulate, chain, repeat
from typing import Literal, TypedDict, get_args

from typing_extensions import NotRequired, Self

from ...defaults import DEFAULT_PROP, resolve_defaults
from ...elements.mixins.disableable_element import DisableableElement
from ...elements.mixins.value_element import ValueElement
from ...events import CodeMirrorKeyBindingEventArguments, GenericEventArguments, Handler, ValueChangeEventArguments
from .constants import SUPPORTED_LANGUAGES, SUPPORTED_THEMES
from .keybindings import KeyBindingElement

# Functional TypedDict syntax because `from` and `class` are Python keywords.
MarkDecorationSpec = TypedDict(
    'MarkDecorationSpec',
    {
        'kind': Literal['mark'],
        'from': int,
        'to': int,
        'class': NotRequired[str],
        'attributes': NotRequired[dict[str, str]],
        'inclusiveStart': NotRequired[bool],
        'inclusiveEnd': NotRequired[bool],
    },
)

LineDecorationSpec = TypedDict(
    'LineDecorationSpec',
    {
        'kind': Literal['line'],
        'line': int,
        'class': NotRequired[str],
        'attributes': NotRequired[dict[str, str]],
    },
)

ReplaceDecorationSpec = TypedDict(
    'ReplaceDecorationSpec',
    {
        'kind': Literal['replace'],
        'from': int,
        'to': int,
        'text': NotRequired[str],
        'class': NotRequired[str],
        'inclusive': NotRequired[bool],
        'block': NotRequired[bool],
    },
)

WidgetDecorationSpec = TypedDict(
    'WidgetDecorationSpec',
    {
        'kind': Literal['widget'],
        'position': int,
        'text': str,
        'class': NotRequired[str],
        'side': NotRequired[Literal[-1, 1]],
    },
)

DecorationSpec = MarkDecorationSpec | LineDecorationSpec | ReplaceDecorationSpec | WidgetDecorationSpec


class CodeMirror(KeyBindingElement, ValueElement[str], DisableableElement,
                 component='codemirror.js',
                 esm={'nicegui-codemirror': 'dist'},
                 default_classes='nicegui-codemirror'):
    VALUE_PROP = 'value'
    LOOPBACK = None

    @resolve_defaults
    def __init__(
        self,
        value: str = '',
        *,
        on_change: Handler[ValueChangeEventArguments[str]] | None = None,
        keymap: dict[str, Handler[CodeMirrorKeyBindingEventArguments] | CodeMirror.KeyBinding] | None = None,
        language: SUPPORTED_LANGUAGES | None = DEFAULT_PROP | None,
        theme: SUPPORTED_THEMES = DEFAULT_PROP | 'basicLight',
        indent: str = DEFAULT_PROP | ' ' * 4,
        line_wrapping: bool = DEFAULT_PROP | False,
        highlight_whitespace: bool = DEFAULT_PROP | False,
        decorations: list[DecorationSpec] | None = None,
        decoration_text_html: bool = False,
        line_tooltips: dict[int, str] | None = None,
        line_tooltip_html: bool = False,
    ) -> None:
        """CodeMirror

        An element to create a code editor using `CodeMirror <https://codemirror.net/>`_.

        It supports syntax highlighting for over 140 languages, more than 30 themes, line numbers, code folding, (limited) auto-completion, and more.

        Supported languages and themes:
            - Languages: A list of supported languages can be found in the `@codemirror/language-data <https://github.com/codemirror/language-data/blob/main/src/language-data.ts>`_ package.
            - Themes: A list can be found in the `@uiw/codemirror-themes-all <https://github.com/uiwjs/react-codemirror/tree/master/themes/all>`_ package.

        At runtime, the methods `supported_languages` and `supported_themes` can be used to get supported languages and themes.

        *Since version 3.13.0:*
        Per-line tooltips can be attached via the ``line_tooltips`` dict.

        *Since version 3.14.0:*
        The ``keymap`` maps keystrokes (CodeMirror key strings) to Python callbacks.
        Pass a bare callable for the default config (prevents the browser default, no per-OS override).
        Wrap with ``KeyBinding`` for per-key overrides such as ``prevent_default=False`` or platform-specific shortcuts (``mac=``, ``linux=``, ``win=``).
        Use ``map_key`` to add keybindings at runtime and ``unmap_key`` to drop them.
        Keybindings do not fire while the editor is disabled.

        :param value: initial value of the editor (default: "")
        :param on_change: callback to be executed when the value changes (default: `None`)
        :param keymap: mapping of CodeMirror key strings (e.g. "Mod-s", "F5") to handlers, optionally wrapped with ``KeyBinding`` (default: ``None``, *added in version 3.14.0*)
        :param language: initial language of the editor (case-insensitive, default: `None`)
        :param theme: initial theme of the editor (default: "basicLight")
        :param indent: string to use for indentation (any string consisting entirely of the same whitespace character, default: "    ")
        :param line_wrapping: whether to wrap lines (default: `False`)
        :param highlight_whitespace: whether to highlight whitespace (default: `False`)
        :param decorations: initial list of decoration specs applied to the editor (default: ``None``)
        :param decoration_text_html: render the ``text`` field of replace/widget decorations as sanitized HTML rather than plain text (default: ``False``)
        :param line_tooltips: initial mapping of 1-indexed line numbers to tooltip content (default: ``None``, *added in version 3.13.0*)
        :param line_tooltip_html: render tooltip content as sanitized HTML rather than plain text (default: ``False``, *added in version 3.13.0*)
        """
        super().__init__(value=value, on_value_change=self._update_codepoints, keymap=keymap)
        self._codepoints = b''
        self._update_codepoints()
        if on_change is not None:
            super().on_value_change(on_change)

        self._props['language'] = language
        self._props['theme'] = theme
        self._props['indent'] = indent
        self._props['line-wrapping'] = line_wrapping
        self._props['highlight-whitespace'] = highlight_whitespace
        self._props['decorations'] = decorations or []
        self._props['decoration-text-html'] = decoration_text_html
        self._props['line-tooltips'] = line_tooltips or {}
        self._props['line-tooltip-html'] = line_tooltip_html
        self._update_method = 'setEditorValueFromProps'

        self._props.add_rename('highlightWhitespace', 'highlight-whitespace')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('lineWrapping', 'line-wrapping')  # DEPRECATED: remove in NiceGUI 4.0

    @property
    def theme(self) -> str:
        """The current theme of the editor."""
        return self._props['theme']

    @theme.setter
    def theme(self, theme: SUPPORTED_THEMES) -> None:
        self._props['theme'] = theme

    def set_theme(self, theme: SUPPORTED_THEMES) -> Self:
        """Sets the theme of the editor."""
        self._props['theme'] = theme
        return self

    @property
    def supported_themes(self) -> list[str]:
        """List of supported themes."""
        return list(get_args(SUPPORTED_THEMES))

    @property
    def language(self) -> str:
        """The current language of the editor."""
        return self._props['language']

    @language.setter
    def language(self, language: SUPPORTED_LANGUAGES | None = None) -> None:
        self._props['language'] = language

    def set_language(self, language: SUPPORTED_LANGUAGES | None = None) -> Self:
        """Sets the language of the editor (case-insensitive)."""
        self._props['language'] = language
        return self

    @property
    def supported_languages(self) -> list[str]:
        """List of supported languages."""
        return list(get_args(SUPPORTED_LANGUAGES))

    @property
    def line_wrapping(self) -> bool:
        """Whether line wrapping is enabled

        *Added in version 3.2.0*
        """
        return self._props['line-wrapping']

    @line_wrapping.setter
    def line_wrapping(self, value: bool) -> None:
        self._props['line-wrapping'] = value

    def set_line_wrapping(self, value: bool) -> Self:
        """Sets whether line wrapping is enabled.

        *Added in version 3.2.0*
        """
        self._props['line-wrapping'] = value
        return self

    @property
    def decorations(self) -> list[DecorationSpec]:
        """Decoration specs applied to the editor; mutating this list syncs to the client.

        Decorations style or modify the editor's rendering without changing the underlying document.
        Each entry is a :class:`MarkDecorationSpec`, :class:`LineDecorationSpec`,
        :class:`ReplaceDecorationSpec`, or :class:`WidgetDecorationSpec` dict.
        For mark and line decorations the ``class`` field produces the visible styling, so the host
        application is responsible for shipping CSS for whatever class names it passes here.
        The ``attributes`` field is applied as raw DOM attributes (including event handlers like
        ``onclick``) and is not sanitized.
        Do not pass untrusted input through it.

        *Added in version X.Y.Z*
        """
        return self._props['decorations']

    @decorations.setter
    def decorations(self, decorations: list[DecorationSpec] | None) -> None:
        self._props['decorations'] = decorations or []

    @property
    def line_tooltips(self) -> dict[int, str]:
        """Mapping of 1-indexed line numbers to tooltip content.

        *Added in version 3.13.0*
        """
        return self._props['line-tooltips']

    @line_tooltips.setter
    def line_tooltips(self, value: dict[int, str]) -> None:
        self._props['line-tooltips'] = value

    def _event_args_to_value(self, e: GenericEventArguments) -> str:
        """The event contains a change set which is applied to the current value."""
        return self._apply_change_set(e.args['sections'], e.args['inserted'])

    @staticmethod
    def _encode_codepoints(doc: str) -> bytes:
        return b''.join(b'\0\1' if ord(c) > 0xFFFF else b'\1' for c in doc)

    def _update_codepoints(self) -> None:
        """Update `self._codepoints` as a concatenation of "1" for code points <=0xFFFF and "01" for code points >0xFFFF.

        This captures how many Unicode code points are encoded by each UTF-16 code unit.
        This is used to convert JavaScript string indices to Python by summing `self._codepoints` up to the JavaScript index.
        """
        if not self._send_update_on_value_change:
            return  # the update is triggered by the user and codepoints are updated incrementally
        self._codepoints = self._encode_codepoints(self.value or '')

    def _apply_change_set(self, sections: list[int], inserted: list[list[str]]) -> str:
        document = self.value or ''
        old_lengths = sections[::2]
        new_lengths = sections[1::2]
        end_positions = accumulate(old_lengths)
        document_parts: list[str] = []
        codepoint_parts: list[bytes] = []
        for end, old_len, new_len, insert in zip(
            end_positions, old_lengths, new_lengths, chain(inserted, repeat([])), strict=False,
        ):
            if new_len == -1:
                start = end - old_len
                py_start = self._codepoints[:start].count(1)
                py_end = py_start + self._codepoints[start:end].count(1)
                document_parts.append(document[py_start:py_end])
                codepoint_parts.append(self._codepoints[start:end])
            else:
                joined_insert = '\n'.join(insert)
                document_parts.append(joined_insert)
                codepoint_parts.append(self._encode_codepoints(joined_insert))
        self._codepoints = b''.join(codepoint_parts)
        return ''.join(document_parts)
