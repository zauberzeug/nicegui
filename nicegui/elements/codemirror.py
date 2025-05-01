import bisect
from itertools import accumulate, zip_longest
from pathlib import Path
from typing import List, Literal, Optional, Tuple, cast, get_args

from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement
from nicegui.events import GenericEventArguments, Handler, ValueChangeEventArguments

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


class CodeMirror(ValueElement, DisableableElement, component='codemirror.js', default_classes='nicegui-codemirror'):
    VALUE_PROP = 'value'
    LOOPBACK = None

    def __init__(
        self,
        value: str = '',
        *,
        on_change: Optional[Handler[ValueChangeEventArguments]] = None,
        language: Optional[SUPPORTED_LANGUAGES] = None,
        theme: SUPPORTED_THEMES = 'basicLight',
        indent: str = ' ' * 4,
        line_wrapping: bool = False,
        highlight_whitespace: bool = False,
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
        super().__init__(value=value, on_value_change=self._update_cumulative)
        self._cumulative_corresponds_to_string = value
        self._cumulative_js_length: List[int] = []
        self._update_cumulative(forced=True)
        if on_change is not None:
            super().on_value_change(on_change)
        self.add_resource(Path(__file__).parent / 'lib' / 'codemirror')

        self._props['language'] = language
        self._props['theme'] = theme
        self._props['indent'] = indent
        self._props['lineWrapping'] = line_wrapping
        self._props['highlightWhitespace'] = highlight_whitespace
        self._update_method = 'setEditorValueFromProps'

    @property
    def theme(self) -> str:
        """The current theme of the editor."""
        return self._props['theme']

    @theme.setter
    def theme(self, theme: str) -> None:
        self._props['theme'] = theme
        self.update()

    def set_theme(self, theme: str) -> None:
        """Sets the theme of the editor."""
        self._props['theme'] = theme
        self.update()

    @property
    def supported_themes(self) -> List[str]:
        """List of supported themes."""
        return list(get_args(SUPPORTED_THEMES))

    @property
    def language(self) -> str:
        """The current language of the editor."""
        return self._props['language']

    @language.setter
    def language(self, language: Optional[str]) -> None:
        self._props['language'] = language
        self.update()

    def set_language(self, language: Optional[str]) -> None:
        """Sets the language of the editor (case-insensitive)."""
        self._props['language'] = language
        self.update()

    @property
    def supported_languages(self) -> List[str]:
        """List of supported languages."""
        return list(get_args(SUPPORTED_LANGUAGES))

    def _event_args_to_value(self, e: GenericEventArguments) -> str:
        """The event contains a change set which is applied to the current value."""
        return self._apply_change_set(e.args['sections'], e.args['inserted'])

    def _update_cumulative(self, *, forced=False) -> None:
        if forced or self._cumulative_corresponds_to_string != self.value:
            self._cumulative_js_length = get_cumulative_js_length(self.value)
            self._cumulative_corresponds_to_string = self.value

    def _apply_change_set(self, sections: List[int], inserted: List[List[str]]) -> str:
        # based on https://github.com/codemirror/state/blob/main/src/change.ts
        doc = self.value or ''

        def _find_python_index(js_index: int) -> int:
            return find_python_index(js_index, self._cumulative_js_length)
        assert sum(sections[::2]) == get_total_js_length(
            self._cumulative_js_length), 'Cannot apply change set to document due to length mismatch'
        pos = 0
        joined_inserts = ('\n'.join(ins) for ins in inserted)
        for section in zip_longest(sections[::2], sections[1::2], joined_inserts, fillvalue=''):
            old_len, new_len, ins = cast(Tuple[int, int, str], section)
            if new_len >= 0:
                first_index = _find_python_index(pos)
                second_index = _find_python_index(pos + old_len)
                doc = doc[:first_index] + ins + doc[second_index:]

                just_before_original_end_part = self._cumulative_js_length[second_index - 1] if second_index > 0 else 0
                original_end_part = self._cumulative_js_length[second_index:]

                self._cumulative_js_length = self._cumulative_js_length[:first_index]
                self._cumulative_js_length += [x + get_total_js_length(self._cumulative_js_length)
                                               for x in get_cumulative_js_length(ins)]
                self._cumulative_js_length += [(x - just_before_original_end_part) +
                                               get_total_js_length(self._cumulative_js_length) for x in original_end_part]
            pos += old_len
            self._cumulative_corresponds_to_string = doc
        return doc


def get_cumulative_js_length(doc: str) -> List[int]:
    """Returns a list, where for each index i, the value is the length of the string from 0 to i in UTF-16 (imagine js_len(doc[:i])"""
    return list(accumulate(len(c.encode('utf-16be'))//2 for c in doc)) if doc else []


def get_total_js_length(cumulative_js_length: List[int]) -> int:
    """Returns the length of the string in UTF-16 (imagine js_len(doc))"""
    return cumulative_js_length[-1] if cumulative_js_length else 0


def find_python_index(js_index: int, cumulative_js_length: List[int]) -> int:
    """Given a js_index, returns the position in cumulative_js_length (1-based)

    Note that 1-based indexing enables doc[:find_python_index(pos)] to replace doc[:pos]
    """
    if js_index == 0 or not cumulative_js_length:
        return 0
    lo1 = len(cumulative_js_length) - (get_total_js_length(cumulative_js_length) - js_index)
    hi1 = js_index
    lo2 = (js_index + 1) // 2
    hi2 = len(cumulative_js_length) - (get_total_js_length(cumulative_js_length) - js_index + 1) // 2
    lo = max(lo1, lo2, 0)
    hi = min(hi1, hi2, len(cumulative_js_length))
    return bisect.bisect_right(cumulative_js_length, js_index, lo, hi)
