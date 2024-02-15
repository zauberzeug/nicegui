import html
from typing import List, Optional, Union

from ..element import Element
from .html import Html


class ChatMessage(Element):

    def __init__(self,
                 text: Union[str, List[str]] = ..., *,  # type: ignore
                 name: Optional[str] = None,
                 label: Optional[str] = None,
                 stamp: Optional[str] = None,
                 avatar: Optional[str] = None,
                 sent: bool = False,
                 text_html: bool = False,
                 ) -> None:
        """Chat Message

        Based on Quasar's [Chat Message ](https://quasar.dev/vue-components/chat/) component.

        - text: the message body (can be a list of strings for multiple message parts)
        - name: the name of the message author
        - label: renders a label header/section only
        - stamp: timestamp of the message
        - avatar: URL to an avatar
        - sent: render as a sent message (so from current user) (default: False)
        - text_html: render text as HTML (default: False)
        """
        super().__init__('q-chat-message')

        if text is ...:
            text = []
        if isinstance(text, str):
            text = [text]
        if not text_html:
            text = [html.escape(part) for part in text]
            text = [part.replace('\n', '<br />') for part in text]

        if name is not None:
            self._props['name'] = name
        if label is not None:
            self._props['label'] = label
        if stamp is not None:
            self._props['stamp'] = stamp
        if avatar is not None:
            self._props['avatar'] = avatar
        self._props['sent'] = sent

        with self:
            for line in text:
                Html(line)
