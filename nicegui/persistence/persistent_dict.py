import abc

from nicegui import observables


class PersistentDict(observables.ObservableDict, abc.ABC):

    @abc.abstractmethod
    async def initialize(self) -> None:
        """Load initial data from the persistence layer."""

    @abc.abstractmethod
    def initialize_sync(self) -> None:
        """Load initial data from the persistence layer in a synchronous context."""

    async def close(self) -> None:
        """Clean up the persistence layer."""
