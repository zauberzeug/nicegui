from dataclasses import dataclass
from itertools import accumulate, chain, repeat
from typing import Literal, get_args

from typing_extensions import Self

from ...defaults import DEFAULT_PROP, resolve_defaults
from ...elements.mixins.disableable_element import DisableableElement
from ...elements.mixins.value_element import ValueElement
from ...events import (
    CodeMirrorKeybindingEventArguments,
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


@dataclass(frozen=True, slots=True, kw_only=True)
class CodeMirrorKeybindingSpec:
    """Wraps a CodeMirror keybinding with per-binding configuration overrides.

    Construct via :meth:`CodeMirror.binding` rather than instantiating directly.
    """
    callback: Handler[CodeMirrorKeybindingEventArguments]
    prevent_default: bool = True
    mac: str | None = None
    linux: str | None = None
    win: str | None = None


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
        keybindings: dict[str, Handler[CodeMirrorKeybindingEventArguments] | CodeMirrorKeybindingSpec] | None = None,
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

        Keybindings map keystrokes to Python callbacks via CodeMirror's keymap.
        Pass a bare callable for the default config (prevents the browser default, no per-OS override).
        Wrap with :meth:`binding` for per-binding overrides such as ``prevent_default=False`` or platform-specific shortcuts (``mac=``, ``linux=``, ``win=``).
        Use :meth:`on_keybinding` to add bindings at runtime and :meth:`remove_keybinding` to drop them.

        :param value: initial value of the editor (default: "")
        :param on_change: callback to be executed when the value changes (default: `None`)
        :param keybindings: mapping of CodeMirror key strings (e.g. ``'Mod-s'``, ``'F5'``) to handlers, optionally wrapped with :meth:`binding` (default: `None`)
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
        self._props['keybindings'] = []
        self._update_method = 'setEditorValueFromProps'

        self._props.add_rename('highlightWhitespace', 'highlight-whitespace')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('lineWrapping', 'line-wrapping')  # DEPRECATED: remove in NiceGUI 4.0

        self._keybinding_specs: dict[str, CodeMirrorKeybindingSpec] = {}
        self.on('keybinding', self._dispatch_keybinding)
        for key, handler in (keybindings or {}).items():
            self.on_keybinding(key, handler)

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

    @staticmethod
    def binding(
        callback: Handler[CodeMirrorKeybindingEventArguments],
        *,
        prevent_default: bool = True,
        mac: str | None = None,
        linux: str | None = None,
        win: str | None = None,
    ) -> CodeMirrorKeybindingSpec:
        """Wrap a keybinding callback with per-binding configuration overrides.

        Use this when you need to opt out of preventing the browser default action
        (e.g. ``Mod-c`` that notifies Python while still letting the browser copy normally),
        or to provide per-platform shortcut overrides::

            ui.codemirror(keybindings={
                'Mod-c': ui.codemirror.binding(log_copy, prevent_default=False),
                'Alt-Down': ui.codemirror.binding(move_down, mac='Cmd-Down'),
            })

        Note:
            The ``key`` field on the event passed to your callback is always the
            dict key (e.g. ``'Alt-Down'``) — never the resolved per-OS variant.

        :param callback: the handler callable
        :param prevent_default: whether to mark the binding as handled (default: `True`).
            When ``True``, the browser default action is suppressed and CodeMirror stops
            keymap traversal at this binding. When ``False``, the event continues to
            lower-precedence CodeMirror bindings (e.g. ``basicSetup``'s ``Mod-z`` undo)
            *and* the browser's native handler. Use ``False`` when you want a Python
            notification without overriding either layer.
        :param mac: alternate key string used only on macOS, overriding ``key`` (default: `None`)
        :param linux: alternate key string used only on Linux, overriding ``key`` (default: `None`)
        :param win: alternate key string used only on Windows, overriding ``key`` (default: `None`)
        """
        return CodeMirrorKeybindingSpec(
            callback=callback,
            prevent_default=prevent_default,
            mac=mac,
            linux=linux,
            win=win,
        )

    def on_keybinding(
        self,
        key: str,
        handler: Handler[CodeMirrorKeybindingEventArguments] | CodeMirrorKeybindingSpec,
    ) -> Self:
        """Bind a keystroke to a callback.

        The ``key`` follows CodeMirror 6's keybinding syntax (e.g. ``'Mod-s'``, ``'F5'``, ``'Mod-Shift-d'``).
        ``Mod`` resolves to ``Cmd`` on macOS and ``Ctrl`` elsewhere.

        Pass a bare callable for the default config (prevents the browser default, no per-OS override),
        or wrap with :meth:`binding` for per-binding overrides.

        Re-registering the same key replaces the prior handler.
        """
        spec = handler if isinstance(handler, CodeMirrorKeybindingSpec) \
            else CodeMirrorKeybindingSpec(callback=handler)
        self._keybinding_specs[key] = spec
        self._sync_keybindings_prop()
        return self

    def remove_keybinding(self, key: str) -> Self:
        """Remove a previously bound keybinding.

        No-op if the key is not currently bound.
        """
        if self._keybinding_specs.pop(key, None) is not None:
            self._sync_keybindings_prop()
        return self

    def _sync_keybindings_prop(self) -> None:
        self._props['keybindings'] = [
            {
                'key': key,
                'preventDefault': spec.prevent_default,
                **({'mac': spec.mac} if spec.mac is not None else {}),
                **({'linux': spec.linux} if spec.linux is not None else {}),
                **({'win': spec.win} if spec.win is not None else {}),
            }
            for key, spec in self._keybinding_specs.items()
        ]

    def _dispatch_keybinding(self, e: GenericEventArguments) -> None:
        key = e.args['key']
        spec = self._keybinding_specs.get(key)
        if spec is None:
            return
        handle_event(spec.callback, CodeMirrorKeybindingEventArguments(
            sender=self,
            client=self.client,
            key=key,
        ))

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
