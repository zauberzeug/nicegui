from uuid import uuid4

from ...element import Element


class ClientStorageElement(Element):
    """An element which requires client storage to re-mount itself after un-mounting."""

    def __init__(self) -> None:
        super().__init__()
        self._props['client-storage-id'] = str(uuid4())
