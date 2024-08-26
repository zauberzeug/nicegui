import ast
import re
from typing import TYPE_CHECKING, Any, Dict, Generic, Optional, TypeVar

from . import helpers

if TYPE_CHECKING:
    from .element import Element

PROPS_PATTERN = re.compile(r'''
# Match a key-value pair optionally followed by whitespace or end of string
([:\w\-]+)          # Capture group 1: Key
(?:                 # Optional non-capturing group for value
    =               # Match the equal sign
    (?:             # Non-capturing group for value options
        (           # Capture group 2: Value enclosed in double quotes
            "       # Match  double quote
            [^"\\]* # Match any character except quotes or backslashes zero or more times
            (?:\\.[^"\\]*)*  # Match any escaped character followed by any character except quotes or backslashes zero or more times
            "       # Match the closing quote
        )
        |
        (           # Capture group 3: Value enclosed in single quotes
            '       # Match a single quote
            [^'\\]* # Match any character except quotes or backslashes zero or more times
            (?:\\.[^'\\]*)*  # Match any escaped character followed by any character except quotes or backslashes zero or more times
            '       # Match the closing quote
        )
        |           # Or
        ([\w\-.,%:\/=]+)  # Capture group 4: Value without quotes
    )
)?                  # End of optional non-capturing group for value
(?:$|\s)            # Match end of string or whitespace
''', re.VERBOSE)

T = TypeVar('T', bound='Element')


class Props(dict, Generic[T]):

    def __init__(self, *args, element: T, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.element = element
        self._warnings: Dict[str, str] = {}

    def add_warning(self, prop: str, message: str) -> None:
        """Add a warning message for a prop."""
        self._warnings[prop] = message

    def __call__(self,
                 add: Optional[str] = None, *,
                 remove: Optional[str] = None) -> T:
        """Add or remove props.

        This allows modifying the look of the element or its layout using `Quasar <https://quasar.dev/>`_ props.
        Since props are simply applied as HTML attributes, they can be used with any HTML element.

        Boolean properties are assumed ``True`` if no value is specified.

        :param add: whitespace-delimited list of either boolean values or key=value pair to add
        :param remove: whitespace-delimited list of property keys to remove
        """
        needs_update = False
        for key in self.parse(remove):
            if key in self:
                needs_update = True
                del self[key]
        for key, value in self.parse(add).items():
            if self.get(key) != value:
                needs_update = True
                self[key] = value
        if needs_update:
            self.element.update()
        for name, message in self._warnings.items():
            if name in self:
                del self[name]
                helpers.warn_once(message)
        return self.element

    @staticmethod
    def parse(text: Optional[str]) -> Dict[str, Any]:
        """Parse a string of props into a dictionary."""
        dictionary = {}
        for match in PROPS_PATTERN.finditer(text or ''):
            key = match.group(1)
            value = match.group(2) or match.group(3) or match.group(4)
            if value is None:
                dictionary[key] = True
            else:
                if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                    value = ast.literal_eval(value)
                dictionary[key] = value
        return dictionary
