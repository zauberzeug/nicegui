from typing import Optional

from ..dependencies import register_component
from ..element import Element

register_component('chat_message', __file__, 'chat_message.js')


class ChatMessage(Element):

    def __init__(self,
                 text: str, *,
                 name: Optional[str] = None,
                 label: Optional[str] = None,
                 stamp: Optional[str] = None,
                 avatar: Optional[str] = None,
                 sent: bool = False,
                 ) -> None:
        """Chat Message

        Based on Quasar's `Chat Message <https://quasar.dev/vue-components/chat/>`_ component.

        :param text: the message body
        :param name: the name of the message author
        :param label: renders a label header/section only
        :param stamp: timestamp of the message
        :param avatar: URL to an avatar
        :param sent: render as a sent message (so from current user) (default: False)
        """
        super().__init__('chat_message')
        self._props['text'] = text
        if name is not None:
            self._props['name'] = name
        if label is not None:
            self._props['label'] = label
        if stamp is not None:
            self._props['stamp'] = stamp
        if avatar is not None:
            self._props['avatar'] = avatar
        self._props['sent'] = sent
