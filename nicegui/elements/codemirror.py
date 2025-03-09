from pathlib import Path
from typing import Callable, List, Literal, Optional, get_args

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
        super().__init__(value=value, on_value_change=on_change)
        self.add_resource(Path(__file__).parent / 'lib' / 'codemirror')

        self._props['language'] = language
        self._props['theme'] = theme
        self._props['indent'] = indent
        self._props['lineWrapping'] = line_wrapping
        self._props['highlightWhitespace'] = highlight_whitespace

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
        changeset = _ChangeSet(sections=e.args['sections'], inserted=e.args['inserted'])
        new_value = changeset.apply(self.value)
        return new_value


# Below is a Python implementation of relevant parts of https://github.com/codemirror/state/blob/main/src/change.ts
# to apply a ChangeSet to a text document.


class _ChangeSet:
    """A change set represents a group of modifications to a document."""

    def __init__(self, sections: List[int], inserted: List[List[str]]) -> None:
        # From https://github.com/codemirror/state/blob/main/src/change.ts#L21:
        # Sections are encoded as pairs of integers. The first is the
        # length in the current document, and the second is -1 for
        # unaffected sections, and the length of the replacement content
        # otherwise. So an insertion would be (0, n>0), a deletion (n>0,
        # 0), and a replacement two positive numbers.
        self.sections: List[int] = sections
        self.inserted: List[str] = ['\n'.join(ins) for ins in inserted]

    def length(self) -> int:
        """Calculate the length of the document before the change."""
        return sum(self.sections[::2])

    def apply(self, doc: str) -> str:
        """Apply the changes to a document, returning the modified document."""
        if self.length() != len(doc):
            raise ValueError('Cannot apply change set to a document with the wrong length')
        return _iter_changes(self, doc, _replacement_func, individual=False)

    def __str__(self) -> str:
        return f'ChangeSet(sections={self.sections}, inserted={self.inserted})'


def _iter_changes(
    changeset: _ChangeSet, doc: str, func: Callable[[str, int, int, int, int, str], str], individual: bool
) -> str:
    inserted = changeset.inserted
    posA, posB, i = 0, 0, 0

    while i < len(changeset.sections):
        len_ = changeset.sections[i]
        i += 1
        ins = changeset.sections[i]
        i += 1

        if ins < 0:
            posA += len_
            posB += len_
        else:
            endA, endB = posA, posB
            text = ''
            while True:
                endA += len_
                endB += ins
                if ins and inserted:
                    text = text + inserted[(i - 2) // 2]
                if individual or i == len(changeset.sections) or changeset.sections[i + 1] < 0:
                    break
                len_ = changeset.sections[i]
                i += 1
                ins = changeset.sections[i]
                i += 1
            doc = func(doc, posA, endA, posB, endB, text)
            posA, posB = endA, endB

    return doc


def _replace_range(doc: str, from_: int, to: int, new: str) -> str:
    return doc[:from_] + new + doc[to:]


def _replacement_func(doc: str, from_a: int, to_a: int, from_b: int, _to_b: int, text: str) -> str:
    return _replace_range(doc, from_b, from_b + (to_a - from_a), text)
