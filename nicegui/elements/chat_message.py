import html
from typing import List, Optional, Union

from ..element import Element
from .html import Html


class ChatMessage(Element):
    """
    Represents a chat message element.

    This element is used to display a chat message in a graphical user interface.
    It can be used to show messages from different authors, with timestamps and avatars.

    Args:
        - text (Union[str, List[str]], optional): The message body. It can be a single string or a list of strings for multiple message parts. Defaults to ... (ellipsis).
        - name (Optional[str], optional): The name of the message author. Defaults to None.
        - label (Optional[str], optional): Renders a label header/section only. Defaults to None.
        - stamp (Optional[str], optional): Timestamp of the message. Defaults to None.
        - avatar (Optional[str], optional): URL to an avatar. Defaults to None.
        - sent (bool, optional): Renders the message as a sent message (from the current user). Defaults to False.
        - text_html (bool, optional): Renders the text as HTML. Defaults to False.

    Attributes:
        - _props (Dict[str, Any]): A dictionary containing the properties of the chat message element.

    Example:
        To create a chat message element with a single line of text:

        ```python
        message = ChatMessage(text="Hello, world!", name="John Doe", stamp="12:34 PM")
        ```

        To create a chat message element with multiple lines of text:

        ```python
        message = ChatMessage(text=["Line 1", "Line 2", "Line 3"], name="John Doe", stamp="12:34 PM")
        ```

    """

    def __init__(
        self,
        text: Union[str, List[str]] = ...,
        *,
        name: Optional[str] = None,
        label: Optional[str] = None,
        stamp: Optional[str] = None,
        avatar: Optional[str] = None,
        sent: bool = False,
        text_html: bool = False,
    ) -> None:
        """
        Chat Message

        Args:
        
            - text (Union[str, List[str]], optional): The message body. It can be a single string or a list of strings for multiple message parts. Defaults to ... (ellipsis).
            - name (Optional[str], optional): The name of the message author. Defaults to None.
            - label (Optional[str], optional): Renders a label header/section only. Defaults to None.
            - stamp (Optional[str], optional): Timestamp of the message. Defaults to None.
            - avatar (Optional[str], optional): URL to an avatar. Defaults to None.
            - sent (bool, optional): Renders the message as a sent message (from the current user). Defaults to False.
            - text_html (bool, optional): Renders the text as HTML. Defaults to False.
            
        Returns:
        
                - None
        """
        super().__init__("q-chat-message")

        if text is ...:
            text = []
        if isinstance(text, str):
            text = [text]
        if not text_html:
            text = [html.escape(part) for part in text]
            text = [part.replace("\n", "<br />") for part in text]

        if name is not None:
            self._props["name"] = name
        if label is not None:
            self._props["label"] = label
        if stamp is not None:
            self._props["stamp"] = stamp
        if avatar is not None:
            self._props["avatar"] = avatar
        self._props["sent"] = sent

        with self:
            for line in text:
                Html(line)
