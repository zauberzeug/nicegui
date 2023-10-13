import asyncio
from typing import Optional

from ..element import Element
from ..elements.button import Button as button
from ..elements.markdown import Markdown as markdown
from ..elements.markdown import remove_indentation
from ..functions.javascript import run_javascript


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

    async def copy_to_clipboard(self) -> None:
        """Copy the code to the clipboard."""
        run_javascript('navigator.clipboard.writeText(`' + self.content + '`)')
        self.copy_button.props('icon=check')
        await asyncio.sleep(3.0)
        self.copy_button.props('icon=content_copy')
