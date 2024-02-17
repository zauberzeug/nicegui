import os
from functools import lru_cache

from docutils.core import publish_parts
from pygments.formatters import HtmlFormatter  # pylint: disable=no-name-in-module

from .mixins.content_element import ContentElement


class ReStructuredText(ContentElement, component='rst.js'):

    def __init__(self, content: str = '') -> None:
        """ReStructuredText

        Renders ReStructuredText onto the page.

        :param content: the ReStructuredText content to be displayed
        """
        super().__init__(content=content)
        self._classes.append('nicegui-markdown')
        self._props['codehilite_css'] = (
            HtmlFormatter(nobackground=True).get_style_defs('.codehilite') +
            HtmlFormatter(nobackground=True, style='github-dark').get_style_defs('.body--dark .codehilite')
        )

    def _handle_content_change(self, content: str) -> None:
        html = prepare_content(content)
        if self._props.get('innerHTML') != html:
            self._props['innerHTML'] = html
            self.run_method('update', html)


@lru_cache(maxsize=int(os.environ.get('RST_CONTENT_CACHE_SIZE', '1000')))
def prepare_content(content: str) -> str:
    """Render ReStructuredText content to HTML."""
    html = publish_parts(
        remove_indentation(content),
        writer_name='html5'
    )

    # print(html)

    # for key in html:
    #     print(key)
    return html["html_body"]  # if not body_only else html["html_body"]


def remove_indentation(text: str) -> str:
    """Remove indentation from a multi-line string based on the indentation of the first non-empty line."""
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ''
    indentation = len(lines[0]) - len(lines[0].lstrip())
    return '\n'.join(line[indentation:] for line in lines)
