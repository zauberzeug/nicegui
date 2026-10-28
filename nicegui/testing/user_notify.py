from typing import Any


class UserNotify:

    def __init__(self) -> None:
        self.messages: list[str] = []

    def contains(self, needle: Any) -> bool:
        """Check if any of the messages contain the given substring."""
        return isinstance(needle, str) and any(needle in message for message in self.messages)
