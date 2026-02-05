import html
from collections.abc import Callable

from .. import helpers
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
                 sanitize: Callable[[str], str] | bool | None = True,  # DEPRECATED: remove `None` in version 4.0.0
                 ) -> None:
        """Chat Message

        Based on Quasar's `Chat Message <https://quasar.dev/vue-components/chat/>`_ component.

        :param text: the message body (can be a list of strings for multiple message parts)
        :param name: the name of the message author
        :param label: renders a label header/section only
        :param stamp: timestamp of the message
        :param avatar: URL to an avatar
        :param sent: render as a sent message (so from current user) (default: ``False``)
        :param text_html: render text as HTML (default: ``False``)
        :param sanitize: sanitization mode (only relevant when ``text_html=True``):
            ``True`` (default) uses client-side sanitization via setHTML or DOMPurify,
            ``False`` disables sanitization (use only with trusted content),
            or pass a callable to apply server-side sanitization
        """
        super().__init__(tag='q-chat-message', label=label)

        if sanitize is None:
            helpers.warn_once('`sanitize=None` is deprecated, defaults to `True` and will be removed in version 4.0.0.')
            sanitize = True  # DEPRECATED: remove this block in version 4.0.0

        if text is None:
            text = []
        if isinstance(text, str):
            text = [text]
        if not text_html:
            text = [html.escape(part) for part in text]
            text = [part.replace('\n', '<br />') for part in text]
            sanitize = False

        self._props.set_optional('name', name)
        self._props.set_optional('stamp', stamp)
        self._props.set_optional('avatar', avatar)
        self._props['sent'] = sent

        with self:
            for line in text:
                Html(line, sanitize=sanitize)
