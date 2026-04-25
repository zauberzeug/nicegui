from itertools import accumulate, chain, repeat
from typing import Any, Literal, get_args

from typing_extensions import Self

from ...defaults import DEFAULT_PROP, resolve_defaults
from ...elements.mixins.disableable_element import DisableableElement
from ...elements.mixins.value_element import ValueElement
from ...events import (
    CodeMirrorFocusChangeEventArguments,
    CodeMirrorGeometryChangeEventArguments,
    CodeMirrorHandlerSpec,
    CodeMirrorSelectionChangeEventArguments,
    CodeMirrorViewportChangeEventArguments,
    GenericEventArguments,
    Handler,
    ValueChangeEventArguments,
    handle_event,
)

SUPPORTED_LANGUAGES = Literal[
    'Angular Template',
    'APL',
    'ASN.1',
    'Asterisk',
    'Brainfuck',
    'C',
    'C#',
    'C++',
    'Clojure',
    'ClojureScript',
    'Closure Stylesheets (GSS)',
    'CMake',
    'Cobol',
    'CoffeeScript',
    'Common Lisp',
    'CQL',
    'Crystal',
    'CSS',
    'Cypher',
    'Cython',
    'D',
    'Dart',
    'diff',
    'Dockerfile',
    'DTD',
    'Dylan',
    'EBNF',
    'ECL',
    'edn',
    'Eiffel',
    'Elm',
    'Erlang',
    'Esper',
    'F#',
    'Factor',
    'FCL',
    'Forth',
    'Fortran',
    'Gas',
    'Gherkin',
    'Go',
    'Groovy',
    'Haskell',
    'Haxe',
    'HTML',
    'HTTP',
    'HXML',
    'IDL',
    'Java',
    'JavaScript',
    'Jinja2',
    'JSON',
    'JSON-LD',
    'JSX',
    'Julia',
    'Kotlin',
    'LaTeX',
    'LESS',
    'Liquid',
    'LiveScript',
    'Lua',
    'MariaDB SQL',
    'Markdown',
    'Mathematica',
    'Mbox',
    'mIRC',
    'Modelica',
    'MS SQL',
    'MscGen',
    'MsGenny',
    'MUMPS',
    'MySQL',
    'Nginx',
    'NSIS',
    'NTriples',
    'Objective-C',
    'Objective-C++',
    'OCaml',
    'Octave',
    'Oz',
    'Pascal',
    'Perl',
    'PGP',
    'PHP',
    'Pig',
    'PLSQL',
    'PostgreSQL',
    'PowerShell',
    'Properties files',
    'ProtoBuf',
    'Pug',
    'Puppet',
    'Python',
    'Q',
    'R',
    'RPM Changes',
    'RPM Spec',
    'Ruby',
    'Rust',
    'SAS',
    'Sass',
    'Scala',
    'Scheme',
    'SCSS',
    'Shell',
    'Sieve',
    'Smalltalk',
    'SML',
    'Solr',
    'SPARQL',
    'Spreadsheet',
    'SQL',
    'SQLite',
    'Squirrel',
    'sTeX',
    'Stylus',
    'Swift',
    'SystemVerilog',
    'Tcl',
    'Textile',
    'TiddlyWiki',
    'Tiki wiki',
    'TOML',
    'Troff',
    'TSX',
    'TTCN',
    'TTCN_CFG',
    'Turtle',
    'TypeScript',
    'VB.NET',
    'VBScript',
    'Velocity',
    'Verilog',
    'VHDL',
    'Vue',
    'Web IDL',
    'WebAssembly',
    'XML',
    'XQuery',
    'Xù',
    'Yacas',
    'YAML',
    'Z80',
]


