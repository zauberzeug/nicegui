from contextlib import AbstractContextManager, nullcontext

from ..client import Client, ClientConnectionTimeout
from ..element import Element
from ..logging import log
from ..timer import Timer as BaseTimer


class Timer(BaseTimer, Element, component='timer.js'):

    def _get_context(self) -> AbstractContextManager:
        return self.parent_slot or nullcontext()

    async def _can_start(self) -> bool:
        """Wait for the client connection before the timer callback can be allowed to manipulate the state.

        See https://github.com/zauberzeug/nicegui/issues/206 for details.
        Returns True if the client is connected, False if the client is not connected and the timer should be cancelled.
        """
        try:
            await self.client.connected()
            return True
        except ClientConnectionTimeout:
            self.cancel()
            log.debug('Timer cancelled because client connection timed out')
            return False

    def _should_stop(self) -> bool:
        return (
            self.is_deleted or
            self.client.id not in Client.instances or
            super()._should_stop()
        )

    def _cleanup(self) -> None:
        super()._cleanup()
        if not self._deleted:
            parent_slot = self.parent_slot
            assert parent_slot is not None
            parent_slot.parent.remove(self)

    def set_visibility(self, visible: bool) -> None:
        raise NotImplementedError('Use `activate()`, `deactivate()` or `cancel()`. See #3670 for more information.')
