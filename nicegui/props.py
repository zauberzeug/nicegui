import ast
import re
import weakref
from collections.abc import Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from . import helpers
from .observables import ObservableDict

if TYPE_CHECKING:
    from .element import Element

PROPS_PATTERN = re.compile(r'''
# Match a key or key-value pair optionally followed by whitespace or end of string
# The value can be unquoted, or enclosed in quotes, or square or curly brackets
(?P<key>[:\w\-]+)           # Capture group 1: Key
(                           # Optional non-capturing group for value
    =                       # An equals sign
    (                       # followed by one of ...
        (?P<double>         # a value enclosed in double quotes
            "                   # Match double quote
            [^"\\]*             # Match any character except quotes or backslashes zero or more times
            (\\.[^"\\]*)*       # Match any escaped character followed by any character except quotes or backslashes zero or more times
            "                   # Match the closing quote
        )
        |                   # or
        (?P<single>         # a value enclosed in single quotes
            '                   # Match a single quote
            [^'\\]*             # Match any character except quotes or backslashes zero or more times
            (\\.[^'\\]*)*       # Match any escaped character followed by any character except quotes or backslashes zero or more times
            '                   # Match the closing quote
        )
        |                   # or
        (?P<square>         # a value enclosed in square brackets
            \[                  # Match the opening [
            [^\]\\]*            # Match any character except a ] or backslashes zero or more times
            (\\.[^\]\\]*)*      # Match any escaped character followed by any character except ] or backslashes zero or more times
            \]                  # Match the closing ]
        )
        |                   # or
        (?P<curly>          # a value enclosed in curly braces
            \{                  # Match the opening {
            [^\}\\]*            # Match any character except } or backslashes zero or more times
            (\\.[^\}\\]*)*      # Match any escaped character followed by any character except ] or backslashes zero or more times
            \}                  # Match the closing }
        )
        |                   # or, as a final alternative ....
        (?P<unquoted>[\w\-.,%:\/=?&;+#@~$]+)  # a value without quotes
    )
)?                          # End of optional non-capturing group for value
($|\s)                      # Match end of string or whitespace
''', re.VERBOSE)

T = TypeVar('T', bound='Element')


class Props(ObservableDict, Generic[T]):

    def __init__(self, *args, element: T, **kwargs) -> None:
        super().__init__(*args, on_change=self._update, **kwargs)
        self._element = weakref.ref(element)
        self._warnings: dict[str, str] = {}
        self._renames: dict[str, str] = {}
        self._suspend_count = 0

    def set_optional(self, key: str, value: Any) -> None:
        """Set a prop value or remove it if None is provided."""
        if value is None:
            self.pop(key, None)
        else:
            self[key] = value

    def set_bool(self, key: str, value: Any) -> None:
        """Set a boolean prop value or remove it if falsy value is provided."""
        if value:
            self[key] = value
        else:
            self.pop(key, None)

    @contextmanager
    def suspend_updates(self) -> Iterator[None]:
        """Suspend updates."""
        self._suspend_count += 1
        try:
            yield
        finally:
            self._suspend_count -= 1

    @property
    def element(self) -> T:
        """The element this props object belongs to."""
        element = self._element()
        if element is None:
            raise RuntimeError('The element this props object belongs to has been deleted.')
        return element

    def _update(self) -> None:
        if self._suspend_count > 0:
            return

        for name, message in self._warnings.items():
            self._check_warning(name, message)

        for name, rename in self._renames.items():
            self._check_rename(name, rename)

        element = self._element()
        if element is not None:
            element.update()

    def add_warning(self, prop: str, message: str) -> None:
        """Add a warning message for a prop."""
        self._warnings[prop] = message
        self._check_warning(prop, message)

    def add_rename(self, prop: str, replacement: str) -> None:
        """Add a rename warning for a prop."""
        self._renames[prop] = replacement
        self._check_rename(prop, replacement)

    def _check_warning(self, name: str, message: str) -> None:
        if name in self:
            with self.suspend_updates():
                del self[name]
            helpers.warn_once(message)

    def _check_rename(self, name: str, rename: str) -> None:
        if name in self:
            with self.suspend_updates():
                self[rename] = self[name]
            helpers.warn_once(f'The prop "{name}" is deprecated. Use "{rename}" instead.')

    def __call__(self,
                 add: str | None = None, *,
                 remove: str | None = None) -> T:
        """Add or remove props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
        """
        element = self.element
        for key in self.parse(remove):
            if key in self:
                del self[key]
        for key, value in self.parse(add).items():
            if self.get(key) != value:
                self[key] = value
        return element

    @staticmethod
    def parse(text: str | None) -> dict[str, Any]:
        """Parse a string of props into a dictionary."""
        if not text:
            return {}
        props: dict[str, Any] = {}
        for match in PROPS_PATTERN.finditer(text):
            match_groups = match.groupdict()
            key = match_groups['key']

            for group in ['single', 'double', 'square', 'curly']:
                if match_groups[group] is not None:
                    props[key] = ast.literal_eval(match_groups[group])
                    break
            else:
                if match_groups['unquoted'] is not None:
                    props[key] = match_groups['unquoted']
                else:
                    props[key] = True

        return props
