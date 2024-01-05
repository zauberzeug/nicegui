import asyncio
import time
from typing import Optional

from ..element import Element
from ..functions.javascript import run_javascript
from .button import Button as button
from .markdown import Markdown as markdown
from .markdown import remove_indentation
from .timer import Timer as timer


class Code(Element):

    def __init__(self, content: str, *, language: Optional[str] = 'python') -> None:
        """Code

        This element displays a code block with syntax highlighting.

        :param content: code to display
        :param language: language of the code (default: "python")
        """
        super().__init__()
        self._classes.append('nicegui-code')

        self.content = remove_indentation(content)

        with self:
            self.markdown = markdown(f'```{language}\n{self.content}\n```').classes('overflow-auto')
            self.copy_button = button(icon='content_copy', on_click=self.copy_to_clipboard) \
                .props('round flat size=sm').classes('absolute right-2 top-2 opacity-20 hover:opacity-80')

        self._last_scroll: float = 0.0
        self.markdown.on('scroll', self._handle_scroll)
        timer(0.1, self._update_copy_button)

    async def copy_to_clipboard(self) -> None:
        """Copy the code to the clipboard."""
        run_javascript('navigator.clipboard.writeText(`' + self.content + '`)')
        self.copy_button.props('icon=check')
        await asyncio.sleep(3.0)
        self.copy_button.props('icon=content_copy')

    def _handle_scroll(self) -> None:
        self._last_scroll = time.time()

    def _update_copy_button(self) -> None:
        self.copy_button.set_visibility(time.time() > self._last_scroll + 1.0)
