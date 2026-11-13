import abc

from .. import observables


class PersistentDict(observables.ObservableDict, abc.ABC):

    @abc.abstractmethod
    async def initialize(self) -> None:
        """Load initial data from the persistence layer."""

    @abc.abstractmethod
    def initialize_sync(self) -> None:
        """Load initial data from the persistence layer in a synchronous context."""

    async def refresh_ttl(self) -> None:
        """Extend the lifetime of the data in the persistence layer, if it has one."""

    async def close(self) -> None:
        """Clean up the persistence layer."""
