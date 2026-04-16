from itertools import accumulate, chain, repeat
from typing import Literal, get_args

from ...defaults import DEFAULT_PROP, resolve_defaults
from ...elements.mixins.disableable_element import DisableableElement
from ...elements.mixins.value_element import ValueElement
from ...events import GenericEventArguments, Handler, ValueChangeEventArguments

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
        on_cursor_line: Handler[GenericEventArguments] | None = None,
        on_save: Handler[GenericEventArguments] | None = None,
        language: SUPPORTED_LANGUAGES | None = DEFAULT_PROP | None,
        theme: SUPPORTED_THEMES = DEFAULT_PROP | 'basicLight',
        indent: str = DEFAULT_PROP | ' ' * 4,
        line_wrapping: bool = DEFAULT_PROP | False,
        highlight_whitespace: bool = DEFAULT_PROP | False,
        custom_completions: list[dict] | None = None,
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
        :param on_cursor_line: callback when the cursor moves to a different line; receives ``e.args["line"]`` (1-indexed)
        :param on_save: callback fired when the user presses Ctrl/Cmd+S inside the editor.
            When set, the binding is installed and the browser's default save behavior is suppressed.
        :param language: initial language of the editor (case-insensitive, default: `None`)
        :param theme: initial theme of the editor (default: "basicLight")
        :param indent: string to use for indentation (any string consisting entirely of the same whitespace character, default: "    ")
        :param line_wrapping: whether to wrap lines (default: `False`)
        :param highlight_whitespace: whether to highlight whitespace (default: `False`)
        :param custom_completions: list of custom completion items (default: `None`).
            Each item is a dict with keys: ``label``, ``detail`` (optional), ``info`` (optional), ``apply`` (optional), ``type`` (optional).
        """
        super().__init__(value=value, on_value_change=self._update_codepoints)
        self._codepoints = b''
        self._update_codepoints()
        if on_change is not None:
            super().on_value_change(on_change)
        if on_cursor_line is not None:
            self.on('cursor-line', on_cursor_line)
        if on_save is not None:
            self.on('save', on_save)

        self._anchor_positions: dict[str, dict[str, int]] = {}
        self.on('anchor-positions', self._update_anchor_mirror)

        self._props['language'] = language
        self._props['theme'] = theme
        self._props['indent'] = indent
        self._props['line-wrapping'] = line_wrapping
        self._props['highlight-whitespace'] = highlight_whitespace
        self._props['custom-completions'] = custom_completions or []
        self._props['decorations'] = {}
        self._props['save-shortcut-enabled'] = on_save is not None
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

    @property
    def custom_completions(self) -> list[dict]:
        """The current custom completions for the editor."""
        return self._props.get('custom-completions', [])

    @custom_completions.setter
    def custom_completions(self, completions: list[dict] | None) -> None:
        self._props['custom-completions'] = completions or []

    def set_completions(self, completions: list[dict] | None) -> None:
        """Sets the custom completions for the editor.

        Each completion item is a dict with keys:
            - ``label``: the text shown in the completion dropdown (required)
            - ``detail``: additional detail shown after the label (optional)
            - ``info``: documentation or description (optional)
            - ``apply``: the text to insert when selected (optional; defaults to the label)
            - ``type``: the type of completion for styling (optional; e.g. ``'function'``, ``'variable'``, ``'class'``)
        """
        self._props['custom-completions'] = completions or []

    def set_decorations(self, decorations: list[dict], set_name: str = 'default') -> None:
        """Set decorations for a named decoration set.

        Decorations allow styling of text ranges or entire lines using CodeMirror's state-managed
        decoration system (survives re-renders unlike DOM manipulation).

        Each decoration dict should have:
            - ``kind``: ``'mark'`` or ``'line'``

        For mark decorations (inline text styling):
            - ``from``: start position (0-indexed character offset)
            - ``to``: end position (0-indexed, exclusive)
            - ``class``: CSS class to apply (optional)
            - ``attributes``: dict of HTML attributes (optional)
            - ``inclusiveStart``: include start in decoration (optional)
            - ``inclusiveEnd``: include end in decoration (optional)

        For line decorations (full-line styling):
            - ``line``: line number (1-indexed)
            - ``class``: CSS class to apply (optional)
            - ``attributes``: dict of HTML attributes (optional)

        Built-in CSS classes available:
            - ``cm-diff-added``: green background for added text
            - ``cm-diff-deleted``: red background with strikethrough
            - ``cm-diff-line-added``: light green line background
            - ``cm-diff-line-deleted``: light red line background
            - ``cm-highlighted``: yellow highlight

        :param decorations: list of decoration specification dicts
        :param set_name: named set for independent management (e.g. ``'diff'``, ``'errors'``)
        """
        current = dict(self._props.get('decorations', {}))
        current[set_name] = decorations
        self._props['decorations'] = current

    def clear_decorations(self, set_name: str | None = None) -> None:
        """Clear decorations.

        :param set_name: clear only this named set, or all decorations if ``None``
        """
        if set_name is None:
            self._props['decorations'] = {}
        else:
            current = dict(self._props.get('decorations', {}))
            current.pop(set_name, None)
            self._props['decorations'] = current

    def highlight_lines(self,
                        line_numbers: list[int],
                        css_class: str = 'cm-highlighted',
                        duration_ms: int = 1500,
                        ) -> None:
        """Highlight specific lines with a CSS class and optional auto-removal.

        :param line_numbers: list of 1-indexed line numbers to highlight
        :param css_class: CSS class to apply to the lines (default: ``'cm-highlighted'``)
        :param duration_ms: time in ms before removing the highlight; 0 for permanent (default: 1500)
        """
        line_indices = [n - 1 for n in line_numbers if n > 0]
        if line_indices:
            self.run_method('highlightLines', line_indices, css_class, duration_ms)

    def set_line_anchors(self, anchors: list[dict], set_name: str = 'default') -> None:
        """Set tracked line anchors for a named set.

        Anchors are document positions identified by string IDs that automatically remap through edits.
        When positions change, the ``anchor-positions`` event fires with updated line numbers.

        This is a batch-replace operation: all anchors in the named set are replaced. Other named
        sets are unaffected.

        :param anchors: list of dicts with ``'id'`` (str) and ``'line'`` (1-indexed int)
        :param set_name: named set for independent management (e.g. ``'breakpoints'``, ``'targets'``)
        """
        self.run_method('setLineAnchors', anchors, set_name)

    def clear_line_anchors(self, set_name: str | None = None) -> None:
        """Clear tracked line anchors.

        :param set_name: clear only this named set, or all sets if ``None``
        """
        self.run_method('clearLineAnchors', set_name)

    def set_diagnostics(self, diagnostics: list[dict]) -> None:
        """Set linting diagnostics with inline messages and gutter icons.

        Uses CodeMirror's built-in lint system. Diagnostics appear as underlines in the editor with
        gutter icons indicating severity.

        :param diagnostics: list of dicts with ``line`` (1-indexed line number), ``severity``
            (``'error'`` | ``'warning'`` | ``'info'`` | ``'hint'``), ``message`` (the diagnostic message),
            and optional ``source`` (source identifier).
        """
        self.run_method('setDiagnosticsFromPython', diagnostics)

    def set_line_tooltips(self, tooltips: dict[int, dict], set_name: str = 'default') -> None:
        """Set hover tooltip metadata for lines.

        When the user hovers a line, its metadata is rendered as a tooltip showing key-value pairs.
        Multiple named sets are merged for the same line.

        Keys starting with underscore are control keys:
            - ``_html``: raw HTML string (overrides key-value rendering; sanitized client-side via DOMPurify)

        :param tooltips: dict mapping 1-indexed line numbers to metadata dicts
        :param set_name: named set for independent management
        """
        str_tooltips = {str(k): v for k, v in tooltips.items()}
        self.run_method('setLineTooltips', str_tooltips, set_name)

    def clear_line_tooltips(self, set_name: str | None = None) -> None:
        """Clear line tooltip metadata.

        :param set_name: clear only this named set, or all sets if ``None``
        """
        self.run_method('clearLineTooltips', set_name)

    def reveal_line(self, line_number: int) -> None:
        """Scroll the editor so the given 1-indexed line is visible.

        :param line_number: 1-indexed line number to scroll into view
        """
        self.run_method('revealLine', line_number)

    @property
    def line_anchor_positions(self) -> dict[str, dict[str, int]]:
        """Current anchor positions mirrored from the browser.

        Updated automatically when document edits remap anchor positions.

        :return: dict of ``set_name`` → ``{anchor_id: 1-indexed line_number}``
        """
        return dict(self._anchor_positions)

    def _update_anchor_mirror(self, e: GenericEventArguments) -> None:
        """Handle anchor-positions events from the JS side."""
        args = e.args if isinstance(e.args, dict) else {}
        set_name = args.get('set_name', 'default')
        anchors = args.get('anchors', {})
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
