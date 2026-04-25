from itertools import accumulate, chain, repeat
from typing import Literal, TypedDict, get_args

from ...defaults import DEFAULT_PROP, resolve_defaults
from ...elements.mixins.disableable_element import DisableableElement
from ...elements.mixins.value_element import ValueElement
from ...events import GenericEventArguments, Handler, ValueChangeEventArguments


class LineAnchor(TypedDict):
    """A single anchor pinned to a line in :meth:`ui.codemirror.set_line_anchors`.

    ``id`` is a caller-chosen stable identifier used to look up the current line in
    :attr:`ui.codemirror.line_anchor_positions` after document edits remap the anchor.
    ``line`` is the 1-indexed initial line number.
    """
    id: str
    line: int


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

        :param value: initial value of the editor (default: "")
        :param on_change: callback to be executed when the value changes (default: `None`)
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

        self._anchor_positions: dict[str, dict[str, int]] = {}
        self.on('anchor-positions', self._update_anchor_mirror)

        self._props['language'] = language
        self._props['theme'] = theme
        self._props['indent'] = indent
        self._props['line-wrapping'] = line_wrapping
        self._props['highlight-whitespace'] = highlight_whitespace
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

    def set_line_anchors(self, anchors: list[LineAnchor], set_name: str = 'default') -> None:
        """Set named anchors that track document positions through edits.

        Each anchor is a :class:`LineAnchor` dict with a caller-chosen ``id`` and an initial ``line``.
        CodeMirror remaps the underlying position when the document changes;
        the current line for each anchor is mirrored on the Python side via :attr:`line_anchor_positions`.

        Multiple named sets can be managed independently (e.g. ``'breakpoints'``, ``'targets'``).
        Calling ``set_line_anchors`` for the same ``set_name`` replaces that set's anchors;
        anchors in other sets are left untouched.

        :raises ValueError: if any anchor has ``line < 1`` or if two anchors share the same ``id``
        """
        seen_ids: set[str] = set()
        for a in anchors:
            if a['line'] < 1:
                raise ValueError(f'line must be >= 1, got {a["line"]} for anchor {a["id"]!r}')
            if a['id'] in seen_ids:
                raise ValueError(f'duplicate anchor id {a["id"]!r} in set {set_name!r}')
            seen_ids.add(a['id'])
        self._anchor_positions[set_name] = {a['id']: a['line'] for a in anchors}
        self.run_method('setLineAnchors', anchors, set_name)

    def clear_line_anchors(self, set_name: str | None = None) -> None:
        """Clear anchors.

        :param set_name: clear only this named set, or all sets if ``None``
        """
        if set_name is None:
            self._anchor_positions.clear()
        else:
            self._anchor_positions.pop(set_name, None)
        self.run_method('clearLineAnchors', set_name)

    @property
    def line_anchor_positions(self) -> dict[str, dict[str, int]]:
        """Current anchor positions mirrored from the browser.

        Returns a nested dict ``{set_name: {anchor_id: 1-indexed line}}``.
        Updated synchronously when :meth:`set_line_anchors` / :meth:`clear_line_anchors` are called,
        and asynchronously when document edits remap anchor positions.
        """
        return {name: dict(positions) for name, positions in self._anchor_positions.items()}

    def _update_anchor_mirror(self, e: GenericEventArguments) -> None:
        set_name = e.args.get('set_name')
        anchors = e.args.get('anchors')
        if isinstance(set_name, str) and isinstance(anchors, dict):
            self._anchor_positions[set_name] = anchors

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