SUPPORTED_THEMES = Literal[
    'abcdef',
    'abcdefDarkStyle',
    'abyss',
    'abyssDarkStyle',
    'androidstudio',
    'androidstudioDarkStyle',
    'andromeda',
    'andromedaDarkStyle',
    'atomone',
    'atomoneDarkStyle',
    'aura',
    'auraDarkStyle',
    'basicDark',
    'basicDarkStyle',
    'basicLight',
    'basicLightStyle',
    'bbedit',
    'bbeditLightStyle',
    'bespin',
    'bespinDarkStyle',
    'consoleDark',
    'consoleLight',
    'copilot',
    'copilotDarkStyle',
    'darcula',
    'darculaDarkStyle',
    'douToneLightStyle',
    'dracula',
    'draculaDarkStyle',
    'duotoneDark',
    'duotoneDarkStyle',
    'duotoneLight',
    'eclipse',
    'eclipseLightStyle',
    'githubDark',
    'githubDarkStyle',
    'githubLight',
    'githubLightStyle',
    'gruvboxDark',
    'gruvboxDarkStyle',
    'gruvboxLight',
    'kimbie',
    'kimbieDarkStyle',
    'material',
    'materialDark',
    'materialDarkStyle',
    'materialLight',
    'materialLightStyle',
    'monokai',
    'monokaiDarkStyle',
    'monokaiDimmed',
    'monokaiDimmedDarkStyle',
    'noctisLilac',
    'noctisLilacLightStyle',
    'nord',
    'nordDarkStyle',
    'okaidia',
    'okaidiaDarkStyle',
    'oneDark',
    'quietlight',
    'quietlightStyle',
    'red',
    'redDarkStyle',
    'solarizedDark',
    'solarizedDarkStyle',
    'solarizedLight',
    'solarizedLightStyle',
    'sublime',
    'sublimeDarkStyle',
    'tokyoNight',
    'tokyoNightDay',
    'tokyoNightDayStyle',
    'tokyoNightStorm',
    'tokyoNightStormStyle',
    'tokyoNightStyle',
    'tomorrowNightBlue',
    'tomorrowNightBlueStyle',
    'vscodeDark',
    'vscodeDarkStyle',
    'vscodeLight',
    'vscodeLightStyle',
    'whiteDark',
    'whiteDarkStyle',
    'whiteLight',
    'whiteLightStyle',
    'xcodeDark',
    'xcodeDarkStyle',
    'xcodeLight',
    'xcodeLightStyle',
]


