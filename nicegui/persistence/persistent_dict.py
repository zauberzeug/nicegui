
from nicegui import observables


class PersistentDict(observables.ObservableDict):

    async def initialize(self) -> None:
        """Load initial data from the persistence layer."""

    async def close(self) -> None:
        """Clean up the persistence layer."""
