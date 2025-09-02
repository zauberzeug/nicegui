from .persistent_dict import PersistentDict


class PseudoPersistentDict(PersistentDict):
    """A persistent dict that is not actually persistent, but only keeps the data in memory (for internal use only)."""

    async def initialize(self) -> None:
        pass

    def initialize_sync(self) -> None:
        pass