class CodeMirror(ValueElement[str], DisableableElement,
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
        on_selection_change: Handler[CodeMirrorSelectionChangeEventArguments] |
        CodeMirrorHandlerSpec[CodeMirrorSelectionChangeEventArguments] | None = None,
        on_focus_change: Handler[CodeMirrorFocusChangeEventArguments] |
        CodeMirrorHandlerSpec[CodeMirrorFocusChangeEventArguments] | None = None,
        on_viewport_change: Handler[CodeMirrorViewportChangeEventArguments] |
        CodeMirrorHandlerSpec[CodeMirrorViewportChangeEventArguments] | None = None,
        on_geometry_change: Handler[CodeMirrorGeometryChangeEventArguments] |
        CodeMirrorHandlerSpec[CodeMirrorGeometryChangeEventArguments] | None = None,
        language: SUPPORTED_LANGUAGES | None = DEFAULT_PROP | None,
        theme: SUPPORTED_THEMES = DEFAULT_PROP | 'basicLight',
        indent: str = DEFAULT_PROP | ' ' * 4,
        line_wrapping: bool = DEFAULT_PROP | False,
        highlight_whitespace: bool = DEFAULT_PROP | False,
    ) -> None:
        """CodeMirror

        An element to create a code editor using `CodeMirror <https://codemirror.net/>`_.

        It supports syntax highlighting for over 140 languages, more than 30 themes, line numbers, code folding, (limited) auto-completion, and more.

        Supported languages and themes:
            - Languages: A list of supported languages can be found in the `@codemirror/language-data <https://github.com/codemirror/language-data/blob/main/src/language-data.ts>`_ package.
            - Themes: A list can be found in the `@uiw/codemirror-themes-all <https://github.com/uiwjs/react-codemirror/tree/master/themes/all>`_ package.

        At runtime, the methods `supported_languages` and `supported_themes` can be used to get supported languages and themes.

        Each ``on_*_change`` handler accepts either a bare callable (default debounce) or a wrapped
        :class:`~nicegui.events.CodeMirrorHandlerSpec` for per-registration overrides
        (e.g. ``ui.codemirror.handler(callback, debounce_ms=200)``).

        :param value: initial value of the editor (default: "")
        :param on_change: callback to be executed when the value changes (default: `None`)
        :param on_selection_change: callback when cursor line or column changes (debounced 30 ms by default)
        :param on_focus_change: callback when the editor gains or loses focus (no debounce by default)
        :param on_viewport_change: callback when the visible line range changes (debounced 100 ms by default)
        :param on_geometry_change: callback when the editor or content size changes (debounced 100 ms by default)
        :param language: initial language of the editor (case-insensitive, default: `None`)
        :param theme: initial theme of the editor (default: "basicLight")
        :param indent: string to use for indentation (any string consisting entirely of the same whitespace character, default: "    ")
        :param line_wrapping: whether to wrap lines (default: `False`)
        :param highlight_whitespace: whether to highlight whitespace (default: `False`)
        """
        super().__init__(value=value, on_value_change=self._update_codepoints)
        self._codepoints = b''
        self._update_codepoints()
        if on_change is not None:
            super().on_value_change(on_change)

        self._props['language'] = language
        self._props['theme'] = theme
        self._props['indent'] = indent
        self._props['line-wrapping'] = line_wrapping
        self._props['highlight-whitespace'] = highlight_whitespace
        self._props['selection-tracking-enabled'] = False
        self._props['focus-tracking-enabled'] = False
        self._props['viewport-tracking-enabled'] = False
        self._props['geometry-tracking-enabled'] = False
        self._props['selection-debounce-ms'] = 30
        self._props['focus-debounce-ms'] = 0
        self._props['viewport-debounce-ms'] = 100
        self._props['geometry-debounce-ms'] = 100
        self._update_method = 'setEditorValueFromProps'

        self._props.add_rename('highlightWhitespace', 'highlight-whitespace')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('lineWrapping', 'line-wrapping')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('selectionTrackingEnabled', 'selection-tracking-enabled')
        self._props.add_rename('focusTrackingEnabled', 'focus-tracking-enabled')
        self._props.add_rename('viewportTrackingEnabled', 'viewport-tracking-enabled')
        self._props.add_rename('geometryTrackingEnabled', 'geometry-tracking-enabled')
        self._props.add_rename('selectionDebounceMs', 'selection-debounce-ms')
        self._props.add_rename('focusDebounceMs', 'focus-debounce-ms')
        self._props.add_rename('viewportDebounceMs', 'viewport-debounce-ms')
        self._props.add_rename('geometryDebounceMs', 'geometry-debounce-ms')

        if on_selection_change is not None:
            self.on_selection_change(on_selection_change)
        if on_focus_change is not None:
            self.on_focus_change(on_focus_change)
        if on_viewport_change is not None:
            self.on_viewport_change(on_viewport_change)
        if on_geometry_change is not None:
            self.on_geometry_change(on_geometry_change)

    @staticmethod
    def handler(
        callback: Handler[Any],
        *,
        debounce_ms: int | None = None,
    ) -> CodeMirrorHandlerSpec[Any]:
        """Wrap a CodeMirror signal handler with per-registration config overrides.

        Use this to override the default debounce for a single signal registration::

            ui.codemirror(on_viewport_change=ui.codemirror.handler(scroll_cb, debounce_ms=200))

        :param callback: the handler callable
        :param debounce_ms: per-signal debounce override in milliseconds; ``None`` keeps the default
        """
        return CodeMirrorHandlerSpec(callback=callback, debounce_ms=debounce_ms)

    def on_selection_change(
        self,
        handler: Handler[CodeMirrorSelectionChangeEventArguments] |
        CodeMirrorHandlerSpec[CodeMirrorSelectionChangeEventArguments],
    ) -> Self:
        """Add a callback for cursor selection changes (line + column).

        Fires on selection moves and on document edits that shift the cursor line or column.
        """
        callback, debounce_ms = self._unpack_handler(handler)
        self.on('selection-change', lambda e: handle_event(callback, CodeMirrorSelectionChangeEventArguments(
            sender=self,
            client=self.client,
            line=int(e.args['line']),
            column=int(e.args['column']),
        )))
        self._props['selection-tracking-enabled'] = True
        if debounce_ms is not None:
            self._props['selection-debounce-ms'] = debounce_ms
        return self

    def on_focus_change(
        self,
        handler: Handler[CodeMirrorFocusChangeEventArguments] |
        CodeMirrorHandlerSpec[CodeMirrorFocusChangeEventArguments],
    ) -> Self:
        """Add a callback for editor focus changes."""
        callback, debounce_ms = self._unpack_handler(handler)
        self.on('focus-change', lambda e: handle_event(callback, CodeMirrorFocusChangeEventArguments(
            sender=self,
            client=self.client,
            focused=bool(e.args['focused']),
        )))
        self._props['focus-tracking-enabled'] = True
        if debounce_ms is not None:
            self._props['focus-debounce-ms'] = debounce_ms
        return self

    def on_viewport_change(
        self,
        handler: Handler[CodeMirrorViewportChangeEventArguments] |
        CodeMirrorHandlerSpec[CodeMirrorViewportChangeEventArguments],
    ) -> Self:
        """Add a callback for viewport (visible line range) changes."""
        callback, debounce_ms = self._unpack_handler(handler)
        self.on('viewport-change', lambda e: handle_event(callback, CodeMirrorViewportChangeEventArguments(
            sender=self,
            client=self.client,
            from_line=int(e.args['from_line']),
            to_line=int(e.args['to_line']),
        )))
        self._props['viewport-tracking-enabled'] = True
        if debounce_ms is not None:
            self._props['viewport-debounce-ms'] = debounce_ms
        return self

    def on_geometry_change(
        self,
        handler: Handler[CodeMirrorGeometryChangeEventArguments] |
        CodeMirrorHandlerSpec[CodeMirrorGeometryChangeEventArguments],
    ) -> Self:
        """Add a callback for editor geometry changes (width, height, content height)."""
        callback, debounce_ms = self._unpack_handler(handler)
        self.on('geometry-change', lambda e: handle_event(callback, CodeMirrorGeometryChangeEventArguments(
            sender=self,
            client=self.client,
            width=int(e.args['width']),
            height=int(e.args['height']),
            content_height=int(e.args['content_height']),
        )))
        self._props['geometry-tracking-enabled'] = True
        if debounce_ms is not None:
            self._props['geometry-debounce-ms'] = debounce_ms
        return self

    @staticmethod
    def _unpack_handler(
        handler: Handler[Any] | CodeMirrorHandlerSpec[Any],
    ) -> tuple[Handler[Any], int | None]:
        if isinstance(handler, CodeMirrorHandlerSpec):
            return handler.callback, handler.debounce_ms
        return handler, None

    def reveal_line(self, line_number: int) -> None:
        """Scroll the editor so the given 1-indexed line is visible.

        :param line_number: 1-indexed line number to scroll into view
        """
        self.run_method('revealLine', line_number)

    @property
    def theme(self) -> str:
        """The current theme of the editor."""
        return self._props['theme']

    @theme.setter
    def theme(self, theme: SUPPORTED_THEMES) -> None:
        self._props['theme'] = theme

    def set_theme(self, theme: SUPPORTED_THEMES) -> None:
        """Sets the theme of the editor."""
        self._props['theme'] = theme

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

    def set_language(self, language: SUPPORTED_LANGUAGES | None = None) -> None:
        """Sets the language of the editor (case-insensitive)."""
        self._props['language'] = language

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

    def set_line_wrapping(self, value: bool) -> None:
        """Sets whether line wrapping is enabled.

        *Added in version 3.2.0*
        """
        self._props['line-wrapping'] = value

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
