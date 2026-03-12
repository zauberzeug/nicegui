from collections.abc import Callable

from .mixins.content_element import ContentElement


class Html(ContentElement, component='html.js'):

    def __init__(self, content: str = '', *, sanitize: Callable[[str], str] | bool = True, tag: str = 'div') -> None:
        """HTML Element

        Renders arbitrary HTML onto the page, wrapped in the specified tag.
        `Tailwind <https://tailwindcss.com/>`_ can be used for styling.
        You can also use `ui.add_head_html` to add html code into the head of the document and `ui.add_body_html`
        to add it into the body.

        :param content: the HTML code to be displayed
        :param sanitize: sanitization mode:
            ``True`` (default) uses client-side sanitization via setHTML or DOMPurify,
            ``False`` disables sanitization (use only with trusted content),
            or pass a callable to apply server-side sanitization
        :param tag: the HTML tag to wrap the content in (default: "div")
        """
        self._sanitize = sanitize
        super().__init__(content=content)
        self._props['tag'] = tag
        self._props['sanitize'] = sanitize is True

    def _handle_content_change(self, content: str) -> None:
        if callable(self._sanitize):
            content = self._sanitize(content)
        super()._handle_content_change(content)
