from typing import Optional

from ..dependencies import register_component
from .mixins.disableable_element import DisableableElement

register_component('chat_message', __file__, 'chat_message.js')


class ChatMessage(DisableableElement):

    def __init__(self, *,
                 sent: Optional[bool] = False,
                 label: Optional[str] = '',
                 name: Optional[str] = '',
                 text: Optional[str] = '',
                 stamp: Optional[str] = None,
                 avatar: Optional[str] = None,
                 ) -> None:
        """Chat Message

        Based on Quasar's `Chat Message <https://quasar.dev/vue-components/chat/`_ component.

        :param sent: Render as a sent message (so from current user) (default: False)
        :param label: Adding a label adds a tiny headline between messages
        :param name: The name of the message author
        :param text: The message body
        :param stamp: The time stamp of the message. (default: `None`))
        :param avatar: URL to avatar. (default: `None`))
        """
        super().__init__(tag='chat_message')
        self._props['sent'] = sent
        self._props['text'] = text
        self._props['stamp'] = stamp
        self._props['name'] = name
        if avatar:
            self._props['avatar'] = avatar
        if stamp:
            self._props['stamp'] = stamp
