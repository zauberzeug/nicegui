import abc

from nicegui import observables


class PersistentDict(observables.ObservableDict, abc.ABC):

    @abc.abstractmethod
    async def initialize(self) -> None:
        """Load initial data from the persistence layer."""

    async def close(self) -> None:
        """Clean up the persistence layer."""
