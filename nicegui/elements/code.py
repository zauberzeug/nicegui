import asyncio
import time

from .button import Button as button
from .markdown import Markdown as markdown
from .markdown import remove_indentation
from .mixins.content_element import ContentElement
from .timer import Timer as timer


class Code(ContentElement, component='code.js', default_classes='nicegui-code'):

    def __init__(self, content: str = '', *, language: str | None = 'python') -> None:
        """Code

        This element displays a code block with syntax highlighting.

        In secure environments (HTTPS or localhost), a copy button is displayed to copy the code to the clipboard.

        :param content: code to display
        :param language: language of the code (default: "python")
        """
        super().__init__(content=remove_indentation(content))

        with self:
            self.markdown = markdown().classes('overflow-auto h-full') \
                .bind_content_from(self, 'content', lambda content: f'```{language}\n{content}\n```')
            self.copy_button = button(icon='content_copy', on_click=self.show_checkmark) \
                .props('round flat size=sm').classes('absolute right-2 top-2 opacity-20 hover:opacity-80') \
                .on('click', js_handler=f'() => navigator.clipboard.writeText(getElement("{self.id}").content)')

        self._props['content'] = self.content
        self._last_scroll: float = 0.0
        self.markdown.on('scroll', self._handle_scroll)
        with self:
            timer(0.1, self._update_copy_button)

    async def show_checkmark(self) -> None:
        """Show a checkmark icon for 3 seconds."""
        self.copy_button.props('icon=check')
        await asyncio.sleep(3.0)
        self.copy_button.props('icon=content_copy')

    def _handle_scroll(self) -> None:
        self._last_scroll = time.time()

    def _update_copy_button(self) -> None:
        self.copy_button.set_visibility(time.time() > self._last_scroll + 1.0)

    def _handle_content_change(self, content: str) -> None:
        self._props['content'] = content
