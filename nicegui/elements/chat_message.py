from __future__ import annotations

import html
from typing import Callable, Literal

from ..defaults import DEFAULT_PROP, resolve_defaults
from .html import Html
from .mixins.label_element import LabelElement


class ChatMessage(LabelElement):

    @resolve_defaults
    def __init__(self,
                 text: str | list[str] | None = None,
                 name: str | None = DEFAULT_PROP | None,
                 label: str | None = DEFAULT_PROP | None,
                 stamp: str | None = DEFAULT_PROP | None,
                 avatar: str | None = DEFAULT_PROP | None,
                 sent: bool = DEFAULT_PROP | False,
                 text_html: bool = False,
                 sanitize: Callable[[str], str] | Literal[False] | None = None,
                 ) -> None:
        """Chat Message

        Based on Quasar's `Chat Message <https://quasar.dev/vue-components/chat/>`_ component.

        Note that since NiceGUI 3.0, you need to specify how to ``sanitize`` the HTML content
        if you activate HTML via ``text_html=True``.
        Especially if you are displaying user input, you should sanitize the content to prevent XSS attacks.
        We recommend ``Sanitizer().sanitize`` which requires the html-sanitizer package to be installed.
        If you are not displaying user input, you can pass ``False`` to disable sanitization.

        :param text: the message body (can be a list of strings for multiple message parts)
        :param name: the name of the message author
        :param label: renders a label header/section only
        :param stamp: timestamp of the message
        :param avatar: URL to an avatar
        :param sent: render as a sent message (so from current user) (default: ``False``)
        :param text_html: render text as HTML (consider using a ``sanitize`` function to prevent XSS attacks) (default: ``False``)
        :param sanitize: a sanitize function to be applied to HTML content or ``False`` to deactivate sanitization (*added in version 3.0.0*)
        """
        super().__init__(tag='q-chat-message', label=label)

        if text is None:
            text = []
        if isinstance(text, str):
            text = [text]
        if not text_html:
            text = [html.escape(part) for part in text]
            text = [part.replace('\n', '<br />') for part in text]
            sanitize = False

        if sanitize is None:
            raise ValueError('You must specify a sanitize function or sanitize=False when using text_html=True')

        self._props.set_optional('name', name)
        self._props.set_optional('stamp', stamp)
        self._props.set_optional('avatar', avatar)
        self._props['sent'] = sent

        with self:
            for line in text:
                Html(line, sanitize=sanitize)
