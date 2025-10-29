from __future__ import annotations

from typing import Callable, Literal

from .mixins.content_element import ContentElement


class Html(ContentElement):

    def __init__(self, content: str = '', *, sanitize: Callable[[str], str] | Literal[False], tag: str = 'div') -> None:
        """HTML Element

        Renders arbitrary HTML onto the page, wrapped in the specified tag.
        `Tailwind <https://tailwindcss.com/>`_ can be used for styling.
        You can also use `ui.add_head_html` to add html code into the head of the document and `ui.add_body_html`
        to add it into the body.

        Note that since NiceGUI 3.0, you need to specify how to ``sanitize`` the HTML content.
        Especially if you are displaying user input, you should sanitize the content to prevent XSS attacks.
        We recommend ``Sanitizer().sanitize`` which requires the html-sanitizer package to be installed.
        If you are not displaying user input, you can pass ``False`` to disable sanitization.

        :param content: the HTML code to be displayed
        :param sanitize: a sanitize function to be applied to the content or ``False`` to deactivate sanitization (*added in version 3.0.0*)
        :param tag: the HTML tag to wrap the content in (default: "div")
        """
        self._sanitize = sanitize
        super().__init__(tag=tag, content=content)

    def _handle_content_change(self, content: str) -> None:
        if self._sanitize:
            content = self._sanitize(content)
        super()._handle_content_change(content)
