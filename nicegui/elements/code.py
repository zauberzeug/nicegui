import asyncio
import time
from typing import Optional

from .. import json
from ..element import Element
from .button import Button as button
from .markdown import Markdown as markdown
from .markdown import remove_indentation
from .timer import Timer as timer


class Code(Element):
    """Code block element with syntax highlighting.

    This element displays a code block with syntax highlighting. It provides a copy button to easily copy the code to the clipboard.

    Attributes:
    
        - content (str): The code to display.
        - language (str, optional): The language of the code (default: "python").

    Examples:
        Create a Code element with Python code:

        >>> code = Code('print("Hello, World!")')

        Create a Code element with JavaScript code:

        >>> code = Code('console.log("Hello, World!")', language='javascript')
    """

    def __init__(self, content: str, *, language: Optional[str] = 'python') -> None:
        """Code

        Args:
        
            - content (str): The code to display.
            - language (str, optional): The language of the code (default: "python").
        """
        super().__init__()
        self._classes.append('nicegui-code')

        self.content = remove_indentation(content)

        with self:
            self.markdown = markdown(f'```{language}\n{self.content}\n```').classes('overflow-auto')
            self.copy_button = button(icon='content_copy', on_click=self.show_checkmark) \
                .props('round flat size=sm').classes('absolute right-2 top-2 opacity-20 hover:opacity-80')
            self.copy_button._props['onclick'] = f'navigator.clipboard.writeText({json.dumps(self.content)})'

        self._last_scroll: float = 0.0
        self.markdown.on('scroll', self._handle_scroll)
        timer(0.1, self._update_copy_button)

    async def show_checkmark(self) -> None:
        """Show a checkmark icon for 3 seconds.

        This method changes the icon of the copy button to a checkmark for 3 seconds, indicating that the code has been copied to the clipboard.
        """
        self.copy_button.props('icon=check')
        await asyncio.sleep(3.0)
        self.copy_button.props('icon=content_copy')

    def _handle_scroll(self) -> None:
        """Handle the scroll event.

        This method is called when the code block is scrolled. It updates the timestamp of the last scroll event.
        """
        self._last_scroll = time.time()

    def _update_copy_button(self) -> None:
        """Update the visibility of the copy button.

        This method checks if enough time has passed since the last scroll event and updates the visibility of the copy button accordingly.
        """
        self.copy_button.set_visibility(time.time() > self._last_scroll + 1.0)
